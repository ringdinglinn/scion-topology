#!/usr/bin/env python3
# scripts/generate-nodeconfig.py
import yaml
import argparse

def node(asn, as_idx, isd, isd_n):
    return {
        "name": f"scion{isd}{asn}",
        "address": f"10.100.{isd}.{asn}",
        "isd": isd_n,
        "as": as_idx
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', required=True, help='ISD config')
    args = parser.parse_args()
    
    with open(args.config, 'r') as f:
        config = yaml.safe_load(f)
    
    isds = config['ISDs']
    hosts = []
    index = 1
    
    for isd in isds:
        for asn in range(1, isds[isd]['n'] + 1):
            hosts.append(node(asn, index, isd, isd+15))
            index += 1
    
    node_config = {
        "hosts": hosts,
        "default_port": 8080,
        "default_sciond_address": "127.0.0.1"
    }
    
    with open('monitor/scionctl/internal/config/nodeconfig.yaml', 'w') as f:
        yaml.dump(node_config, f, default_flow_style=False, sort_keys=False)
    
    print(f"✅ Generated nodeconfig.yaml with {len(hosts)} nodes")

if __name__ == '__main__':
    main()