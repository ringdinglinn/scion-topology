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
R_VALUES_DC = [0.37524, 0.4575]
R_VALUES = [0.05, 0.15, 0.25, 0.35, 0.45]
M_DC = 0.0425
M = 0.5

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

def create_cut(cut_values, assignment, degree_diff=None):
    n_cuts = int((cut_values == -1).sum()) // 2
    a = int((assignment == -1).sum().item())
    b = int((assignment == 1).sum().item())
    if degree_diff is not None:
        a = degree_diff[assignment == -1].sum()
        b = degree_diff[assignment == 1].sum()
    return n_cuts, a, b

def cheeger(c, a, b):
    return c / min(a, b)

# --- NETWORK PARTITIONING ---------------------------------------------------------------

def initial_partition(n, r, mask_nodes, it=0):
    keep_mask = torch.ones(n, dtype=torch.bool)
    keep_mask[mask_nodes] = False
    perm = torch.arange(n)[keep_mask][torch.randperm(keep_mask.sum())]
    r = min(1 - r, r)
    k = max(1, round(len(perm) * r))
    A_idx = perm[:k]
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

def calculate_prospective_cut_sizes_weighted(assignment, mask_bool, degree_diff):
    num_neg_total = (assignment == -1).sum().item()
    num_pos_total = (assignment == 1).sum().item()
    n = num_neg_total + num_pos_total

    neg_diff_total = degree_diff[assignment.numpy() == -1].sum()
    pos_diff_total = degree_diff[assignment.numpy() == 1].sum()

    # prospective degree_diff sums after each node flips
    # if node is -1, flipping removes it from neg and adds to pos
    # if node is +1, flipping removes it from pos and adds to neg
    num_neg = np.where(assignment.numpy() == -1,
                       neg_diff_total - degree_diff,
                       neg_diff_total + degree_diff)
    num_pos = np.where(assignment.numpy() == 1,
                       pos_diff_total - degree_diff,
                       pos_diff_total + degree_diff)

    num_neg[mask_bool] = 0
    num_pos[mask_bool] = 0
    return num_neg, num_pos, n

def update_balanced(balanced, assignment, r, m, mask_bool):
    a, b, n = calculate_prospective_cut_sizes(assignment, mask_bool)

    s = np.minimum(a, b)
    max_m = round(n * m)
    s_r = round(min(n * r, n * (1 - r)))

    balance_ok = (np.abs(s_r - s) <= max_m)
    non_empty_ok = (a > 0) & (b > 0)
    balanced[:] = balance_ok & non_empty_ok 

def partition_pass(adj_sp, full_adj, r, m, mode="dc", mask_nodes=[], it=0):
    n = adj_sp.shape[0]

    mask_bool = np.zeros(n, dtype=bool)
    mask_bool[mask_nodes] = True

    degree = np.zeros(n, dtype=np.float32)
    np.add.at(degree, full_adj.row, 1)
    max_degree = degree.max() + 1
    degree_diff = max_degree - degree

    assignment = initial_partition(n, r, mask_nodes, it=it)

    moveable = np.ones(n, dtype=bool)
    moveable[mask_nodes] = False

    cut_values = compute_cut_values(adj_sp, assignment)

    balanced = np.ones(n, dtype=bool)
    update_balanced(balanced, assignment, r, m, mask_bool)

    gains = np.zeros(n, dtype=float)

    if (mode=="dc"):
        cut = create_cut(cut_values, assignment, degree_diff=degree_diff)
    else:
        cut = create_cut(cut_values, assignment)
    opt_cut = (cheeger(*cut), np.where(assignment == -1)[0].tolist(), cut_values, gains)

    while (moveable & balanced).any().item():
        if (mode=="dc"):
            num_neg, num_pos, _ = calculate_prospective_cut_sizes_weighted(assignment, mask_bool, degree_diff)
        else:
            num_neg, num_pos, _ = calculate_prospective_cut_sizes(assignment, mask_bool)
        min_size = np.minimum(num_neg, num_pos)
    
        row_sums = row_sums_from_cut(adj_sp, cut_values, n)
        gains[moveable] = (-row_sums / min_size)[moveable]

        candidates = np.where(moveable & balanced)[0]

        max_vertex = int(candidates[np.argmax(gains[candidates])].item())
        assignment[max_vertex] *= -1

        # flip sign of all cut_values touching max_vertex
        affected = (adj_sp.row == max_vertex) | (adj_sp.col == max_vertex)
        cut_values[affected] *= -1

        update_balanced(balanced, assignment, r, m, mask_bool)
        moveable[max_vertex] = False

        if (mode=="dc"):
            cut = create_cut(cut_values, assignment, degree_diff=degree_diff)
        else:
            cut = create_cut(cut_values, assignment)
        ch = cheeger(*cut)

        if (ch < opt_cut[0]):
            opt_cut = (ch, np.where(assignment == -1)[0].tolist(), cut_values, gains)

    return opt_cut

