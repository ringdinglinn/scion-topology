#!/usr/bin/env bats


@test "scion32 can ping scion24" {
  run docker exec monitor scionctl scionping start scion32 scion24 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}