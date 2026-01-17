#!/usr/bin/env bats

@test "scion11 can scion-ping scion12" {
  # Generate a new ping log
  run docker exec monitor scionctl scionping start scion11 scion12 --count 1
  sleep 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"Error"* ]]

  # Get the latest ping log filename
  run docker exec monitor scionctl scionping list scion11
  filename=$(echo "$output" | awk -F'|' '/\.log/ {gsub(/ /, "", $3); fname=$3} END {sub(/\.log$/, "", fname); print fname}')

  # Get the ping file output
  run docker exec monitor scionctl scionping file scion11 $filename
  ping_output="$output"

  # Extract the packet loss value
  packet_loss_line=$(echo "$ping_output" | grep "packet loss")
  packet_loss_value=$(echo "$packet_loss_line" | awk '{print $6}')

  # Assert packet loss is 0%
  [ "$packet_loss_value" = "0%" ]
}

