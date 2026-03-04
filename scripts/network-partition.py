import math
import networkx as nx
import torch
import time
from helpers.parse_topology import yaml_to_graph, graph_to_yaml
import argparse
import matplotlib.pyplot as plt
import numpy as np

NR_PASSES = 5
R_VALUES = [0.051, 0.15, 0.25, 0.35, 0.45]
MIN_PART_SIZE = 1 # not yet implemented
M = 0.05

# --- Utilities ----------------------------------------------------------------


def build_sparse_coo_from_nx(G):
    """
    Build COO arrays (row_idx, col_idx, data, shape) from a networkx Graph.
    Returns torch.LongTensor(row_idx), torch.LongTensor(col_idx), torch.FloatTensor(data), shape.
    The adjacency is returned as a (possibly symmetric) COO representation.
    """
    # get scipy coo
    A = nx.to_scipy_sparse_array(G).tocoo()
    row = torch.tensor(A.row, dtype=torch.long)
    col = torch.tensor(A.col, dtype=torch.long)
    data = torch.tensor(A.data, dtype=torch.float32)
    return row, col, data, A.shape

def update_balanced(balanced, assignment, r, mask_bool):
    """
    Updates the balanced tensor in-place, ignoring masked nodes.
    """
    m = M  # 0.05

    # only consider unmasked nodes
    valid = ~mask_bool

    num_neg = (assignment[valid] == -1).sum().item()
    num_pos = (assignment[valid] == 1).sum().item()
    n = num_neg + num_pos

    # compute per-node balance only for unmasked nodes
    a = num_neg + assignment
    b = num_pos - assignment
    # zero out masked nodes so they don't affect s
    a[mask_bool] = 0
    b[mask_bool] = 0

    s = torch.minimum(a, b)

    max_m = round(n * m)
    print(f"r = {r}, max_m = {max_m}")
    s_r = round(min(n * r, n * (1 - r)))

    balance_ok = (torch.abs(s_r - s) <= max_m)
    non_empty_ok = (a > 0) & (b > 0)

    balanced.copy_(balance_ok & non_empty_ok)

# --- Sparse helpers -----------------------------------------------------------

def compute_cut_data_from_adj(adj_sp, assignment):
    cut_data = adj_sp.values() * assignment[adj_sp.indices()[0]] * assignment[adj_sp.indices()[1]].to(adj_sp.values().dtype)
    return torch.sparse_coo_tensor(adj_sp.indices(), cut_data, adj_sp.size())

def row_sum_from_coo(row_idx, values, n_rows):
    """
    Given COO (row_idx, values), compute row-wise sum vector of length n_rows.
    Uses scatter_add.
    """
    row_sums = torch.zeros(n_rows, dtype=values.dtype)
    row_sums = row_sums.scatter_add(0, row_idx, values)
    return row_sums

def count_neg_entries_in_DX(row_idx, col_idx, cut_data, assignment):
    """
    Compute D @ cut_matrix values for each nonzero entry: value2 = assignment[row]*cut_data
    Count how many of those are equal to -1 (exact equality, same semantics as original).
    Returns integer count.
    """
    v2 = assignment[row_idx].to(cut_data.dtype) * cut_data
    # equality with -1 (use elementwise comparison)
    return int((v2 == -1).sum().item())

def create_cut(cut_data, assignment):
    n_cuts_raw = int((cut_data.values() == -1).sum().item())
    n_cuts = n_cuts_raw // 2

    a, b = int((assignment == -1).sum().item()), int((assignment == 1).sum().item())
    return (n_cuts, a, b)

def cheeger(c, a, b):
    return c / min(a, b)

def initial_partition(n, r, mask_nodes):
    k = round((n - len(mask_nodes)) * r)
    all_idx = torch.arange(n)
    keep_mask = torch.ones(n, dtype=torch.bool)
    keep_mask[mask_nodes] = False
    perm = all_idx[keep_mask][torch.randperm(keep_mask.sum())]
    A_idx = perm[:k]
    return A_idx

def initialize_adj_matrix(adj_sp, mask_nodes, n):
    indices = torch.tensor(np.array([adj_sp.row, adj_sp.col]), dtype=torch.long)
    data = torch.tensor(adj_sp.data, dtype=torch.float32)
    adj = torch.sparse_coo_tensor(indices, data, (n, n))
    
    # zero out masked rows and cols via diagonal mask
    mask = torch.ones(n, dtype=torch.float32)
    mask[mask_nodes] = 0
    mask_sp = torch.diag(mask).to_sparse()
    
    return mask_sp @ adj @ mask_sp

