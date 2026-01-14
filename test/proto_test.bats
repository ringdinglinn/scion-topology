#!/usr/bin/env bats

@test "scion11 can scion-ping scion12" {
  run docker exec monitor scionctl scionping start scion11 scion13 --count 1
  sleep 1
  [[ "$output" != *"Error"* ]]
  [ "$status" -eq 0 ]

  #check if sent == received or if packet loss == 0%
  run docker exec monitor scionctl scionping list scion11
  filename=$(echo "$output" | awk -F'|' '/\.log/ {gsub(/ /, "", $3); fname=$3} END {sub(/\.log$/, "", fname); print fname}')

  run docker exec monitor scionctl scionping file scion11 $filename
  ping_output="$output"
  packet_loss_line=$(echo "$ping_output" | grep "packet loss")
  packet_loss_value=$(echo "$packet_loss_line" | awk '{print $6}')
  [ "$packet_loss_value" = "0%" ]
}

