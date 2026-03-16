import re
import argparse
import pandas as pd
from pathlib import Path
import networkx as nx
from helpers.parse_topology import yaml_to_graph, get_label_to_node_dict
import os
from collections import defaultdict
from helpers.node_addresses import name_to_isd_as, isd_as_to_label


def count_paths(filepath):
    with open(filepath, "r") as f:
        content = f.read()
    matches = re.findall(r"^\[\s*\d+\]", content, re.MULTILINE)
    return len(matches)

def count_simple_paths(G, src, dst):
    return sum(1 for _ in nx.all_simple_paths(G, src, dst))

def count_all_simple_paths(G):
    nodes = list(G.nodes)
    total = 0
    for i, u in enumerate(nodes):
        for v in nodes[i+1:]:
            total += sum(1 for _ in nx.all_simple_paths(G, u, v))
    return total

def parse_filename(f):
    parts = f.split("scion")
    topo_name = parts[0].rstrip("_")
    src_part = parts[1].split("_to_")[0] 
    dst_part = parts[2]                    
    isd1, as1 = src_part.split("-")
    isd2, as2 = dst_part.split("-")
    return topo_name, int(isd1), int(as1), int(isd2), int(as2)

def parse_folder(folder_path, output_path, topo_path):
    folder = Path(folder_path)
    files = sorted(folder.glob("*.txt"))

    topo_files = defaultdict(list)
    for f in files:
        topo_name, isd1, as1, isd2, as2 = parse_filename(f.stem)
        if (topo_name not in topo_files.keys()):
            topo_files[topo_name] = []
        topo_files[topo_name].append((isd1, as1, isd2, as2, f))
        
    rows = []
    for topo_name, topo_file_list in topo_files.items():
        topo = topo_name.split("_")[0]
        G = yaml_to_graph(os.path.join(topo_path, topo, topo_name + ".yaml"))
        # total_paths = count_all_simple_paths(G)

        intra_isd_paths_scion = []
        inter_isd_paths_scion = []
        intra_isd_paths_nx = []
        inter_isd_paths_nx = []

        for isd1, as1, isd2, as2, f in topo_file_list:
            label_to_node = get_label_to_node_dict(G)

            src = isd_as_to_label(str(isd1), str(as1))
            dst = isd_as_to_label(str(isd2), str(as2))
            u = label_to_node[src]
            v = label_to_node[dst]

            print(f"Computing all simple paths for {topo_name}, {isd1}-{as1}, {isd2}-{as2}")
            if (isd1 == isd2):
                intra_isd_paths_scion.append(count_paths(f))
                intra_isd_paths_nx.append(count_simple_paths(G, u, v))
            else:
                inter_isd_paths_scion.append(count_paths(f))
                inter_isd_paths_nx.append(count_simple_paths(G, u, v))

        rows.append({
            "topology": topo_name,
            "intra_isd_paths_scion": sum(intra_isd_paths_scion) / len(intra_isd_paths_scion) if len(intra_isd_paths_scion) > 0 else 0,
            "inter_isd_paths_scion": sum(inter_isd_paths_scion) / len(inter_isd_paths_scion) if len(inter_isd_paths_scion) > 0 else 0,
            "intra_isd_paths_nx": sum(intra_isd_paths_nx) / len(intra_isd_paths_nx) if len(intra_isd_paths_nx) > 0 else 0,
            "inter_isd_paths_nx": sum(inter_isd_paths_nx) / len(inter_isd_paths_nx) if len(inter_isd_paths_nx) > 0 else 0,
        })

    new_data = pd.DataFrame(rows)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    new_data.to_csv(output_path, index=False)
    print(f"Created new CSV at {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", "-f", required=True, help="Folder with path text files")
    parser.add_argument("--topologies", "-t", required=True, help="Folder containing all topology configurations")
    parser.add_argument("--output", "-o", required=True, help="Output CSV path")
    args = parser.parse_args()

    parse_folder(args.folder, args.output, args.topologies)