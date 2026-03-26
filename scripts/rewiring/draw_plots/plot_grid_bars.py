import os
import matplotlib.pyplot as plt
import ast
import numpy as np
from scripts.rewiring.draw_plots.utils import apply_styling, METRIC_LABELS
import matplotlib as mpl
from itertools import cycle

apply_styling()

def plot_metric_grid(metric, groups, output_dir, title=None):
    row_names = list(groups.keys())
    col_names = sorted(set(r for col in groups.values() for r in col.keys()))
    n_rows = len(row_names)
    n_cols = len(col_names)
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(5 * n_cols, 2.5 * n_rows), squeeze=False)
    fig.suptitle(f"{title}" if title else metric, fontsize=14, fontweight="bold", y=0.995)

    for row_idx, row_name in enumerate(row_names):

        # compute y max for this row only
        row_max_y = 0
        for col_name in col_names:
            for r in groups[row_name].get(col_name, []):
                try:
                    d = ast.literal_eval(r[metric])
                    if isinstance(d, dict):
                        row_max_y = max(row_max_y, max(d.values()))
                except (KeyError, ValueError):
                    pass
        y_top = row_max_y * 1.15 if row_max_y > 0 else 1.0

        for col_idx, col_name in enumerate(col_names):
            ax = axes[row_idx][col_idx]
            rows = groups[row_name].get(col_name, [])
            if not rows:
                ax.axis("off")
                continue
            try:
                parsed = [ast.literal_eval(r[metric]) for r in rows]
            except (KeyError, ValueError):
                ax.set_title(f"{row_name} / {col_name}\n(metric unavailable)")
                ax.axis("off")
                continue
            all_keys = sorted(set(k for d in parsed for k in d.keys()))
            n_topos = len(rows)
            n_keys = len(all_keys)
            x = np.arange(n_topos)
            bar_width = 0.8 / n_keys
            for j, key in enumerate(all_keys):
                y = [d.get(key, 0) for d in parsed]
                offset = (j - n_keys / 2 + 0.5) * bar_width
                ax.bar(x + offset, y, width=bar_width, label=str(key))
            ax.set_xticks(x)
            ax.set_xticklabels(range(n_topos), fontsize=8)         
            ax.set_title(f"{row_name} / {col_name}", pad=10)
            ax.set_ylabel(METRIC_LABELS.get(metric, metric) if col_idx == 0 else "")
            ax.yaxis.grid(True, linestyle="--", linewidth=0.5)
            ax.set_axisbelow(True)
            if col_idx != 0:
                ax.tick_params(labelleft=False)
            ax.set_ylim(bottom=0, top=y_top)
            ax.legend(fontsize=7)

    plt.tight_layout(rect=[0, 0, 1, 0.995])
    os.makedirs(output_dir, exist_ok=True)
    safe_name = metric.replace(" ", "_").replace("|", "").replace("/", "_")
    out_path = os.path.join(output_dir, f"{safe_name}.png")
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved: {out_path}")