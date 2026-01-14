#!/usr/bin/env

for i in {1..4}; do
    for j in {1..5}; do
        for k in {1..4}; do
            for l in {1..5}; do
                if [[ "$i$j" == "$k$l" ]]; then
                    continue
                fi
                echo "Test scion$i$j to scion$k$l"
            done
        done
    done
done