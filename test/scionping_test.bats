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
@test "scion3-1 can scion-ping scion3-2" {
	current_node="scion3-1"
	run docker exec monitor scionctl scionping start scion3-1 scion3-2 --count 1
	sleep 1
	[ "$status" -eq 0 ]
	[[ "$output" != *"Error"* ]]
	run docker exec monitor scionctl scionping list scion3-1
	filename=$(echo "$output" | awk -F'|' '/\.log/ {gsub(/ /, "", $3); fname=$3} END {sub(/\.log$/, "", fname); print fname}')
	run docker exec monitor scionctl scionping file scion3-1 $filename
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
@test "scion1-3 can scion-ping scion2-3" {
	current_node="scion1-3"
	run docker exec monitor scionctl scionping start scion1-3 scion2-3 --count 1
	sleep 1
	[ "$status" -eq 0 ]
	[[ "$output" != *"Error"* ]]
	run docker exec monitor scionctl scionping list scion1-3
	filename=$(echo "$output" | awk -F'|' '/\.log/ {gsub(/ /, "", $3); fname=$3} END {sub(/\.log$/, "", fname); print fname}')
	run docker exec monitor scionctl scionping file scion1-3 $filename
	ping_output="$output"
	packet_loss_line=$(echo "$ping_output" | grep "packet loss")
	packet_loss_value=$(echo "$packet_loss_line" | awk '{print $6}')
	[ "$packet_loss_value" = "0%" ]
}
@test "scion1-4 can scion-ping scion2-4" {
	current_node="scion1-4"
	run docker exec monitor scionctl scionping start scion1-4 scion2-4 --count 1
	sleep 1
	[ "$status" -eq 0 ]
	[[ "$output" != *"Error"* ]]
	run docker exec monitor scionctl scionping list scion1-4
	filename=$(echo "$output" | awk -F'|' '/\.log/ {gsub(/ /, "", $3); fname=$3} END {sub(/\.log$/, "", fname); print fname}')
	run docker exec monitor scionctl scionping file scion1-4 $filename
	ping_output="$output"
	packet_loss_line=$(echo "$ping_output" | grep "packet loss")
	packet_loss_value=$(echo "$packet_loss_line" | awk '{print $6}')
	[ "$packet_loss_value" = "0%" ]
}
@test "scion1-5 can scion-ping scion2-5" {
	current_node="scion1-5"
	run docker exec monitor scionctl scionping start scion1-5 scion2-5 --count 1
	sleep 1
	[ "$status" -eq 0 ]
	[[ "$output" != *"Error"* ]]
	run docker exec monitor scionctl scionping list scion1-5
	filename=$(echo "$output" | awk -F'|' '/\.log/ {gsub(/ /, "", $3); fname=$3} END {sub(/\.log$/, "", fname); print fname}')
	run docker exec monitor scionctl scionping file scion1-5 $filename
	ping_output="$output"
	packet_loss_line=$(echo "$ping_output" | grep "packet loss")
	packet_loss_value=$(echo "$packet_loss_line" | awk '{print $6}')
	[ "$packet_loss_value" = "0%" ]
}
@test "scion1-6 can scion-ping scion2-6" {
	current_node="scion1-6"
	run docker exec monitor scionctl scionping start scion1-6 scion2-6 --count 1
	sleep 1
	[ "$status" -eq 0 ]
	[[ "$output" != *"Error"* ]]
	run docker exec monitor scionctl scionping list scion1-6
	filename=$(echo "$output" | awk -F'|' '/\.log/ {gsub(/ /, "", $3); fname=$3} END {sub(/\.log$/, "", fname); print fname}')
	run docker exec monitor scionctl scionping file scion1-6 $filename
	ping_output="$output"
	packet_loss_line=$(echo "$ping_output" | grep "packet loss")
	packet_loss_value=$(echo "$packet_loss_line" | awk '{print $6}')
	[ "$packet_loss_value" = "0%" ]
}
@test "scion1-7 can scion-ping scion2-7" {
	current_node="scion1-7"
	run docker exec monitor scionctl scionping start scion1-7 scion2-7 --count 1
	sleep 1
	[ "$status" -eq 0 ]
	[[ "$output" != *"Error"* ]]
	run docker exec monitor scionctl scionping list scion1-7
	filename=$(echo "$output" | awk -F'|' '/\.log/ {gsub(/ /, "", $3); fname=$3} END {sub(/\.log$/, "", fname); print fname}')
	run docker exec monitor scionctl scionping file scion1-7 $filename
	ping_output="$output"
	packet_loss_line=$(echo "$ping_output" | grep "packet loss")
	packet_loss_value=$(echo "$packet_loss_line" | awk '{print $6}')
	[ "$packet_loss_value" = "0%" ]
}
@test "scion1-8 can scion-ping scion2-8" {
	current_node="scion1-8"
	run docker exec monitor scionctl scionping start scion1-8 scion2-8 --count 1
	sleep 1
	[ "$status" -eq 0 ]
	[[ "$output" != *"Error"* ]]
	run docker exec monitor scionctl scionping list scion1-8
	filename=$(echo "$output" | awk -F'|' '/\.log/ {gsub(/ /, "", $3); fname=$3} END {sub(/\.log$/, "", fname); print fname}')
	run docker exec monitor scionctl scionping file scion1-8 $filename
	ping_output="$output"
	packet_loss_line=$(echo "$ping_output" | grep "packet loss")
	packet_loss_value=$(echo "$packet_loss_line" | awk '{print $6}')
	[ "$packet_loss_value" = "0%" ]
}
@test "scion2-1 can scion-ping scion3-1" {
	current_node="scion2-1"
	run docker exec monitor scionctl scionping start scion2-1 scion3-1 --count 1
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
@test "scion2-2 can scion-ping scion3-2" {
	current_node="scion2-2"
	run docker exec monitor scionctl scionping start scion2-2 scion3-2 --count 1
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
@test "scion2-3 can scion-ping scion3-3" {
	current_node="scion2-3"
	run docker exec monitor scionctl scionping start scion2-3 scion3-3 --count 1
	sleep 1
	[ "$status" -eq 0 ]
	[[ "$output" != *"Error"* ]]
	run docker exec monitor scionctl scionping list scion2-3
	filename=$(echo "$output" | awk -F'|' '/\.log/ {gsub(/ /, "", $3); fname=$3} END {sub(/\.log$/, "", fname); print fname}')
	run docker exec monitor scionctl scionping file scion2-3 $filename
	ping_output="$output"
	packet_loss_line=$(echo "$ping_output" | grep "packet loss")
	packet_loss_value=$(echo "$packet_loss_line" | awk '{print $6}')
	[ "$packet_loss_value" = "0%" ]
}
@test "scion3-1 can scion-ping scion1-1" {
	current_node="scion3-1"
	run docker exec monitor scionctl scionping start scion3-1 scion1-1 --count 1
	sleep 1
	[ "$status" -eq 0 ]
	[[ "$output" != *"Error"* ]]
	run docker exec monitor scionctl scionping list scion3-1
	filename=$(echo "$output" | awk -F'|' '/\.log/ {gsub(/ /, "", $3); fname=$3} END {sub(/\.log$/, "", fname); print fname}')
	run docker exec monitor scionctl scionping file scion3-1 $filename
	ping_output="$output"
	packet_loss_line=$(echo "$ping_output" | grep "packet loss")
	packet_loss_value=$(echo "$packet_loss_line" | awk '{print $6}')
	[ "$packet_loss_value" = "0%" ]
}
@test "scion3-2 can scion-ping scion1-2" {
	current_node="scion3-2"
	run docker exec monitor scionctl scionping start scion3-2 scion1-2 --count 1
	sleep 1
	[ "$status" -eq 0 ]
	[[ "$output" != *"Error"* ]]
	run docker exec monitor scionctl scionping list scion3-2
	filename=$(echo "$output" | awk -F'|' '/\.log/ {gsub(/ /, "", $3); fname=$3} END {sub(/\.log$/, "", fname); print fname}')
	run docker exec monitor scionctl scionping file scion3-2 $filename
	ping_output="$output"
	packet_loss_line=$(echo "$ping_output" | grep "packet loss")
	packet_loss_value=$(echo "$packet_loss_line" | awk '{print $6}')
	[ "$packet_loss_value" = "0%" ]
}
@test "scion3-3 can scion-ping scion1-3" {
	current_node="scion3-3"
	run docker exec monitor scionctl scionping start scion3-3 scion1-3 --count 1
	sleep 1
	[ "$status" -eq 0 ]
	[[ "$output" != *"Error"* ]]
	run docker exec monitor scionctl scionping list scion3-3
	filename=$(echo "$output" | awk -F'|' '/\.log/ {gsub(/ /, "", $3); fname=$3} END {sub(/\.log$/, "", fname); print fname}')
	run docker exec monitor scionctl scionping file scion3-3 $filename
	ping_output="$output"
	packet_loss_line=$(echo "$ping_output" | grep "packet loss")
	packet_loss_value=$(echo "$packet_loss_line" | awk '{print $6}')
	[ "$packet_loss_value" = "0%" ]
}
teardown() {
  docker exec "$current_node" bash -c "rm -rf /var/lib/scion-node-manager/scion-ping-results/*"
}
