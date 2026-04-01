#!/usr/bin/env bats
current_node=""

# Minimal intra-ISD
@test "bat request from scion1-1 to scion1-2" {
    run docker exec scion1-1 scion-bat http://16-ffaa:1:2,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion2-1 to scion2-2" {
    run docker exec scion2-1 scion-bat http://17-ffaa:2:2,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
# Diagonal ISD-to_ISD
@test "bat request from scion1-1 to scion2-1" {
    run docker exec scion1-1 scion-bat http://17-ffaa:2:1,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion1-2 to scion2-2" {
    run docker exec scion1-2 scion-bat http://17-ffaa:2:2,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion2-1 to scion1-1" {
    run docker exec scion2-1 scion-bat http://16-ffaa:1:1,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion2-2 to scion1-2" {
    run docker exec scion2-2 scion-bat http://16-ffaa:1:2,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
