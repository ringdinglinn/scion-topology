import math
import networkx as nx
import scipy.sparse
import numpy as np
from scripts.helpers.parse_topology import yaml_to_graph, graph_to_yaml
import argparse

NR_PASSES = 20
R_VALUES_DC = [0.4575, 0.3725]
R_VALUES = [0.05, 0.15, 0.25, 0.35, 0.45]
M_DC = 0.0425
M = 0.5

def is_balanced(a, b, is_a, r, m, n):
    if (is_a):
        a -= 1
        b += 1
    else:
        a += 1
        b -= 1
    s = min(a, b)

    max_m = round(n * m)
    s_r = round(min(n * r, n * (1 - r)))

    balance_ok = (abs(s_r - s) <= max_m)
    non_empty_ok = (a > 0) & (b > 0)

    return balance_ok & non_empty_ok

def update_gains(G, idx_to_node, node_to_idx, assignment, gains, vertex, mask_nodes):
    gains[vertex] = -np.inf
    node = idx_to_node[vertex]
    cut_edges = 0
    for neighbor in G.neighbors(node):
        j = node_to_idx[neighbor]
        if j in mask_nodes:
            continue
        # Before move: check if edge was cut
        # After move: assignment[vertex] flips
        if assignment[vertex] == assignment[j]:
            # Same partition BEFORE move → edge NOT cut
            # After move → edge WILL BE cut
            gains[j] += 2  # Moving vertex away increases neighbor's gain
            cut_edges += 1  # One more cut edge
        else:
            # Different partition BEFORE move → edge IS cut
            # After move → edge will NOT be cut
            gains[j] -= 2  # Moving vertex closer decreases neighbor's gain
            cut_edges -= 1  # One fewer cut edge
    return cut_edges

def intialize_gains(G, idx_to_node, node_to_idx, assignment, mask_nodes):
    n = assignment.shape[0]
    gains = np.zeros(n)
    n_cut_edges = 0
    for i in range(n):
        if (i in mask_nodes):
            gains[i] = -np.inf
            continue
        node = idx_to_node[i]
        for neighbor in G.neighbors(node):
            j = node_to_idx[neighbor]
            if (j in mask_nodes):
                continue
            if assignment[j] != assignment[i]:
                gains[i] += 1
                n_cut_edges += 1
            else:
                gains[i] -= 1

    n_cut_edges //= 2
    order = np.argsort(-gains)
    return gains, order, n_cut_edges


# --- Algorithm ---------------------------------------------------------------

def initial_partition(n, r, mask_nodes):
    mask_set = set(mask_nodes)
    non_masked_indices = np.array([i for i in range(n) if i not in mask_set])
    n_moveable = len(non_masked_indices)
    
    if n_moveable == 0:
        return np.zeros(n), 0, 0
    
    perm = np.random.permutation(non_masked_indices)
    
    r = min(1 - r, r)
    k = max(1, round(n_moveable * r))
    
    assignment = np.ones(n)
    assignment[list(mask_nodes)] = 0
    
    A_idx = perm[:k]
    assignment[A_idx] = -1
    
    size_a = k
    size_b = n_moveable - k
    
    return assignment, size_a, size_b

def calulate_cheeger(n_cut, size_a, size_b):
    return n_cut / min(size_a, size_b)


