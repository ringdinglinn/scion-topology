import os
import matplotlib.pyplot as plt
import networkx as nx
import colorsys
from scripts.rewiring.draw_plots.utils import apply_styling

def get_node_colors(G):
    isds = sorted(set(data["isd_n"] for _, data in G.nodes(data=True)))
    hues = [i / len(isds) for i in range(len(isds))]
    isd_to_hue = {isd: hue for isd, hue in zip(isds, hues)}
    colors = []
    for _, data in G.nodes(data=True):
        hue = isd_to_hue[data["isd_n"]]
        if data.get("is_core"):
            r, g, b = colorsys.hsv_to_rgb(hue, 0.6, 0.6)
        else:
            r, g, b = colorsys.hsv_to_rgb(hue, 0.2, 0.95)
        colors.append((r, g, b))
    return colors

def plot_graph(G, title=None, output_path=None, save=False, show=True):
    apply_styling()
    _, ax = plt.subplots(figsize=(8, 6))
    pos = nx.spring_layout(G, seed=42)
    node_colors = get_node_colors(G)
    labels = {node: data["label"] for node, data in G.nodes(data=True)}
    nx.draw(G, pos, ax=ax, labels=labels, node_color=node_colors,
            node_size=300, font_size=7, edge_color="gray")
    if title:
        ax.set_title(title, fontsize=8)
    plt.tight_layout()
    if save and output_path:
        plt.savefig(output_path, dpi=300)
        print(f"Saved: {output_path}")
    if show:
        plt.show()
    plt.close()

def plot_graph_grid(groups, graphs, output_dir=None, sort_by=None, save=True, show=False):
    apply_styling()
    if save:
        os.makedirs(output_dir, exist_ok=True)
    for group_name, subgroups in groups.items():
        subgroup_names = sorted(subgroups.keys())
        n_cols = len(subgroup_names)
        n_rows = max(len(rows) for rows in subgroups.values())
        _, axes = plt.subplots(n_rows, n_cols, figsize=(5 * n_cols, 4 * n_rows))
        if n_cols == 1:
            axes = [[ax] for ax in axes]
        if n_rows == 1:
            axes = [axes]
        for col_idx, sub_name in enumerate(subgroup_names):
            rows = subgroups[sub_name]
            if sort_by:
                rows = sorted(rows, key=lambda r: r.get(sort_by, ""))
            for row_idx, row in enumerate(rows):
                ax = axes[row_idx][col_idx] if n_rows > 1 else axes[0][col_idx]
                name = os.path.basename(row["topology"]).replace(".yaml", "")
                G = graphs[name]
                pos = nx.spring_layout(G, seed=42)
                node_colors = get_node_colors(G)
                labels = {node: data["label"] for node, data in G.nodes(data=True)}
                nx.draw(G, pos, ax=ax, labels=labels, node_color=node_colors,
                        node_size=300, font_size=7, edge_color="gray")
                ax.set_title(f"{sub_name}\n{name}", fontsize=8)
            for extra_row in range(len(rows), n_rows):
                ax = axes[extra_row][col_idx] if n_rows > 1 else axes[0][col_idx]
                ax.axis("off")
        plt.tight_layout()
        if save and output_dir is not None:
            out_path = os.path.join(output_dir, f"{group_name}.png")
            plt.savefig(out_path, dpi=300)
            print(f"Saved: {out_path}")
        if show:
            plt.show()
        plt.close()