# --- Top-level ---------------------------------------------------------------

def run_network_partitioning(adj_mat, r_values, m, mode="dc", mask_nodes=[], it=0):
    results = {}
    opt = (lambda x, y: x < y)
    masked_adj = initialize_adj_matrix(adj_mat, mask_nodes, adj_mat.shape[0])

    for r in r_values:
        best_cheeger = math.inf
        best_partition = None
        updates = 0

        for i in range(NR_PASSES):
            res = partition_pass(masked_adj, adj_mat, r, m, mode=mode, mask_nodes=mask_nodes, it=(it*NR_PASSES + i))

            ch, part_a, cut_vals, gains = res
            if opt(ch, best_cheeger):
                best_cheeger = ch
                best_partition = (ch, part_a, cut_vals, gains)
                updates += 1

        if best_partition is None:
            results[str(r)] = None
        else:
            ch, part_a, cut_vals, gains = best_partition
            results[str(r)] = {"cheeger": ch, "partition": part_a, "cut_values": cut_vals, "gains": gains}

    
    results = {k: v for k, v in results.items() if v is not None}
    if not results:
        return None
    best_r = min(results.keys(), key=lambda k: results[k]["cheeger"])
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
    
def divide_and_conquer_min(G, adj, min_res, it, mask_nodes, node_scores, counter):
    partition_a = min_res["partition"]
    partition_b = list(set(G.nodes()) - set(mask_nodes) - set(partition_a))

    node_scores[partition_a] = counter
    node_scores[partition_b] = counter
    counter += 1

    if (len(partition_a) <= 1):
        return node_scores
    elif (len(partition_b) <= 1):
        return node_scores

    min_res_a = run_network_partitioning(adj, R_VALUES_DC, M_DC, it=it, mask_nodes=(partition_b + mask_nodes))
    min_res_b = run_network_partitioning(adj, R_VALUES_DC, M_DC, it=it, mask_nodes=(partition_a + mask_nodes))

    if (min_res_a["cheeger"] < min_res_b["cheeger"]):
        mask_nodes = mask_nodes + partition_b

        return divide_and_conquer_min(G, adj, min_res_a, it, mask_nodes, node_scores, counter)
    else:
        mask_nodes = mask_nodes + partition_a

        return divide_and_conquer_min(G, adj, min_res_b, it, mask_nodes, node_scores, counter)

def get_new_edge_scores(full_adj, min_res, it):
    partition_a = min_res["partition"]
    partition_b = list(set(G.nodes()) - set(partition_a))
    node_scores = np.full(len(G.nodes()), 0)
    if (len(partition_a) > 1):
        min_res_a = run_network_partitioning(full_adj, R_VALUES_DC, M_DC, mask_nodes=partition_b, it=it)
        divide_and_conquer_min(G, full_adj, min_res_a, it, partition_b, node_scores, 0)
    if (len(partition_b) > 1):
        min_res_b = run_network_partitioning(full_adj, R_VALUES_DC, M_DC, mask_nodes=partition_a, it=it)
        divide_and_conquer_min(G, full_adj, min_res_b, it, partition_a, node_scores, 0)

    return node_scores

