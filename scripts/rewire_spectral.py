import numpy as np
import networkx as nx
from scipy.sparse.linalg import eigsh
import scipy
import math
from matplotlib import pyplot as plt
import argparse
from helpers.parse_topology import yaml_to_graph, graph_to_yaml
from scipy.sparse.linalg import ArpackError

# --- Visualization ----------------------------------------

def draw_partition(G, partition_a):
    cut_edges = [(u, v) for (u, v) in G.edges if (u in partition_a) != (v in partition_a)]

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
            node_size=800, font_size=8, edge_color=edge_colors)
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

# ------- SCION ----------------
def can_connect(G, u, v):
    return G.nodes[u]["isd_n"] == G.nodes[v]["isd_n"] or (G.nodes[u]["is_core"] and G.nodes[v]["is_core"])

def build_can_connect_matrix(G):
    n = len(G.nodes())
    rows, cols = np.meshgrid(np.arange(n), np.arange(n), indexing='ij')
    rows, cols = rows.ravel(), cols.ravel()

    mask = rows != cols
    rows, cols = rows[mask], cols[mask]

    CC = np.array([[can_connect(G, i, j) for j in range(n)] for i in range(n)], dtype=float)
    return CC

def build_validity_matrix(G, A):
    can_connect_sp = build_can_connect_matrix(G)
    valid_sp = can_connect_sp - A   # valid edges are ones that can connect and don't exist already
    valid_sp = np.maximum(valid_sp - np.identity(len(G.nodes())), 0)  # remove self-loops
    return valid_sp

# -------- Eigenpairs updating -------

def get_core_adj_mat(G):
    core_nodes = []
    core_indices = {}
    for node in G.nodes():
        if (G.nodes[node]["is_core"]):
            core_indices[node] = len(core_nodes)
            core_nodes.append(node)
    C = G.subgraph(core_nodes)
    A_core = nx.adjacency_matrix(C)
    return A_core, core_indices

def get_top_t_eigenpairs(A, t):
    eigenvalues, eigenvectors = eigsh(A, k=t, which='LM')
    idx = np.argsort(eigenvalues)[::-1]
    return eigenvalues[idx], eigenvectors[:, idx]

def get_bottom_t_eigenpairs(L, t):
    try:
        ncv = min(max(2 * t + 1, 20), L.shape[0] - 1)
        eigenvalues, eigenvectors = eigsh(L, k=t, which='SM', ncv=ncv)
    except ArpackError:
        # fall back to full dense decomposition
        eigenvalues, eigenvectors = np.linalg.eigh(L)
        eigenvalues = eigenvalues[:t]
        eigenvectors = eigenvectors[:, :t]

    idx = np.argsort(eigenvalues)
    return eigenvalues[idx], eigenvectors[:, idx]

def delta_mu2_matrix(v2):
    v2 = v2.reshape(-1,1)
    return (v2**2) + (v2**2).T - 2*(v2 @ v2.T)

def optimize(G, path, t=10, k=5):
    n = len(G.nodes())
    t = min(t, n-2)
    A = nx.adjacency_matrix(G).toarray().astype(float)
    L = nx.laplacian_matrix(G).toarray().astype(float)
    A_core, core_indices = get_core_adj_mat(G)
    L_core = np.diag(np.sum(A_core, axis=1)) - A_core
    mus, V = get_bottom_t_eigenpairs(L, t)
    for i in range(k):
        flag = False

        # SCION constraint 1: only cores form inter-isd connections
        CC = build_validity_matrix(G, A)
        dR = delta_mu2_matrix(V[:, 1])

        dR_max = dR * CC

        dR_min = dR_max.copy()
        dR_min[A == 0] = math.inf

        while (not flag):
            old_edge = np.unravel_index(np.argmin(dR_min), (n, n))
            a_min = dR_min[old_edge]

            new_edge = np.unravel_index(np.argmax(dR_max), (n,n))
            a_max = dR_max[new_edge]

            if (a_max - a_min <= 0):
                print(f"negative impact!")
                break

            A[old_edge[0], old_edge[1]] = 0
            A[old_edge[1], old_edge[0]] = 0
            A[new_edge[0], new_edge[1]] = 1
            A[new_edge[1], new_edge[0]] = 1

            u_, v_ = int(old_edge[0]), int(old_edge[1])
            if (u_ in core_indices and v_ in core_indices):
                u, v = core_indices[u_], core_indices[v_]
                A_core[u, v] = 0
                A_core[v, u] = 0
            u_, v_ = int(new_edge[0]), int(new_edge[1])
            if (new_edge[0] in core_indices and new_edge[1] in core_indices):
                u, v = core_indices[u_], core_indices[v_]
                A_core[u, v] = 1
                A_core[v, u] = 1

            L = np.diag(np.sum(A, axis=1)) - A
            mus, V = get_bottom_t_eigenpairs(L, t)
            # SCION constraint 2: cutting an edge may not disconnect the cores-subgraph
            L_core = np.diag(np.sum(A_core, axis=1)) - A_core
            mus_core, _ = get_bottom_t_eigenpairs(L_core, t)

            if (mus[1] <= 0 or mus_core[1] <= 0 or old_edge not in G.edges()):
                # min_index += 1
                dR_min[*old_edge] = math.inf
            elif (new_edge in G.edges()):
                # max_index += 1
                dR_max[*new_edge] = -math.inf
            else:
                # highlight_edges(G, {old_edge})
                G.remove_edge(*old_edge)
                G.add_edge(*new_edge)
                # highlight_edges(G, {new_edge}, color="limegreen")
                graph_to_yaml(G, path + "_it" + str(i+1) + ".yaml")

                flag = True
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--topology-config", "-tc", required=True)
    args = parser.parse_args()
    G = yaml_to_graph(args.topology_config)
    path = args.topology_config.split("_")[0]

    path += "_rac"
    optimize(G, path)



