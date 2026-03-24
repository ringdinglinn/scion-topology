import networkx as nx
import argparse
from helpers.parse_topology import graph_to_yaml
import random
import numpy as np
from plots.plot_graphs import plot_graph
from collections import defaultdict
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--topology-config", "-tc", required=True)
    args = parser.parse_args()

    nr_isds = random.randint(3, 6)

    n = random.randint(20, 50)
    nr_core_nodes = max(random.randint(6, 20), nr_isds)
    nr_core_nodes = min(n, nr_core_nodes)
    print(f"nr core nodes: {nr_core_nodes}")

    def isd_sizes(nr_isds, nr_nodes):
        fracs = [random.random() for isd in range(nr_isds)]
        sum_fracs = np.sum(np.array(fracs))
        ratio = nr_nodes / sum_fracs
        nr_nodes_isds = [max(3, round(frac * ratio)) for frac in fracs]

        print(nr_nodes_isds)
        return nr_nodes_isds
    
    nr_nodes_isds = isd_sizes(nr_isds, n) 

    G = nx.extended_barabasi_albert_graph(n, 2, 0.4, 0.4)

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
            G.nodes[node]["as_n"] = len(isds[i]) + 1
            G.nodes[node]["isd_n"] = i + 1
            isds[i].append(node)


    core_nodes = []

    print(f"nr core nodes: {nr_core_nodes}")
    while(len(core_nodes) < nr_core_nodes):
        for isd in nr_nodes_isds:
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

    for i in range(nr_isds):
        for j in range(i + 1, nr_isds):
            isd_i_cores = [n for n in isds[i] if G.nodes[n]["is_core"]]
            isd_j_cores = [n for n in isds[j] if G.nodes[n]["is_core"]]
            if not any(G.has_edge(u, v) for u in isd_i_cores for v in isd_j_cores):
                G.add_edge(random.choice(isd_i_cores), random.choice(isd_j_cores))


    # sparsify -------

    bridges = set(nx.bridges(G))
    p = 0.2
    for edge in list(G.edges()):
        if edge not in bridges and (edge[1], edge[0]) not in bridges:
            if random.random() < p:
                G.remove_edge(*edge)
                bridges = set(nx.bridges(G))

    isd_cores = defaultdict(list)
    for node in G.nodes:
        if G.nodes[node].get("is_core"):
            isd = G.nodes[node]["isd_n"]
            isd_cores[isd].append(node)

    isd_list = list(isd_cores.keys())

    for i, isd in enumerate(isd_list):
        cores = isd_cores[isd]

        ## constraint 1: enforce that core nodes within isd are a connected subgraph
        core_subgraph = G.subgraph(cores)
        components = list(nx.connected_components(core_subgraph))

        for j in range(len(components) - 1):
            src = random.choice(list(components[j]))
            dst = random.choice(list(components[j + 1]))
            G.add_edge(src, dst)
        
        ## constraint 2: make sure isds are connected
        has_inter_core_edge = any(
            G.nodes[nb].get("is_core") and G.nodes[nb]["isd_n"] != isd
            for core in cores
            for nb in G.neighbors(core)
        )
        if not has_inter_core_edge:
            # Pick a random core from any other ISD and connect
            other_isds = [other for other in isd_list if other != isd]
            if other_isds:
                src = random.choice(cores)
                dst = random.choice(isd_cores[random.choice(other_isds)])
                G.add_edge(src, dst)


    for node, data in G.nodes(data=True):
        G.nodes[node]['label'] = f"{data['isd_n']}-{data['as_n']}"

    plot_graph(G)


    gname = args.topology_config.split("/")[-1]
    graph_to_yaml(G, args.topology_config + "/" + gname + "_it0.yaml")