def find_new_edge(min_res, active_nodes, adj_sp, scores):
    partition_a = min_res["partition"]
    partition_b = list(set(active_nodes) - set(partition_a))

    valid_sp = build_validity_matrix(adj_sp, partition_a, partition_b)
    valid_coo = valid_sp.tocoo()

    if valid_coo.nnz == 0:
        print("no valid edges found")
        return None

    combined_score = scores[valid_coo.row] + scores[valid_coo.col]

    idx = np.argmax(combined_score)
    u = int(valid_coo.row[idx])
    v = int(valid_coo.col[idx])

    return (u, v)

def divide_and_conquer_max(G, adj, min_res, it, active_nodes, mask_nodes):
    if (min_res["cheeger"] < 0):
        return None
    
    if (len(active_nodes) == 2):
        return (active_nodes[0], active_nodes[1])

    partition_a = min_res["partition"]
    partition_b = list(set(active_nodes) - set(min_res["partition"]))

    if (len(partition_a) == 1):
        min_res_b = run_network_partitioning(adj, R_VALUES_DC, M_DC, it=it, mask_nodes=(partition_a + mask_nodes))
        return divide_and_conquer_max(G, adj, min_res_b, it, partition_b, (partition_a + mask_nodes))
    elif (len(partition_b) == 1):
        min_res_a = run_network_partitioning(adj, R_VALUES_DC, M_DC, it=it, mask_nodes=(partition_b + mask_nodes))
        return divide_and_conquer_max(G, adj, min_res_a, it, partition_a, (partition_b + mask_nodes))
    
    min_res_a = run_network_partitioning(adj, R_VALUES_DC, M_DC, it=it, mask_nodes=(partition_b + mask_nodes))
    min_res_b = run_network_partitioning(adj, R_VALUES_DC, M_DC, it=it, mask_nodes=(partition_a + mask_nodes))

    if (min_res_a["cheeger"] > min_res_b["cheeger"]):
        return divide_and_conquer_max(G, adj, min_res_a, it, partition_a, (partition_b + mask_nodes))
    else:
        return divide_and_conquer_max(G, adj, min_res_b, it, partition_b, (partition_a + mask_nodes))

def iteration(G, it, min_res, non_core_nodes, delete=True, add=True):
    full_adj = nx.to_scipy_sparse_array(G).tocoo()

    del_edge = divide_and_conquer_max(G, full_adj, min_res, it, G.nodes(), [])

    node_scores = get_new_edge_scores(full_adj, min_res, it)
    new_edge = find_new_edge(min_res, G.nodes(), full_adj, node_scores)

    if (del_edge != None and new_edge != None):    
        H = G.copy()
        if (add):
            H.add_edge(new_edge[0], new_edge[1])
        
        if (delete):
            H.remove_edge(del_edge[0], del_edge[1])

        H_min_res = run_network_partitioning(nx.to_scipy_sparse_array(H).tocoo(), R_VALUES, M, mode="global", it=it)
        print(f"it: {i}, new cheeger: {H_min_res['cheeger']}, old cheeger: {min_res['cheeger']}")
        core_min_res = run_network_partitioning(nx.to_scipy_sparse_array(H).tocoo(), R_VALUES, M, mode="global", mask_nodes=non_core_nodes)

        if (add and H_min_res["cheeger"] < min_res["cheeger"]):
            return G, min_res

        if (core_min_res["cheeger"] <= 0.0 or H_min_res["cheeger"] <= 0):
            return G, min_res
        
        return H, H_min_res

    return G, min_res

MAX_ITERATIONS = 5

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--topology-config", "-tc", required=True)
    parser.add_argument("--add-only", action="store_true")
    parser.add_argument("--delete-only", action="store_true")
    args = parser.parse_args()
    G = yaml_to_graph(args.topology_config)
    path = args.topology_config.split("_")[0]

    if args.add_only:
        path += "_rnpa"
    elif args.delete_only:
        path += "_rnpd"
    else:
        path += "_rnp"


    min_res = run_network_partitioning(nx.to_scipy_sparse_array(G).tocoo(), R_VALUES, M, mode="global")
    for i in range(MAX_ITERATIONS):
        non_core_nodes = [node for node in G.nodes() if not G.nodes[node]["is_core"]]
        G, min_res = iteration(G, i, min_res, non_core_nodes, delete=(not args.add_only), add=(not args.delete_only))
        graph_to_yaml(G, path + f"_it{i+1}.yaml")