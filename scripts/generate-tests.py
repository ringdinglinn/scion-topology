#!/usr/bin/env python3
import yaml
import argparse

def generate_test_combinations(config, test_generator):
    tests = []
    tests.append('#!/usr/bin/env bats\n')
    tests.append('current_node=""\n\n')
    
    isds = config['ISDs']
    isd_list = sorted(isds.keys())
    
    # Intra-ISD tests (AS 1 -> AS 2 in each ISD)
    tests.append('# Minimal intra-ISD\n')
    for isd in isd_list:
        if isds[isd]['n'] >= 2:
            tests.append(test_generator(isd, 1, isd, 2))
    
    # Diagonal cases
    tests.append('# Diagonal ISD-to_ISD\n')
    if len(isd_list) >= 2:
        for i, src_isd in enumerate(isd_list):
            src_max = isds[src_isd]['n']
            dst_isd = isd_list[(i + 1) % len(isd_list)]
            dst_max = isds[dst_isd]['n']
            for src_as in range(1, src_max + 1):
                if src_as <= dst_max:
                    tests.append(test_generator(src_isd, src_as, dst_isd, src_as))
    
    return tests

def generate_ping_test(src_isd, src_as, dst_isd, dst_as):
    src_name = f"scion{src_isd}-{src_as}"
    dst_name = f"scion{dst_isd}-{dst_as}"
    
    return f'''@test "{src_name} can scion-ping {dst_name}" {{
\tcurrent_node="{src_name}"
\trun docker exec monitor scionctl scionping start {src_name} {dst_name} --count 1
\tsleep 1
\t[ "$status" -eq 0 ]
\t[[ "$output" != *"Error"* ]]
\trun docker exec monitor scionctl scionping list {src_name}
\tfilename=$(echo "$output" | awk -F'|' '/\\.log/ {{gsub(/ /, "", $3); fname=$3}} END {{sub(/\\.log$/, "", fname); print fname}}')
\trun docker exec monitor scionctl scionping file {src_name} $filename
\tping_output="$output"
\tpacket_loss_line=$(echo "$ping_output" | grep "packet loss")
\tpacket_loss_value=$(echo "$packet_loss_line" | awk '{{print $6}}')
\t[ "$packet_loss_value" = "0%" ]
}}
'''

def generate_bat_test(src_isd, src_as, dst_isd, dst_as):
    src_name = f"scion{src_isd}-{src_as}"
    dst_isd_num = 15 + dst_isd
    
    return f'''@test "bat request from {src_name} to scion{dst_isd}-{dst_as}" {{
    run docker exec {src_name} scion-bat http://{dst_isd_num}-ffaa:{dst_isd}:{dst_as},127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}}
'''

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', required=True, help='ISD config file')
    args = parser.parse_args()
    
    with open(args.config, 'r') as f:
        config = yaml.safe_load(f)
    
    # Generate scionping tests
    with open('test/scionping_test.bats', 'w') as f:
        tests = generate_test_combinations(config, generate_ping_test)
        tests.append('teardown() {\n')
        tests.append('  docker exec "$current_node" bash -c "rm -rf /var/lib/scion-node-manager/scion-ping-results/*"\n')
        tests.append('}\n')
        tests_str = ''.join(tests)
        f.write(tests_str)
    
    # Generate bat tests
    with open('test/scion_bat_test.bats', 'w') as f:
        tests = generate_test_combinations(config, generate_bat_test)
        tests_str = ''.join(tests)
        f.write(tests_str)
    
    print("✅ Generated test files")

if __name__ == '__main__':
    main()