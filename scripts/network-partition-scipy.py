import math
import networkx as nx
import scipy.sparse
import torch
import numpy as np
import time
from helpers.parse_topology import yaml_to_graph, graph_to_yaml
import argparse
import matplotlib.pyplot as plt

NR_PASSES = 5
R_VALUES = [0.051, 0.15, 0.25, 0.35, 0.45]
M = 0.05

# --- Visualization / main (unchanged) ----------------------------------------

def draw_partition(G, partition_a, cut_edges):
    color_map = ["skyblue" if n in partition_a else "salmon" for n in G.nodes()]
    labels = {n: G.nodes[n]["label"] for n in G.nodes()}
    edge_color_map = ["gray" if (u,v) not in cut_edges else "red" for (u,v) in G.edges()]
    pos = nx.spring_layout(G, seed=42)
    nx.draw(G, pos, labels=labels, node_color=color_map, with_labels=True,
            node_size=800, font_size=8, edge_color=edge_color_map)
    handles = [
        plt.Line2D([0], [0], marker="o", color="w", markerfacecolor="skyblue", markersize=12, label="Partition +1"),
        plt.Line2D([0], [0], marker="o", color="w", markerfacecolor="salmon",  markersize=12, label="Partition -1"),
    ]
    plt.legend(handles=handles)
    plt.title("Graph Partition")
    plt.show()

def highlight_edges(G, edges, color="red"):
    color_map = ["gray" if (u,v) not in edges else color for (u,v) in G.edges()]
    labels = {n: G.nodes[n]["label"] for n in G.nodes()}
    pos = nx.spring_layout(G, seed=42)
    nx.draw(G, pos, labels=labels, node_color="skyblue", with_labels=True,
            node_size=800, font_size=8, edge_color=color_map)
    plt.title("Graph Partition")
    plt.show()

def highlight_nodes(G, nodes, color="red"):
    color_map = ["gray" if v not in nodes else color for v in G.nodes()]
    labels = {n: G.nodes[n]["label"] for n in G.nodes()}
    pos = nx.spring_layout(G, seed=42)
    nx.draw(G, pos, node_color=color_map, with_labels=True,
            node_size=800, font_size=8, edge_color="grey")
    plt.title("Graph Partition")
    plt.show()

# --- Utilities ----------------------------------------------------------------

def update_balanced(balanced, assignment, r, mask_bool):
    m = M
    valid = ~mask_bool
    num_neg = (assignment[valid] == -1).sum().item()
    num_pos = (assignment[valid] == 1).sum().item()
    n = num_neg + num_pos

    a = num_neg + assignment
    b = num_pos - assignment
    a[mask_bool] = 0
    b[mask_bool] = 0

    s = torch.minimum(a, b)
    max_m = round(n * m)
    s_r = round(min(n * r, n * (1 - r)))

    balance_ok = (torch.abs(s_r - s) <= max_m)
    non_empty_ok = (a > 0) & (b > 0)
    balanced.copy_(balance_ok & non_empty_ok)

# --- Sparse helpers (scipy + numpy) ------------------------------------------

def initialize_adj_matrix(adj_sp, mask_nodes, n):
    """Filter out edges touching masked nodes. Returns scipy COO matrix."""
    node_mask = np.zeros(n, dtype=bool)
    node_mask[mask_nodes] = True
    edge_mask = ~(node_mask[adj_sp.row] | node_mask[adj_sp.col])
    return scipy.sparse.coo_matrix(
        (adj_sp.data[edge_mask], (adj_sp.row[edge_mask], adj_sp.col[edge_mask])),
        shape=(n, n)
    )

def compute_cut_values(adj_sp, assignment):
    """
    For each edge (i,j): cut_value = w_ij * s[i] * s[j]
    Returns numpy array of values (same indices as adj_sp.row/col).
    """
    s = assignment.numpy()
    return adj_sp.data * s[adj_sp.row] * s[adj_sp.col]

def row_sums_from_cut(adj_sp, cut_values, n):
    """Scatter-add cut_values by row index. Returns torch tensor."""
    sums = np.zeros(n, dtype=np.float32)
    np.add.at(sums, adj_sp.row, cut_values)
    return torch.from_numpy(sums)

def create_cut(adj_sp, cut_values, assignment):
    n_cuts = int((cut_values == -1).sum()) // 2  # symmetric: each cut edge counted twice
    a = int((assignment == -1).sum().item())
    b = int((assignment == 1).sum().item())
    return n_cuts, a, b

def cheeger(c, a, b):
    return c / min(a, b)

# --- Algorithm ---------------------------------------------------------------

def initial_partition(n, r, mask_nodes):
    keep_mask = torch.ones(n, dtype=torch.bool)
    keep_mask[mask_nodes] = False
    perm = torch.arange(n)[keep_mask][torch.randperm(keep_mask.sum())]
    k = round(len(perm) * r)
    return perm[:k]