# --- Algorithm ---------------------------------------------------------------

def partition_pass(G, r, mode="min", mask_nodes=[]):
    n = len(list(G.nodes()))
    if n == 0:
        return None

    # Build adjacency as COO via scipy then to torch
    adj_sp = nx.to_scipy_sparse_array(G).tocoo()
    # Sanity: if adjacency has shape mismatch, handle it
    assert adj_sp.shape[0] == n and adj_sp.shape[1] == n, "Adjacency shape mismatch with node list"

    # create a tensor boolean mask using mask_nodes index array
    mask_bool = torch.zeros(n, dtype=torch.bool)
    mask_bool[mask_nodes] = True

    adj_sp = initialize_adj_matrix(adj_sp, mask_nodes, n)

    # initial random partition: choose k nodes for A (assignment -1), rest 1
    A_idx = initial_partition(n, r, mask_nodes)

    assignment = torch.ones(n, dtype=torch.int32)
    assignment[A_idx] = -1
    assignment[mask_nodes] = 0

    moveable = torch.ones(n, dtype=torch.bool)
    moveable[mask_nodes] = False

    cut_data = compute_cut_data_from_adj(adj_sp, assignment)

    # balanced per vertex
    balanced = torch.ones(n, dtype=torch.bool)
    update_balanced(balanced, assignment, r, mask_bool)

    opt_cut = (cheeger(*create_cut(cut_data, assignment)), torch.where(assignment == -1)[0].tolist(), cut_data)
    num_neg, num_pos = torch.full((n,), 0), torch.full((n,), 0)

    print(moveable, balanced)
    print((moveable & balanced).any().item())
    while (moveable & balanced).any().item():
        # Compute gains:
        # gains = - (cut_matrix).sum(axis=1)
        num_neg_total = (assignment == -1).sum().item()
        num_neg = torch.full((n,), num_neg_total, dtype=assignment.dtype)
        # num_neg is prospective size of cut B if node i were moved?
        num_neg = num_neg + assignment

        num_pos_total = (assignment == 1).sum().item()
        num_pos = torch.full((n,), num_pos_total, dtype=assignment.dtype)
        num_pos = num_pos - assignment

        min_size = torch.minimum(num_neg, num_pos)

        row_sums = row_sum_from_coo(cut_data.row, cut_data, n)
        gains = - row_sums / min_size if mode == "min" else row_sums / min_size

        # Find candidate indices where moveable & balanced
        candidates = torch.where(moveable & balanced)[0]
        if candidates.numel() == 0:
            break

        candidate_vals = gains[candidates]
        # choose the candidate with maximum gain (ties broken arbitrarily)
        max_idx = torch.argmax(candidate_vals)
        max_vertex = int(candidates[max_idx].item())

        # flip assignment for that vertex
        assignment[max_vertex] *= -1

        # Update cut_data: because cut_data = adj_value * assignment[col]
        # flipping assignment[v] toggles sign of all entries with col == v
        affected = (cut_data.col == max_vertex) | (cut_data.row == max_vertex)
        if affected.any().item():
            cut_data[affected] *= -1        

        # Update balanced after flip
        update_balanced(balanced, assignment, r, mask_bool)

        # mark vertex as non-moveable
        moveable[max_vertex] = False

        cut = (cheeger(*create_cut(cut_data, assignment)), torch.where(assignment == -1)[0].tolist(), cut_data)
        opt_cut = (min if mode == "min" else max)([opt_cut, cut], key=lambda x: x[0])

    return opt_cut


# --- Top-level helpers -------------------------------------------------------

def run(G, mode="min", mask_nodes=[]):
    results = {}
    opt = (lambda x, y: x < y) if mode == "min" else (lambda x, y: x > y)

    for r in R_VALUES:
        start = time.time()

        best_cheeger = math.inf if mode == "min" else -math.inf
        best_partition = None
        updates = 0

        for i in range(NR_PASSES):
            res = partition_pass(G, r, mode=mode, mask_nodes=mask_nodes)

            if res is None:
                print(f"r={r} pass {i}: no improving moves.")
                continue

            ch, part_a, cut = res

            if opt(ch, best_cheeger):
                best_cheeger = ch
                best_partition = (ch, part_a, cut)
                updates += 1

            print(
                f"r={r} pass {i}  "
                f"updates={updates}  "
                f"cheeger={ch:.6f}"
            )

        elapsed = time.time() - start

        if best_partition is None:
            results[str(r)] = None
        else:
            ch, part_a, cut = best_partition
            results[str(r)] = {
                "cheeger": ch,
                "partition": part_a,
                "cut_data": cut,
            }

        print(f"r={r}: {elapsed:.2f}s")

    return results


