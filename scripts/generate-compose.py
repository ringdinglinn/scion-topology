#!/usr/bin/env python3
# scripts/generate-compose.py
import yaml
import argparse

# Hard-coded services that don't change
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
    },
    'endhost-as1-5': {
        'container_name': 'endhost-as1-5',
        'image': 'endhost-as1-5:1.0',
        'hostname': 'endhost-as1-5',
        'volumes': ['/sys/fs/cgroup:/sys/fs/cgroup'],
        'tmpfs': ['/run', '/run/lock'],
        'networks': {
            'as_net_1-5': {'ipv4_address': '10.1.5.200'},
            'transit_net': {'ipv4_address': '10.100.1.150'}
        },
        'depends_on': ['scion1-5']
    },
    'endhost-as3-5': {
        'container_name': 'endhost-as3-5',
        'image': 'endhost-as3-5:1.0',
        'hostname': 'endhost-as3-5',
        'volumes': ['/sys/fs/cgroup:/sys/fs/cgroup'],
        'tmpfs': ['/run', '/run/lock'],
        'networks': {
            'as_net_3-5': {'ipv4_address': '10.3.5.200'},
            'transit_net': {'ipv4_address': '10.100.3.200'}
        },
        'depends_on': ['scion3-5']
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
    """Generate a single scion service configuration"""
    name = f"scion{isd}-{as_num}"
    return {
        'image': f'{name}:{version}',
        'container_name': name,
        'hostname': name,
        'networks': {
            f'as_net_{isd}-{as_num}': {} if name != "scion1-5" else {"ipv4_address": "10.1.5.100"},
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
    """Generate Mac-specific volume override for a scion service"""
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
    """Generate a single as_net network configuration"""
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
    
    # Combine static + dynamic services
    all_services = {**STATIC_SERVICES, **scion_services}

    # Generate as_net networks dynamically
    dynamic_networks = {}
    for isd in isds:
        n = isds[isd]["n"]
        for as_num in range(n):
            dynamic_networks.update(generate_network(isd, as_num+1))
    
    # Combine static + dynamic networks
    all_networks = {**dynamic_networks, **STATIC_NETWORKS}

    # Create main docker-compose.yml
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