#!/usr/bin/env bats
current_node=""

# Minimal intra-ISD
@test "bat request from scion1-1 to scion1-2" {
    run docker exec scion1-1 scion-bat http://16-ffaa:1:2,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
# Diagonal ISD-to_ISD
@test "bat request from scion1-1 to scion1-1" {
    run docker exec scion1-1 scion-bat http://16-ffaa:1:1,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion1-2 to scion1-2" {
    run docker exec scion1-2 scion-bat http://16-ffaa:1:2,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion1-3 to scion1-3" {
    run docker exec scion1-3 scion-bat http://16-ffaa:1:3,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion1-4 to scion1-4" {
    run docker exec scion1-4 scion-bat http://16-ffaa:1:4,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion1-5 to scion1-5" {
    run docker exec scion1-5 scion-bat http://16-ffaa:1:5,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion1-6 to scion1-6" {
    run docker exec scion1-6 scion-bat http://16-ffaa:1:6,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion1-7 to scion1-7" {
    run docker exec scion1-7 scion-bat http://16-ffaa:1:7,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion1-8 to scion1-8" {
    run docker exec scion1-8 scion-bat http://16-ffaa:1:8,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion1-9 to scion1-9" {
    run docker exec scion1-9 scion-bat http://16-ffaa:1:9,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion1-10 to scion1-10" {
    run docker exec scion1-10 scion-bat http://16-ffaa:1:10,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion1-11 to scion1-11" {
    run docker exec scion1-11 scion-bat http://16-ffaa:1:11,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion1-12 to scion1-12" {
    run docker exec scion1-12 scion-bat http://16-ffaa:1:12,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion1-13 to scion1-13" {
    run docker exec scion1-13 scion-bat http://16-ffaa:1:13,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion1-14 to scion1-14" {
    run docker exec scion1-14 scion-bat http://16-ffaa:1:14,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion1-15 to scion1-15" {
    run docker exec scion1-15 scion-bat http://16-ffaa:1:15,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion1-16 to scion1-16" {
    run docker exec scion1-16 scion-bat http://16-ffaa:1:16,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion1-17 to scion1-17" {
    run docker exec scion1-17 scion-bat http://16-ffaa:1:17,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion1-18 to scion1-18" {
    run docker exec scion1-18 scion-bat http://16-ffaa:1:18,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion1-19 to scion1-19" {
    run docker exec scion1-19 scion-bat http://16-ffaa:1:19,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion1-20 to scion1-20" {
    run docker exec scion1-20 scion-bat http://16-ffaa:1:20,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion1-21 to scion1-21" {
    run docker exec scion1-21 scion-bat http://16-ffaa:1:21,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion1-22 to scion1-22" {
    run docker exec scion1-22 scion-bat http://16-ffaa:1:22,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion1-23 to scion1-23" {
    run docker exec scion1-23 scion-bat http://16-ffaa:1:23,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion1-24 to scion1-24" {
    run docker exec scion1-24 scion-bat http://16-ffaa:1:24,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion1-25 to scion1-25" {
    run docker exec scion1-25 scion-bat http://16-ffaa:1:25,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion1-26 to scion1-26" {
    run docker exec scion1-26 scion-bat http://16-ffaa:1:26,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion1-27 to scion1-27" {
    run docker exec scion1-27 scion-bat http://16-ffaa:1:27,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
