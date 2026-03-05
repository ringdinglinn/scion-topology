import re
import argparse
import pandas as pd
from pathlib import Path
import networkx as nx
from helpers.parse_topology import yaml_to_graph, get_label_to_node_dict
import os
from helpers.node_addresses import name_to_isd_as, isd_as_to_label

def count_paths(filepath):
    with open(filepath, "r") as f:
        content = f.read()
    matches = re.findall(r"^\[\s*\d+\]", content, re.MULTILINE)
    return len(matches)

def count_simple_paths(G, src, dst):
    return sum(1 for _ in nx.all_simple_paths(G, src, dst))

def parse_folder(folder_path, output_path, topo_path):
    folder = Path(folder_path)
    files = sorted(folder.glob("*.txt"))

    rows = []
    for f in files:
        parts = f.stem.split("_")
        src_name = parts[2]
        dst_name = parts[4]
        src = isd_as_to_label(*name_to_isd_as(src_name))
        dst = isd_as_to_label(*name_to_isd_as(dst_name))
        topo = parts[0]
        topo_name = "_".join(parts[:2])

        G = yaml_to_graph(os.path.join(topo_path, topo, topo_name + ".yaml"))
        label_to_node = get_label_to_node_dict(G)
        u = label_to_node[src]
        v = label_to_node[dst]

        rows.append({
            "topology": topo_name,
            "num_scion_paths": count_paths(f),
            "num_simple_paths": count_simple_paths(G, u, v),
        })

    new_data = pd.DataFrame(rows)

    if Path(output_path).exists():
        existing = pd.read_csv(output_path)
        for col in ["num_paths", "num_simple_paths"]:
            if col in existing.columns:
                existing = existing.drop(columns=[col])
        merged = existing.merge(new_data, on="topology", how="outer")
        merged.to_csv(output_path, index=False)
        print(f"Updated existing CSV at {output_path}")
    else:
        new_data.to_csv(output_path, index=False)
        print(f"Created new CSV at {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", "-f", required=True, help="Folder with path text files")
    parser.add_argument("--topologies", "-t", required=True, help="Folder containing all topology configurations")
    parser.add_argument("--output", "-o", required=True, help="Output CSV path")
    args = parser.parse_args()

    parse_folder(args.folder, args.output, args.topologies)