import numpy as np
import networkx as nx
from scipy.sparse.linalg import eigsh
import scipy
import math
from matplotlib import pyplot as plt
import argparse
from helpers.parse_topology import yaml_to_graph, graph_to_yaml

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


def update_eigenvalue(x_j, delta_M):
    delta_a_j = x_j.T @ delta_M @ x_j
    return delta_a_j

def update_eigenvals(X, delta_M):
    delta_a = X.T @ delta_M @ X
    return np.diag(delta_a)

def update_eigenvec(j, X, a, delta_M, t):
    delta_xj = np.zeros(X.shape[0])
    for i in range(t):
        if i == j: continue
        delta_xj += ((X[:, i].T @ delta_M @ X[:, j]) / (a[j] - a[i])) * X[:, i]
    return delta_xj

def update_eigenvecs(X, a, delta_M):
    n = delta_M.shape[0]
    D = np.fromfunction(lambda j, i : 1 / (a[j] - a[i]) if j != i else 0, (n, n))
    delta_X = X @ ((X.T @ delta_M @ X) * D)
    return delta_X

def update_spectral_gap(i, j, X):
    # spectral gap = lambda_1 - lambda_2
    # delta spectral gap = delta_lambda_1 - delta_lambda_2
    # delta_lambda_1 - delta_lambda_2 = u_1.T @ delta_A @ u_1 - u_2.T @ delta_A @ u_2 
    # delta_A is -1 or 1 for Aij, 0 otherwise
    # delta spectral gap = 2*(u1j*u1i - u2j*u2i)

    return 2 * (X[j,0] * X[i,0] - X[j,1] * X[i,1])

def update_spectral_gap_mat(u1, u2):
    return 2 * (np.outer(u1, u1) - np.outer(u2, u2))

def get_top_t_eigenpairs(A, t):
    eigenvalues, eigenvectors = eigsh(A, k=t, which='LM')

    # Sort descending by eigenvalue
    idx = np.argsort(eigenvalues)[::-1]
    return eigenvalues[idx], eigenvectors[:, idx]

def get_bottom_t_eigenpairs(L, t):
    eigenvalues, eigenvectors = eigsh(L, k=t, which='SM')
    # Sort ascending by eigenvalue
    idx = np.argsort(eigenvalues)
    return eigenvalues[idx], eigenvectors[:, idx]

def delta_mu2_matrix(v2):
    v2 = v2.reshape(-1,1)
    return (v2**2) + (v2**2).T - 2*(v2 @ v2.T)


def optimize(G, path, t=20, k=5):
    n = len(G.nodes())
    t = min(t, n)
    A = nx.adjacency_matrix(G).toarray().astype(float)
    L = nx.laplacian_matrix(G).toarray().astype(float)
    lambdas, U = get_top_t_eigenpairs(A, t)
    mus, V = get_bottom_t_eigenpairs(L, t)
    delta_A = np.zeros((n, n))
    for i in range(k):
        # CC = can_connect matrix for new edges
        CC = build_validity_matrix(G, A)
        # dR = update_spectral_gap_mat(U[:, 0], U[:, 1])
        dR = delta_mu2_matrix(V[:, 1])
        # dR[A == 1] *= -1
        new_edge = np.unravel_index(np.argmax(dR * CC), (n, n))
        dR1 = dR[new_edge]

        edge_vals = {(i, j): dR[i, j] for i in range(n) for j in range(n)}
        # show_edge_weights(G, edge_vals)

        dR[A == 0] = math.inf        
        old_edge = np.unravel_index(np.argmin(dR), (n, n))
        dR2 = dR[old_edge]
        print(f"dR1 = {dR1}, dR2 = {dR2}, sum = {dR1 + dR2}, mu 2 {mus[1]}, new mu 2: {mus[1] + dR1 + dR2}")
        print(G.nodes(data=True)[old_edge[0]]["label"], G.nodes(data=True)[old_edge[1]]["label"])

        delta_A = np.zeros((n, n))
        delta_A[new_edge[0], new_edge[1]] = 1
        delta_A[new_edge[1], new_edge[0]] = 1
        delta_A[old_edge[0], old_edge[1]] = -1
        delta_A[old_edge[1], old_edge[0]] = -1

        A[new_edge[0], new_edge[1]] = 1
        A[new_edge[1], new_edge[0]] = 1
        A[old_edge[0], old_edge[1]] = 0
        A[old_edge[1], old_edge[0]] = 0
        
        delta_X = np.column_stack([update_eigenvec(j, U, lambdas, delta_A, t) for j in range(t)])
        delta_a = [update_eigenvalue(U[:, j], delta_A) for j in range(t)]

        U += delta_X
        lambdas += delta_a
        
        L = np.diag(A.sum(axis=1)) - A
        mus, V = get_bottom_t_eigenpairs(L, t)

        # highlight_edges(G, {old_edge})
        G.remove_edge(*old_edge)
        G.add_edge(*new_edge)
        # highlight_edges(G, {new_edge}, color="limegreen")

        graph_to_yaml(G, path + "_it" + str(i+1) + ".yaml")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--topology-config", "-tc", required=True)
    args = parser.parse_args()
    G = yaml_to_graph(args.topology_config)
    path = args.topology_config.split("_")[0]

    path += "_rac"
    optimize(G, path)



