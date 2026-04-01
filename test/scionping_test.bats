#!/usr/bin/env bats
current_node=""

# Minimal intra-ISD
@test "scion1-1 can scion-ping scion1-2" {
	current_node="scion1-1"
	run docker exec monitor scionctl scionping start scion1-1 scion1-2 --count 1
	sleep 1
	[ "$status" -eq 0 ]
	[[ "$output" != *"Error"* ]]
	run docker exec monitor scionctl scionping list scion1-1
	filename=$(echo "$output" | awk -F'|' '/\.log/ {gsub(/ /, "", $3); fname=$3} END {sub(/\.log$/, "", fname); print fname}')
	run docker exec monitor scionctl scionping file scion1-1 $filename
	ping_output="$output"
	packet_loss_line=$(echo "$ping_output" | grep "packet loss")
	packet_loss_value=$(echo "$packet_loss_line" | awk '{print $6}')
	[ "$packet_loss_value" = "0%" ]
}
@test "scion2-1 can scion-ping scion2-2" {
	current_node="scion2-1"
	run docker exec monitor scionctl scionping start scion2-1 scion2-2 --count 1
	sleep 1
	[ "$status" -eq 0 ]
	[[ "$output" != *"Error"* ]]
	run docker exec monitor scionctl scionping list scion2-1
	filename=$(echo "$output" | awk -F'|' '/\.log/ {gsub(/ /, "", $3); fname=$3} END {sub(/\.log$/, "", fname); print fname}')
	run docker exec monitor scionctl scionping file scion2-1 $filename
	ping_output="$output"
	packet_loss_line=$(echo "$ping_output" | grep "packet loss")
	packet_loss_value=$(echo "$packet_loss_line" | awk '{print $6}')
	[ "$packet_loss_value" = "0%" ]
}
# Diagonal ISD-to_ISD
@test "scion1-1 can scion-ping scion2-1" {
	current_node="scion1-1"
	run docker exec monitor scionctl scionping start scion1-1 scion2-1 --count 1
	sleep 1
	[ "$status" -eq 0 ]
	[[ "$output" != *"Error"* ]]
	run docker exec monitor scionctl scionping list scion1-1
	filename=$(echo "$output" | awk -F'|' '/\.log/ {gsub(/ /, "", $3); fname=$3} END {sub(/\.log$/, "", fname); print fname}')
	run docker exec monitor scionctl scionping file scion1-1 $filename
	ping_output="$output"
	packet_loss_line=$(echo "$ping_output" | grep "packet loss")
	packet_loss_value=$(echo "$packet_loss_line" | awk '{print $6}')
	[ "$packet_loss_value" = "0%" ]
}
@test "scion1-2 can scion-ping scion2-2" {
	current_node="scion1-2"
	run docker exec monitor scionctl scionping start scion1-2 scion2-2 --count 1
	sleep 1
	[ "$status" -eq 0 ]
	[[ "$output" != *"Error"* ]]
	run docker exec monitor scionctl scionping list scion1-2
	filename=$(echo "$output" | awk -F'|' '/\.log/ {gsub(/ /, "", $3); fname=$3} END {sub(/\.log$/, "", fname); print fname}')
	run docker exec monitor scionctl scionping file scion1-2 $filename
	ping_output="$output"
	packet_loss_line=$(echo "$ping_output" | grep "packet loss")
	packet_loss_value=$(echo "$packet_loss_line" | awk '{print $6}')
	[ "$packet_loss_value" = "0%" ]
}
@test "scion2-1 can scion-ping scion1-1" {
	current_node="scion2-1"
	run docker exec monitor scionctl scionping start scion2-1 scion1-1 --count 1
	sleep 1
	[ "$status" -eq 0 ]
	[[ "$output" != *"Error"* ]]
	run docker exec monitor scionctl scionping list scion2-1
	filename=$(echo "$output" | awk -F'|' '/\.log/ {gsub(/ /, "", $3); fname=$3} END {sub(/\.log$/, "", fname); print fname}')
	run docker exec monitor scionctl scionping file scion2-1 $filename
	ping_output="$output"
	packet_loss_line=$(echo "$ping_output" | grep "packet loss")
	packet_loss_value=$(echo "$packet_loss_line" | awk '{print $6}')
	[ "$packet_loss_value" = "0%" ]
}
@test "scion2-2 can scion-ping scion1-2" {
	current_node="scion2-2"
	run docker exec monitor scionctl scionping start scion2-2 scion1-2 --count 1
	sleep 1
	[ "$status" -eq 0 ]
	[[ "$output" != *"Error"* ]]
	run docker exec monitor scionctl scionping list scion2-2
	filename=$(echo "$output" | awk -F'|' '/\.log/ {gsub(/ /, "", $3); fname=$3} END {sub(/\.log$/, "", fname); print fname}')
	run docker exec monitor scionctl scionping file scion2-2 $filename
	ping_output="$output"
	packet_loss_line=$(echo "$ping_output" | grep "packet loss")
	packet_loss_value=$(echo "$packet_loss_line" | awk '{print $6}')
	[ "$packet_loss_value" = "0%" ]
}
teardown() {
  docker exec "$current_node" bash -c "rm -rf /var/lib/scion-node-manager/scion-ping-results/*"
}
