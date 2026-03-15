import networkx as nx
import argparse
from helpers.parse_topology import graph_to_yaml
import random
import numpy as np
from plots.plot_graphs import plot_graph
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--topology-config", "-tc", required=True)
    args = parser.parse_args()

    nr_isds = random.randint(3, 6)

    n = random.randint(20, 50)
    nr_core_nodes = min(random.randint(3, 15), nr_isds)

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

    for isd in isds:
        core_nodes = random.sample(isd, 2)
        for core in core_nodes:
            G.nodes[core]["is_core"] = True
        isd_core = [node for node in isd if G.nodes[node]["is_core"]]
        for node in isd:
            if not any(G.has_edge(node, core) for core in isd_core):
                candidates = [core for core in isd_core if core != node]
                if candidates:
                    G.add_edge(node, random.choice(candidates))


    for node, data in G.nodes(data=True):
        G.nodes[node]['label'] = f"{data['isd_n']}-{data['as_n']}"

    plot_graph(G)


    gname = args.topology_config.split("/")[-1]
    graph_to_yaml(G, args.topology_config + "/" + gname + "_it0.yaml")

