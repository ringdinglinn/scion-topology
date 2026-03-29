import argparse
import networkx as nx
from topology_optimization.scripts.helpers.parse_topology import yaml_to_graph
from scripts.helpers.node_addresses import node_to_address, node_to_name, name_to_address
import subprocess
import os
from pathlib import Path
import sys

def furthest_pairs(candidates):
    max_dist = max(d for d, *_ in candidates)
    pairs = [(u, v) for d, u, v in candidates if d == max_dist]
    
    return max_dist, pairs

def furthest_pairs_isds(G, lengths, isd_1, isd_2):
    candidates = [
        (d, u, v)
        for u in lengths
        for v, d in lengths[u].items()
        if G.nodes[u]["isd_n"] == isd_1 and G.nodes[v]["isd_n"] == isd_2
    ]
    if not candidates:
        return 0, []
    return furthest_pairs(candidates)

def pairs_of_dist(candidates, d):
    pairs = [(u, v) for d_val, u, v in candidates if d_val == d]
    return pairs

def pairs_of_dist_isd(G, lengths, isd_1, isd_2, d):
    candidates = [
        (d, u, v)
        for u in lengths
        for v, d in lengths[u].items()
        if G.nodes[u]["isd_n"] == isd_1 and G.nodes[v]["isd_n"] == isd_2
    ]
    if not candidates:
        return 0, []
    return pairs_of_dist(candidates, d)

def get_show_paths(src_name, dst_address):
    result = subprocess.run(
            ["docker", "exec", src_name, "scion", "showpaths", dst_address, "-m", "1000"],
            capture_output=True,
            text=True
        )
    
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return None
    
    return result.stdout

def save(args, results):
    """results: list of (src_name, dst_name, conn_type, output_str)"""
    config_name = Path(args.config).stem
    path = os.path.join(args.output_path, f"{config_name}.txt")
    os.makedirs(args.output_path, exist_ok=True)
    with open(path, "w") as f:
        for src_name, dst_name, conn_type, result in results:
            f.write(f"=== {src_name}_to_{dst_name} [{conn_type}] ===\n")
            f.write(result if result else "")
            f.write("\n")
    print(f"Output saved to {path}")

def eval_pair(G, u, v, conn_type):
    src_name = node_to_name(G.nodes[u])
    dst_name = node_to_name(G.nodes[v])
    dst_address = node_to_address(G.nodes[v])
    result = get_show_paths(src_name, dst_address)
    return src_name, dst_name, conn_type, result or ""

def search_dir_for_yaml(path):
    yaml_files = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.yaml') or file.endswith('.yml'):
                yaml_files.append(os.path.join(root, file))
    return yaml_files

def get_max_distance(g):
    lengths = dict(nx.all_pairs_shortest_path_length(g))
    dists = [d for u in lengths for d in lengths[u].values()]
    return max(dists)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate the number of paths in this topology and save the output.")
    parser.add_argument("--config", "-i", required=True, help="Path to the isd config")
    parser.add_argument("--output-path", "-o", required=True)
    parser.add_argument("--exhaustive", "-X", action="store_true")
    args = parser.parse_args()

    G = yaml_to_graph(args.config)
    isds = {data["isd_n"] for _, data in G.nodes(data=True)}
    isds = sorted(list(isds))

    if (not args.exhaustive):
        path = os.path.dirname(args.config)
        graph_paths = search_dir_for_yaml(path)
        topo_name = (Path(args.config).stem).split('_')[0]
        graphs = [yaml_to_graph(p) for p in graph_paths]
        diameters = [nx.diameter(g) for g in graphs]
        print(diameters)
        min_diameter = min(diameters)

        print("min_diameter:", min_diameter)

        
        lengths = dict(nx.all_pairs_shortest_path_length(G))

        all_results = []
        for i, isd_1 in enumerate(isds):
            for j in range(i, len(isds)):
                pairs = pairs_of_dist_isd(G, lengths, isd_1, isds[j], min_diameter)
                print(pairs)
                conn_type = "intra" if isd_1 == isds[j] else "inter"
                for u, v in pairs:
                    print(u, v, conn_type)
                    all_results.append(eval_pair(G, u, v, conn_type))

    else:
        all_results = []
        for u in G.nodes():
            for v in G.nodes():
                if (u != v):
                    all_results.append(eval_pair(G, u, v, "total"))

    save(args, all_results)