def partition_pass(adj_sp, r, mode="min", mask_nodes=[]):
    n = adj_sp.shape[0]
    if n == 0:
        return None

    assert adj_sp.shape == (n, n)

    mask_bool = torch.zeros(n, dtype=torch.bool)
    mask_bool[mask_nodes] = True

    # filter masked nodes from adjacency
    adj_sp = initialize_adj_matrix(adj_sp, mask_nodes, n)

    # initial assignment
    A_idx = initial_partition(n, r, mask_nodes)
    assignment = torch.ones(n, dtype=torch.int32)
    assignment[A_idx] = -1
    assignment[mask_nodes] = 0

    moveable = torch.ones(n, dtype=torch.bool)
    moveable[mask_nodes] = False

    # cut_values: numpy array, same indices as adj_sp
    cut_values = compute_cut_values(adj_sp, assignment)

    balanced = torch.ones(n, dtype=torch.bool)
    update_balanced(balanced, assignment, r, mask_bool)

    cut = create_cut(adj_sp, cut_values, assignment)
    opt_cut = (cheeger(*cut), torch.where(assignment == -1)[0].tolist(), cut_values.copy())

    while (moveable & balanced).any().item():
        num_neg_total = (assignment == -1).sum().item()
        num_pos_total = (assignment == 1).sum().item()

        num_neg = num_neg_total + assignment
        num_pos = num_pos_total - assignment
        num_neg[mask_bool] = 0
        num_pos[mask_bool] = 0
        min_size = torch.minimum(num_neg, num_pos).float()
        min_size[min_size == 0] = 1  # avoid div by zero

        row_sums = row_sums_from_cut(adj_sp, cut_values, n)
        gains = -row_sums / min_size if mode == "min" else row_sums / min_size

        candidates = torch.where(moveable & balanced)[0]
        if candidates.numel() == 0:
            break

        max_vertex = int(candidates[torch.argmax(gains[candidates])].item())
        assignment[max_vertex] *= -1

        # flip sign of all cut_values touching max_vertex
        affected = (adj_sp.row == max_vertex) | (adj_sp.col == max_vertex)
        cut_values[affected] *= -1

        update_balanced(balanced, assignment, r, mask_bool)
        moveable[max_vertex] = False

        cut = create_cut(adj_sp, cut_values, assignment)
        ch = cheeger(*cut)
        if (mode == "min" and ch < opt_cut[0]) or (mode == "max" and ch > opt_cut[0]):
            opt_cut = (ch, torch.where(assignment == -1)[0].tolist(), cut_values.copy())

    return opt_cut

# --- Aggregate Min Adjacency Matrix ------------------------------------------

# the min_adj_sp is an adjacency matrix with the minimum cut edges removed
# it must always correspond to the current minimum cut, meaning it has 
# the most edges present of all possible min_adj_sp
# the agg_adj_sp is all min_adj_sp equal and minimum size aggregated, meaning
# all minimum edges are removed from it.

def get_cur_min_edges(min_cut_data):
    return -np.minimum(min_cut_data, 0)

def aggregate_min_edges(agg_min_edges, cur_min_edges):
    if (agg_min_edges.shape[0] == 0):
        agg_min_edges = cur_min_edges.copy()
    else:
        agg_adj_sp = np.maximum(agg_min_edges, cur_min_edges)
    return agg_adj_sp


# --- Top-level ---------------------------------------------------------------

def run(adj_mat, mode="min", mask_nodes=[]):
    results = {}
    opt = (lambda x, y: x < y) if mode == "min" else (lambda x, y: x > y)
    agg_min_edges = []
    min_edges = []
    cur_min_edges = []

    for r in R_VALUES:
        start = time.time()
        best_cheeger = math.inf if mode == "min" else -math.inf
        best_partition = None
        updates = 0

        for i in range(NR_PASSES):
            res = partition_pass(adj_mat, r, mode=mode, mask_nodes=mask_nodes)
            if res is None:
                continue

            ch, part_a, cut_values = res
            cur_min_edges = get_cur_min_edges(cut_values)
            if ch == best_cheeger:
                # if equal, the cut is aggregated to the agg_min_edges
                agg_min_edges = aggregate_min_edges(agg_min_edges, cur_min_edges)
            elif opt(ch, best_cheeger):
                best_cheeger = ch
                best_partition = (ch, part_a, cut_values)
                updates += 1

                # if better cheeger is found, min_adj_sp and and agg_adj_sp are overwritten
                min_edges = cur_min_edges
                agg_min_edges = min_edges.copy()

            print(f"r={r} pass {i}  updates={updates}  cheeger={ch:.6f}")

        elapsed = time.time() - start
        if best_partition is None:
            results[str(r)] = None
        else:
            ch, part_a, cut_values = best_partition
            results[str(r)] = {"cheeger": ch, "partition": part_a, "cut_values": cut_values, "agg_min_edges": agg_min_edges}

        print(f"r={r}: {elapsed:.2f}s")

    return results


# --- get_global_max_cut ------------------------------------------------------

def can_connect(G, u, v):
    return G.nodes[u]["isd_n"] == G.nodes[v]["isd_n"] or (G.nodes[u]["is_core"] and G.nodes[v]["is_core"])

