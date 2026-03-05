from metrics import metrics_complex, metrics_basic, spectral, sparsity, border_breadth
import argparse
from helpers.parse_topology import yaml_to_graph
import os
import csv
from pathlib import Path

def run_all_metrics(G):
    results = {}
    results.update(metrics_basic.compute(G))
    results.update(metrics_complex.compute(G))
    results.update(spectral.compute(G))
    results.update(sparsity.compute(G))
    results.update(border_breadth.compute(G))

    return results

def search_dir_for_yaml(path):
    yaml_files = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.yaml') or file.endswith('.yml'):
                yaml_files.append(os.path.join(root, file))
        for cur_dir in dirs:
            yaml_files.extend(search_dir_for_yaml(cur_dir))
    return yaml_files

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the mathematical evaluations on the topologies.")
    parser.add_argument("--input-path", "-i", required=True, help="Path to the collected topologies")
    parser.add_argument("--output-path", "-o", required=True, help="")
    args = parser.parse_args()

    topo_paths = search_dir_for_yaml(args.input_path)
    results = { Path(topo_path).stem : run_all_metrics(yaml_to_graph(topo_path)) for topo_path in topo_paths }

    with open(args.output_path, 'w', newline='') as csvfile:
        fieldnames = set()
        for metrics_dict in results.values():
            fieldnames.update(metrics_dict.keys())
        fieldnames = sorted(list(fieldnames))
        
        writer = csv.DictWriter(csvfile, fieldnames=['topology'] + fieldnames)
        writer.writeheader()
        
        for topo_path, metrics in results.items():
            row = {'topology': topo_path}
            row.update(metrics)
            writer.writerow(row)