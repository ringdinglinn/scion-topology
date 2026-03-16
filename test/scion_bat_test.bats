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
@test "bat request from scion3-1 to scion3-2" {
    run docker exec scion3-1 scion-bat http://18-ffaa:3:2,127.0.0.1:32765/hello
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
@test "bat request from scion1-8 to scion2-8" {
    run docker exec scion1-8 scion-bat http://17-ffaa:2:8,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion1-9 to scion2-9" {
    run docker exec scion1-9 scion-bat http://17-ffaa:2:9,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion1-10 to scion2-10" {
    run docker exec scion1-10 scion-bat http://17-ffaa:2:10,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion1-11 to scion2-11" {
    run docker exec scion1-11 scion-bat http://17-ffaa:2:11,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion1-12 to scion2-12" {
    run docker exec scion1-12 scion-bat http://17-ffaa:2:12,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion1-13 to scion2-13" {
    run docker exec scion1-13 scion-bat http://17-ffaa:2:13,127.0.0.1:32765/hello
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
@test "bat request from scion3-1 to scion1-1" {
    run docker exec scion3-1 scion-bat http://16-ffaa:1:1,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion3-2 to scion1-2" {
    run docker exec scion3-2 scion-bat http://16-ffaa:1:2,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion3-3 to scion1-3" {
    run docker exec scion3-3 scion-bat http://16-ffaa:1:3,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion3-4 to scion1-4" {
    run docker exec scion3-4 scion-bat http://16-ffaa:1:4,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion3-5 to scion1-5" {
    run docker exec scion3-5 scion-bat http://16-ffaa:1:5,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion3-6 to scion1-6" {
    run docker exec scion3-6 scion-bat http://16-ffaa:1:6,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
