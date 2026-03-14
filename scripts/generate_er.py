import networkx as nx
import argparse
from helpers.parse_topology import graph_to_yaml
import random
import numpy as np
from plots.plot_graphs import plot_graph

def get_dfs_subgraph(G, seed, max_n, isd_n, as_n, visited=None):
    if visited is None:
        visited = set()
    if len(visited) >= max_n:
        return G.subgraph(visited).copy()
    if ("label" in G.nodes[seed]):
        return G.subgraph(visited).copy()
    G.nodes[seed]["isd_n"] = isd_n
    G.nodes[seed]["as_n"] = as_n
    G.nodes[seed]["label"] = f"{isd_n}-{as_n}"
    as_n += 1
    visited.add(seed)
    N = G.neighbors(seed)
    for i in N:
        if (i not in visited):
            get_dfs_subgraph(G, i, max_n, isd_n, as_n, visited)
    return G.subgraph(visited).copy()
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--topology-config", "-tc", required=True)
    args = parser.parse_args()

    nr_isds = random.randint(2, 6)
    nr_core_nodes = random.randint(10, 25)

    n = random.randint(30, 100)

    def isd_sizes(nr_isds, nr_nodes):
        fracs = [random.random() for isd in range(nr_isds)]
        sum_fracs = np.sum(np.array(fracs))
        ratio = nr_nodes / sum_fracs
        nr_nodes_isds = [max(2, round(frac * ratio)) for frac in fracs]

        print(nr_nodes_isds)
        return nr_nodes_isds
    
    nr_nodes_isds = isd_sizes(nr_isds, n) 

    G = nx.erdos_renyi_graph(n, 0.3)
    largest_cc = max(nx.connected_components(G), key=len)
    G = G.subgraph(largest_cc).copy()

    for node in list(G.nodes()):
        G.nodes[node]["is_core"] = False

    isds = [[] for _ in nr_nodes_isds]

    for i, isd in enumerate(isds):
        candidate = random.choice(list(G.nodes()))
        while "isd_n" in G.nodes[candidate]:
            candidate = random.choice(list(G.nodes()))
        G.nodes[candidate]["isd_n"] = i+1
        G.nodes[candidate]["as_n"] = 1
        G.nodes[candidate]["is_core"] = True
        isd.append(candidate)

    isds_filled = [False for _ in nr_nodes_isds]

    while not all(isds_filled):
        for i, nr_n in enumerate(nr_nodes_isds):
            if (isds_filled[i]):
                continue
            if len(isds[i]) >= nr_nodes_isds[i]:
                isds_filled[i] = True
            candidates = [neighbor for node in isds[i] for neighbor in nx.neighbors(G, node) if "isd_n" not in G.nodes[neighbor]]
            if len(candidates) == 0:
                isds_filled[i] = True
                continue
            node = random.choice(candidates)
            G.nodes[node]["as_n"] = len(isds[i])
            G.nodes[node]["isd_n"] = i + 1
            isds[i].append(node)


    core_nodes = []

    while(len(core_nodes) < nr_core_nodes):
        core_candidate = random.choice(list(G.nodes()))
        if G.nodes[core_candidate]["is_core"]:
            continue
        G.nodes[core_candidate]["is_core"] = True
        core_nodes.append(core_candidate)

    nodes_to_remove = [n for n in G.nodes() if "isd_n" not in G.nodes[n]]
    G.remove_nodes_from(nodes_to_remove)
    edges_to_remove = [
        (u, v) for u, v in G.edges()
        if not (G.nodes[u]["is_core"] and G.nodes[v]["is_core"])
        and G.nodes[u]["isd_n"] != G.nodes[v]["isd_n"]
    ]
    G.remove_edges_from(edges_to_remove)

    for node, data in G.nodes(data=True):
        G.nodes[node]['label'] = f"{data['isd_n']}-{data['as_n']}"


    # sparsify -------

    bridges = set(nx.bridges(G))
    p = 0.4
    for edge in list(G.edges()):
        if edge not in bridges and (edge[1], edge[0]) not in bridges:
            if random.random() < p:
                G.remove_edge(*edge)
                bridges = set(nx.bridges(G))

    plot_graph(G)


    gname = args.topology_config.split("/")[-1]
    graph_to_yaml(G, args.topology_config + "/" + gname + "_it0.yaml")

