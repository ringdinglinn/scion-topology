import argparse
import csv
import re
import os
import matplotlib.pyplot as plt
from collections import defaultdict
from plots import plot_grid, plot_grid_bars
from plots.plot_graphs import plot_graphs
from helpers.parse_topology import yaml_to_graph
from pathlib import Path


AVAILABLE_METRICS = [
    "algebaric connectivity", "assortativity", "average_clustering",
    "avg_degree", "cheeger constant", "degree_entropy", "degree_std",
    "effective graph resistance", "natural connectivity", "sparsity",
    "spectral gap", "spectral radius", "transitivity", "|E|", "|V|",
]

def parse_args():
    parser = argparse.ArgumentParser(
        description="Plot topology metrics from a CSV, grouped by regex."
    )
    parser.add_argument("--input", "-i", required=True, help="Path to the CSV file.")
    parser.add_argument("--output-dir", "-o", default="plots", help="Directory to save plots.")
    parser.add_argument("--topologies-path", "-t", required=True, help="The path that contains all the topology configurations.")
    parser.add_argument(
        "--metrics", "-m", nargs="+", default=AVAILABLE_METRICS,
        help=f"Metrics to plot. Available: {AVAILABLE_METRICS}"
    )
    parser.add_argument(
        "--group-by", "-g", required=True,
        help="Regex with a capture group to extract the group label from the 'topology' column. "
             "E.g. 'configurations/([^/]+)/' groups by top-level folder."
    )
    parser.add_argument(
        "--sort-by", "-s", default=None,
        help="Column to sort rows within each group (e.g. 'topology')."
    )
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

def get_graph_yaml_dir(topologies_path, graph_name):
    topo_name = graph_name.split("_")[0]
    return os.path.join(topologies_path, topo_name, graph_name + ".yaml")

def main():
    args = parse_args()
    rows = load_csv(args.input)
    groups = group_rows(rows, args.group_by)

    topo_paths = [get_graph_yaml_dir(args.topologies_path, row["topology"]) for row in rows]
    graph_dict = {Path(topo_path).stem: yaml_to_graph(topo_path) for topo_path in topo_paths}

    print(f"Found {len(groups)} groups: {list(groups.keys())}")

    for metric in args.metrics:
        plot_grid.plot_metric(metric, groups, args.output_dir, args.sort_by)

    plot_grid_bars.plot_metric("border_breadth", groups, args.output_dir, args.sort_by)

    plot_graphs(groups, graph_dict, args.output_dir)


if __name__ == "__main__":
    main()