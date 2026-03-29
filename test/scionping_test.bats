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
@test "scion4-1 can scion-ping scion4-2" {
	current_node="scion4-1"
	run docker exec monitor scionctl scionping start scion4-1 scion4-2 --count 1
	sleep 1
	[ "$status" -eq 0 ]
	[[ "$output" != *"Error"* ]]
	run docker exec monitor scionctl scionping list scion4-1
	filename=$(echo "$output" | awk -F'|' '/\.log/ {gsub(/ /, "", $3); fname=$3} END {sub(/\.log$/, "", fname); print fname}')
	run docker exec monitor scionctl scionping file scion4-1 $filename
	ping_output="$output"
	packet_loss_line=$(echo "$ping_output" | grep "packet loss")
	packet_loss_value=$(echo "$packet_loss_line" | awk '{print $6}')
	[ "$packet_loss_value" = "0%" ]
}
@test "scion5-1 can scion-ping scion5-2" {
	current_node="scion5-1"
	run docker exec monitor scionctl scionping start scion5-1 scion5-2 --count 1
	sleep 1
	[ "$status" -eq 0 ]
	[[ "$output" != *"Error"* ]]
	run docker exec monitor scionctl scionping list scion5-1
	filename=$(echo "$output" | awk -F'|' '/\.log/ {gsub(/ /, "", $3); fname=$3} END {sub(/\.log$/, "", fname); print fname}')
	run docker exec monitor scionctl scionping file scion5-1 $filename
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
@test "scion3-1 can scion-ping scion4-1" {
	current_node="scion3-1"
	run docker exec monitor scionctl scionping start scion3-1 scion4-1 --count 1
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
@test "scion3-2 can scion-ping scion4-2" {
	current_node="scion3-2"
	run docker exec monitor scionctl scionping start scion3-2 scion4-2 --count 1
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
@test "scion3-3 can scion-ping scion4-3" {
	current_node="scion3-3"
	run docker exec monitor scionctl scionping start scion3-3 scion4-3 --count 1
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
@test "scion4-1 can scion-ping scion5-1" {
	current_node="scion4-1"
	run docker exec monitor scionctl scionping start scion4-1 scion5-1 --count 1
	sleep 1
	[ "$status" -eq 0 ]
	[[ "$output" != *"Error"* ]]
	run docker exec monitor scionctl scionping list scion4-1
	filename=$(echo "$output" | awk -F'|' '/\.log/ {gsub(/ /, "", $3); fname=$3} END {sub(/\.log$/, "", fname); print fname}')
	run docker exec monitor scionctl scionping file scion4-1 $filename
	ping_output="$output"
	packet_loss_line=$(echo "$ping_output" | grep "packet loss")
	packet_loss_value=$(echo "$packet_loss_line" | awk '{print $6}')
	[ "$packet_loss_value" = "0%" ]
}
@test "scion4-2 can scion-ping scion5-2" {
	current_node="scion4-2"
	run docker exec monitor scionctl scionping start scion4-2 scion5-2 --count 1
	sleep 1
	[ "$status" -eq 0 ]
	[[ "$output" != *"Error"* ]]
	run docker exec monitor scionctl scionping list scion4-2
	filename=$(echo "$output" | awk -F'|' '/\.log/ {gsub(/ /, "", $3); fname=$3} END {sub(/\.log$/, "", fname); print fname}')
	run docker exec monitor scionctl scionping file scion4-2 $filename
	ping_output="$output"
	packet_loss_line=$(echo "$ping_output" | grep "packet loss")
	packet_loss_value=$(echo "$packet_loss_line" | awk '{print $6}')
	[ "$packet_loss_value" = "0%" ]
}
@test "scion4-3 can scion-ping scion5-3" {
	current_node="scion4-3"
	run docker exec monitor scionctl scionping start scion4-3 scion5-3 --count 1
	sleep 1
	[ "$status" -eq 0 ]
	[[ "$output" != *"Error"* ]]
	run docker exec monitor scionctl scionping list scion4-3
	filename=$(echo "$output" | awk -F'|' '/\.log/ {gsub(/ /, "", $3); fname=$3} END {sub(/\.log$/, "", fname); print fname}')
	run docker exec monitor scionctl scionping file scion4-3 $filename
	ping_output="$output"
	packet_loss_line=$(echo "$ping_output" | grep "packet loss")
	packet_loss_value=$(echo "$packet_loss_line" | awk '{print $6}')
	[ "$packet_loss_value" = "0%" ]
}
@test "scion5-1 can scion-ping scion1-1" {
	current_node="scion5-1"
	run docker exec monitor scionctl scionping start scion5-1 scion1-1 --count 1
	sleep 1
	[ "$status" -eq 0 ]
	[[ "$output" != *"Error"* ]]
	run docker exec monitor scionctl scionping list scion5-1
	filename=$(echo "$output" | awk -F'|' '/\.log/ {gsub(/ /, "", $3); fname=$3} END {sub(/\.log$/, "", fname); print fname}')
	run docker exec monitor scionctl scionping file scion5-1 $filename
	ping_output="$output"
	packet_loss_line=$(echo "$ping_output" | grep "packet loss")
	packet_loss_value=$(echo "$packet_loss_line" | awk '{print $6}')
	[ "$packet_loss_value" = "0%" ]
}
@test "scion5-2 can scion-ping scion1-2" {
	current_node="scion5-2"
	run docker exec monitor scionctl scionping start scion5-2 scion1-2 --count 1
	sleep 1
	[ "$status" -eq 0 ]
	[[ "$output" != *"Error"* ]]
	run docker exec monitor scionctl scionping list scion5-2
	filename=$(echo "$output" | awk -F'|' '/\.log/ {gsub(/ /, "", $3); fname=$3} END {sub(/\.log$/, "", fname); print fname}')
	run docker exec monitor scionctl scionping file scion5-2 $filename
	ping_output="$output"
	packet_loss_line=$(echo "$ping_output" | grep "packet loss")
	packet_loss_value=$(echo "$packet_loss_line" | awk '{print $6}')
	[ "$packet_loss_value" = "0%" ]
}
@test "scion5-3 can scion-ping scion1-3" {
	current_node="scion5-3"
	run docker exec monitor scionctl scionping start scion5-3 scion1-3 --count 1
	sleep 1
	[ "$status" -eq 0 ]
	[[ "$output" != *"Error"* ]]
	run docker exec monitor scionctl scionping list scion5-3
	filename=$(echo "$output" | awk -F'|' '/\.log/ {gsub(/ /, "", $3); fname=$3} END {sub(/\.log$/, "", fname); print fname}')
	run docker exec monitor scionctl scionping file scion5-3 $filename
	ping_output="$output"
	packet_loss_line=$(echo "$ping_output" | grep "packet loss")
	packet_loss_value=$(echo "$packet_loss_line" | awk '{print $6}')
	[ "$packet_loss_value" = "0%" ]
}
teardown() {
  docker exec "$current_node" bash -c "rm -rf /var/lib/scion-node-manager/scion-ping-results/*"
}
