import math
import networkx as nx
import scipy.sparse
import torch
import numpy as np
import time
from helpers.parse_topology import yaml_to_graph, graph_to_yaml
import argparse
import matplotlib.pyplot as plt

NR_PASSES = 10
R_VALUES = [0.05, 0.15, 0.25, 0.35, 0.45]
M = 0.05

# --- Visualization ----------------------------------------

def draw_partition(G, partition_a):
    cut_edges = [(u, v) for (u, v) in G.edges if (u in partition_a) != (v in partition_a)]

    color_map = ["skyblue" if n in partition_a else "salmon" for n in G.nodes()]
    labels = {n: G.nodes[n]["label"] for n in G.nodes()}
    edge_color_map = ["gray" if (u,v) not in cut_edges else "red" for (u,v) in G.edges()]
    pos = nx.spring_layout(G, seed=42)
    nx.draw(G, pos, node_color=color_map, with_labels=True,
            node_size=200, font_size=8, edge_color=edge_color_map)
    handles = [
        plt.Line2D([0], [0], marker="o", color="w", markerfacecolor="skyblue", markersize=12, label="Partition +1"),
        plt.Line2D([0], [0], marker="o", color="w", markerfacecolor="salmon",  markersize=12, label="Partition -1"),
    ]
    plt.legend(handles=handles)
    plt.title("Graph Partition")
    plt.show()

def get_edge_weights(masked_adj, edge_scores):
    weights = {}
    for i, (u, v) in enumerate(zip(masked_adj.row, masked_adj.col)):
        if u < v:  # only store upper triangle
            score = edge_scores[i]
            weights[(u, v)] = score
    return weights

def show_edge_weights(G, edge_weights):
    labels = {n: G.nodes[n]["label"] for n in G.nodes()}
    pos = nx.spring_layout(G, seed=42)
    
    edge_colors = []
    edge_labels = {}
    for u, v in G.edges():
        weight = edge_weights.get((u, v), edge_weights.get((v, u), None))
        edge_colors.append("red" if weight is not None else "gray")
        if weight is not None:
            edge_labels[(u, v)] = f"{weight:.2f}"

    nx.draw(G, pos, labels=labels, node_color="skyblue", with_labels=True,
            node_size=200, font_size=8, edge_color=edge_colors)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=7)
    plt.title("Edge Weights")
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

# --- NETWORK PARTITIONING ---------------------------------------------------------------

def initial_partition(n, r, mask_nodes, iteration=0):
    keep_mask = torch.ones(n, dtype=torch.bool)
    keep_mask[mask_nodes] = False
    
    # use iteration as seed for reproducibility but diversity across passes
    torch.manual_seed(iteration)
    perm = torch.arange(n)[keep_mask][torch.randperm(keep_mask.sum())]
    
    r = min(1-r, r)
    k = round(len(perm) * r)
    k = max(1, k)
    
    # rotate the partition boundary by iteration to ensure different starting points
    offset = (iteration * k) % len(perm)
    indices = torch.cat([perm[offset:], perm[:offset]])
    A_idx = indices[:k]
    
    assignment = torch.ones(n, dtype=torch.int32)
    assignment[A_idx] = -1
    assignment[mask_nodes] = 0
    return assignment

def calculate_prospective_cut_sizes(assignment, mask_bool):
    num_neg_total = (assignment == -1).sum().item()
    num_pos_total = (assignment == 1).sum().item()

    n = num_neg_total + num_pos_total

    num_neg = num_neg_total + assignment
    num_pos = num_pos_total - assignment
    num_neg[mask_bool] = 0
    num_pos[mask_bool] = 0
    return num_neg, num_pos, n

def update_balanced(balanced, assignment, r, mask_bool):
    a, b, n = calculate_prospective_cut_sizes(assignment, mask_bool)

    s = np.minimum(a, b)
    max_m = round(n * M)
    s_r = round(min(n * r, n * (1 - r)))

    balance_ok = (np.abs(s_r - s) <= max_m)
    non_empty_ok = (a > 0) & (b > 0)
    balanced[:] = balance_ok & non_empty_ok 

