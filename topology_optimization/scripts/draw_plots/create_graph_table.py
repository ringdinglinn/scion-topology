import argparse
import os
from topology_optimization.scripts.draw_plots.utils import TOPO_NAMES
from topology_optimization.scripts.helpers.parse_topology import yaml_to_graph
import re

def graphs_to_latex_table(graphs_dict) -> str:
    rows = []
    for ID, G in graphs_dict.items():
        name = TOPO_NAMES[ID]
        n_nodes = G.number_of_nodes()
        n_edges = G.number_of_edges()
        n_avg_degree = round(sum(d for _, d in G.degree()) / n_nodes, 2) if n_nodes > 0 else 0
        n_isds = len(set(data["isd_n"] for _, data in G.nodes(data=True) if "isd_n" in data))
        n_cores = sum(1 for _, data in G.nodes(data=True) if data.get("is_core") is True)
        rows.append((name, n_nodes, n_edges, n_avg_degree, n_isds, n_cores))

    lines = []
    lines.append(r"\begin{table}[h]")
    lines.append(r"    \centering")
    lines.append(r"    \begin{tabular}{lrrrrr}")
    lines.append(r"        \toprule")
    lines.append(r"        Topology & Nodes & Edges & Avg. Degree & ISDs & Core ASes \\")
    lines.append(r"        \midrule")
    for name, n_nodes, n_edges, n_avg_degree, n_isds, n_cores in rows:
        lines.append(f"        {name} & {n_nodes} & {n_edges} & {n_avg_degree} & {n_isds} & {n_cores} \\\\")
    lines.append(r"        \bottomrule")
    lines.append(r"    \end{tabular}")
    lines.append(r"    \caption{Topology statistics}")
    lines.append(r"    \label{tab:topology_stats}")
    lines.append(r"\end{table}")

    return "\n".join(lines)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate LaTeX table from graph topologies")
    parser.add_argument("--topology_folder", "-i", type=str, required=True, help="Path to folder containing topology files")
    parser.add_argument("--output_dir", "-o", type=str, required=True, help="Path to output directory for table.tex")
    args = parser.parse_args()

    graphs = {}

    for root, dirs, files in os.walk(args.topology_folder):
        for file in files:
            if file.endswith('.yaml') and file[:-5].endswith('0'):
                filepath = os.path.join(root, file)
                G = yaml_to_graph(filepath)
                gname = os.path.splitext(file)[0].split("_")[0]
                graphs[gname] = G

    graphs = dict(sorted(graphs.items(), key=lambda kv: int(re.search(r'\d+', kv[0]).group())))
    table = graphs_to_latex_table(graphs)
    with open(os.path.join(args.output_dir, "graphs_table.tex"), "w") as f:
        f.write(table)