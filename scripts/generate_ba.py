import networkx as nx
import argparse
from helpers.parse_topology import graph_to_yaml

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--topology-config", "-tc", required=True)
    parser.add_argument("--n", "-n", required=True)
    parser.add_argument("--m", "-m", required=True)
    args = parser.parse_args()

    G = nx.barabasi_albert_graph(int(args.n), int(args.m))

    for idx, node in enumerate(G.nodes()):
        G.nodes[node]["isd_n"] = 1
        G.nodes[node]["is_core"] = True
        G.nodes[node]["as_n"] = idx+1
        G.nodes[node]["label"] = f"1-{idx+1}"

    gname = args.topology_config.split("/")[-1]
    graph_to_yaml(G, args.topology_config + "/" + gname + "_it0.yaml")