def partition_pass(G, r, m, masked_nodes, mode="dc"):
    idx_to_node = {i:node for i, node in enumerate(list(G.nodes()))}
    node_to_idx = {node:i for i, node in enumerate(list(G.nodes()))}
    n = len(G.nodes())
    if n == 0:
        return None

    assignment, size_a, size_b = initial_partition(n, r, masked_nodes)

    degrees = np.array([G.degree[idx_to_node[i]] for i in range(len(assignment))])
    deg_a = degrees[assignment == -1].sum()
    deg_b = degrees[assignment == 1].sum()
    cur_deg = deg_a if (size_a <= size_b) else deg_b
    deg = cur_deg

    moveable = np.ones(n, dtype=bool)
    moveable[list(masked_nodes)] = False

    gains, order, n_cut_edges = intialize_gains(G, idx_to_node, node_to_idx, assignment, masked_nodes) 

    best_assignment = assignment.copy() 
    min_cut_edges = n_cut_edges

    while (moveable).any().item():
        idx = 0
        vertex = order[idx]

        while idx < len(gains) :
            vertex = order[idx]
            if ((not is_balanced(size_a, size_b, assignment[vertex]==-1, r, m, n) or not moveable[vertex])):
                idx += 1
            else:
                break

        if idx == len(gains):
            break

        # update stuff

        if assignment[vertex] == -1:
            size_a -= 1
            size_b += 1
            deg_a -= G.degree[idx_to_node[vertex]]
            deg_b += G.degree[idx_to_node[vertex]]
        else:
            size_a += 1
            size_b -= 1
            deg_a += G.degree[idx_to_node[vertex]]
            deg_b -= G.degree[idx_to_node[vertex]]

        delta_edges = update_gains(G, idx_to_node, node_to_idx, assignment, gains, vertex, masked_nodes)
        n_cut_edges += delta_edges
        assignment[vertex] *= -1

        if (size_a <= size_b):
            cur_deg = deg_a
        else:
            cur_deg = deg_b

        moveable[vertex] = False

        order = np.argsort(-gains)

        if (min_cut_edges > n_cut_edges):
            best_assignment = assignment.copy()
            deg = cur_deg
            min_cut_edges = n_cut_edges

    if (np.sum(best_assignment==-1) <= np.sum(best_assignment==1)):
        partition = np.where(best_assignment==-1)[0].tolist()
    else:
        partition = np.where(best_assignment==1)[0].tolist()
    return min_cut_edges/len(partition), min_cut_edges, partition, deg

def run_network_partitioning(G, r_values, m, mode="dc", mask_nodes=[]):
    best_cheeger = math.inf
    best_cut = math.inf
    best_partition = (math.inf, math.inf, None, math.inf)
    for r in r_values:

        for _ in range(NR_PASSES):
            res = partition_pass(G,r, m, mask_nodes, mode=mode)

            ch, cut_edges, part_a, degrees = res
            if ((mode=="dc" and (best_cut > cut_edges or (best_cut == cut_edges and best_partition[3] > degrees)))
                or (mode!="dc" and (ch < best_cheeger or (ch == best_cheeger and best_partition[3] > degrees)))):
                best_cut = cut_edges
                best_cheeger = ch
                best_partition = (ch, cut_edges, part_a, degrees)

    return {"cheeger": best_partition[0], "partition": best_partition[2]}


# --- DIVIDE AND CONQUER LOGIC -----------------------

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
    
def divide_and_conquer_min(G, min_res, mask_nodes, node_scores, counter):
    partition_a = min_res["partition"]
    partition_b = list(set(G.nodes()) - set(mask_nodes) - set(partition_a))

    node_scores[partition_a] = counter
    node_scores[partition_b] = counter
    counter += 1

    if (len(partition_a) <= 1):
        return node_scores
    elif (len(partition_b) <= 1):
        return node_scores

    min_res_a = run_network_partitioning(G, R_VALUES_DC, M_DC, mask_nodes=(partition_b + mask_nodes))
    min_res_b = run_network_partitioning(G, R_VALUES_DC, M_DC, mask_nodes=(partition_a + mask_nodes))

    degrees = np.array([G.degree(node) for node in G.nodes()])
    deg_a = sum(degrees[node] for node in partition_a)
    deg_b = sum(degrees[node] for node in partition_b)

    if (min_res_a["cheeger"] < min_res_b["cheeger"] or (min_res_a["cheeger"] == min_res_b["cheeger"] and deg_a <= deg_b)):
        mask_nodes = mask_nodes + partition_b
        return divide_and_conquer_min(G, min_res_a, mask_nodes, node_scores, counter)
    else:
        mask_nodes = mask_nodes + partition_a
        return divide_and_conquer_min(G, min_res_b, mask_nodes, node_scores, counter)

def get_new_edge_scores(G, min_res):
    partition_a = min_res["partition"]
    partition_b = list(set(G.nodes()) - set(partition_a))
    node_scores = np.full(len(G.nodes()), 0)
    if (len(partition_a) > 1):
        min_res_a = run_network_partitioning(G, R_VALUES_DC, M_DC, mask_nodes=partition_b)
        divide_and_conquer_min(G, min_res_a, partition_b, node_scores, 0)
    if (len(partition_b) > 1):
        min_res_b = run_network_partitioning(G, R_VALUES_DC, M_DC, mask_nodes=partition_a)
        divide_and_conquer_min(G, min_res_b, partition_a, node_scores, 0)

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