# --- VISUALIZATION -----------------------------------------------------------

def draw_partition(G, partition_a, cut_edges):
    color_map = ["skyblue" if n in partition_a else "salmon" for n in G.nodes()]
    labels = {n: G.nodes[n]["label"] for n in G.nodes()}

    edge_color_map = ["gray" if (u,v) not in cut_edges else "red" for (u,v) in G.edges()]

    pos = nx.spring_layout(G, seed=42)
    nx.draw(G, pos, labels=labels, node_color=color_map, with_labels=True,
            node_size=800, font_size=8, edge_color=edge_color_map)
    
    # legend
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

# --- main --------------------------------------------------------------------

def can_connect(G, u, v):
    u_data = G.nodes[u]
    v_data = G.nodes[v]

    if u_data["isd_n"] == v_data["isd_n"]:
        return True

    if u_data["is_core"] and v_data["is_core"]:
        return True

    return False


def get_global_max_cut(G, min_cut_data, list_a, list_b):
    result_a = max(run(G, mode="max", mask_nodes=list_b).values(), key=lambda x: x["cheeger"])
    result_b = max(run(G, mode="max", mask_nodes=list_a).values(), key=lambda x: x["cheeger"])

    max_res = max([result_a, result_b], key=lambda x: x["cheeger"])
    max_cut_data = max_res["cut_data"].coalesce()

    # --------------------------------------------------
    # STEP 1: row u with most -1 entries
    # --------------------------------------------------
    rows, cols = max_cut_data.indices()
    values = max_cut_data.values()

    neg_mask = values == -1
    neg_rows = rows[neg_mask]

    n_rows = max_cut_data.size(0)

    counts = torch.bincount(
        neg_rows,
        minlength=n_rows
    )

    u = torch.argmax(counts).item()

    # pick ONE column where (u, col) == -1
    u_neg_cols = cols[neg_mask & (rows == u)]
    v_og = u_neg_cols[0].item()   # or random choice

    # --------------------------------------------------
    # STEP 2: valid columns from min_cut_data
    # --------------------------------------------------
    min_cut_data = min_cut_data.coalesce()

    m_rows, m_cols = min_cut_data.indices()
    m_vals = min_cut_data.values()

    n_cols = min_cut_data.size(1)

    cols_with_neg1 = torch.unique(
        m_cols[m_vals == -1]
    )

    valid_cols_mask = torch.ones(n_cols, dtype=torch.bool)
    valid_cols_mask[cols_with_neg1] = False

    row_u_mask = (m_rows == u)

    cols_at_u = m_cols[row_u_mask]
    vals_at_u = m_vals[row_u_mask]

    zero_cols_at_u = cols_at_u[vals_at_u == 0]

    valid_cols = zero_cols_at_u[
        valid_cols_mask[zero_cols_at_u]
    ]

    valid_cols = torch.tensor(
        [
            col.item()
            for col in valid_cols
            if can_connect(G, u, col.item())
        ],
        device=zero_cols_at_u.device,
        dtype=zero_cols_at_u.dtype,
    )

    if len(valid_cols) == 0:
        raise Exception("no vertices to connect to")
    
    v_new = valid_cols[0]

    return (u, v_og), (u, v_new)


def iteration(G, path, iteration):
    # nx.draw(G, with_labels=True, node_color="lightblue", edge_color="gray")
    # plt.show()

    min_res = min(run(G).values(), key=lambda x: x["cheeger"])
    min_partition = min_res["partition"]

    min_set_a = set(min_partition)
    min_edges = [(u, v) for (u, v) in G.edges if (u in min_set_a) != (v in min_set_a)]

    draw_partition(G, min_set_a, min_edges)

    del_edge, new_edge = get_global_max_cut(G, min_res["cut_data"], min_partition, list(G.nodes() - min_partition))

    print(new_edge, del_edge)

    G.add_edge(new_edge[0], new_edge[1])
    G.remove_edge(del_edge[0], del_edge[1])
    highlight_edges(G, {new_edge}, color="limegreen")

    graph_to_yaml(G, path + f"_it{iteration}" + ".yaml")

    return G

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse the topology config into an NetworkX graph.")
    parser.add_argument("--topology-config", "-tc", required=True, help="Path to the topology yaml file")
    args = parser.parse_args()

    G = yaml_to_graph(args.topology_config)

    path = (args.topology_config).split("_")[0]

    for i in range(5):
        G = iteration(G, path, i+1)
