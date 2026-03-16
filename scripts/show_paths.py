import argparse
import networkx as nx
from helpers.parse_topology import yaml_to_graph
from helpers.node_addresses import node_to_address, node_to_name, name_to_address
import subprocess
import os
from pathlib import Path

# Get the single furthest pair
def furthest_pair(G, isd_1, isd_2):
    lengths = dict(nx.all_pairs_shortest_path_length(G))
    max_dist = 0
    pair = (None, None)
    for u in lengths:
        for v, d in lengths[u].items():
            if d > max_dist and G.nodes[u]["isd_n"] == isd_1 and G.nodes[v]["isd_n"] == isd_2:
                max_dist = d
                pair = (u, v)
    return max_dist, *pair

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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate the number of paths in this topology and save the output.")
    parser.add_argument("--config", "-i", required=True, help="Path to the isd config")
    parser.add_argument("--output-path", "-o", required=True, help="")
    args = parser.parse_args()

    G = yaml_to_graph(args.config)
    isds = {data["isd_n"] for _, data in G.nodes(data=True)}
    isds = sorted(list(isds))
    for i, isd_1 in enumerate(isds):
        for j in range(i, len(isds)):
            dist, u, v = furthest_pair(G, isd_1, isds[j])
            src_name = node_to_name(G.nodes[u])
            dst_address = node_to_address(G.nodes[v])
            result = get_show_paths(src_name, dst_address)

            config_name = Path(args.config).stem  
            path = os.path.join(args.output_path, f"{config_name}_{src_name}_to_{node_to_name(G.nodes[v])}.txt")

            os.makedirs(args.output_path, exist_ok=True)

            if result:
                with open(path, "w") as f:
                    f.write(result)
                print(f"Output saved to {args.output_path}")
            else:
                print("Failed to get paths")