def divide_and_conquer_max(G, min_res, active_nodes, mask_nodes):
    if (min_res["cheeger"] < 0):
        return None
    
    if (len(active_nodes) == 2):
        return (active_nodes[0], active_nodes[1])

    partition_a = min_res["partition"]
    partition_b = list(set(active_nodes) - set(min_res["partition"]))

    if (len(partition_a) == 1):
        min_res_b = run_network_partitioning(G, R_VALUES_DC, M_DC, mask_nodes=(partition_a + mask_nodes))
        return divide_and_conquer_max(G, min_res_b, partition_b, (partition_a + mask_nodes))
    elif (len(partition_b) == 1):
        min_res_a = run_network_partitioning(G, R_VALUES_DC, M_DC, mask_nodes=(partition_b + mask_nodes))
        return divide_and_conquer_max(G, min_res_a, partition_a, (partition_b + mask_nodes))
    
    min_res_a = run_network_partitioning(G, R_VALUES_DC, M_DC, mask_nodes=(partition_b + mask_nodes))
    min_res_b = run_network_partitioning(G, R_VALUES_DC, M_DC, mask_nodes=(partition_a + mask_nodes))

    degrees = np.array([G.degree(node) for node in G.nodes()])
    deg_a = sum(degrees[node] for node in partition_a)
    deg_b = sum(degrees[node] for node in partition_b)

    if (min_res_a["cheeger"] > min_res_b["cheeger"] or (min_res_a["cheeger"] == min_res_b["cheeger"] and deg_a >= deg_b)):
        return divide_and_conquer_max(G, min_res_a, partition_a, (partition_b + mask_nodes))
    else:
        return divide_and_conquer_max(G, min_res_b, partition_b, (partition_a + mask_nodes))
        


# --- TOP LEVEL LOGIC ---------------

def iteration(G, min_res, non_core_nodes, delete=True, add=True):
    full_adj = nx.to_scipy_sparse_array(G).tocoo()

    del_edge = divide_and_conquer_max(G, min_res, G.nodes(), [])

    node_scores = get_new_edge_scores(G, min_res)
    new_edge = find_new_edge(min_res, G.nodes(), full_adj, node_scores)


    if (del_edge != None and new_edge != None):    
        H = G.copy()

        if (add):
            H.add_edge(new_edge[0], new_edge[1])
        
        if (delete):
            H.remove_edge(del_edge[0], del_edge[1])

        H_min_res = run_network_partitioning(H, R_VALUES, M, mode="global")
        print(f"new cheeger: {H_min_res['cheeger']}, old cheeger: {min_res['cheeger']}")
        core_min_res = run_network_partitioning(H, R_VALUES, M, mode="global", mask_nodes=non_core_nodes)

        if (add and (H_min_res["cheeger"] < min_res["cheeger"] or H_min_res["cheeger"] <= 0)):
            return G, min_res

        if (add and core_min_res["cheeger"] <= 0.0):
            print("disconnected core")
            return G, min_res
        
        return H, H_min_res

    return G, min_res


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--topology-config", "-tc", required=True)
    parser.add_argument("--output-dir", "-o", required=True)
    parser.add_argument("--add-only", action="store_true")
    parser.add_argument("--delete-only", action="store_true")
    parser.add_argument("--iterations", "-k", required=True)
    args = parser.parse_args()
    G = yaml_to_graph(args.topology_config)
    topo_name = args.topology_config.split('/')[-1]
    topo_name = topo_name.split('_')[0]
    path = args.output_dir + topo_name

    print(f"optimizing topology {topo_name}")

    path += "_rnp"

    min_res = run_network_partitioning(G, R_VALUES, M, mode="global")

    for i in range(int(args.iterations)):
        non_core_nodes = [node for node in G.nodes() if not G.nodes[node]["is_core"]]
        G, min_res = iteration(G, min_res, non_core_nodes, delete=(not args.add_only), add=(not args.delete_only))
        graph_to_yaml(G, path + f"_it{i+1}.yaml")