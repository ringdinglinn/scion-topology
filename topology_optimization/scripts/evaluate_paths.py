import re
import argparse
import pandas as pd
from pathlib import Path


def parse_combined_file(filepath):
    with open(filepath, "r") as f:
        content = f.read()

    # Split on the === headers, tolerating whitespace/CRLF
    sections = re.split(r"===\s*(.+?)\s*===\r?\n", content)
    # sections: ['', header1, body1, header2, body2, ...]
    pairs = []
    for i in range(1, len(sections) - 1, 2):
        header = sections[i]
        body   = sections[i + 1]
        m = re.search(r"\[(\w+)\]", header)
        if not m:
            print(f"Warning: no conn_type found in header: {header!r}")
            continue
        conn_type = m.group(1)
        pairs.append((conn_type, body))
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

        for conn_type, body in parse_combined_file(filepath):
            n_paths = count_paths(body)
            if conn_type == "intra":
                intra.append(n_paths)
            elif conn_type == "inter":
                inter.append(n_paths)
            elif conn_type == "total":
                total.append(n_paths)

        rows.append({
            "topology":            topo_name,
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