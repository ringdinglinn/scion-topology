import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import argparse
import os
from topology_optimization.scripts.draw_plots.utils import apply_styling, METRIC_LABELS, METRIC_NAMES


def plot_correlation_matrix(csv_path, output_dir, metric="pearson_r", pvalue_col="pearson_p", alpha=0.05, metrics=None, filter_metrics=None):
    apply_styling()
    df = pd.read_csv(csv_path)

    matrix = df.pivot(index="graph_metric", columns="path_metric", values=metric)
    pmatrix = df.pivot(index="graph_metric", columns="path_metric", values=pvalue_col)

    if metrics is not None:
        matrix  = matrix.loc[[m for m in metrics if m in matrix.index]]
        pmatrix = pmatrix.loc[matrix.index]
    elif filter_metrics is not None:
        matrix  = matrix.loc[[i for i in matrix.index if i not in filter_metrics]]
        pmatrix = pmatrix.loc[matrix.index]

    matrix = matrix.loc[matrix.abs().mean(axis=1).sort_values(ascending=False).index]
    pmatrix = pmatrix.loc[matrix.index]

    matrix  = matrix.T
    pmatrix = pmatrix.T

    n_rows, n_cols = matrix.shape
    fig, ax = plt.subplots(figsize=(1.0 * n_cols + 2, 0.6 * n_rows + 2))

    cmap = mcolors.LinearSegmentedColormap.from_list(
        "rg_diverging", ["#d73027", "#f7f7f7", "#1a9850"]
    )
    norm = mcolors.TwoSlopeNorm(vmin=-1, vcenter=0, vmax=1)

    im = ax.imshow(matrix.values, cmap=cmap, norm=norm, aspect="auto")

    for i in range(n_rows):
        for j in range(n_cols):
            val = matrix.values[i, j]
            p   = pmatrix.values[i, j]
            if np.isnan(val):
                continue
            sig = "" if (np.isnan(p) or p >= alpha) else "*"
            text_color = "black" if abs(val) < 0.6 else "white"
            ax.text(j, i, f"{val:.2f}{sig}", ha="center", va="center",
                    fontsize=8, color=text_color, fontweight="bold" if sig else "normal")

    ax.set_xticks(range(n_cols))
    col_lables = [METRIC_NAMES[col] for col in matrix.columns]
    ax.set_xticklabels(col_lables, rotation=30, ha="right", fontsize=9)
    row_labels = [METRIC_NAMES[idx] for idx in matrix.index]
    ax.set_yticks(range(n_rows))
    ax.set_yticklabels(row_labels, fontsize=9)

    cbar = fig.colorbar(im, ax=ax, fraction=0.03, pad=0.02)
    cbar.set_label(METRIC_LABELS[metric], fontsize=9)

    ax.set_title(
        f"Correlation matrix ({METRIC_LABELS[metric]}),  * p < {alpha}",
        fontsize=11, fontweight="bold", pad=12
    )

    plt.tight_layout()
    os.makedirs(output_dir, exist_ok=True)
    out_path = os.path.join(output_dir, f"correlation_matrix_{metric}.png")
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input",  "-i", required=True, help="Correlation CSV from correlate.py")
    parser.add_argument("--output", "-o", required=True, help="Output directory")
    parser.add_argument("--correlation-type", "-c", default="pearson_r",
                        choices=["pearson_r", "spearman_r"], help="Which correlation to plot")
    parser.add_argument("--metrics", "-m",  nargs="+", required=False, help="Metrics to inlcude")
    parser.add_argument("--filter-metrics", "-f",  nargs="+", required=False, help="Metrics to inlcude")
    parser.add_argument("--alpha",  "-a", type=float, default=0.05,
                        help="Significance threshold for * annotation")
    args = parser.parse_args()

    pvalue_col = "pearson_p" if args.correlation_type == "pearson_r" else "spearman_p"
    plot_correlation_matrix(args.input, args.output, args.correlation_type, pvalue_col, args.alpha, args.metrics, args.filter_metrics)