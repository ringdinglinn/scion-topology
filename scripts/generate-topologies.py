#!/usr/bin/env python3
# scripts/generate-topologies.py
import json
import argparse
from collections import defaultdict
import yaml
import os
from helpers.parse_topology import yaml_to_graph
from helpers.node_addresses import isd_as_to_label, label_to_idx
from collections import deque

def parse_edge(edge_str):
    """Parse edge string like '1-1 1-4' into components"""
    parts = edge_str.split(' ')
    src_isd, src_as = parts[0].split('-')
    dst_isd, dst_as = parts[1].split('-')
    return (int(src_isd), int(src_as)), (int(dst_isd), int(dst_as)),

def addr(isd, asn):
    return f"10.100.{isd}.{asn}"

def port(dst_isd, dst_as):
    return 50000 + dst_isd * 100 + dst_as

def get_link_type(core_ases, src_isd, src_as, dst_isd, dst_as, core_dists, G):
    src_core = src_as in core_ases.get(src_isd, set())
    dst_core = dst_as in core_ases.get(dst_isd, set())
    src_idx = label_to_idx(G, isd_as_to_label(src_isd, src_as))
    dst_idx = label_to_idx(G, isd_as_to_label(dst_isd, dst_as))

    if (src_core and dst_core): return "core"
    elif (not src_core and not dst_core):
        if core_dists[src_idx] < core_dists[dst_idx]:
            return "child"
        elif core_dists[src_idx] > core_dists[dst_idx]:
            return "parent"
        else:
            return "peer"
    elif src_core: return "child"
    else: return "parent"

def generate_topology_file(isd, as_num, edges, core_ases, core_dists, G, output_dir):
    """Generate topology JSON for a specific AS"""
    node = (isd, as_num)
    
    # Calculate ISD number (16, 17, 18, ...)
    isd_num = 15 + isd

    # Build interfaces
    interfaces = {}
    interface_id = 1

    is_core = as_num in core_ases.get(isd, set())
    
    for src, dst in edges:
        dst_isd, dst_as = dst
        dst_isd_num = 15 + dst_isd
        src_isd, src_as = src
        src_isd_num = 15 + src_isd

        if src == node:
            # Outgoing edge
            interfaces[str(interface_id)] = {
                "underlay": {
                    "local": f"{addr(src_isd, src_as)}:{port(dst_isd, dst_as)}",
                    "remote": f"{addr(dst_isd, dst_as)}:{port(src_isd, src_as)}"
                },
                "isd_as": f"{dst_isd_num}-ffaa:{dst_isd}:{dst_as}",
                "link_to": get_link_type(core_ases, src_isd, src_as, dst_isd, dst_as, core_dists, G),
                "mtu": 1472
            }
            interface_id += 1
        elif dst == node:
            # Incoming edge (add reverse)
            
            interfaces[str(interface_id)] = {
                "underlay": {
                    "local": f"{addr(dst_isd, dst_as)}:{port(src_isd, src_as)}",
                    "remote": f"{addr(src_isd, src_as)}:{port(dst_isd, dst_as)}"
                },
                "isd_as": f"{src_isd_num}-ffaa:{src_isd}:{src_as}",
                "link_to": get_link_type(core_ases, dst_isd, dst_as, src_isd, src_as, core_dists, G),
                "mtu": 1472
            }
            interface_id += 1
    
    # Build topology JSON
    topology = {
        "attributes": ["core"] if is_core else [],
        "isd_as": f"{isd_num}-ffaa:{isd}:{as_num}",
        "dispatched_ports": "31000-32767",
        "mtu": 1472,
        "control_service": {
            "cs": {
                "addr": "127.0.0.1:31000"
            }
        },
        "discovery_service": {
            "cs": {
                "addr": "127.0.0.1:31000"
            }
        },
        "border_routers": {
            "br": {
                "internal_addr": "127.0.0.1:31002",
                "interfaces": interfaces
            }
        }
    }
    
    # Write to file
    as_dir = os.path.join(output_dir, f"isd{isd}", f"as{as_num}")
    os.makedirs(as_dir, exist_ok=True)
    filename = os.path.join(as_dir, "topology.json")    
    with open(filename, 'w') as f:
        json.dump(topology, f, indent=4)
    
    print(f"✅ Generated {filename}")

def get_closeness_to_core(G):
    dist = {}
    queue = deque()

    for node in G.nodes():
        if (G.nodes[node]["is_core"]):
            dist[node] = 0
            queue.append(node)

    while queue:
        current = queue.popleft()
        neighbors = G.neighbors(current)
        for neighbor in neighbors:
            if neighbor not in dist:
                dist[neighbor] = dist[current] + 1
                queue.append(neighbor)

    return dist


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--topology-path', '-tp', required=True, help='Path to Topology/ISD configuration')
    parser.add_argument('--output-dir', '-o', required=True, help='Topologies directory')
    args = parser.parse_args()
    
    edges = []

    with open(args.topology_path, 'r') as f:
        config = yaml.safe_load(f)

    G = yaml_to_graph(args.topology_path)
    core_dists = get_closeness_to_core(G)
    

    for line in config["Topology"]:
        line = line.strip()
        if line:
            src, dst = parse_edge(line)
            edges.append((src, dst))
    
    # Create output directory
    import os
    os.makedirs(args.output_dir, exist_ok=True)
    
    isds = config['ISDs']

    core_ases = {
        int(isd): set(isds[isd].get("core", []))
        for isd in isds
    }
    
    for isd in isds:
        for as_num in range(1, isds[isd]["n"] + 1):
            generate_topology_file(isd, as_num, edges, core_ases, core_dists, G, args.output_dir)
    
    print(f"\n✅ Generated all topology files in {args.output_dir}")

if __name__ == '__main__':
    main()