import math
import networkx as nx
import scipy.sparse
import numpy as np
from scripts.helpers.parse_topology import yaml_to_graph, graph_to_yaml
import argparse
import matplotlib.pyplot as plt

NR_PASSES = 6
R_VALUES_DC = [0.4575, 0.3725]
R_VALUES = [0.05, 0.15, 0.25, 0.35, 0.45]
M_DC = 0.0425
M = 0.5

def visualize_partition(G, partition_a, mask_nodes, title="Graph Partition"):
    """
    Visualize the graph partition with cut edges highlighted.
    """    
    # Create color map for nodes
    node_colors = []
    for node in G.nodes():
        if node in partition_a:
            node_colors.append('lightblue')
        elif node not in mask_nodes:
            node_colors.append('lightcoral')
        else:
            node_colors.append('grey')
    
    # Identify cut edges
    cut_edges = []
    internal_edges = []
    for u, v in G.edges():
        if (u in partition_a) != (v in partition_a) and (u not in mask_nodes) and (v not in mask_nodes):
            cut_edges.append((u, v))
        else:
            internal_edges.append((u, v))
    
    # Draw graph
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G, seed=42)
    
    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, 
                          node_size=500, alpha=0.9)
    
    # Draw internal edges (gray)
    nx.draw_networkx_edges(G, pos, edgelist=internal_edges, 
                          width=1, alpha=0.5, edge_color='gray')
    
    # Draw cut edges (red, thicker)
    nx.draw_networkx_edges(G, pos, edgelist=cut_edges, 
                          width=2, alpha=0.8, edge_color='red')
    
    # Draw labels
    nx.draw_networkx_labels(G, pos, font_size=10)
    
    # Add legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='lightblue', label=f'Partition A ({len(partition_a)} nodes)'),
        Patch(facecolor='lightcoral', label=f'Partition B ({len(G.nodes()) - len(partition_a)} nodes)'),
        Patch(facecolor='red', label=f'Cut edges ({len(cut_edges)})')
    ]
    plt.legend(handles=legend_elements, loc='upper right')
    
    plt.title(title)
    plt.axis('off')
    plt.tight_layout()
    plt.show()
    
    return len(cut_edges)

def highlight_edges(G, edges, title="Highlighted Edges"):
    """
    Highlight a set of edges in the graph.
    """
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G, seed=42)
    
    # Draw all nodes
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=500, alpha=0.9)
    
    # Draw all edges in gray
    nx.draw_networkx_edges(G, pos, width=1, alpha=0.3, edge_color='gray')
    
    # Draw highlighted edges in red
    nx.draw_networkx_edges(G, pos, edgelist=edges, width=3, alpha=0.8, edge_color='orange')
    
    # Draw labels
    nx.draw_networkx_labels(G, pos, font_size=10)
    
    plt.title(title)
    plt.axis('off')
    plt.tight_layout()
    plt.show()


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

def partition_pass(G, r, m, masked_nodes):
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


        # if (min_cut_edges > n_cut_edges):
        #     min_cut_edges = n_cut_edges
        best_assignment = assignment.copy()
        deg = cur_deg
        min_cut_edges = n_cut_edges

    if (np.sum(best_assignment==-1) >= np.sum(best_assignment==1)):
        partition = np.where(best_assignment==-1)[0].tolist()
    else:
        partition = np.where(best_assignment==1)[0].tolist()
    return min_cut_edges, partition, deg


def run_network_partitioning(G, r_values, m, mode="dc", mask_nodes=[]):
    best_cheeger = math.inf
    best_cut = math.inf
    best_partition = (math.inf, math.inf, None, math.inf)
    for r in r_values:

        for i in range(NR_PASSES):
            res = partition_pass(G, r, m, mask_nodes)

            cut_edges, part_a, degrees = res
            print(cut_edges, part_a, degrees)
            if (mode=="dc"):
                if (best_cut > cut_edges or (best_cut == cut_edges and best_partition[3] <= degrees)):
                    print("update")
                    best_cut = cut_edges
                    best_partition = (cut_edges/len(part_a), cut_edges, part_a, degrees)
            else:
                if (cut_edges/len(part_a) < best_cheeger or (cut_edges/len(part_a) == best_cheeger and best_partition[3] <= degrees)):
                    print("update")
                    best_cheeger = cut_edges/len(part_a)
                    best_partition = (cut_edges/len(part_a), cut_edges, part_a, degrees)


    # visualize_partition(G, best_partition[2], mask_nodes)
    print(best_partition[2])
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

def get_new_edge_scores(min_res):
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

    del_edge = divide_and_conquer_max(G, min_res, G.nodes(), [])
    while(del_edge not in G.edges()):
        del_edge = divide_and_conquer_max(G, min_res, G.nodes(), [])
    # highlight_edges(G, [del_edge])

    node_scores = get_new_edge_scores(min_res)
    new_edge = find_new_edge(min_res, G.nodes(), nx.adjacency_matrix(G),  node_scores)

    if (del_edge != None and new_edge != None):    
        H = G.copy()
        if (add):
            H.add_edge(new_edge[0], new_edge[1])
        
        if (delete):
            H.remove_edge(del_edge[0], del_edge[1])

        H_min_res = run_network_partitioning(G, R_VALUES_DC, M_DC)
        print(f"new cheeger: {H_min_res['cheeger']}, old cheeger: {min_res['cheeger']}")
        core_min_res = run_network_partitioning(G, R_VALUES_DC, M_DC,mask_nodes=non_core_nodes)

        if (add and (H_min_res["cheeger"] < min_res["cheeger"] or H_min_res["cheeger"] <= 0)):
            return G, min_res

        if (add and core_min_res["cheeger"] <= 0.0):
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

    min_res = run_network_partitioning(G, R_VALUES_DC, M_DC)
    for i in range(int(args.iterations)):
        non_core_nodes = [node for node in G.nodes() if not G.nodes[node]["is_core"]]
        G, min_res = iteration(G, min_res, non_core_nodes, delete=(not args.add_only), add=(not args.delete_only))
        graph_to_yaml(G, path + f"_it{i+1}.yaml")