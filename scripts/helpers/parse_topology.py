import networkx as nx
import argparse
import yaml

def get_isd_and_as(node_label, isds):
    isd_n, as_n = node_label.split("-")[0], node_label.split("-")[1]
    is_core = int(as_n) in isds[int(isd_n)]["core"]
    return isd_n, as_n, is_core

def yaml_to_graph(filepath):
    G = nx.Graph()
    node_map = {}
    counter = 0

    with open(filepath, 'r') as f:
        config = yaml.safe_load(f)

    topo = config["Topology"]
    isds = config["ISDs"]

    def get_node(label):
        nonlocal counter
        if label not in node_map:
            isd_n, as_n, is_core = get_isd_and_as(label, isds)
            node_map[label] = counter
            G.add_node(counter, label=label, isd_n=isd_n, as_n=as_n, is_core=is_core)
            counter += 1
        return node_map[label]
    
    for line in topo:
        parts = line.strip().split()
        if len(parts) == 2:
            a, b = get_node(parts[0]), get_node(parts[1])
            G.add_edge(a, b)

    return G

def edges_to_yaml(G):
    edgelist = [f"{G.nodes[u]['label']} {G.nodes[v]['label']}" for (u, v) in G.edges]
    return edgelist

def graph_to_isds(G):
    isds = {}
    for node, data in G.nodes(data=True):
        isd = int(data['isd_n'])
        as_n = int(data['as_n'])
        if isd not in isds:
            isds[isd] = {'n': 0, 'core': []}
        isds[isd]['n'] += 1
        if data['is_core']:
            isds[isd]['core'].append(as_n)
    return isds

def graph_to_yaml(G, path):
    yaml_graph = { "ISDs": graph_to_isds(G), "Topology": edges_to_yaml(G)}

    with open(path, 'w') as f:
        yaml.safe_dump(yaml_graph, f)

def get_label_to_node_dict(G):
    return {data["label"]: node for node, data in G.nodes(data=True)}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse an edge list into a NetworkX graph.")
    parser.add_argument("--input", "-i", required=True, help="Path to the input text file")
    args = parser.parse_args()

    G, node_map = yaml_to_graph(args.input)

    print(f"Nodes ({G.number_of_nodes()}):")
    for label, idx in sorted(node_map.items(), key=lambda x: x[1]):
        print(f"  {idx}: {label}")

    print(f"\nEdges ({G.number_of_edges()}):")
    for u, v in G.edges():
        print(f"  {u} -- {v}  ({G.nodes[u]['label']} -- {G.nodes[v]['label']})")