import re
import argparse
import pandas as pd
from pathlib import Path
from scripts.helpers.node_addresses import name_to_isd_as


def parse_combined_file(filepath):
    with open(filepath, "r") as f:
        content = f.read()
    sections = re.split(r"===\s*(.+?)\s*===\r?\n", content)
    pairs = []
    for i in range(1, len(sections) - 1, 2):
        header = sections[i]
        body   = sections[i + 1]
        m = re.search(r"(\S+?)_to_(\S+?)\s+\[(\w+)\]", header)
        if not m:
            print(f"Warning: could not parse header: {header!r}")
            continue
        src       = m.group(1)
        dst       = m.group(2)
        conn_type = m.group(3)
        pairs.append((src, dst, conn_type, body))
    return pairs

def count_paths(content: str):
    return len(re.findall(r"^\[\s*\d+\]", content, re.MULTILINE))

def parse_folder(folder_path, output_path):
    folder = Path(folder_path)
    rows = []
    for filepath in sorted(folder.glob("*.txt")):
        topo_name = filepath.stem
        intra, inter, total = [], [], []
        print(topo_name)
        zero_paths = False
        for src, dst, conn_type, body in parse_combined_file(filepath):
            src_isd, _ = name_to_isd_as(src)
            dst_isd, _ = name_to_isd_as(dst)
            n_paths = count_paths(body)
            if (n_paths == 0):
                zero_paths = True
                continue
            if src_isd == dst_isd:
                intra.append(n_paths)
            else:
                inter.append(n_paths)
            total.append(n_paths)
        if (zero_paths): print(f"encountered 0 paths in {topo_name}")
        rows.append({
            "topology":            topo_name,
            "total_paths":         sum(total),
            "total_paths_avg":     sum(total) / len(total) if total else 0,
            "total_pairs":         len(total),
            "inter_isd_paths_avg": sum(inter) / len(inter) if inter else 0,
            "inter_isd_pairs":     len(inter),
            "intra_isd_paths_avg": sum(intra) / len(intra) if intra else 0,
            "intra_isd_pairs":     len(intra),
        })
    pd.DataFrame(rows).to_csv(output_path, index=False)
    print(f"Created new CSV at {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", "-f", required=True, help="Folder with path text files")
    parser.add_argument("--output", "-o", required=True, help="Output CSV path")
    args = parser.parse_args()

    parse_folder(args.folder, args.output)