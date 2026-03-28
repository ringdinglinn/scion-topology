import networkx as nx
import numpy as np
from community import best_partition
from topology_optimization.scripts.draw_plots.plot_graphs import plot_graph
import argparse
from topology_optimization.scripts.helpers.parse_topology import graph_to_yaml
import random

def watts_strogatz_communities(sizes, k=4, p=0.1, p_inter=0.01, seed=42):
    random.seed(seed)
    G = nx.Graph()
    offset = 0
    for community_id, size in enumerate(sizes):
        ws = nx.watts_strogatz_graph(size, k, p, seed=seed + community_id)
        mapping = {n: n + offset for n in ws.nodes()}
        ws = nx.relabel_nodes(ws, mapping)
        for node in ws.nodes():
            ws.nodes[node]["isd_n"] = community_id
        G = nx.compose(G, ws)
        offset += size

    isd_nodes = {}
    for node in G.nodes():
        isd = G.nodes[node]["isd_n"]
        isd_nodes.setdefault(isd, [])
        isd_nodes[isd].append(node)

    isd_ids = list(isd_nodes.keys())
    for i, isd_a in enumerate(isd_ids):
        for isd_b in isd_ids[i+1:]:
            n_connectors = random.randint(1, 2)
            connectors_a = random.sample(isd_nodes[isd_a], min(n_connectors, len(isd_nodes[isd_a])))
            connectors_b = random.sample(isd_nodes[isd_b], min(n_connectors, len(isd_nodes[isd_b])))
            for a, b in zip(connectors_a, connectors_b):
                G.add_edge(a, b)

    return G

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--topology-config", "-tc", required=True)
    args = parser.parse_args()

    # Generate Watts-Strogatz graph
    n = 30
    k = 4
    p = 0.3
    G = watts_strogatz_communities(sizes=[15, 15, 15])

    # Ensure connectivity
    while not nx.is_connected(G):
        G = nx.watts_strogatz_graph(n, k, p)

    # Community detection (Louvain)
    partition = best_partition(G)  # {node: community_id}

    # Assign isd_n to each node
    nx.set_node_attributes(G, partition, "isd_n")

    # Find inter-ISD edges and mark core nodes
    for node in G.nodes():
        isd = G.nodes[node]["isd_n"]
        is_core = any(G.nodes[nb]["isd_n"] != isd for nb in G.neighbors(node))
        G.nodes[node]["is_core"] = is_core

    # Enumerate nodes within each ISD and assign as_n + label
    from collections import defaultdict
    isd_counters = defaultdict(int)

    for node in sorted(G.nodes()):
        isd = G.nodes[node]["isd_n"]
        isd_counters[isd] += 1
        as_n = isd_counters[isd]
        G.nodes[node]["as_n"] = as_n
        G.nodes[node]["label"] = f"{isd}-{as_n}"

    # Print summary
    for node, data in G.nodes(data=True):
        print(f"Node {node}: {data}")

    
    plot_graph(G)


    gname = args.topology_config.split("/")[-1]
    graph_to_yaml(G, args.topology_config + "/" + gname + "_it0.yaml")