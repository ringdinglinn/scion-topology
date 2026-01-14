#!/bin/bash
count=0
for i in {1..4}; do
    for j in {1..5}; do
        for k in {1..4}; do
            for l in {1..5}; do
                if [[ "$i$j" == "$k$l" ]]; then
                    continue
                fi
                printf '@test "scion%d%d can ping scion%d%d" {\n  run docker exec monitor scionctl scionping start scion%d%d scion%d%d --count 1\n  [ "$status" -eq 0 ]\n  [[ "$output" != *"Error"* ]]\n}\n\n' "$i" "$j" "$k" "$l" "$i" "$j" "$k" "$l" >> scionping_test.bats
                count=$((count+1))
            done
        done
    done
done
echo "Total tests: $count"