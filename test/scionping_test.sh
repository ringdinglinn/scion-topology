#!/usr/bin/env bats

@test "scion11 can scion-ping scion12" {
  run docker exec monitor scionctl scionping start scion11 scion12 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion11 can scion-ping scion13" {
  run docker exec monitor scionctl scionping start scion11 scion13 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion11 can scion-ping scion14" {
  run docker exec monitor scionctl scionping start scion11 scion14 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion11 can scion-ping scion15" {
  run docker exec monitor scionctl scionping start scion11 scion15 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion11 can scion-ping scion21" {
  run docker exec monitor scionctl scionping start scion11 scion21 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion11 can scion-ping scion22" {
  run docker exec monitor scionctl scionping start scion11 scion22 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion11 can scion-ping scion23" {
  run docker exec monitor scionctl scionping start scion11 scion23 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion11 can scion-ping scion24" {
  run docker exec monitor scionctl scionping start scion11 scion24 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion11 can scion-ping scion25" {
  run docker exec monitor scionctl scionping start scion11 scion25 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion11 can scion-ping scion31" {
  run docker exec monitor scionctl scionping start scion11 scion31 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion11 can scion-ping scion32" {
  run docker exec monitor scionctl scionping start scion11 scion32 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion11 can scion-ping scion33" {
  run docker exec monitor scionctl scionping start scion11 scion33 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion11 can scion-ping scion34" {
  run docker exec monitor scionctl scionping start scion11 scion34 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion11 can scion-ping scion35" {
  run docker exec monitor scionctl scionping start scion11 scion35 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion11 can scion-ping scion41" {
  run docker exec monitor scionctl scionping start scion11 scion41 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion11 can scion-ping scion42" {
  run docker exec monitor scionctl scionping start scion11 scion42 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion11 can scion-ping scion43" {
  run docker exec monitor scionctl scionping start scion11 scion43 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion11 can scion-ping scion44" {
  run docker exec monitor scionctl scionping start scion11 scion44 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion11 can scion-ping scion45" {
  run docker exec monitor scionctl scionping start scion11 scion45 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion12 can scion-ping scion11" {
  run docker exec monitor scionctl scionping start scion12 scion11 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion12 can scion-ping scion13" {
  run docker exec monitor scionctl scionping start scion12 scion13 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion12 can scion-ping scion14" {
  run docker exec monitor scionctl scionping start scion12 scion14 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion12 can scion-ping scion15" {
  run docker exec monitor scionctl scionping start scion12 scion15 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion12 can scion-ping scion21" {
  run docker exec monitor scionctl scionping start scion12 scion21 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion12 can scion-ping scion22" {
  run docker exec monitor scionctl scionping start scion12 scion22 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion12 can scion-ping scion23" {
  run docker exec monitor scionctl scionping start scion12 scion23 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion12 can scion-ping scion24" {
  run docker exec monitor scionctl scionping start scion12 scion24 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion12 can scion-ping scion25" {
  run docker exec monitor scionctl scionping start scion12 scion25 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion12 can scion-ping scion31" {
  run docker exec monitor scionctl scionping start scion12 scion31 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion12 can scion-ping scion32" {
  run docker exec monitor scionctl scionping start scion12 scion32 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion12 can scion-ping scion33" {
  run docker exec monitor scionctl scionping start scion12 scion33 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion12 can scion-ping scion34" {
  run docker exec monitor scionctl scionping start scion12 scion34 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion12 can scion-ping scion35" {
  run docker exec monitor scionctl scionping start scion12 scion35 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion12 can scion-ping scion41" {
  run docker exec monitor scionctl scionping start scion12 scion41 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion12 can scion-ping scion42" {
  run docker exec monitor scionctl scionping start scion12 scion42 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion12 can scion-ping scion43" {
  run docker exec monitor scionctl scionping start scion12 scion43 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion12 can scion-ping scion44" {
  run docker exec monitor scionctl scionping start scion12 scion44 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion12 can scion-ping scion45" {
  run docker exec monitor scionctl scionping start scion12 scion45 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion13 can scion-ping scion11" {
  run docker exec monitor scionctl scionping start scion13 scion11 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion13 can scion-ping scion12" {
  run docker exec monitor scionctl scionping start scion13 scion12 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion13 can scion-ping scion14" {
  run docker exec monitor scionctl scionping start scion13 scion14 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion13 can scion-ping scion15" {
  run docker exec monitor scionctl scionping start scion13 scion15 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion13 can scion-ping scion21" {
  run docker exec monitor scionctl scionping start scion13 scion21 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion13 can scion-ping scion22" {
  run docker exec monitor scionctl scionping start scion13 scion22 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion13 can scion-ping scion23" {
  run docker exec monitor scionctl scionping start scion13 scion23 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion13 can scion-ping scion24" {
  run docker exec monitor scionctl scionping start scion13 scion24 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion13 can scion-ping scion25" {
  run docker exec monitor scionctl scionping start scion13 scion25 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion13 can scion-ping scion31" {
  run docker exec monitor scionctl scionping start scion13 scion31 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion13 can scion-ping scion32" {
  run docker exec monitor scionctl scionping start scion13 scion32 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion13 can scion-ping scion33" {
  run docker exec monitor scionctl scionping start scion13 scion33 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion13 can scion-ping scion34" {
  run docker exec monitor scionctl scionping start scion13 scion34 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion13 can scion-ping scion35" {
  run docker exec monitor scionctl scionping start scion13 scion35 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion13 can scion-ping scion41" {
  run docker exec monitor scionctl scionping start scion13 scion41 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion13 can scion-ping scion42" {
  run docker exec monitor scionctl scionping start scion13 scion42 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion13 can scion-ping scion43" {
  run docker exec monitor scionctl scionping start scion13 scion43 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion13 can scion-ping scion44" {
  run docker exec monitor scionctl scionping start scion13 scion44 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion13 can scion-ping scion45" {
  run docker exec monitor scionctl scionping start scion13 scion45 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion14 can scion-ping scion11" {
  run docker exec monitor scionctl scionping start scion14 scion11 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion14 can scion-ping scion12" {
  run docker exec monitor scionctl scionping start scion14 scion12 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion14 can scion-ping scion13" {
  run docker exec monitor scionctl scionping start scion14 scion13 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion14 can scion-ping scion15" {
  run docker exec monitor scionctl scionping start scion14 scion15 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion14 can scion-ping scion21" {
  run docker exec monitor scionctl scionping start scion14 scion21 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion14 can scion-ping scion22" {
  run docker exec monitor scionctl scionping start scion14 scion22 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion14 can scion-ping scion23" {
  run docker exec monitor scionctl scionping start scion14 scion23 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion14 can scion-ping scion24" {
  run docker exec monitor scionctl scionping start scion14 scion24 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion14 can scion-ping scion25" {
  run docker exec monitor scionctl scionping start scion14 scion25 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion14 can scion-ping scion31" {
  run docker exec monitor scionctl scionping start scion14 scion31 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion14 can scion-ping scion32" {
  run docker exec monitor scionctl scionping start scion14 scion32 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion14 can scion-ping scion33" {
  run docker exec monitor scionctl scionping start scion14 scion33 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion14 can scion-ping scion34" {
  run docker exec monitor scionctl scionping start scion14 scion34 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion14 can scion-ping scion35" {
  run docker exec monitor scionctl scionping start scion14 scion35 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion14 can scion-ping scion41" {
  run docker exec monitor scionctl scionping start scion14 scion41 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion14 can scion-ping scion42" {
  run docker exec monitor scionctl scionping start scion14 scion42 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion14 can scion-ping scion43" {
  run docker exec monitor scionctl scionping start scion14 scion43 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion14 can scion-ping scion44" {
  run docker exec monitor scionctl scionping start scion14 scion44 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion14 can scion-ping scion45" {
  run docker exec monitor scionctl scionping start scion14 scion45 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion15 can scion-ping scion11" {
  run docker exec monitor scionctl scionping start scion15 scion11 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion15 can scion-ping scion12" {
  run docker exec monitor scionctl scionping start scion15 scion12 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion15 can scion-ping scion13" {
  run docker exec monitor scionctl scionping start scion15 scion13 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion15 can scion-ping scion14" {
  run docker exec monitor scionctl scionping start scion15 scion14 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion15 can scion-ping scion21" {
  run docker exec monitor scionctl scionping start scion15 scion21 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion15 can scion-ping scion22" {
  run docker exec monitor scionctl scionping start scion15 scion22 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion15 can scion-ping scion23" {
  run docker exec monitor scionctl scionping start scion15 scion23 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion15 can scion-ping scion24" {
  run docker exec monitor scionctl scionping start scion15 scion24 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion15 can scion-ping scion25" {
  run docker exec monitor scionctl scionping start scion15 scion25 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion15 can scion-ping scion31" {
  run docker exec monitor scionctl scionping start scion15 scion31 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion15 can scion-ping scion32" {
  run docker exec monitor scionctl scionping start scion15 scion32 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion15 can scion-ping scion33" {
  run docker exec monitor scionctl scionping start scion15 scion33 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion15 can scion-ping scion34" {
  run docker exec monitor scionctl scionping start scion15 scion34 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion15 can scion-ping scion35" {
  run docker exec monitor scionctl scionping start scion15 scion35 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion15 can scion-ping scion41" {
  run docker exec monitor scionctl scionping start scion15 scion41 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion15 can scion-ping scion42" {
  run docker exec monitor scionctl scionping start scion15 scion42 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion15 can scion-ping scion43" {
  run docker exec monitor scionctl scionping start scion15 scion43 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion15 can scion-ping scion44" {
  run docker exec monitor scionctl scionping start scion15 scion44 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion15 can scion-ping scion45" {
  run docker exec monitor scionctl scionping start scion15 scion45 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion21 can scion-ping scion11" {
  run docker exec monitor scionctl scionping start scion21 scion11 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion21 can scion-ping scion12" {
  run docker exec monitor scionctl scionping start scion21 scion12 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion21 can scion-ping scion13" {
  run docker exec monitor scionctl scionping start scion21 scion13 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion21 can scion-ping scion14" {
  run docker exec monitor scionctl scionping start scion21 scion14 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion21 can scion-ping scion15" {
  run docker exec monitor scionctl scionping start scion21 scion15 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion21 can scion-ping scion22" {
  run docker exec monitor scionctl scionping start scion21 scion22 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion21 can scion-ping scion23" {
  run docker exec monitor scionctl scionping start scion21 scion23 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion21 can scion-ping scion24" {
  run docker exec monitor scionctl scionping start scion21 scion24 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion21 can scion-ping scion25" {
  run docker exec monitor scionctl scionping start scion21 scion25 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion21 can scion-ping scion31" {
  run docker exec monitor scionctl scionping start scion21 scion31 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion21 can scion-ping scion32" {
  run docker exec monitor scionctl scionping start scion21 scion32 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion21 can scion-ping scion33" {
  run docker exec monitor scionctl scionping start scion21 scion33 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion21 can scion-ping scion34" {
  run docker exec monitor scionctl scionping start scion21 scion34 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion21 can scion-ping scion35" {
  run docker exec monitor scionctl scionping start scion21 scion35 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion21 can scion-ping scion41" {
  run docker exec monitor scionctl scionping start scion21 scion41 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion21 can scion-ping scion42" {
  run docker exec monitor scionctl scionping start scion21 scion42 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion21 can scion-ping scion43" {
  run docker exec monitor scionctl scionping start scion21 scion43 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion21 can scion-ping scion44" {
  run docker exec monitor scionctl scionping start scion21 scion44 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion21 can scion-ping scion45" {
  run docker exec monitor scionctl scionping start scion21 scion45 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion22 can scion-ping scion11" {
  run docker exec monitor scionctl scionping start scion22 scion11 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion22 can scion-ping scion12" {
  run docker exec monitor scionctl scionping start scion22 scion12 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion22 can scion-ping scion13" {
  run docker exec monitor scionctl scionping start scion22 scion13 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion22 can scion-ping scion14" {
  run docker exec monitor scionctl scionping start scion22 scion14 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion22 can scion-ping scion15" {
  run docker exec monitor scionctl scionping start scion22 scion15 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion22 can scion-ping scion21" {
  run docker exec monitor scionctl scionping start scion22 scion21 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion22 can scion-ping scion23" {
  run docker exec monitor scionctl scionping start scion22 scion23 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion22 can scion-ping scion24" {
  run docker exec monitor scionctl scionping start scion22 scion24 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion22 can scion-ping scion25" {
  run docker exec monitor scionctl scionping start scion22 scion25 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion22 can scion-ping scion31" {
  run docker exec monitor scionctl scionping start scion22 scion31 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion22 can scion-ping scion32" {
  run docker exec monitor scionctl scionping start scion22 scion32 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion22 can scion-ping scion33" {
  run docker exec monitor scionctl scionping start scion22 scion33 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion22 can scion-ping scion34" {
  run docker exec monitor scionctl scionping start scion22 scion34 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion22 can scion-ping scion35" {
  run docker exec monitor scionctl scionping start scion22 scion35 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion22 can scion-ping scion41" {
  run docker exec monitor scionctl scionping start scion22 scion41 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion22 can scion-ping scion42" {
  run docker exec monitor scionctl scionping start scion22 scion42 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion22 can scion-ping scion43" {
  run docker exec monitor scionctl scionping start scion22 scion43 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion22 can scion-ping scion44" {
  run docker exec monitor scionctl scionping start scion22 scion44 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion22 can scion-ping scion45" {
  run docker exec monitor scionctl scionping start scion22 scion45 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion23 can scion-ping scion11" {
  run docker exec monitor scionctl scionping start scion23 scion11 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion23 can scion-ping scion12" {
  run docker exec monitor scionctl scionping start scion23 scion12 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion23 can scion-ping scion13" {
  run docker exec monitor scionctl scionping start scion23 scion13 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion23 can scion-ping scion14" {
  run docker exec monitor scionctl scionping start scion23 scion14 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion23 can scion-ping scion15" {
  run docker exec monitor scionctl scionping start scion23 scion15 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion23 can scion-ping scion21" {
  run docker exec monitor scionctl scionping start scion23 scion21 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion23 can scion-ping scion22" {
  run docker exec monitor scionctl scionping start scion23 scion22 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion23 can scion-ping scion24" {
  run docker exec monitor scionctl scionping start scion23 scion24 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion23 can scion-ping scion25" {
  run docker exec monitor scionctl scionping start scion23 scion25 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion23 can scion-ping scion31" {
  run docker exec monitor scionctl scionping start scion23 scion31 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion23 can scion-ping scion32" {
  run docker exec monitor scionctl scionping start scion23 scion32 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion23 can scion-ping scion33" {
  run docker exec monitor scionctl scionping start scion23 scion33 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion23 can scion-ping scion34" {
  run docker exec monitor scionctl scionping start scion23 scion34 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion23 can scion-ping scion35" {
  run docker exec monitor scionctl scionping start scion23 scion35 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion23 can scion-ping scion41" {
  run docker exec monitor scionctl scionping start scion23 scion41 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion23 can scion-ping scion42" {
  run docker exec monitor scionctl scionping start scion23 scion42 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion23 can scion-ping scion43" {
  run docker exec monitor scionctl scionping start scion23 scion43 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion23 can scion-ping scion44" {
  run docker exec monitor scionctl scionping start scion23 scion44 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion23 can scion-ping scion45" {
  run docker exec monitor scionctl scionping start scion23 scion45 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion24 can scion-ping scion11" {
  run docker exec monitor scionctl scionping start scion24 scion11 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion24 can scion-ping scion12" {
  run docker exec monitor scionctl scionping start scion24 scion12 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion24 can scion-ping scion13" {
  run docker exec monitor scionctl scionping start scion24 scion13 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion24 can scion-ping scion14" {
  run docker exec monitor scionctl scionping start scion24 scion14 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion24 can scion-ping scion15" {
  run docker exec monitor scionctl scionping start scion24 scion15 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion24 can scion-ping scion21" {
  run docker exec monitor scionctl scionping start scion24 scion21 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion24 can scion-ping scion22" {
  run docker exec monitor scionctl scionping start scion24 scion22 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion24 can scion-ping scion23" {
  run docker exec monitor scionctl scionping start scion24 scion23 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion24 can scion-ping scion25" {
  run docker exec monitor scionctl scionping start scion24 scion25 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion24 can scion-ping scion31" {
  run docker exec monitor scionctl scionping start scion24 scion31 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion24 can scion-ping scion32" {
  run docker exec monitor scionctl scionping start scion24 scion32 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion24 can scion-ping scion33" {
  run docker exec monitor scionctl scionping start scion24 scion33 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion24 can scion-ping scion34" {
  run docker exec monitor scionctl scionping start scion24 scion34 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion24 can scion-ping scion35" {
  run docker exec monitor scionctl scionping start scion24 scion35 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion24 can scion-ping scion41" {
  run docker exec monitor scionctl scionping start scion24 scion41 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion24 can scion-ping scion42" {
  run docker exec monitor scionctl scionping start scion24 scion42 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion24 can scion-ping scion43" {
  run docker exec monitor scionctl scionping start scion24 scion43 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion24 can scion-ping scion44" {
  run docker exec monitor scionctl scionping start scion24 scion44 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion24 can scion-ping scion45" {
  run docker exec monitor scionctl scionping start scion24 scion45 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion25 can scion-ping scion11" {
  run docker exec monitor scionctl scionping start scion25 scion11 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion25 can scion-ping scion12" {
  run docker exec monitor scionctl scionping start scion25 scion12 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion25 can scion-ping scion13" {
  run docker exec monitor scionctl scionping start scion25 scion13 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion25 can scion-ping scion14" {
  run docker exec monitor scionctl scionping start scion25 scion14 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion25 can scion-ping scion15" {
  run docker exec monitor scionctl scionping start scion25 scion15 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion25 can scion-ping scion21" {
  run docker exec monitor scionctl scionping start scion25 scion21 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion25 can scion-ping scion22" {
  run docker exec monitor scionctl scionping start scion25 scion22 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion25 can scion-ping scion23" {
  run docker exec monitor scionctl scionping start scion25 scion23 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion25 can scion-ping scion24" {
  run docker exec monitor scionctl scionping start scion25 scion24 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion25 can scion-ping scion31" {
  run docker exec monitor scionctl scionping start scion25 scion31 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion25 can scion-ping scion32" {
  run docker exec monitor scionctl scionping start scion25 scion32 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion25 can scion-ping scion33" {
  run docker exec monitor scionctl scionping start scion25 scion33 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion25 can scion-ping scion34" {
  run docker exec monitor scionctl scionping start scion25 scion34 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion25 can scion-ping scion35" {
  run docker exec monitor scionctl scionping start scion25 scion35 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion25 can scion-ping scion41" {
  run docker exec monitor scionctl scionping start scion25 scion41 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion25 can scion-ping scion42" {
  run docker exec monitor scionctl scionping start scion25 scion42 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion25 can scion-ping scion43" {
  run docker exec monitor scionctl scionping start scion25 scion43 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion25 can scion-ping scion44" {
  run docker exec monitor scionctl scionping start scion25 scion44 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion25 can scion-ping scion45" {
  run docker exec monitor scionctl scionping start scion25 scion45 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion31 can scion-ping scion11" {
  run docker exec monitor scionctl scionping start scion31 scion11 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion31 can scion-ping scion12" {
  run docker exec monitor scionctl scionping start scion31 scion12 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion31 can scion-ping scion13" {
  run docker exec monitor scionctl scionping start scion31 scion13 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion31 can scion-ping scion14" {
  run docker exec monitor scionctl scionping start scion31 scion14 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion31 can scion-ping scion15" {
  run docker exec monitor scionctl scionping start scion31 scion15 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion31 can scion-ping scion21" {
  run docker exec monitor scionctl scionping start scion31 scion21 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion31 can scion-ping scion22" {
  run docker exec monitor scionctl scionping start scion31 scion22 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion31 can scion-ping scion23" {
  run docker exec monitor scionctl scionping start scion31 scion23 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion31 can scion-ping scion24" {
  run docker exec monitor scionctl scionping start scion31 scion24 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion31 can scion-ping scion25" {
  run docker exec monitor scionctl scionping start scion31 scion25 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion31 can scion-ping scion32" {
  run docker exec monitor scionctl scionping start scion31 scion32 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion31 can scion-ping scion33" {
  run docker exec monitor scionctl scionping start scion31 scion33 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion31 can scion-ping scion34" {
  run docker exec monitor scionctl scionping start scion31 scion34 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion31 can scion-ping scion35" {
  run docker exec monitor scionctl scionping start scion31 scion35 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion31 can scion-ping scion41" {
  run docker exec monitor scionctl scionping start scion31 scion41 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion31 can scion-ping scion42" {
  run docker exec monitor scionctl scionping start scion31 scion42 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion31 can scion-ping scion43" {
  run docker exec monitor scionctl scionping start scion31 scion43 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion31 can scion-ping scion44" {
  run docker exec monitor scionctl scionping start scion31 scion44 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion31 can scion-ping scion45" {
  run docker exec monitor scionctl scionping start scion31 scion45 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion32 can scion-ping scion11" {
  run docker exec monitor scionctl scionping start scion32 scion11 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion32 can scion-ping scion12" {
  run docker exec monitor scionctl scionping start scion32 scion12 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion32 can scion-ping scion13" {
  run docker exec monitor scionctl scionping start scion32 scion13 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion32 can scion-ping scion14" {
  run docker exec monitor scionctl scionping start scion32 scion14 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion32 can scion-ping scion15" {
  run docker exec monitor scionctl scionping start scion32 scion15 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion32 can scion-ping scion21" {
  run docker exec monitor scionctl scionping start scion32 scion21 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion32 can scion-ping scion22" {
  run docker exec monitor scionctl scionping start scion32 scion22 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion32 can scion-ping scion23" {
  run docker exec monitor scionctl scionping start scion32 scion23 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion32 can scion-ping scion24" {
  run docker exec monitor scionctl scionping start scion32 scion24 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion32 can scion-ping scion25" {
  run docker exec monitor scionctl scionping start scion32 scion25 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion32 can scion-ping scion31" {
  run docker exec monitor scionctl scionping start scion32 scion31 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion32 can scion-ping scion33" {
  run docker exec monitor scionctl scionping start scion32 scion33 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion32 can scion-ping scion34" {
  run docker exec monitor scionctl scionping start scion32 scion34 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion32 can scion-ping scion35" {
  run docker exec monitor scionctl scionping start scion32 scion35 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion32 can scion-ping scion41" {
  run docker exec monitor scionctl scionping start scion32 scion41 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion32 can scion-ping scion42" {
  run docker exec monitor scionctl scionping start scion32 scion42 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion32 can scion-ping scion43" {
  run docker exec monitor scionctl scionping start scion32 scion43 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion32 can scion-ping scion44" {
  run docker exec monitor scionctl scionping start scion32 scion44 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion32 can scion-ping scion45" {
  run docker exec monitor scionctl scionping start scion32 scion45 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion33 can scion-ping scion11" {
  run docker exec monitor scionctl scionping start scion33 scion11 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion33 can scion-ping scion12" {
  run docker exec monitor scionctl scionping start scion33 scion12 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion33 can scion-ping scion13" {
  run docker exec monitor scionctl scionping start scion33 scion13 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion33 can scion-ping scion14" {
  run docker exec monitor scionctl scionping start scion33 scion14 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion33 can scion-ping scion15" {
  run docker exec monitor scionctl scionping start scion33 scion15 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion33 can scion-ping scion21" {
  run docker exec monitor scionctl scionping start scion33 scion21 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion33 can scion-ping scion22" {
  run docker exec monitor scionctl scionping start scion33 scion22 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion33 can scion-ping scion23" {
  run docker exec monitor scionctl scionping start scion33 scion23 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion33 can scion-ping scion24" {
  run docker exec monitor scionctl scionping start scion33 scion24 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion33 can scion-ping scion25" {
  run docker exec monitor scionctl scionping start scion33 scion25 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion33 can scion-ping scion31" {
  run docker exec monitor scionctl scionping start scion33 scion31 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion33 can scion-ping scion32" {
  run docker exec monitor scionctl scionping start scion33 scion32 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion33 can scion-ping scion34" {
  run docker exec monitor scionctl scionping start scion33 scion34 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion33 can scion-ping scion35" {
  run docker exec monitor scionctl scionping start scion33 scion35 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion33 can scion-ping scion41" {
  run docker exec monitor scionctl scionping start scion33 scion41 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion33 can scion-ping scion42" {
  run docker exec monitor scionctl scionping start scion33 scion42 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion33 can scion-ping scion43" {
  run docker exec monitor scionctl scionping start scion33 scion43 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion33 can scion-ping scion44" {
  run docker exec monitor scionctl scionping start scion33 scion44 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion33 can scion-ping scion45" {
  run docker exec monitor scionctl scionping start scion33 scion45 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion34 can scion-ping scion11" {
  run docker exec monitor scionctl scionping start scion34 scion11 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion34 can scion-ping scion12" {
  run docker exec monitor scionctl scionping start scion34 scion12 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion34 can scion-ping scion13" {
  run docker exec monitor scionctl scionping start scion34 scion13 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion34 can scion-ping scion14" {
  run docker exec monitor scionctl scionping start scion34 scion14 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion34 can scion-ping scion15" {
  run docker exec monitor scionctl scionping start scion34 scion15 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion34 can scion-ping scion21" {
  run docker exec monitor scionctl scionping start scion34 scion21 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion34 can scion-ping scion22" {
  run docker exec monitor scionctl scionping start scion34 scion22 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion34 can scion-ping scion23" {
  run docker exec monitor scionctl scionping start scion34 scion23 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion34 can scion-ping scion24" {
  run docker exec monitor scionctl scionping start scion34 scion24 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion34 can scion-ping scion25" {
  run docker exec monitor scionctl scionping start scion34 scion25 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion34 can scion-ping scion31" {
  run docker exec monitor scionctl scionping start scion34 scion31 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion34 can scion-ping scion32" {
  run docker exec monitor scionctl scionping start scion34 scion32 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion34 can scion-ping scion33" {
  run docker exec monitor scionctl scionping start scion34 scion33 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion34 can scion-ping scion35" {
  run docker exec monitor scionctl scionping start scion34 scion35 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion34 can scion-ping scion41" {
  run docker exec monitor scionctl scionping start scion34 scion41 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion34 can scion-ping scion42" {
  run docker exec monitor scionctl scionping start scion34 scion42 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion34 can scion-ping scion43" {
  run docker exec monitor scionctl scionping start scion34 scion43 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion34 can scion-ping scion44" {
  run docker exec monitor scionctl scionping start scion34 scion44 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion34 can scion-ping scion45" {
  run docker exec monitor scionctl scionping start scion34 scion45 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion35 can scion-ping scion11" {
  run docker exec monitor scionctl scionping start scion35 scion11 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion35 can scion-ping scion12" {
  run docker exec monitor scionctl scionping start scion35 scion12 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion35 can scion-ping scion13" {
  run docker exec monitor scionctl scionping start scion35 scion13 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion35 can scion-ping scion14" {
  run docker exec monitor scionctl scionping start scion35 scion14 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion35 can scion-ping scion15" {
  run docker exec monitor scionctl scionping start scion35 scion15 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion35 can scion-ping scion21" {
  run docker exec monitor scionctl scionping start scion35 scion21 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion35 can scion-ping scion22" {
  run docker exec monitor scionctl scionping start scion35 scion22 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion35 can scion-ping scion23" {
  run docker exec monitor scionctl scionping start scion35 scion23 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion35 can scion-ping scion24" {
  run docker exec monitor scionctl scionping start scion35 scion24 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion35 can scion-ping scion25" {
  run docker exec monitor scionctl scionping start scion35 scion25 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion35 can scion-ping scion31" {
  run docker exec monitor scionctl scionping start scion35 scion31 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion35 can scion-ping scion32" {
  run docker exec monitor scionctl scionping start scion35 scion32 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion35 can scion-ping scion33" {
  run docker exec monitor scionctl scionping start scion35 scion33 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion35 can scion-ping scion34" {
  run docker exec monitor scionctl scionping start scion35 scion34 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion35 can scion-ping scion41" {
  run docker exec monitor scionctl scionping start scion35 scion41 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion35 can scion-ping scion42" {
  run docker exec monitor scionctl scionping start scion35 scion42 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion35 can scion-ping scion43" {
  run docker exec monitor scionctl scionping start scion35 scion43 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion35 can scion-ping scion44" {
  run docker exec monitor scionctl scionping start scion35 scion44 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion35 can scion-ping scion45" {
  run docker exec monitor scionctl scionping start scion35 scion45 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion41 can scion-ping scion11" {
  run docker exec monitor scionctl scionping start scion41 scion11 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion41 can scion-ping scion12" {
  run docker exec monitor scionctl scionping start scion41 scion12 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion41 can scion-ping scion13" {
  run docker exec monitor scionctl scionping start scion41 scion13 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion41 can scion-ping scion14" {
  run docker exec monitor scionctl scionping start scion41 scion14 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion41 can scion-ping scion15" {
  run docker exec monitor scionctl scionping start scion41 scion15 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion41 can scion-ping scion21" {
  run docker exec monitor scionctl scionping start scion41 scion21 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion41 can scion-ping scion22" {
  run docker exec monitor scionctl scionping start scion41 scion22 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion41 can scion-ping scion23" {
  run docker exec monitor scionctl scionping start scion41 scion23 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion41 can scion-ping scion24" {
  run docker exec monitor scionctl scionping start scion41 scion24 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion41 can scion-ping scion25" {
  run docker exec monitor scionctl scionping start scion41 scion25 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion41 can scion-ping scion31" {
  run docker exec monitor scionctl scionping start scion41 scion31 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion41 can scion-ping scion32" {
  run docker exec monitor scionctl scionping start scion41 scion32 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion41 can scion-ping scion33" {
  run docker exec monitor scionctl scionping start scion41 scion33 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion41 can scion-ping scion34" {
  run docker exec monitor scionctl scionping start scion41 scion34 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion41 can scion-ping scion35" {
  run docker exec monitor scionctl scionping start scion41 scion35 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion41 can scion-ping scion42" {
  run docker exec monitor scionctl scionping start scion41 scion42 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion41 can scion-ping scion43" {
  run docker exec monitor scionctl scionping start scion41 scion43 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion41 can scion-ping scion44" {
  run docker exec monitor scionctl scionping start scion41 scion44 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion41 can scion-ping scion45" {
  run docker exec monitor scionctl scionping start scion41 scion45 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion42 can scion-ping scion11" {
  run docker exec monitor scionctl scionping start scion42 scion11 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion42 can scion-ping scion12" {
  run docker exec monitor scionctl scionping start scion42 scion12 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion42 can scion-ping scion13" {
  run docker exec monitor scionctl scionping start scion42 scion13 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion42 can scion-ping scion14" {
  run docker exec monitor scionctl scionping start scion42 scion14 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion42 can scion-ping scion15" {
  run docker exec monitor scionctl scionping start scion42 scion15 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion42 can scion-ping scion21" {
  run docker exec monitor scionctl scionping start scion42 scion21 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion42 can scion-ping scion22" {
  run docker exec monitor scionctl scionping start scion42 scion22 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion42 can scion-ping scion23" {
  run docker exec monitor scionctl scionping start scion42 scion23 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion42 can scion-ping scion24" {
  run docker exec monitor scionctl scionping start scion42 scion24 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion42 can scion-ping scion25" {
  run docker exec monitor scionctl scionping start scion42 scion25 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion42 can scion-ping scion31" {
  run docker exec monitor scionctl scionping start scion42 scion31 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion42 can scion-ping scion32" {
  run docker exec monitor scionctl scionping start scion42 scion32 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion42 can scion-ping scion33" {
  run docker exec monitor scionctl scionping start scion42 scion33 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion42 can scion-ping scion34" {
  run docker exec monitor scionctl scionping start scion42 scion34 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion42 can scion-ping scion35" {
  run docker exec monitor scionctl scionping start scion42 scion35 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion42 can scion-ping scion41" {
  run docker exec monitor scionctl scionping start scion42 scion41 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion42 can scion-ping scion43" {
  run docker exec monitor scionctl scionping start scion42 scion43 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion42 can scion-ping scion44" {
  run docker exec monitor scionctl scionping start scion42 scion44 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion42 can scion-ping scion45" {
  run docker exec monitor scionctl scionping start scion42 scion45 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion43 can scion-ping scion11" {
  run docker exec monitor scionctl scionping start scion43 scion11 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion43 can scion-ping scion12" {
  run docker exec monitor scionctl scionping start scion43 scion12 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion43 can scion-ping scion13" {
  run docker exec monitor scionctl scionping start scion43 scion13 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion43 can scion-ping scion14" {
  run docker exec monitor scionctl scionping start scion43 scion14 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion43 can scion-ping scion15" {
  run docker exec monitor scionctl scionping start scion43 scion15 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion43 can scion-ping scion21" {
  run docker exec monitor scionctl scionping start scion43 scion21 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion43 can scion-ping scion22" {
  run docker exec monitor scionctl scionping start scion43 scion22 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion43 can scion-ping scion23" {
  run docker exec monitor scionctl scionping start scion43 scion23 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion43 can scion-ping scion24" {
  run docker exec monitor scionctl scionping start scion43 scion24 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion43 can scion-ping scion25" {
  run docker exec monitor scionctl scionping start scion43 scion25 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion43 can scion-ping scion31" {
  run docker exec monitor scionctl scionping start scion43 scion31 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion43 can scion-ping scion32" {
  run docker exec monitor scionctl scionping start scion43 scion32 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion43 can scion-ping scion33" {
  run docker exec monitor scionctl scionping start scion43 scion33 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion43 can scion-ping scion34" {
  run docker exec monitor scionctl scionping start scion43 scion34 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion43 can scion-ping scion35" {
  run docker exec monitor scionctl scionping start scion43 scion35 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion43 can scion-ping scion41" {
  run docker exec monitor scionctl scionping start scion43 scion41 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion43 can scion-ping scion42" {
  run docker exec monitor scionctl scionping start scion43 scion42 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion43 can scion-ping scion44" {
  run docker exec monitor scionctl scionping start scion43 scion44 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion43 can scion-ping scion45" {
  run docker exec monitor scionctl scionping start scion43 scion45 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion44 can scion-ping scion11" {
  run docker exec monitor scionctl scionping start scion44 scion11 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion44 can scion-ping scion12" {
  run docker exec monitor scionctl scionping start scion44 scion12 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion44 can scion-ping scion13" {
  run docker exec monitor scionctl scionping start scion44 scion13 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion44 can scion-ping scion14" {
  run docker exec monitor scionctl scionping start scion44 scion14 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion44 can scion-ping scion15" {
  run docker exec monitor scionctl scionping start scion44 scion15 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion44 can scion-ping scion21" {
  run docker exec monitor scionctl scionping start scion44 scion21 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion44 can scion-ping scion22" {
  run docker exec monitor scionctl scionping start scion44 scion22 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion44 can scion-ping scion23" {
  run docker exec monitor scionctl scionping start scion44 scion23 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion44 can scion-ping scion24" {
  run docker exec monitor scionctl scionping start scion44 scion24 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion44 can scion-ping scion25" {
  run docker exec monitor scionctl scionping start scion44 scion25 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion44 can scion-ping scion31" {
  run docker exec monitor scionctl scionping start scion44 scion31 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion44 can scion-ping scion32" {
  run docker exec monitor scionctl scionping start scion44 scion32 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion44 can scion-ping scion33" {
  run docker exec monitor scionctl scionping start scion44 scion33 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion44 can scion-ping scion34" {
  run docker exec monitor scionctl scionping start scion44 scion34 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion44 can scion-ping scion35" {
  run docker exec monitor scionctl scionping start scion44 scion35 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion44 can scion-ping scion41" {
  run docker exec monitor scionctl scionping start scion44 scion41 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion44 can scion-ping scion42" {
  run docker exec monitor scionctl scionping start scion44 scion42 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion44 can scion-ping scion43" {
  run docker exec monitor scionctl scionping start scion44 scion43 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion44 can scion-ping scion45" {
  run docker exec monitor scionctl scionping start scion44 scion45 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion45 can scion-ping scion11" {
  run docker exec monitor scionctl scionping start scion45 scion11 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion45 can scion-ping scion12" {
  run docker exec monitor scionctl scionping start scion45 scion12 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion45 can scion-ping scion13" {
  run docker exec monitor scionctl scionping start scion45 scion13 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion45 can scion-ping scion14" {
  run docker exec monitor scionctl scionping start scion45 scion14 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion45 can scion-ping scion15" {
  run docker exec monitor scionctl scionping start scion45 scion15 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion45 can scion-ping scion21" {
  run docker exec monitor scionctl scionping start scion45 scion21 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion45 can scion-ping scion22" {
  run docker exec monitor scionctl scionping start scion45 scion22 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion45 can scion-ping scion23" {
  run docker exec monitor scionctl scionping start scion45 scion23 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion45 can scion-ping scion24" {
  run docker exec monitor scionctl scionping start scion45 scion24 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion45 can scion-ping scion25" {
  run docker exec monitor scionctl scionping start scion45 scion25 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion45 can scion-ping scion31" {
  run docker exec monitor scionctl scionping start scion45 scion31 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion45 can scion-ping scion32" {
  run docker exec monitor scionctl scionping start scion45 scion32 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion45 can scion-ping scion33" {
  run docker exec monitor scionctl scionping start scion45 scion33 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion45 can scion-ping scion34" {
  run docker exec monitor scionctl scionping start scion45 scion34 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion45 can scion-ping scion35" {
  run docker exec monitor scionctl scionping start scion45 scion35 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion45 can scion-ping scion41" {
  run docker exec monitor scionctl scionping start scion45 scion41 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion45 can scion-ping scion42" {
  run docker exec monitor scionctl scionping start scion45 scion42 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion45 can scion-ping scion43" {
  run docker exec monitor scionctl scionping start scion45 scion43 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

@test "scion45 can scion-ping scion44" {
  run docker exec monitor scionctl scionping start scion45 scion44 --count 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]
}

