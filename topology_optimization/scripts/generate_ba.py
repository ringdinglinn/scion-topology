import networkx as nx
import argparse
from topology_optimization.scripts.helpers.parse_topology import graph_to_yaml
import random
import numpy as np
from topology_optimization.scripts.draw_plots.plot_graphs import plot_graph
from collections import defaultdict
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", "-o", required=True)
    args = parser.parse_args()

    # ----- Randomize basic variables -----
    n = random.randint(20, 50)
    nr_isds = random.randint(3, 6)
    nr_core_nodes = max(random.randint(6, 20), nr_isds)
    print(f"n = {n}, nr_isds = {nr_isds}, nr core nodes = {nr_core_nodes}")

    # ----- Determine nr nodes per ISD ----
    fracs = np.array([random.random() for _ in range(nr_isds)])
    nr_nodes_isds = [max(3, round(f)) for f in fracs / fracs.sum() * n]
    isds = [[] for _ in nr_nodes_isds]
    n = sum(nr_nodes_isds)
    print(nr_nodes_isds)


    # ----- Initiate network ------
    G = nx.barabasi_albert_graph(n, 3)

    for node in list(G.nodes()):
        G.nodes[node]["is_core"] = False

    core_nodes = []

    # ----- Pick one random node for each ISD to form the first core ----
    for i, isd in enumerate(isds):
        candidate = random.choice(list(G.nodes()))
        while "isd_n" in G.nodes[candidate]:
            candidate = random.choice(list(G.nodes()))
        G.nodes[candidate]["isd_n"] = i+1
        G.nodes[candidate]["as_n"] = 1
        G.nodes[candidate]["is_core"] = True
        core_nodes.append(candidate)
        isd.append(candidate)


    # ----- Grow ISDs ------
    ### For one ISD after another, get all neighbors of current nodes in the ISD, pick a random one and add to the ISD.
    ### Move on to next ISD, repeat cycling through ISDs until all are filled
    isds_filled = [False for _ in nr_nodes_isds]

    while not all(isds_filled):
        for i, nr_n in enumerate(nr_nodes_isds):
            if (isds_filled[i]):
                continue
            candidates = [neighbor for node in isds[i] for neighbor in nx.neighbors(G, node) if "isd_n" not in G.nodes[neighbor]]
            if len(candidates) == 0:
                isds_filled[i] = True
                continue
            node = random.choice(candidates)
            G.nodes[node]["as_n"] = len(isds[i]) + 1
            G.nodes[node]["isd_n"] = i + 1
            isds[i].append(node)
            if len(isds[i]) == nr_nodes_isds[i]:
                isds_filled[i] = True

    # ----- Pick rest of core nodes ------
    while(len(core_nodes) < nr_core_nodes):
        core_candidate = random.choice(list(G.nodes()))
        if G.nodes[core_candidate]["is_core"]:
            continue
        G.nodes[core_candidate]["is_core"] = True
        core_nodes.append(core_candidate)

        
    # ----- Remove ISD-spanning edges between non-core nodes -----
    nodes_to_remove = [n for n in G.nodes() if "isd_n" not in G.nodes[n]]
    G.remove_nodes_from(nodes_to_remove)
    edges_to_remove = [
        (u, v) for u, v in G.edges()
        if not (G.nodes[u]["is_core"] and G.nodes[v]["is_core"])
        and G.nodes[u]["isd_n"] != G.nodes[v]["isd_n"]
    ]
    G.remove_edges_from(edges_to_remove)

    # ------ C2: all core nodes form a connected subgraph --------
    # if disconnected, pick random nodes from each side and add edge
    # this also ensures that all of ISDs are connected, if they were disconnected when edges were removed in previous step.
    core_subgraph = G.subgraph(core_nodes)
    components = list(nx.connected_components(core_subgraph))
    for j in range(len(components) - 1):
        src = random.choice(list(components[j]))
        dst = random.choice(list(components[j + 1]))
        G.add_edge(src, dst)

    for node, data in G.nodes(data=True):
        G.nodes[node]['label'] = f"{data['isd_n']}-{data['as_n']}"

    plot_graph(G)

    gname = args.output.split("/")[-1]
    graph_to_yaml(G, args.output + "/" + gname + "_it0.yaml")

