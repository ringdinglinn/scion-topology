import numpy as np
import networkx as nx
from scipy.sparse.linalg import eigsh
import scipy
import math
from matplotlib import pyplot as plt
import argparse
from scripts.helpers.parse_topology import yaml_to_graph, graph_to_yaml
from scipy.sparse.linalg import ArpackError
from scipy.sparse import diags, csr_matrix

TOLERANCE = 1e-8
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
    valid_sp = np.maximum(can_connect_sp - np.identity(len(G.nodes())), 0)  # remove self-loops
    return valid_sp

def get_core_adj_mat(G):
    core_nodes = []
    core_indices = {}
    for node in G.nodes():
        if (G.nodes[node]["is_core"]):
            core_indices[node] = len(core_nodes)
            core_nodes.append(node)
    C = G.subgraph(core_nodes)
    A_core = nx.adjacency_matrix(C).toarray()
    return A_core, core_indices

def get_top_t_eigenpairs(A, t):
    eigenvalues, eigenvectors = eigsh(A, k=t, which='LM')
    idx = np.argsort(eigenvalues)[::-1]
    return eigenvalues[idx], eigenvectors[:, idx]

def get_bottom_t_eigenpairs(L, t):
    n = L.shape[0]
    t = min(n - 1, t)
    
    eigenvalues, eigenvectors = eigsh(L, k=t, sigma=1e-6, which='LM')
    
    idx = np.argsort(eigenvalues)
    return eigenvalues[idx], eigenvectors[:, idx]

def delta_mu2_matrix(v2):
    v2 = v2.reshape(-1, 1)
    return np.abs(v2 - v2.T)

def update_adjacencies(A, A_core, core_indices, old_edge, new_edge, delete=True):
    if delete:
        A[old_edge[0], old_edge[1]] = 0
        A[old_edge[1], old_edge[0]] = 0
    A[new_edge[0], new_edge[1]] = 1
    A[new_edge[1], new_edge[0]] = 1

    u_, v_ = int(old_edge[0]), int(old_edge[1])
    if (u_ in core_indices and v_ in core_indices and delete):
        u, v = core_indices[u_], core_indices[v_]
        A_core[u, v] = 0
        A_core[v, u] = 0
    u_, v_ = int(new_edge[0]), int(new_edge[1])
    if (u_ in core_indices and v_ in core_indices):
        u, v = core_indices[u_], core_indices[v_]
        A_core[u, v] = 1
        A_core[v, u] = 1

    return A, A_core


def optimize(G, path, t=10, k=5, delete=True, add=True):
    n = len(G.nodes())
    t = min(t, n-2)
    A = nx.adjacency_matrix(G).toarray()
    L = nx.laplacian_matrix(G)
    A_core, core_indices = get_core_adj_mat(G)
    L_core = np.diag(np.sum(A_core, axis=1)) - A_core
    mus, V = get_bottom_t_eigenpairs(L, 2)
    for i in range(k):
        flag = False

        # SCION constraint 1: only cores form inter-isd connections
        CC = build_validity_matrix(G, A)
        dR = delta_mu2_matrix(V[:, 1])

        dR_max = dR * CC

        dR_min = dR.copy()
        dR_min[A == 0] = math.inf

        while (not flag):
            old_edge = np.unravel_index(np.argmin(dR_min), (n, n))
            a_min = dR_min[old_edge]

            new_edge = np.unravel_index(np.argmax(dR_max), (n,n))
            a_max = dR_max[new_edge]

            if (a_max - a_min <= 0):
                print(f"negative impact!")
                break

            A, A_core = update_adjacencies(A, A_core, core_indices, old_edge, new_edge, delete=delete)

            L = diags(np.sum(A, axis=1)) - csr_matrix(A)
            new_mus, new_V = get_bottom_t_eigenpairs(L, 2)
            # SCION constraint 2: cutting an edge may not disconnect the cores-subgraph
            L_core = diags(np.sum(A_core, axis=1)) - csr_matrix(A_core)
            new_mus_core, _ = get_bottom_t_eigenpairs(L_core, 2)

            if (new_mus_core[1] <= TOLERANCE or new_mus[1] <= TOLERANCE or old_edge not in G.edges() or new_edge in G.edges()):
                A, A_core = update_adjacencies(A, A_core, core_indices, new_edge, old_edge, delete=delete)
                dR_min[*old_edge] = math.inf
            elif (new_edge in G.edges()):
                A, A_core = update_adjacencies(A, A_core, core_indices, new_edge, old_edge, delete=delete)
                dR_max[*new_edge] = -math.inf
            else:
                mus, V, mus_core = new_mus, new_V, new_mus_core
                # highlight_edges(G, {old_edge})
                if delete:
                    G.remove_edge(*old_edge)
                if add:
                    G.add_edge(*new_edge)
                # highlight_edges(G, {new_edge}, color="limegreen")
                graph_to_yaml(G, path + "_it" + str(i+1) + ".yaml")

                flag = True
        
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

    if args.add_only:
        path += "_raca"
    elif args.delete_only:
        path += "_racd"
    else:
        path += "_rac"


    optimize(G, path, k=int(args.iterations), delete=(not args.add_only), add=(not args.delete_only))



