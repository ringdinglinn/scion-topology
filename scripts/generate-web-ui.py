#!/usr/bin/env python3
import yaml
import json
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', required=True, help='ISD config file')
    parser.add_argument('--template', required=True, help='HTML template file')
    parser.add_argument('--output', required=True, help='Output HTML file')
    args = parser.parse_args()
    
    with open(args.config, 'r') as f:
        config = yaml.safe_load(f)
    
    isds = config['ISDs']
    
    # Generate server list
    servers = []
    scion_addresses = []
    
    for isd in sorted(isds.keys()):
        isd_num = 15 + isd
        for asn in range(1, isds[isd]['n'] + 1):
            name = f"scion{isd}-{asn}"
            ip = f"10.100.{isd}.{asn}"
            addr = f"{isd_num}-ffaa:{isd}:{asn}"
            
            servers.append({"name": name, "ip": ip})
            scion_addresses.append({"name": name, "addr": addr})
    
    # Read template
    with open(args.template, 'r') as f:
        template = f.read()
    
    # Replace placeholders
    html = template.replace('{{SERVERS_JSON}}', json.dumps(servers))
    html = html.replace('{{SCION_ADDRESSES_JSON}}', json.dumps(scion_addresses))
    
    # Write output
    with open(args.output, 'w') as f:
        f.write(html)
    
    print(f"✅ Generated {args.output}")

if __name__ == '__main__':
    main()