def partition_pass(adj_sp, r, mode="min", mask_nodes=[], iteration=0):
    n = adj_sp.shape[0]

    mask_bool = np.zeros(n, dtype=bool)
    mask_bool[mask_nodes] = True

    assignment = initial_partition(n, r, mask_nodes, iteration=iteration)

    moveable = np.ones(n, dtype=bool)
    moveable[mask_nodes] = False

    # cut_values: numpy array, same indices as adj_sp
    cut_values = compute_cut_values(adj_sp, assignment)
    edge_scores = np.full(adj_sp.nnz, math.inf if mode=="min" else 0)
    edge_nrs = np.full(adj_sp.nnz, math.inf if mode=="min" else 0)

    balanced = np.ones(n, dtype=bool)
    update_balanced(balanced, assignment, r, mask_bool)

    gains = np.zeros(n, dtype=float)

    cut = create_cut(adj_sp, cut_values, assignment)
    opt_cut = (cheeger(*cut), np.where(assignment == -1)[0].tolist(), cut_values, gains)
    if (mode=="min"):
        edge_scores[cut_values == -1] = np.minimum(edge_scores[cut_values == -1], opt_cut[0])
        edge_nrs[cut_values == -1] = np.minimum(edge_nrs[cut_values == -1], float(-cut_values[cut_values==-1].sum())/2)

    while (moveable & balanced).any().item():
        num_neg, num_pos, _ = calculate_prospective_cut_sizes(assignment, mask_bool)
        min_size = np.minimum(num_neg, num_pos)
    
        row_sums = row_sums_from_cut(adj_sp, cut_values, n)
        gains[moveable] = (-row_sums / min_size)[moveable] if mode == "min" else (row_sums / min_size)[moveable]

        candidates = np.where(moveable & balanced)[0]

        max_vertex = int(candidates[np.argmax(gains[candidates])].item())
        assignment[max_vertex] *= -1

        # flip sign of all cut_values touching max_vertex
        affected = (adj_sp.row == max_vertex) | (adj_sp.col == max_vertex)
        cut_values[affected] *= -1

        update_balanced(balanced, assignment, r, mask_bool)
        moveable[max_vertex] = False

        cut = create_cut(adj_sp, cut_values, assignment)
        ch = cheeger(*cut)

        if (mode == "min" and ch < opt_cut[0]) or (mode == "max" and ch > opt_cut[0]):
            opt_cut = (ch, np.where(assignment == -1)[0].tolist(), cut_values, gains)
            if (mode=="min"):
                edge_scores[cut_values == -1] = np.minimum(edge_scores[cut_values == -1], float(-cut_values[cut_values==-1].sum())/2)
                edge_nrs[cut_values == -1] = np.minimum(edge_nrs[cut_values == -1], float(-cut_values[cut_values==-1].sum())/2)

    return opt_cut, edge_scores, edge_nrs

# --- Top-level ---------------------------------------------------------------

def run_network_partitioning(adj_mat, mode="min", mask_nodes=[], iteration=0):
    results = {}
    opt = (lambda x, y: x < y) if mode == "min" else (lambda x, y: x > y)

    masked_adj = initialize_adj_matrix(adj_mat, mask_nodes, adj_mat.shape[0])
    edge_scores = np.full(masked_adj.nnz, math.inf if mode=="min" else 0)
    edge_nrs = np.full(masked_adj.nnz, math.inf if mode=="min" else 0)

    r_values = R_VALUES if mode=="min" else [0.5]
    for r in r_values:
        start = time.time()
        best_cheeger = math.inf if mode == "min" else -math.inf
        best_partition = None
        updates = 0

        for i in range(NR_PASSES):
            res = partition_pass(masked_adj, r, mode=mode, mask_nodes=mask_nodes, iteration=(iteration*NR_PASSES + i))
            if res is None:
                continue

            (ch, part_a, cut_vals, gains), cur_edge_scores, cur_edge_nrs = res
            if opt(ch, best_cheeger):
                best_cheeger = ch
                best_partition = (ch, part_a, cut_vals, gains)
                updates += 1


            if (mode == "min"):
                edge_scores = np.minimum(edge_scores, cur_edge_scores)
                edge_nrs = np.minimum(edge_nrs, cur_edge_nrs)

            # print(f"r={r} pass {i}  updates={updates}  cheeger={ch:.6f}")

        elapsed = time.time() - start
        if best_partition is None:
            results[str(r)] = None
        else:
            ch, part_a, cut_vals, gains = best_partition
            results[str(r)] = {"cheeger": ch, "partition": part_a, "cut_values": cut_vals, "gains": gains, "edge_scores" :  get_edge_weights(masked_adj, edge_scores), "edge_nrs": get_edge_weights(masked_adj, edge_nrs)}

        # print(f"r={r}: {elapsed:.2f}s")
    
    results = {k: v for k, v in results.items() if v is not None}
    if not results:
        return None
    best_r = max(results.keys(), key=lambda k: results[k]["cheeger"] if mode == "max" else -results[k]["cheeger"])
    return results[best_r]


