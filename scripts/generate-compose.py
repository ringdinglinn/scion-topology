#!/usr/bin/env python3
# scripts/generate-compose.py
import yaml
import argparse

STATIC_SERVICES = {
    'monitor': {
        'image': 'monitor:1.0',
        'container_name': 'monitor',
        'hostname': 'monitor',
        'ports': ['8080:8080'],
        'networks': {
            'transit_net': {'ipv4_address': '10.100.0.100'}
        },
        'volumes': ['./captures:/data', '/sys/fs/cgroup:/sys/fs/cgroup'],
        'tmpfs': ['/run', '/run/lock']
    }
}

STATIC_NETWORKS = {
    'transit_net': {
        'driver': 'bridge',
        'ipam': {
            'config': [{'subnet': '10.100.0.0/16'}]
        }
    }
}

def generate_scion_service(isd, as_num, version):
    name = f"scion{isd}-{as_num}"
    return {
        'image': f'{name}:{version}',
        'container_name': name,
        'hostname': name,
        'networks': {
            f'as_net_{isd}-{as_num}': {},
            'transit_net': {
                'ipv4_address': f'10.100.{isd}.{as_num}'
            }
        },
        'volumes': [
            '/sys/fs/cgroup:/sys/fs/cgroup',
            '/home/shared:/shared'
        ],
        'tmpfs': ['/run', '/run/lock']
    }

def generate_mac_volume_override(isd, as_num):
    name = f"scion{isd}-{as_num}"
    return {
        name: {
            'volumes': [
                '/sys/fs/cgroup:/sys/fs/cgroup',
                '/Users/Shared:/shared'
            ]
        }
    }

def generate_network(isd, as_num):
    return {
        f'as_net_{isd}-{as_num}': {
            'ipam': {
                'config': [
                    {'subnet': f'10.{isd}.{as_num}.0/24'}
                ]
            }
        }
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', required=True, help='ISD config')
    parser.add_argument('--version', required=True, help='Docker image version')
    args = parser.parse_args()
    
    with open(args.config, 'r') as f:
        config = yaml.safe_load(f)
    
    isds = config['ISDs']

    VERSION = args.version

    # Generate scion services dynamically
    scion_services = {}
    mac_overrides = {}
    for isd in isds:
        n = isds[isd]["n"]
        for as_num in range(n):
            name = f"scion{isd}-{as_num+1}"
            scion_services[name] = generate_scion_service(isd, as_num+1, VERSION)
            mac_overrides.update(generate_mac_volume_override(isd, as_num+1))
    
    all_services = {**STATIC_SERVICES, **scion_services}

    dynamic_networks = {}
    for isd in isds:
        n = isds[isd]["n"]
        for as_num in range(n):
            dynamic_networks.update(generate_network(isd, as_num+1))
    
    all_networks = {**dynamic_networks, **STATIC_NETWORKS}

    compose = {
        'name': 'SCION Testbed',
        'services': all_services,
        'networks': all_networks
    }

    with open('docker-compose.yml', 'w') as f:
        yaml.dump(compose, f, default_flow_style=False, sort_keys=False)
    
    print(f"✅ Generated docker-compose.yml with {len(scion_services)} scion nodes")

    # Create docker-compose.mac.yml (only overrides)
    mac_compose = {
        'services': mac_overrides
    }

    with open('docker-compose.mac.yml', 'w') as f:
        yaml.dump(mac_compose, f, default_flow_style=False, sort_keys=False)
    
    print(f"✅ Generated docker-compose.mac.yml with Mac volume overrides")

if __name__ == '__main__':
    main()