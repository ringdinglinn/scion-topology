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
@test "bat request from scion4-1 to scion4-2" {
    run docker exec scion4-1 scion-bat http://19-ffaa:4:2,127.0.0.1:32765/hello
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
@test "bat request from scion3-1 to scion4-1" {
    run docker exec scion3-1 scion-bat http://19-ffaa:4:1,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion3-2 to scion4-2" {
    run docker exec scion3-2 scion-bat http://19-ffaa:4:2,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion3-3 to scion4-3" {
    run docker exec scion3-3 scion-bat http://19-ffaa:4:3,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion3-4 to scion4-4" {
    run docker exec scion3-4 scion-bat http://19-ffaa:4:4,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion3-5 to scion4-5" {
    run docker exec scion3-5 scion-bat http://19-ffaa:4:5,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion3-6 to scion4-6" {
    run docker exec scion3-6 scion-bat http://19-ffaa:4:6,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion3-7 to scion4-7" {
    run docker exec scion3-7 scion-bat http://19-ffaa:4:7,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion3-8 to scion4-8" {
    run docker exec scion3-8 scion-bat http://19-ffaa:4:8,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion4-1 to scion1-1" {
    run docker exec scion4-1 scion-bat http://16-ffaa:1:1,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion4-2 to scion1-2" {
    run docker exec scion4-2 scion-bat http://16-ffaa:1:2,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion4-3 to scion1-3" {
    run docker exec scion4-3 scion-bat http://16-ffaa:1:3,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion4-4 to scion1-4" {
    run docker exec scion4-4 scion-bat http://16-ffaa:1:4,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion4-5 to scion1-5" {
    run docker exec scion4-5 scion-bat http://16-ffaa:1:5,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion4-6 to scion1-6" {
    run docker exec scion4-6 scion-bat http://16-ffaa:1:6,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion4-7 to scion1-7" {
    run docker exec scion4-7 scion-bat http://16-ffaa:1:7,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion4-8 to scion1-8" {
    run docker exec scion4-8 scion-bat http://16-ffaa:1:8,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion4-9 to scion1-9" {
    run docker exec scion4-9 scion-bat http://16-ffaa:1:9,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion4-10 to scion1-10" {
    run docker exec scion4-10 scion-bat http://16-ffaa:1:10,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
