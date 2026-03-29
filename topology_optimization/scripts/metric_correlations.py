import pandas as pd
import numpy as np
import argparse
import re
from scipy import stats

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--path-results", "-pr", required=True, help="Path to paths CSV")
    parser.add_argument("--math-results", "-mr", required=True, help="Path to graph metrics CSV")
    parser.add_argument("--output", "-o", required=True, help="Output CSV for correlation results")
    args = parser.parse_args()

    paths_df   = pd.read_csv(args.path_results)
    metrics_df = pd.read_csv(args.math_results)

    merged = pd.merge(paths_df, metrics_df, on="topology", how="inner")
    print(f"Merged {len(merged)} rows")

    path_cols = [
        "total_paths_avg",
        "inter_isd_paths_avg",
        "intra_isd_paths_avg",
    ]
    exclude = {"topology", "total_pairs", "inter_isd_pairs",
               "intra_isd_pairs", "total_paths", "border_breadth"}
    graph_cols = [
        c for c in metrics_df.columns
        if c not in exclude and metrics_df[c].dtype in [np.float64, np.int64]
    ]

    records = []
    for pc in path_cols:
        for gc in graph_cols:
            sub = merged[[pc, gc]].dropna()
            if len(sub) < 3:
                continue
            r_pearson,  p_pearson  = stats.pearsonr(sub[pc],  sub[gc])
            r_spearman, p_spearman = stats.spearmanr(sub[pc], sub[gc])
            records.append({
                "path_metric":      pc,
                "graph_metric":     gc,
                "pearson_r":        round(r_pearson,  4),
                "pearson_p":        round(p_pearson,  4),
                "spearman_r":       round(r_spearman, 4),
                "spearman_p":       round(p_spearman, 4),
                "n":                len(sub),
            })

    result = pd.DataFrame(records).sort_values(
        ["path_metric", "pearson_r"], ascending=[True, False]
    )
    result.to_csv(args.output, index=False)
    print(f"Saved correlations to {args.output}")

    for pc in path_cols:
        print(f"\n── {pc} (top 5 by |Pearson r|) ──")
        top = (result[result["path_metric"] == pc]
               .assign(abs_r=lambda df: df["pearson_r"].abs())
               .nlargest(5, "abs_r")
               .drop(columns="abs_r"))
        print(top.to_string(index=False))

if __name__ == "__main__":
    main()