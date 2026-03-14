import networkx as nx
import argparse
from helpers.parse_topology import graph_to_yaml
import random
import numpy as np

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--topology-config", "-tc", required=True)
    parser.add_argument("--n", "-n", required=True)
    parser.add_argument("--m", "-m", required=True)
    parser.add_argument("--p", "-p", required=True)
    parser.add_argument("--q", "-q", required=True)
    parser.add_argument("--max-isds", required=False, default=6)
    parser.add_argument("--min-isds", required=False, default=2)
    parser.add_argument("--max-cores", required=False, default=16)
    parser.add_argument("--min-cores", required=False, default=6)
    args = parser.parse_args()

    n, m, p, q = int(args.n), int(args.m), float(args.p), float(args.q)
    nr_isds = random.randint(int(args.min_isds), int(args.max_isds))
    min_cores = max(int(args.min_cores), nr_isds)
    nr_cores = random.randint(min_cores, int(args.max_cores))
    
    print(f"nr isds = {nr_isds}, nr cores = {nr_cores}")

    def isd_sizes(nr_isds, nr_nodes):
        fracs = [random.random() for isd in range(nr_isds)]
        sum_fracs = np.sum(np.array(fracs))
        ratio = nr_nodes / sum_fracs
        nr_nodes_isds = [max(2, round(frac * ratio)) for frac in fracs]

        print(nr_nodes_isds)
        return nr_nodes_isds
    
    def set_core_node(H):
        core_candiate = random.choice(list(H.nodes()))
        while H.nodes[core_candiate]["is_core"]:
            core_candiate = random.choice(list(H.nodes()))
        H.nodes[core_candiate]["is_core"] = True


    nr_nodes_isds = isd_sizes(nr_isds, n)
    isds = []
    for i, nr_nodes in enumerate(nr_nodes_isds):
        H = nx.extended_barabasi_albert_graph(nr_nodes, m, p, q)
        for node in list(H.nodes()):
            H.nodes[node]["is_core"] = False
        set_core_node(H)
        isds.append(H)

    for i, H in enumerate(isds):
        for j, node in enumerate(H.nodes()):
            H.nodes[node]["isd_n"] = i+1
            H.nodes[node]["as_n"] = j+1
            H.nodes[node]["label"] = f"{i+1}-{j+1}"

    G = nx.disjoint_union_all(isds)    

    for i in range(max(0, nr_cores - nr_isds)):
        while True:
            core_node = random.choice(list(G.nodes()))
            if not G.nodes[core_node]["is_core"]:
                G.nodes[core_node]["is_core"] = True
                break

    cores = [node for node, data in list(G.nodes(data=True)) if data["is_core"]]

    for core_u in cores:
        for i in range(m):
            core_v = random.choice(cores)
            while ((core_u, core_v) in G.edges() or core_u == core_v):
                core_v = random.choice(cores)
            G.add_edge(core_u, core_v)


    gname = args.topology_config.split("/")[-1]
    graph_to_yaml(G, args.topology_config + "/" + gname + "_it0.yaml")