def can_connect(G, u, v):
    return G.nodes[u]["isd_n"] == G.nodes[v]["isd_n"] or (G.nodes[u]["is_core"] and G.nodes[v]["is_core"])

def build_can_connect_matrix(n):
    rows, cols = np.meshgrid(np.arange(n), np.arange(n), indexing='ij')
    rows, cols = rows.ravel(), cols.ravel()

    mask = rows != cols
    rows, cols = rows[mask], cols[mask]

    cc_data = np.array([can_connect(G, int(i), int(j)) for i, j in zip(rows, cols)], dtype=np.float32)
    can_connect_sp = scipy.sparse.coo_matrix((cc_data, (rows, cols)), shape=(n, n))
    can_connect_sp.eliminate_zeros()
    return can_connect_sp

def build_validity_matrix(adj_sp, u_partition, v_partition):
    n = adj_sp.shape[0]
    can_connect_sp = build_can_connect_matrix(n)

    u_partition_diag = scipy.sparse.diags([1.0 if i in set(u_partition) else 0.0 for i in range(n)])
    v_partition_diag = scipy.sparse.diags([1.0 if i in set(v_partition) else 0.0 for i in range(n)])

    valid_sp = can_connect_sp - adj_sp                                      # valid edges are ones that can connect and don't exist already
    valid_sp = u_partition_diag @ valid_sp @ v_partition_diag               # enforces that in valid_sp v is in v_partition and u is in u_partition
    return valid_sp

def find_old_edge(G, min_res, adj_sp):
    adj_csr = scipy.sparse.csr_matrix(adj_sp)
    degrees = np.array(adj_sp.sum(axis=1)).flatten()

    partition_a = min_res["partition"]
    # bridges = set(nx.bridges(G))

    # def has_no_deg1_neighbors(node):
    #     neighbors = adj_csr.getrow(node).indices
    #     return not any(degrees[nb] == 1 for nb in neighbors)

    finite_edges = {uv: score for uv, score in min_res["edge_nrs"].items() if score != math.inf}
    # finite_edges = {(u,v): score for (u,v), score in finite_edges.items() if G.degree(u) > 1 and G.degree(v) > 1}
    # finite_edges = {(u,v): score for (u,v), score in finite_edges.items() if (u, v) not in bridges and (v, u) not in bridges}

    if (len(finite_edges) == 0):
        print("No finite edges")
        return
    
    cut_edge_nrs = {(u, v): score for (u, v), score in min_res["edge_nrs"].items()
                    if (u in partition_a) != (v in partition_a)}
    
    min_edge = min(cut_edge_nrs, key=lambda uv: cut_edge_nrs[uv], default=None)
    print("min cut edge:", min_edge, "nr edges:", cut_edge_nrs.get(min_edge))
        

    max_edge = max(finite_edges, key=lambda uv: finite_edges[uv], default=None)
    max_edge_score = min_res["edge_nrs"][max_edge]
    max_edges = [(u, v) for (u, v), score in min_res["edge_nrs"].items() if score == max_edge_score ]
    max_edge = max(max_edges, key=lambda uv: degrees[uv[0]] + degrees[uv[1]])

    max_edge_nr = min_res["edge_nrs"][max_edge]
    print(f"MAX EDGE NR: {max_edge_nr}")

    del_edge = max_edge

    # highlight_edges(G, {del_edge})
    return del_edge

def find_new_edge(min_res, active_nodes, adj_sp):
    partition_a = min_res["partition"]
    partition_b = list(set(active_nodes) - set(partition_a))

    valid_sp = build_validity_matrix(adj_sp, partition_a, partition_b)
    valid_coo = valid_sp.tocoo()
    degrees = np.array(adj_sp.tocsr().sum(axis=1)).flatten()

    if valid_coo.nnz == 0:
        print("no valid edges found")
        return None

    combined_degrees = degrees[valid_coo.row] + degrees[valid_coo.col]
    best = np.argmin(combined_degrees)
    u = int(valid_coo.row[best])
    v = int(valid_coo.col[best])

    print(f"new edge: {u}, {v}")
    # highlight_nodes(G, {u, v}, color="limegreen")

    return (u, v)

