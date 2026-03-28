from metrics import metrics_complex, metrics_basic, spectral, sparsity, border_breadth
import argparse
from topology_optimization.scripts.helpers.parse_topology import yaml_to_graph
import os
import pandas as pd
from pathlib import Path

def run_all_metrics(G):
    results = {}
    results.update(metrics_basic.compute(G))
    results.update(metrics_complex.compute(G))
    results.update(spectral.compute(G))
    # results.update(sparsity.compute(G))
    results.update(border_breadth.compute(G))
    return results

def search_dir_for_yaml(path):
    yaml_files = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.yaml') or file.endswith('.yml'):
                yaml_files.append(os.path.join(root, file))
    return yaml_files

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the mathematical evaluations on the topologies.")
    parser.add_argument("--input-path", "-i", required=True, help="Path to the collected topologies")
    parser.add_argument("--output-path", "-o", required=True, help="Path to the output CSV")
    args = parser.parse_args()

    topo_paths = search_dir_for_yaml(args.input_path)
    results = {Path(topo_path).stem: run_all_metrics(yaml_to_graph(topo_path)) for topo_path in topo_paths}

    new_data = pd.DataFrame([{"topology": name, **metrics} for name, metrics in results.items()])

    output_path = Path(args.output_path)
    new_data.to_csv(output_path, index=False)
    print(f"Created new CSV at {output_path}")