import os
import matplotlib.pyplot as plt
from topology_optimization.scripts.draw_plots.utils import apply_styling, METRIC_NAMES, METRIC_LABELS, TOPO_NAMES
import matplotlib as mpl
from itertools import cycle

apply_styling()

def plot_metrics(metrics, groups, output_dir, title=None):
    linestyles = ["--", ":", "-:"]
    markerstyles = ["d", "x", "s"]
    group_names = list(groups.keys())
    n_groups = len(group_names)
    n_cols = min(4, n_groups)
    n_rows = (n_groups + n_cols - 1) // n_cols

    subplot_h = max(3, 6 // n_rows)
    subplot_w = max(4, 10 // n_cols)
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(subplot_w * n_cols, subplot_h * n_rows))

    axes = [axes] if n_groups == 1 else axes.flatten()

    metric_names = [METRIC_NAMES.get(m, m) for m in metrics]
    fig.suptitle(f"{title} | {' | '.join(metric_names)}" if title else " | ".join(metric_names), fontsize=14, fontweight="bold", y=1.02)

    metric_labels = [METRIC_LABELS.get(m, m) for m in metrics]

    all_subgroups = set()
    for subdict in groups.values():
        all_subgroups.update(subdict.keys())
    all_subgroups = sorted(all_subgroups)

    colors = [c["color"] for c in mpl.rcParams["axes.prop_cycle"]]
    color_map = {name: col for name, col in zip(all_subgroups, cycle(colors))}
    handles, labels = [], []

    global_max_y = 0
    for subgroups in groups.values():
        for rows in subgroups.values():
            for metric in metrics:
                valid = [float(r[metric]) for r in rows if r.get(metric)]
                if valid:
                    global_max_y = max(global_max_y, max(valid))
    y_top = global_max_y * 1.15

    for i, group_name in enumerate(group_names):
        ax = axes[i]
        row, col = divmod(i, n_cols)
        subgroups = groups[group_name]

        for sub_name, rows in subgroups.items():
            for m_idx, metric in enumerate(metrics):
                valid_rows = [r for r in rows if r.get(metric)]
                if not valid_rows:
                    continue
                y_values = [float(r[metric]) for r in valid_rows]
                if (len(metrics) > 1):
                    linestyle = linestyles[m_idx % len(linestyles)]
                    markerstyle = "."
                    legend_key = f"{sub_name} | {METRIC_NAMES[metric]}"
                else:
                    linestyle = "-"
                    markerstyle = "."
                    legend_key = f"{sub_name}"
                line, = ax.plot(
                    range(len(y_values)), y_values,
                    marker=markerstyle, markersize=5, color=color_map[sub_name],
                    linestyle=linestyle, label=legend_key
                )
                if legend_key not in labels:
                    handles.append(line)
                    labels.append(legend_key)

        ax.set_xticks(range(len(y_values)))
        ax.set_xlabel("Iterations" if row == n_rows - 1 else "")
        ax.set_title(TOPO_NAMES[group_name])
        ax.yaxis.grid(True, linestyle="--", linewidth=0.5)
        ax.set_axisbelow(True)
        ax.set_ylabel(metric_labels[0] if col == 0 else "")
        ax.set_ylim(bottom=0, top=y_top)

    for j in range(i + 1, len(axes)):
        axes[j].axis("off")
    if handles:
        fig.legend(handles, labels, loc="lower center", ncol=min(len(labels), 5),
                   bbox_to_anchor=(0.5, -0.03))

    plt.tight_layout(rect=[0, 0.03, 1, 1])
    os.makedirs(output_dir, exist_ok=True)
    safe_name = "_vs_".join(m.replace(" ", "_").replace("|", "").replace("/", "_") for m in metrics)
    out_path = os.path.join(output_dir, f"{safe_name}.png")
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved: {out_path}")