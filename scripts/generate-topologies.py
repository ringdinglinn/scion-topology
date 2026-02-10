#!/usr/bin/env python3
# scripts/generate-topologies.py
import json
import argparse
from collections import defaultdict

def parse_edge(edge_str):
    """Parse edge string like '1-1:1-4:child' into components"""
    parts = edge_str.split(':')
    src_isd, src_as = parts[0].split('-')
    dst_isd, dst_as = parts[1].split('-')
    link_type = parts[2]
    return (int(src_isd), int(src_as)), (int(dst_isd), int(dst_as)), link_type

def get_link_type_reverse(link_type):
    """Get the reverse link type"""
    reverse_map = {
        'core': 'core',
        'parent': 'child',
        'child': 'parent',
        'peer': 'peer'
    }
    return reverse_map[link_type]

def generate_topology_file(isd, as_num, edges, output_dir):
    """Generate topology JSON for a specific AS"""
    node = (isd, as_num)
    
    # Calculate ISD number (16, 17, 18, ...)
    isd_num = 15 + isd
    
    # Determine if this is a core AS (has any core links)
    is_core = any(
        link_type == 'core' 
        for (src, dst, link_type) in edges 
        if src == node or dst == node
    )
    
    # Build interfaces
    interfaces = {}
    interface_id = 1
    
    for src, dst, link_type in edges:
        if src == node:
            # Outgoing edge
            dst_isd, dst_as = dst
            dst_isd_num = 15 + dst_isd
            
            interfaces[str(interface_id)] = {
                "underlay": {
                    "local": f"10.100.0.{isd}{as_num}:500{isd}{as_num}",
                    "remote": f"10.100.0.{dst_isd}{dst_as}:500{dst_isd}{dst_as}"
                },
                "isd_as": f"{dst_isd_num}-ffaa:1:{dst_isd}{dst_as}",
                "link_to": link_type,
                "mtu": 1472
            }
            interface_id += 1
        elif dst == node:
            # Incoming edge (add reverse)
            src_isd, src_as = src
            src_isd_num = 15 + src_isd
            reverse_link_type = get_link_type_reverse(link_type)
            
            interfaces[str(interface_id)] = {
                "underlay": {
                    "local": f"10.100.0.{isd}{as_num}:500{src_isd}{src_as}",
                    "remote": f"10.100.0.{src_isd}{src_as}:500{isd}{as_num}"
                },
                "isd_as": f"{src_isd_num}-ffaa:1:{src_isd}{src_as}",
                "link_to": reverse_link_type,
                "mtu": 1472
            }
            interface_id += 1
    
    # Build topology JSON
    topology = {
        "attributes": ["core"] if is_core else [],
        "isd_as": f"{isd_num}-ffaa:1:{isd}{as_num}",
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
    filename = f"{output_dir}/topology{as_num}.json"
    with open(filename, 'w') as f:
        json.dump(topology, f, indent=4)
    
    print(f"✅ Generated {filename}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--edges', required=True, help='Space-separated edge list')
    parser.add_argument('--isds', required=True, help='Space-separated ISD list')
    args = parser.parse_args()
    
    # Parse edges
    edges = []
    for edge_str in args.edges.split():
        src, dst, link_type = parse_edge(edge_str)
        edges.append((src, dst, link_type))
    
    # Create output directory
    import os
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Generate topology for each AS
    ISDS = [int(x) for x in args.isds.split()]
    for isd in ISDS:
        for as_num in range(1, args.as_count + 1):
            generate_topology_file(isd, as_num, edges, args.output_dir)
    
    print(f"\n✅ Generated all topology files in {args.output_dir}")

if __name__ == '__main__':
    main()