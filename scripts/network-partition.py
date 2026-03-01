import math
import json
import networkx as nx
import torch
import numpy as np
from scipy import sparse as sp
import time
from helpers.parse_topology import yaml_to_graph, graph_to_yaml
import argparse
import matplotlib.pyplot as plt
import yaml


# --- Utilities ----------------------------------------------------------------

MIN_PART_SIZE = 1

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

def update_balanced(balanced, assignment, r):
    """
    Updates the balanced tensor in-place.
    - balanced: torch.BoolTensor of shape (n,)
    - assignment: torch.IntTensor of shape (n,) with values ±1
    - r: float, target fraction
    """
    m = 0.05

    n = assignment.numel()
    num_neg = (assignment == -1).sum().item()
    num_pos = n - num_neg

    a = num_neg + assignment
    b = num_pos - assignment
    s = torch.minimum(a, b)

    max_m = round(n * m)
    s_r = round(min(n * r, n * (1 - r)))

    # in-place update
    balance_ok = (torch.abs(s_r - s) <= max_m)
    non_empty_ok = (a > 0) & (b > 0)

    # in-place update
    balanced.copy_(balance_ok & non_empty_ok)

# --- Sparse helpers -----------------------------------------------------------

def compute_cut_data_from_adj(adj_row, adj_col, adj_data, assignment):
    """
    Given adjacency in COO (adj_row, adj_col, adj_data) and assignment (tensor of ±1),
    compute cut_matrix = adj @ diag(assignment) in COO-value form.
    For each nonzero (i,j) of adj, cut_value = adj_value * assignment[j].
    Returns cut_row, cut_col, cut_data (same indices as adjacency with new values).
    (We simply reuse adj_row/adj_col and modify data.)
    """
    # assignment is 1-D tensor (n,), and adj_col indexes into it
    cut_data = adj_data * assignment[adj_row] * assignment[adj_col].to(adj_data.dtype)
    return adj_row, adj_col, cut_data

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
    n_cuts_raw = int((cut_data == -1).sum().item())
    n_cuts = n_cuts_raw // 2

    a, b = int((assignment == -1).sum().item()), int((assignment == 1).sum().item())
    return (n_cuts, a, b)

def cheeger(c, a, b):
    return c / min(a, b)

# --- Algorithm ---------------------------------------------------------------

def partition_pass(G, r, mode="min"):
    """
    One pass of the partition improvement heuristic, implemented with PyTorch tensors.
    Returns tuple (min_cuts, |A|, |B|) found during this pass (same semantics as original).
    """
    nodes = list(G.nodes())
    n = len(nodes)
    if n == 0:
        return None

    # Mapping from node label -> contiguous index [0..n-1]
    idx_of_node = {node: i for i, node in enumerate(nodes)}
    # Build adjacency as COO via scipy then to torch
    adj_sp = nx.to_scipy_sparse_array(G).tocoo()
    # Sanity: if adjacency has shape mismatch, handle it
    assert adj_sp.shape[0] == n and adj_sp.shape[1] == n, "Adjacency shape mismatch with node list"

    adj_row = torch.tensor(adj_sp.row, dtype=torch.long)
    adj_col = torch.tensor(adj_sp.col, dtype=torch.long)
    adj_data = torch.tensor(adj_sp.data, dtype=torch.float32)

    # initial random partition: choose k nodes for A (assignment -1), rest 1
    k = round(n * r)
    perm = torch.randperm(n)
    A_idx = perm[:k]

    assignment = torch.ones(n, dtype=torch.int32)
    assignment[A_idx] = -1

    moveable = torch.ones(n, dtype=torch.bool)

    # Compute cut_matrix = adj @ diag(assignment) in COO form
    cut_row, cut_col, cut_data = compute_cut_data_from_adj(adj_row, adj_col, adj_data, assignment)

    # balanced per vertex
    balanced = torch.ones(n, dtype=torch.bool)
    update_balanced(balanced, assignment, r)

    cuts = []
    
    cuts.append((cheeger(*create_cut(cut_data, assignment)), assignment))

    while (moveable & balanced).any().item():
        # Compute gains:
        # gains = - (cut_matrix).sum(axis=1)
        num_neg_total = (assignment == -1).sum().item()
        num_neg = torch.full((n,), num_neg_total, dtype=assignment.dtype)
        num_neg = num_neg - assignment

        num_pos_total = (assignment == 1).sum().item()
        num_pos = torch.full((n,), num_pos_total, dtype=assignment.dtype)
        num_pos = num_pos + assignment

        min_size = torch.minimum(num_neg, num_pos)

        row_sums = row_sum_from_coo(cut_row, cut_data, n)
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
        affected = (cut_col == max_vertex) | (cut_row == max_vertex)
        if affected.any().item():
            cut_data[affected] *= -1        

        # Update balanced after flip
        update_balanced(balanced, assignment, r)

        cuts.append((cheeger(*create_cut(cut_data, assignment)), torch.where(assignment == -1)[0].tolist()))

        # mark vertex as non-moveable
        moveable[max_vertex] = False

    return (max if mode == "max" else min)(cuts, key=lambda x: x[0]) if cuts else None


