import networkx as nx
import argparse
import os
from topology_optimization.scripts.draw_plots.utils import TOPO_NAMES
import re
from collections import defaultdict
import pandas as pd

SUBGROUP_LABELS = {"rac" : "$R_{AC}$", "rnp" : "$R_{NP}$"}

def paths_to_latex_table(groups) -> str:
    algo_order = ["$R_{AC}$", "$R_{NP}$"]
    avg_col = "total_paths_avg"

    # Pre-collect all deltas to normalise colour intensity
    all_deltas = []
    for topo, algos in groups.items():
        for algo in algo_order:
            algo_rows = algos.get(algo, [])
            if algo_rows:
                d = float(algo_rows[-1].get(avg_col, 0)) - float(algo_rows[0].get(avg_col, 0))
                all_deltas.append(d)
    max_abs = max((abs(d) for d in all_deltas), default=1) or 1

    def delta_cell(d: float) -> str:
        intensity = int(round(abs(d) / max_abs * 100))
        color = "green" if d >= 0 else "red"
        return f"\\cellcolor{{{color}!{intensity}}}{d:+.2f}"

    lines = []
    lines.append(r"\begin{table}[h]")
    lines.append(r"    \centering")
    lines.append(r"    \resizebox{\textwidth}{!}{")
    lines.append(r"    \begin{tabular}{l" + "rrr" * len(algo_order) + "}")
    lines.append(r"        \toprule")

    lines.append("        & " + " & ".join(
        f"\\multicolumn{{3}}{{c}}{{{algo}}}" for algo in algo_order
    ) + r" \\")
    lines.append("        " + "".join(
        f"\\cmidrule(lr){{{2 + i*3}-{4 + i*3}}}" for i in range(len(algo_order))
    ))
    lines.append("        Topology & " + " & ".join(
        r"Start & End & $\Delta$" for _ in algo_order
    ) + r" \\")
    lines.append(r"        \midrule")

    for topo, algos in sorted(groups.items(), key=lambda item: int(re.search(r'\d+', item[0]).group())):
        topo_label = TOPO_NAMES.get(topo, topo)
        row = [topo_label]
        for algo in algo_order:
            algo_rows = algos.get(algo, [])
            if algo_rows:
                s_avg = float(algo_rows[0].get(avg_col, 0))
                e_avg = float(algo_rows[-1].get(avg_col, 0))
                d_avg = e_avg - s_avg
                row += [f"{s_avg:.2f}", f"{e_avg:.2f}", delta_cell(d_avg)]
            else:
                row += ["--", "--", "--"]
        lines.append("        " + " & ".join(row) + r" \\")

    lines.append(r"        \bottomrule")
    lines.append(r"    \end{tabular}}")
    lines.append(r"    \caption{Path statistics}")
    lines.append(r"    \label{tab:path_stats}")
    lines.append(r"\end{table}")

    return "\n".join(lines)


def group_rows(rows, group_regex, subgroup_regex=None):
    print("subgroup regex", subgroup_regex)
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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate LaTeX table from graph topologies")
    parser.add_argument("--input", "-i", type=str, required=True, help="Path to the path eval results")
    parser.add_argument("--output_dir", "-o", type=str, required=True, help="Path to output directory for table.tex")
    parser.add_argument("--group-by", "-g", type=str, required=True)
    parser.add_argument("--subgroup-by", "-sg", type=str, required=True)
    args = parser.parse_args()

    rows = pd.read_csv(args.input).to_dict('records')
    groups = group_rows(rows, args.group_by, args.subgroup_by)

    for topo, algos in groups.items():
        for old_key, new_key in SUBGROUP_LABELS.items():
            if old_key in algos:
                algos[new_key] = algos.pop(old_key)

    for topo, algos in groups.items():
        for algo, algo_rows in algos.items():
            algos[algo] = sorted(algo_rows, key=lambda r: int(re.search(r'_it(\d+)', r["topology"]).group(1)))
    
    for topo, algos in groups.items():
        baseline_rows = algos.pop("default", [])
        for algo, alg_rows in algos.items():
            # prepend baseline if not already present
            it0_present = any(r['topology'].endswith('_it0') for r in alg_rows)
            if baseline_rows and not it0_present:
                algos[algo] = baseline_rows + alg_rows

    table = paths_to_latex_table(groups)
    with open(os.path.join(args.output_dir, "paths_table.tex"), "w") as f:
        f.write(table)