import argparse
import csv
import re
from collections import defaultdict
from plots import plot_grid

def parse_args():
    parser = argparse.ArgumentParser(description="Plot number of paths from a CSV, grouped by regex.")
    parser.add_argument("--input", "-i", required=True, help="Path to the paths CSV file.")
    parser.add_argument("--output", "-o", default="plots", help="Directory to save plots.")
    parser.add_argument(
        "--group-by", "-g", required=True,
        help="Regex with a capture group to extract the group label from the 'topology' column."
    )
    parser.add_argument("--sort-by", "-s", default=None, help="Column to sort rows within each group.")
    return parser.parse_args()

def load_csv(path):
    with open(path, "r") as f:
        reader = csv.DictReader(f)
        return list(reader)

def group_rows(rows, group_regex):
    pattern = re.compile(group_regex)
    groups = defaultdict(list)
    for row in rows:
        m = pattern.search(row["topology"])
        key = m.group(1) if m else "ungrouped"
        groups[key].append(row)
    return groups

def main():
    args = parse_args()
    rows = load_csv(args.input)
    groups = group_rows(rows, args.group_by)
    print(f"Found {len(groups)} groups: {list(groups.keys())}")
    plot_grid.plot_metric("num_paths", groups, args.output, args.sort_by)

if __name__ == "__main__":
    main()