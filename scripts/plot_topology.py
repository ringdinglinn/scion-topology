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
import pprint


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
        "--sort-by", "-s", required=True,
        help="Column to sort rows within each group (e.g. 'topology')."
    )
    parser.add_argument(
        "--subgroup-by", "-sg",
        help="Optional second regex with capture group for subgrouping (e.g. algorithm)."
    )
    return parser.parse_args()


def load_csv(path):
    with open(path, "r") as f:
        reader = csv.DictReader(f)
        return list(reader)

def attach_baselines(groups):
    it0_pattern = re.compile(r"_it0$")

    for topo, algos in groups.items():

        baseline_rows = []
        for algo, rows in algos.items():
            for r in rows:
                if it0_pattern.search(r["topology"]):
                    baseline_rows.append(r)

        if not baseline_rows:
            continue

        for algo in algos:
            # avoid duplicates
            has_it0 = any(it0_pattern.search(r["topology"]) for r in algos[algo])
            if not has_it0:
                algos[algo] = baseline_rows + algos[algo]

    return groups

def group_rows(rows, group_regex, subgroup_regex=None):
    group_pattern = re.compile(group_regex)
    subgroup_pattern = re.compile(subgroup_regex) if subgroup_regex else None

    groups = defaultdict(lambda: defaultdict(list))

    for row in rows:
        g = group_pattern.search(row["topology"])
        group_key = g.group(1) if g else "ungrouped"

        if subgroup_pattern:
            s = subgroup_pattern.search(row["topology"])
            subgroup_key = s.group(1) if s else "default"
        else:
            subgroup_key = "default"

        groups[group_key][subgroup_key].append(row)

    return groups

def get_graph_yaml_dir(topologies_path, graph_name):
    topo_name = graph_name.split("_")[0]
    return os.path.join(topologies_path, topo_name, graph_name + ".yaml")

def main():
    args = parse_args()
    rows = load_csv(args.input)
    groups = group_rows(rows, args.group_by, args.subgroup_by)
    for topo, algos in groups.items():
        baseline_rows = algos.pop("default", [])
        for algo, alg_rows in algos.items():
            # prepend baseline if not already present
            it0_present = any(r['topology'].endswith('_it0') for r in alg_rows)
            if baseline_rows and not it0_present:
                algos[algo] = baseline_rows + alg_rows


    topo_paths = [get_graph_yaml_dir(args.topologies_path, row["topology"]) for row in rows]
    graph_dict = {Path(topo_path).stem: yaml_to_graph(topo_path) for topo_path in topo_paths}


    for metric in args.metrics:
        plot_grid.plot_metric(metric, groups, args.output_dir, args.sort_by)

    # plot_grid_bars.plot_metric("border_breadth", groups, args.output_dir, args.sort_by)

    plot_graphs(groups, graph_dict, args.output_dir + "/graphs")


if __name__ == "__main__":
    main()