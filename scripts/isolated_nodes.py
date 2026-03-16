import sys
import argparse
from helpers.parse_topology import yaml_to_graph
import networkx as nx


def get_is_core(G, node) -> bool:
    return G.nodes[node]["is_core"]


def find_non_core_without_core_neighbor(G) -> list:
    isolated = []

    for node in G.nodes:
        if get_is_core(G, node):
            continue 

        neighbors = list(G.neighbors(node))
        has_core_neighbor = any(get_is_core(G, nb) for nb in neighbors)

        if not has_core_neighbor:
            isolated.append(node)

    return isolated


def main():
    parser = argparse.ArgumentParser(
        description="Find non-core nodes with no direct connection to a core node."
    )
    parser.add_argument("yaml_path", help="Path to the topology YAML file")
    args = parser.parse_args()

    print(f"Loading graph from: {args.yaml_path}")
    G = yaml_to_graph(args.yaml_path)

    total_nodes   = G.number_of_nodes()
    core_nodes    = [n for n in G.nodes if get_is_core(G, n)]
    noncore_nodes = [n for n in G.nodes if not get_is_core(G, n)]

    print(f"\nGraph summary:")
    print(f"  Total nodes : {total_nodes}")
    print(f"  Core nodes  : {len(core_nodes)}")
    print(f"  Non-core    : {len(noncore_nodes)}")

    isolated = find_non_core_without_core_neighbor(G)

    print(f"\n{'='*55}")
    if not isolated:
        print("✓ All non-core nodes have at least one core neighbour.")
    else:
        print(f"✗ {len(isolated)} non-core node(s) with NO core neighbour:\n")
        for node in isolated:
            label     = G.nodes[node].get("label", node)
            print(f"  [{label}]")
    print(f"{'='*55}")


if __name__ == "__main__":
    main()