def get_non_isd_nodes(G, isd_n):
    return [n for n, data in G.nodes(data=True) if data["isd_n"] != isd_n]

def get_isd_nodes(G, isd_n):
    return [(n,data) for n, data in G.nodes(data=True) if data["isd_n"] == isd_n]

def get_core_nodes(nodes):
    return [n for n, data in nodes if data["is_core"]]

def get_v_e_for_isd(G, isd_n):
    isd_nodes = set(get_isd_nodes(G, isd_n))
    v = len(isd_nodes)
    e = sum(1 for u, w in G.edges() if u in isd_nodes and w in isd_nodes)
    return v, e

def get_v_e_for_core(G):
    core_nodes = set(get_core_nodes(G))
    v = len(core_nodes)
    e = sum(1 for u, w in G.edges() if u in core_nodes and w in core_nodes)
    return v, e

def get_subdivision_max_cheeger(G, global_ratio, v_sub):
    even_edge_n = float(math.floor(global_ratio * v_sub))
    return even_edge_n / float(v_sub)

def get_max_cheeger(G):
    global_ratio = float(len(G.edges())) / float(len(G.nodes()))
    min_max_isd_cheeger = math.inf
    isds = sorted(set(data["isd_n"] for _, data in G.nodes(data=True)))
    all_isd_nodes = [get_isd_nodes(G, isd_n) for isd_n in isds]

    core_v = float(len(get_core_nodes(G.nodes(data=True))))
    even_edge_core = float(math.floor(global_ratio * core_v))
    core_max_cheeger = get_subdivision_max_cheeger(G, global_ratio, core_v)
    min_max_isd_cheeger = min(core_max_cheeger, min_max_isd_cheeger)

    for isd_nodes in all_isd_nodes:
        min_max_isd_cheeger = min(get_subdivision_max_cheeger(G, global_ratio, len(isd_nodes)), min_max_isd_cheeger)
        isd_core = get_core_nodes(isd_nodes)
        connecting_nodes = math.floor(2 * even_edge_core / core_v) * len(isd_core)
        inter_isd_cheeg = float(connecting_nodes) / float(len(isd_nodes))
        min_max_isd_cheeger = min(inter_isd_cheeg, min_max_isd_cheeger)

    return min_max_isd_cheeger

def iteration(G, max_cheeger, iteration, min_res, non_core_nodes):
    full_adj = nx.to_scipy_sparse_array(G).tocoo()

    min_res = run_network_partitioning(full_adj, iteration=iteration)

    # draw_partition(G, min_res["partition"])
    # show_edge_weights(G, min_res["edge_nrs"])

    print(f"max cheeger: {max_cheeger}")

    if (max_cheeger <= min_res["cheeger"]):
        print(f"reached maximum configuration in iteration {iteration}!")
        return G, min_res

    del_edge = find_old_edge(G, min_res, full_adj)
    new_edge = find_new_edge(min_res, G.nodes(), full_adj)

    if (del_edge != None and new_edge != None):    
        H = G.copy()
        H.add_edge(new_edge[0], new_edge[1])
        H.remove_edge(del_edge[0], del_edge[1])

        H_min_res = run_network_partitioning(nx.to_scipy_sparse_array(H).tocoo(), iteration=iteration)
        core_min_res = run_network_partitioning(nx.to_scipy_sparse_array(H).tocoo(), mask_nodes=non_core_nodes)

        print(f"H cheeger: {H_min_res['cheeger']}, G cheeger: {min_res['cheeger']}, core cheeger: {core_min_res['cheeger']}")
        if (H_min_res["cheeger"] < min_res["cheeger"] or core_min_res["cheeger"] <= 0.0):
            return G, min_res
        
        return H, H_min_res

    return G, min_res

MAX_ITERATIONS = 5

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--topology-config", "-tc", required=True)
    args = parser.parse_args()
    G = yaml_to_graph(args.topology_config)
    path = args.topology_config.split("_")[0]
    path += "_rnp"

    max_cheeger = get_max_cheeger(G)
    for i in range(MAX_ITERATIONS):
        min_res = run_network_partitioning(nx.to_scipy_sparse_array(G).tocoo())
        non_core_nodes = [node for node in G.nodes() if not G.nodes[node]["is_core"]]
        G, min_res = iteration(G, max_cheeger, i, min_res, non_core_nodes)
        graph_to_yaml(G, path + f"_it{i+1}.yaml")