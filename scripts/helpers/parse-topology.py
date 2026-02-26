import networkx as nx
import argparse

def parse_graph(filepath):
    G = nx.Graph()
    node_map = {}
    counter = 0

    def get_node(label):
        nonlocal counter
        if label not in node_map:
            node_map[label] = counter
            G.add_node(counter, label=label)
            counter += 1
        return node_map[label]

    with open(filepath) as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 2:
                a, b = get_node(parts[0]), get_node(parts[1])
                G.add_edge(a, b)

    return G, node_map


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse an edge list into a NetworkX graph.")
    parser.add_argument("--input", "-i", required=True, help="Path to the input text file")
    args = parser.parse_args()

    G, node_map = parse_graph(args.input)

    print(f"Nodes ({G.number_of_nodes()}):")
    for label, idx in sorted(node_map.items(), key=lambda x: x[1]):
        print(f"  {idx}: {label}")

    print(f"\nEdges ({G.number_of_edges()}):")
    for u, v in G.edges():
        print(f"  {u} -- {v}  ({G.nodes[u]['label']} -- {G.nodes[v]['label']})")