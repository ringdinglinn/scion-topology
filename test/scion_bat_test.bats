#!/usr/bin/env bats
current_node=""

# Minimal intra-ISD
@test "bat request from scion0-1 to scion0-2" {
    run docker exec scion0-1 scion-bat http://15-ffaa:0:2,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
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
@test "bat request from scion3-1 to scion3-2" {
    run docker exec scion3-1 scion-bat http://18-ffaa:3:2,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
# Diagonal ISD-to_ISD
@test "bat request from scion0-1 to scion1-1" {
    run docker exec scion0-1 scion-bat http://16-ffaa:1:1,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion0-2 to scion1-2" {
    run docker exec scion0-2 scion-bat http://16-ffaa:1:2,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion0-3 to scion1-3" {
    run docker exec scion0-3 scion-bat http://16-ffaa:1:3,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion0-4 to scion1-4" {
    run docker exec scion0-4 scion-bat http://16-ffaa:1:4,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion0-5 to scion1-5" {
    run docker exec scion0-5 scion-bat http://16-ffaa:1:5,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion0-6 to scion1-6" {
    run docker exec scion0-6 scion-bat http://16-ffaa:1:6,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion0-7 to scion1-7" {
    run docker exec scion0-7 scion-bat http://16-ffaa:1:7,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion0-8 to scion1-8" {
    run docker exec scion0-8 scion-bat http://16-ffaa:1:8,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion0-9 to scion1-9" {
    run docker exec scion0-9 scion-bat http://16-ffaa:1:9,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion0-10 to scion1-10" {
    run docker exec scion0-10 scion-bat http://16-ffaa:1:10,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion0-11 to scion1-11" {
    run docker exec scion0-11 scion-bat http://16-ffaa:1:11,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion0-12 to scion1-12" {
    run docker exec scion0-12 scion-bat http://16-ffaa:1:12,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion0-13 to scion1-13" {
    run docker exec scion0-13 scion-bat http://16-ffaa:1:13,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion0-14 to scion1-14" {
    run docker exec scion0-14 scion-bat http://16-ffaa:1:14,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion0-15 to scion1-15" {
    run docker exec scion0-15 scion-bat http://16-ffaa:1:15,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
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
@test "bat request from scion1-3 to scion2-3" {
    run docker exec scion1-3 scion-bat http://17-ffaa:2:3,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion1-4 to scion2-4" {
    run docker exec scion1-4 scion-bat http://17-ffaa:2:4,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion1-5 to scion2-5" {
    run docker exec scion1-5 scion-bat http://17-ffaa:2:5,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion1-6 to scion2-6" {
    run docker exec scion1-6 scion-bat http://17-ffaa:2:6,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion1-7 to scion2-7" {
    run docker exec scion1-7 scion-bat http://17-ffaa:2:7,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion2-1 to scion3-1" {
    run docker exec scion2-1 scion-bat http://18-ffaa:3:1,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion2-2 to scion3-2" {
    run docker exec scion2-2 scion-bat http://18-ffaa:3:2,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion2-3 to scion3-3" {
    run docker exec scion2-3 scion-bat http://18-ffaa:3:3,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion2-4 to scion3-4" {
    run docker exec scion2-4 scion-bat http://18-ffaa:3:4,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion2-5 to scion3-5" {
    run docker exec scion2-5 scion-bat http://18-ffaa:3:5,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion2-6 to scion3-6" {
    run docker exec scion2-6 scion-bat http://18-ffaa:3:6,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion2-7 to scion3-7" {
    run docker exec scion2-7 scion-bat http://18-ffaa:3:7,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion3-1 to scion0-1" {
    run docker exec scion3-1 scion-bat http://15-ffaa:0:1,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion3-2 to scion0-2" {
    run docker exec scion3-2 scion-bat http://15-ffaa:0:2,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion3-3 to scion0-3" {
    run docker exec scion3-3 scion-bat http://15-ffaa:0:3,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion3-4 to scion0-4" {
    run docker exec scion3-4 scion-bat http://15-ffaa:0:4,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion3-5 to scion0-5" {
    run docker exec scion3-5 scion-bat http://15-ffaa:0:5,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion3-6 to scion0-6" {
    run docker exec scion3-6 scion-bat http://15-ffaa:0:6,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion3-7 to scion0-7" {
    run docker exec scion3-7 scion-bat http://15-ffaa:0:7,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion3-8 to scion0-8" {
    run docker exec scion3-8 scion-bat http://15-ffaa:0:8,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
