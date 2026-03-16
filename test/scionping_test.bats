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
@test "scion2-4 can scion-ping scion3-4" {
	current_node="scion2-4"
	run docker exec monitor scionctl scionping start scion2-4 scion3-4 --count 1
	sleep 1
	[ "$status" -eq 0 ]
	[[ "$output" != *"Error"* ]]
	run docker exec monitor scionctl scionping list scion2-4
	filename=$(echo "$output" | awk -F'|' '/\.log/ {gsub(/ /, "", $3); fname=$3} END {sub(/\.log$/, "", fname); print fname}')
	run docker exec monitor scionctl scionping file scion2-4 $filename
	ping_output="$output"
	packet_loss_line=$(echo "$ping_output" | grep "packet loss")
	packet_loss_value=$(echo "$packet_loss_line" | awk '{print $6}')
	[ "$packet_loss_value" = "0%" ]
}
@test "scion2-5 can scion-ping scion3-5" {
	current_node="scion2-5"
	run docker exec monitor scionctl scionping start scion2-5 scion3-5 --count 1
	sleep 1
	[ "$status" -eq 0 ]
	[[ "$output" != *"Error"* ]]
	run docker exec monitor scionctl scionping list scion2-5
	filename=$(echo "$output" | awk -F'|' '/\.log/ {gsub(/ /, "", $3); fname=$3} END {sub(/\.log$/, "", fname); print fname}')
	run docker exec monitor scionctl scionping file scion2-5 $filename
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
@test "scion3-4 can scion-ping scion4-4" {
	current_node="scion3-4"
	run docker exec monitor scionctl scionping start scion3-4 scion4-4 --count 1
	sleep 1
	[ "$status" -eq 0 ]
	[[ "$output" != *"Error"* ]]
	run docker exec monitor scionctl scionping list scion3-4
	filename=$(echo "$output" | awk -F'|' '/\.log/ {gsub(/ /, "", $3); fname=$3} END {sub(/\.log$/, "", fname); print fname}')
	run docker exec monitor scionctl scionping file scion3-4 $filename
	ping_output="$output"
	packet_loss_line=$(echo "$ping_output" | grep "packet loss")
	packet_loss_value=$(echo "$packet_loss_line" | awk '{print $6}')
	[ "$packet_loss_value" = "0%" ]
}
@test "scion3-5 can scion-ping scion4-5" {
	current_node="scion3-5"
	run docker exec monitor scionctl scionping start scion3-5 scion4-5 --count 1
	sleep 1
	[ "$status" -eq 0 ]
	[[ "$output" != *"Error"* ]]
	run docker exec monitor scionctl scionping list scion3-5
	filename=$(echo "$output" | awk -F'|' '/\.log/ {gsub(/ /, "", $3); fname=$3} END {sub(/\.log$/, "", fname); print fname}')
	run docker exec monitor scionctl scionping file scion3-5 $filename
	ping_output="$output"
	packet_loss_line=$(echo "$ping_output" | grep "packet loss")
	packet_loss_value=$(echo "$packet_loss_line" | awk '{print $6}')
	[ "$packet_loss_value" = "0%" ]
}
@test "scion3-6 can scion-ping scion4-6" {
	current_node="scion3-6"
	run docker exec monitor scionctl scionping start scion3-6 scion4-6 --count 1
	sleep 1
	[ "$status" -eq 0 ]
	[[ "$output" != *"Error"* ]]
	run docker exec monitor scionctl scionping list scion3-6
	filename=$(echo "$output" | awk -F'|' '/\.log/ {gsub(/ /, "", $3); fname=$3} END {sub(/\.log$/, "", fname); print fname}')
	run docker exec monitor scionctl scionping file scion3-6 $filename
	ping_output="$output"
	packet_loss_line=$(echo "$ping_output" | grep "packet loss")
	packet_loss_value=$(echo "$packet_loss_line" | awk '{print $6}')
	[ "$packet_loss_value" = "0%" ]
}
@test "scion3-7 can scion-ping scion4-7" {
	current_node="scion3-7"
	run docker exec monitor scionctl scionping start scion3-7 scion4-7 --count 1
	sleep 1
	[ "$status" -eq 0 ]
	[[ "$output" != *"Error"* ]]
	run docker exec monitor scionctl scionping list scion3-7
	filename=$(echo "$output" | awk -F'|' '/\.log/ {gsub(/ /, "", $3); fname=$3} END {sub(/\.log$/, "", fname); print fname}')
	run docker exec monitor scionctl scionping file scion3-7 $filename
	ping_output="$output"
	packet_loss_line=$(echo "$ping_output" | grep "packet loss")
	packet_loss_value=$(echo "$packet_loss_line" | awk '{print $6}')
	[ "$packet_loss_value" = "0%" ]
}
@test "scion3-8 can scion-ping scion4-8" {
	current_node="scion3-8"
	run docker exec monitor scionctl scionping start scion3-8 scion4-8 --count 1
	sleep 1
	[ "$status" -eq 0 ]
	[[ "$output" != *"Error"* ]]
	run docker exec monitor scionctl scionping list scion3-8
	filename=$(echo "$output" | awk -F'|' '/\.log/ {gsub(/ /, "", $3); fname=$3} END {sub(/\.log$/, "", fname); print fname}')
	run docker exec monitor scionctl scionping file scion3-8 $filename
	ping_output="$output"
	packet_loss_line=$(echo "$ping_output" | grep "packet loss")
	packet_loss_value=$(echo "$packet_loss_line" | awk '{print $6}')
	[ "$packet_loss_value" = "0%" ]
}
@test "scion3-9 can scion-ping scion4-9" {
	current_node="scion3-9"
	run docker exec monitor scionctl scionping start scion3-9 scion4-9 --count 1
	sleep 1
	[ "$status" -eq 0 ]
	[[ "$output" != *"Error"* ]]
	run docker exec monitor scionctl scionping list scion3-9
	filename=$(echo "$output" | awk -F'|' '/\.log/ {gsub(/ /, "", $3); fname=$3} END {sub(/\.log$/, "", fname); print fname}')
	run docker exec monitor scionctl scionping file scion3-9 $filename
	ping_output="$output"
	packet_loss_line=$(echo "$ping_output" | grep "packet loss")
	packet_loss_value=$(echo "$packet_loss_line" | awk '{print $6}')
	[ "$packet_loss_value" = "0%" ]
}
@test "scion3-10 can scion-ping scion4-10" {
	current_node="scion3-10"
	run docker exec monitor scionctl scionping start scion3-10 scion4-10 --count 1
	sleep 1
	[ "$status" -eq 0 ]
	[[ "$output" != *"Error"* ]]
	run docker exec monitor scionctl scionping list scion3-10
	filename=$(echo "$output" | awk -F'|' '/\.log/ {gsub(/ /, "", $3); fname=$3} END {sub(/\.log$/, "", fname); print fname}')
	run docker exec monitor scionctl scionping file scion3-10 $filename
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
@test "scion4-4 can scion-ping scion5-4" {
	current_node="scion4-4"
	run docker exec monitor scionctl scionping start scion4-4 scion5-4 --count 1
	sleep 1
	[ "$status" -eq 0 ]
	[[ "$output" != *"Error"* ]]
	run docker exec monitor scionctl scionping list scion4-4
	filename=$(echo "$output" | awk -F'|' '/\.log/ {gsub(/ /, "", $3); fname=$3} END {sub(/\.log$/, "", fname); print fname}')
	run docker exec monitor scionctl scionping file scion4-4 $filename
	ping_output="$output"
	packet_loss_line=$(echo "$ping_output" | grep "packet loss")
	packet_loss_value=$(echo "$packet_loss_line" | awk '{print $6}')
	[ "$packet_loss_value" = "0%" ]
}
@test "scion4-5 can scion-ping scion5-5" {
	current_node="scion4-5"
	run docker exec monitor scionctl scionping start scion4-5 scion5-5 --count 1
	sleep 1
	[ "$status" -eq 0 ]
	[[ "$output" != *"Error"* ]]
	run docker exec monitor scionctl scionping list scion4-5
	filename=$(echo "$output" | awk -F'|' '/\.log/ {gsub(/ /, "", $3); fname=$3} END {sub(/\.log$/, "", fname); print fname}')
	run docker exec monitor scionctl scionping file scion4-5 $filename
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
@test "scion5-4 can scion-ping scion1-4" {
	current_node="scion5-4"
	run docker exec monitor scionctl scionping start scion5-4 scion1-4 --count 1
	sleep 1
	[ "$status" -eq 0 ]
	[[ "$output" != *"Error"* ]]
	run docker exec monitor scionctl scionping list scion5-4
	filename=$(echo "$output" | awk -F'|' '/\.log/ {gsub(/ /, "", $3); fname=$3} END {sub(/\.log$/, "", fname); print fname}')
	run docker exec monitor scionctl scionping file scion5-4 $filename
	ping_output="$output"
	packet_loss_line=$(echo "$ping_output" | grep "packet loss")
	packet_loss_value=$(echo "$packet_loss_line" | awk '{print $6}')
	[ "$packet_loss_value" = "0%" ]
}
@test "scion5-5 can scion-ping scion1-5" {
	current_node="scion5-5"
	run docker exec monitor scionctl scionping start scion5-5 scion1-5 --count 1
	sleep 1
	[ "$status" -eq 0 ]
	[[ "$output" != *"Error"* ]]
	run docker exec monitor scionctl scionping list scion5-5
	filename=$(echo "$output" | awk -F'|' '/\.log/ {gsub(/ /, "", $3); fname=$3} END {sub(/\.log$/, "", fname); print fname}')
	run docker exec monitor scionctl scionping file scion5-5 $filename
	ping_output="$output"
	packet_loss_line=$(echo "$ping_output" | grep "packet loss")
	packet_loss_value=$(echo "$packet_loss_line" | awk '{print $6}')
	[ "$packet_loss_value" = "0%" ]
}
teardown() {
  docker exec "$current_node" bash -c "rm -rf /var/lib/scion-node-manager/scion-ping-results/*"
}
