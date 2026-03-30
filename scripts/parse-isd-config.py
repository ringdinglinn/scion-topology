#!/usr/bin/env python3
import yaml
import sys
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config_path', '-cp', required=True)
    args = parser.parse_args()
    
    with open(args.config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    isds = config['ISDs']
    
    isd_list = ' '.join(str(isd_id) for isd_id in isds.keys())
    print(f"ISDS := {isd_list}")
    
    for isd_id, isd_config in isds.items():
        as_range = ' '.join(str(i) for i in range(1, isd_config['n'] + 1))
        print(f"ISD{isd_id}_AS_RANGE := {as_range}")
        print(f"ISD{isd_id}_AS_COUNT := {isd_config['n']}")
    
    total_as = sum(isd_config['n'] for isd_config in isds.values())
    print(f"TOTAL_AS_COUNT := {total_as}")

if __name__ == '__main__':
    main()