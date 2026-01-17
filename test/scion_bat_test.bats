#!/usr/bin/env bats

# Minimal intra-ISD
@test "bat request from scion11 to scion12" {
    run docker exec scion11 scion-bat http://16-ffaa:1:12,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion21 to scion22" {
    run docker exec scion21 scion-bat http://17-ffaa:1:22,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion31 to scion32" {
    run docker exec scion31 scion-bat http://18-ffaa:1:32,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion41 to scion42" {
    run docker exec scion41 scion-bat http://19-ffaa:1:42,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}

# ISD-to-ISD mesh (first node of each ISD to first node of every other ISD)

@test "bat request from scion11 to scion21" {
    run docker exec scion11 scion-bat http://17-ffaa:1:21,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion11 to scion31" {
    run docker exec scion11 scion-bat http://18-ffaa:1:31,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion11 to scion41" {
    run docker exec scion11 scion-bat http://19-ffaa:1:41,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion21 to scion11" {
    run docker exec scion21 scion-bat http://16-ffaa:1:11,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion21 to scion31" {
    run docker exec scion21 scion-bat http://18-ffaa:1:31,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion21 to scion41" {
    run docker exec scion21 scion-bat http://19-ffaa:1:41,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion31 to scion11" {
    run docker exec scion31 scion-bat http://16-ffaa:1:11,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion31 to scion21" {
    run docker exec scion31 scion-bat http://17-ffaa:1:21,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion31 to scion41" {
    run docker exec scion31 scion-bat http://19-ffaa:1:41,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion41 to scion11" {
    run docker exec scion41 scion-bat http://16-ffaa:1:11,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion41 to scion21" {
    run docker exec scion41 scion-bat http://17-ffaa:1:21,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion41 to scion31" {
    run docker exec scion41 scion-bat http://18-ffaa:1:31,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}

# Cross-ISD, cross-AS edge cases (last node of each ISD to last node of another ISD)
@test "bat request from scion15 to scion25" {
    run docker exec scion15 scion-bat http://17-ffaa:1:25,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion25 to scion35" {
    run docker exec scion25 scion-bat http://18-ffaa:1:35,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion35 to scion45" {
    run docker exec scion35 scion-bat http://19-ffaa:1:45,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion45 to scion15" {
    run docker exec scion45 scion-bat http://16-ffaa:1:15,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}

# Diagonal/edge cases
@test "bat request from scion12 to scion23" {
    run docker exec scion12 scion-bat http://17-ffaa:1:23,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion22 to scion33" {
    run docker exec scion22 scion-bat http://18-ffaa:1:33,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion32 to scion43" {
    run docker exec scion32 scion-bat http://19-ffaa:1:43,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion42 to scion13" {
    run docker exec scion42 scion-bat http://16-ffaa:1:13,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}
@test "bat request from scion13 to scion44" {
    run docker exec scion13 scion-bat http://19-ffaa:1:44,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}

@test "bat request from scion23 to scion34" {
    run docker exec scion23 scion-bat http://18-ffaa:1:34,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}

@test "bat request from scion33 to scion14" {
    run docker exec scion33 scion-bat http://16-ffaa:1:14,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}

@test "bat request from scion43 to scion24" {
    run docker exec scion43 scion-bat http://17-ffaa:1:24,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}

@test "bat request from scion11 to scion45 {
    run docker exec scion11 scion-bat http://19-ffaa:1:45,127.0.0.1:32765/hello
    [ "$status" -eq 0 ]
    [[ "$output" == *"Oh, hello!"* ]]
}