# --- Top-level helpers -------------------------------------------------------

def run_passes(G, r, n_passes, mode="min"):
    best_cheeger = math.inf if mode == "min" else -math.inf
    best_partition = None
    updates = 0

    for i in range(n_passes):
        res = partition_pass(G, r, mode)
        if res is None:
            print(f"pass {i}: no improving moves.")
            continue
        c, s = res
        current = c

        is_better = current < best_cheeger if mode == "min" else current > best_cheeger
        if is_better:
            best_cheeger   = current
            best_partition = c, s
            updates += 1

        print(f"pass {i}  updates={updates}  cheeger={current:.6f}")

    return best_partition

# --- JSON encoder for torch types -------------------------------------------

class TorchJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if torch.is_tensor(obj):
            return obj.tolist()
        if isinstance(obj, (np.integer,)):
            return int(obj)
        if isinstance(obj, (np.floating,)):
            return float(obj)
        return super().default(obj)
    

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

def run(graph, mode="min"):
    r_s = [0.15, 0.25, 0.35, 0.45]
    results = {}
    for r in r_s:
        start = time.time()
        res = run_passes(graph, r, 5, mode)
        elapsed = time.time() - start
        if res is None:
            results[str(r)] = None
        else:
            c, s = res
            results[str(r)] = {"cheeger": c, "partition": s}
        print(f"r={r}: {elapsed:.2f}s")
    
    return results

def can_connect(u, v):
    if u["isd_n"] == v["isd_n"]:
        return True
    
    if u["is_core"] and v["is_core"]:
        return True
    
    return False

def iteration(G, path, iteration):
    nx.draw(G, with_labels=True, node_color="lightblue", edge_color="gray")
    plt.show()

    min_res = min(run(G).values(), key=lambda x: x["cheeger"])
    min_partition = min_res["partition"]

    max_res = max(run(G, mode="max").values(), key=lambda x: x["cheeger"])
    max_partition = max_res["partition"]

    min_set_a = set(min_partition)
    min_edges = [(u, v) for (u, v) in G.edges if (u in min_set_a) != (v in min_set_a)]
    max_set_a = set(max_partition)
    max_edges = [(u, v) for (u, v) in G.edges if (u in max_set_a) != (v in max_set_a)]

    T = nx.minimum_spanning_tree(G)
    msp_edges = set(T.edges())
    del_edges = set(max_edges) - msp_edges - set(min_edges)

    if len(del_edges) == 0:
        raise Exception('No edges to delete')
    
    del_edge = del_edges.pop()

    new_edge = None
    for u in min_set_a:
        for v in set(list(G.nodes)) - min_set_a:
            if (u, v) not in min_edges and can_connect(G.nodes[u], G.nodes[v]):
                new_edge = (u,v)
                break

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