def get_global_max_cut(adj_sp, agg_adj_sp, list_a, list_b):
    n = adj_sp.shape[0]
    result_a = max(run(agg_adj_sp, mode="max", mask_nodes=list_b).values(), key=lambda x: x["cheeger"])
    result_b = max(run(agg_adj_sp, mode="max", mask_nodes=list_a).values(), key=lambda x: x["cheeger"])

    if result_a["cheeger"] >= result_b["cheeger"]:
        max_res = result_a
        active_mask = list_b
        anti_mask = list_a
    else:
        max_res = result_b
        active_mask = list_a
        anti_mask = list_b

    max_adj_sp = initialize_adj_matrix(agg_adj_sp, active_mask, n)
    max_cut_values = max_res["cut_values"]
    max_res = max([result_a, result_b], key=lambda x: x["cheeger"])

    # --- Build full-graph sparse matrices ---
    # can_connect as sparse matrix
    rows, cols = np.meshgrid(np.arange(n), np.arange(n), indexing='ij')
    rows, cols = rows.ravel(), cols.ravel()

    # exclude self-loops
    mask = rows != cols
    rows, cols = rows[mask], cols[mask]

    cc_data = np.array([can_connect(G, int(i), int(j)) for i, j in zip(rows, cols)], dtype=np.float32)
    can_connect_sp = scipy.sparse.coo_matrix((cc_data, (rows, cols)), shape=(n, n))
    can_connect_sp.eliminate_zeros()

    # max_cut and min_cut as full-graph sparse matrices (masked nodes already zeroed via initialize_adj_matrix)
    max_cut_sp = scipy.sparse.coo_matrix((max_cut_values, (max_adj_sp.row, max_adj_sp.col)), shape=(n, n))

    anti_mask_diag = scipy.sparse.diags([1.0 if i in set(anti_mask) else 0.0 for i in range(n)])
    active_mask_diag = scipy.sparse.diags([1.0 if i in set(active_mask) else 0.0 for i in range(n)])

    existing_edges = can_connect_sp.multiply(adj_sp.sign())

    valid_sp = can_connect_sp - existing_edges

    valid_sp = anti_mask_diag @ valid_sp @ active_mask_diag

    max_cut_neg = max_cut_sp.minimum(0)

    # count cut edges per node, restricted to valid edges only

    # u: valid rows only
    row_cut_counts = np.array(max_cut_neg.sum(axis=1)).flatten()
    u_scores = np.zeros(n)
    valid_rows = np.unique(valid_sp.tocoo().row)
    u_scores[valid_rows] = -row_cut_counts[valid_rows]
    u = int(np.argmax(u_scores))

    # v: valid cols only
    v_scores = np.zeros(n)
    valid_cols = np.unique(valid_sp.tocoo().col)
    v_scores[valid_cols] = 1.0
    v = int(np.argmax(v_scores))

    col_cut_counts = np.array((agg_adj_sp - adj_sp).sum(axis=0)).flatten()
    v_scores = np.zeros(n)
    valid_cols = np.unique(valid_sp.tocoo().col)
    v_scores[valid_cols] = adj_sp.nnz + col_cut_counts[valid_cols]
    v = int(np.argmax(v_scores))

    highlight_nodes(G, {u}, color="blue")
    highlight_nodes(G, {v}, color="limegreen")

    u_row = max_cut_sp.getrow(u)
    neg_cols = u_row.indices[u_row.data == -1]
    if len(neg_cols) == 0:
        raise Exception("no max cut edge from u found")
    degrees = np.array(adj_sp.sum(axis=1)).flatten()
    v_old = int(neg_cols[np.argmax(degrees[neg_cols])])

    highlight_nodes(G, {v_old}, color="red")

    return (u, v_old), (u, v)

def iteration(G, path, iteration):
    full_adj = nx.to_scipy_sparse_array(G).tocoo()

    min_res = min(run(full_adj).values(), key=lambda x: x["cheeger"])
    min_partition = min_res["partition"]

    min_set_a = set(min_partition)
    min_edges = [(u, v) for (u, v) in G.edges if (u in min_set_a) != (v in min_set_a)]
    draw_partition(G, min_set_a, min_edges)

    agg_min_edges = min_res["agg_min_edges"]  # 0/1 array, length = full_adj.nnz
    non_cut_mask = agg_min_edges == 0
    adj_mat_no_min = scipy.sparse.coo_matrix(
        (full_adj.data[non_cut_mask], (full_adj.row[non_cut_mask], full_adj.col[non_cut_mask])),
        shape=full_adj.shape
    )

    del_edge, new_edge = get_global_max_cut(full_adj, adj_mat_no_min, min_partition, list(set(G.nodes()) - min_set_a))
    print(new_edge, del_edge)

    G.add_edge(new_edge[0], new_edge[1])
    G.remove_edge(del_edge[0], del_edge[1])
    highlight_edges(G, {new_edge}, color="limegreen")
    graph_to_yaml(G, path + f"_it{iteration}.yaml")
    return G

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--topology-config", "-tc", required=True)
    args = parser.parse_args()
    G = yaml_to_graph(args.topology_config)
    path = args.topology_config.split("_")[0]
    for i in range(5):
        G = iteration(G, path, i+1)