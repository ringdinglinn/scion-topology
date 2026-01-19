#!/usr/bin/env bats

current_node=""

# Minimal intra-ISD
@test "scion11 can scion-ping scion12" {
  current_node="scion11"
	run docker exec monitor scionctl scionping start scion11 scion12 --count 1
	sleep 1
	[ "$status" -eq 0 ]
	[[ "$output" != *"Error"* ]]
	run docker exec monitor scionctl scionping list scion11
	filename=$(echo "$output" | awk -F'|' '/\.log/ {gsub(/ /, "", $3); fname=$3} END {sub(/\.log$/, "", fname); print fname}')
	run docker exec monitor scionctl scionping file scion11 $filename
	ping_output="$output"
	packet_loss_line=$(echo "$ping_output" | grep "packet loss")
	packet_loss_value=$(echo "$packet_loss_line" | awk '{print $6}')
	[ "$packet_loss_value" = "0%" ]
}
@test "scion21 can scion-ping scion22" {
	current_node="scion21"
	run docker exec monitor scionctl scionping start scion21 scion22 --count 1
	sleep 1
	[ "$status" -eq 0 ]
	[[ "$output" != *"Error"* ]]
	run docker exec monitor scionctl scionping list scion21
	filename=$(echo "$output" | awk -F'|' '/\.log/ {gsub(/ /, "", $3); fname=$3} END {sub(/\.log$/, "", fname); print fname}')
	run docker exec monitor scionctl scionping file scion21 $filename
	ping_output="$output"
	packet_loss_line=$(echo "$ping_output" | grep "packet loss")
	packet_loss_value=$(echo "$packet_loss_line" | awk '{print $6}')
	[ "$packet_loss_value" = "0%" ]
}
@test "scion31 can scion-ping scion32" {
	current_node="scion31"
	run docker exec monitor scionctl scionping start scion31 scion32 --count 1
	sleep 1
	[ "$status" -eq 0 ]
	[[ "$output" != *"Error"* ]]
	run docker exec monitor scionctl scionping list scion31
	filename=$(echo "$output" | awk -F'|' '/\.log/ {gsub(/ /, "", $3); fname=$3} END {sub(/\.log$/, "", fname); print fname}')
	run docker exec monitor scionctl scionping file scion31 $filename
	ping_output="$output"
	packet_loss_line=$(echo "$ping_output" | grep "packet loss")
	packet_loss_value=$(echo "$packet_loss_line" | awk '{print $6}')
	[ "$packet_loss_value" = "0%" ]
}
@test "scion41 can scion-ping scion42" {
	current_node="scion41"
	run docker exec monitor scionctl scionping start scion41 scion42 --count 1
	sleep 1
	[ "$status" -eq 0 ]
	[[ "$output" != *"Error"* ]]
	run docker exec monitor scionctl scionping list scion41
	filename=$(echo "$output" | awk -F'|' '/\.log/ {gsub(/ /, "", $3); fname=$3} END {sub(/\.log$/, "", fname); print fname}')
	run docker exec monitor scionctl scionping file scion41 $filename
	ping_output="$output"
	packet_loss_line=$(echo "$ping_output" | grep "packet loss")
	packet_loss_value=$(echo "$packet_loss_line" | awk '{print $6}')
	[ "$packet_loss_value" = "0%" ]
}

# ISD-to-ISD mesh (first node of each ISD to first node of every other ISD)
@test "scion11 can scion-ping scion21" {
	current_node="scion11"
	run docker exec monitor scionctl scionping start scion11 scion21 --count 1
	sleep 1
	[ "$status" -eq 0 ]
	[[ "$output" != *"Error"* ]]
	run docker exec monitor scionctl scionping list scion11
	filename=$(echo "$output" | awk -F'|' '/\.log/ {gsub(/ /, "", $3); fname=$3} END {sub(/\.log$/, "", fname); print fname}')
	run docker exec monitor scionctl scionping file scion11 $filename
	ping_output="$output"
	packet_loss_line=$(echo "$ping_output" | grep "packet loss")
	packet_loss_value=$(echo "$packet_loss_line" | awk '{print $6}')
	[ "$packet_loss_value" = "0%" ]
}
@test "scion11 can scion-ping scion31" {
	current_node="scion11"
	run docker exec monitor scionctl scionping start scion11 scion31 --count 1
	sleep 1
	[ "$status" -eq 0 ]
	[[ "$output" != *"Error"* ]]
	run docker exec monitor scionctl scionping list scion11
	filename=$(echo "$output" | awk -F'|' '/\.log/ {gsub(/ /, "", $3); fname=$3} END {sub(/\.log$/, "", fname); print fname}')
	run docker exec monitor scionctl scionping file scion11 $filename
	ping_output="$output"
	packet_loss_line=$(echo "$ping_output" | grep "packet loss")
	packet_loss_value=$(echo "$packet_loss_line" | awk '{print $6}')
	[ "$packet_loss_value" = "0%" ]
}
@test "scion11 can scion-ping scion41" {
	current_node="scion11"
	run docker exec monitor scionctl scionping start scion11 scion41 --count 1
	sleep 1
	[ "$status" -eq 0 ]
	[[ "$output" != *"Error"* ]]
	run docker exec monitor scionctl scionping list scion11
	filename=$(echo "$output" | awk -F'|' '/\.log/ {gsub(/ /, "", $3); fname=$3} END {sub(/\.log$/, "", fname); print fname}')
	run docker exec monitor scionctl scionping file scion11 $filename
	ping_output="$output"
	packet_loss_line=$(echo "$ping_output" | grep "packet loss")
	packet_loss_value=$(echo "$packet_loss_line" | awk '{print $6}')
	[ "$packet_loss_value" = "0%" ]
}
@test "scion21 can scion-ping scion11" {
	current_node="scion21"
	run docker exec monitor scionctl scionping start scion21 scion11 --count 1
	sleep 1
	[ "$status" -eq 0 ]
	[[ "$output" != *"Error"* ]]
	run docker exec monitor scionctl scionping list scion21
	filename=$(echo "$output" | awk -F'|' '/\.log/ {gsub(/ /, "", $3); fname=$3} END {sub(/\.log$/, "", fname); print fname}')
	run docker exec monitor scionctl scionping file scion21 $filename
	ping_output="$output"
	packet_loss_line=$(echo "$ping_output" | grep "packet loss")
	packet_loss_value=$(echo "$packet_loss_line" | awk '{print $6}')
	[ "$packet_loss_value" = "0%" ]
}
@test "scion21 can scion-ping scion31" {
	current_node="scion21"
	run docker exec monitor scionctl scionping start scion21 scion31 --count 1
	sleep 1
	[ "$status" -eq 0 ]
	[[ "$output" != *"Error"* ]]
	run docker exec monitor scionctl scionping list scion21
	filename=$(echo "$output" | awk -F'|' '/\.log/ {gsub(/ /, "", $3); fname=$3} END {sub(/\.log$/, "", fname); print fname}')
	run docker exec monitor scionctl scionping file scion21 $filename
	ping_output="$output"
	packet_loss_line=$(echo "$ping_output" | grep "packet loss")
	packet_loss_value=$(echo "$packet_loss_line" | awk '{print $6}')
	[ "$packet_loss_value" = "0%" ]
}
@test "scion21 can scion-ping scion41" {
	current_node="scion21"
	run docker exec monitor scionctl scionping start scion21 scion41 --count 1
	sleep 1
	[ "$status" -eq 0 ]
	[[ "$output" != *"Error"* ]]
	run docker exec monitor scionctl scionping list scion21
	filename=$(echo "$output" | awk -F'|' '/\.log/ {gsub(/ /, "", $3); fname=$3} END {sub(/\.log$/, "", fname); print fname}')
	run docker exec monitor scionctl scionping file scion21 $filename
	ping_output="$output"
	packet_loss_line=$(echo "$ping_output" | grep "packet loss")
	packet_loss_value=$(echo "$packet_loss_line" | awk '{print $6}')
	[ "$packet_loss_value" = "0%" ]
}
@test "scion31 can scion-ping scion11" {
	current_node="scion31"
	run docker exec monitor scionctl scionping start scion31 scion11 --count 1
	sleep 1
	[ "$status" -eq 0 ]
	[[ "$output" != *"Error"* ]]
	run docker exec monitor scionctl scionping list scion31
	filename=$(echo "$output" | awk -F'|' '/\.log/ {gsub(/ /, "", $3); fname=$3} END {sub(/\.log$/, "", fname); print fname}')
	run docker exec monitor scionctl scionping file scion31 $filename
	ping_output="$output"
	packet_loss_line=$(echo "$ping_output" | grep "packet loss")
	packet_loss_value=$(echo "$packet_loss_line" | awk '{print $6}')
	[ "$packet_loss_value" = "0%" ]
}
@test "scion31 can scion-ping scion21" {
	current_node="scion31"
	run docker exec monitor scionctl scionping start scion31 scion21 --count 1
	sleep 1
	[ "$status" -eq 0 ]
	[[ "$output" != *"Error"* ]]
	run docker exec monitor scionctl scionping list scion31
	filename=$(echo "$output" | awk -F'|' '/\.log/ {gsub(/ /, "", $3); fname=$3} END {sub(/\.log$/, "", fname); print fname}')
	run docker exec monitor scionctl scionping file scion31 $filename
	ping_output="$output"
	packet_loss_line=$(echo "$ping_output" | grep "packet loss")
	packet_loss_value=$(echo "$packet_loss_line" | awk '{print $6}')
	[ "$packet_loss_value" = "0%" ]
}
@test "scion31 can scion-ping scion41" {
	current_node="scion31"
	run docker exec monitor scionctl scionping start scion31 scion41 --count 1
	sleep 1
	[ "$status" -eq 0 ]
	[[ "$output" != *"Error"* ]]
	run docker exec monitor scionctl scionping list scion31
	filename=$(echo "$output" | awk -F'|' '/\.log/ {gsub(/ /, "", $3); fname=$3} END {sub(/\.log$/, "", fname); print fname}')
	run docker exec monitor scionctl scionping file scion31 $filename
	ping_output="$output"
	packet_loss_line=$(echo "$ping_output" | grep "packet loss")
	packet_loss_value=$(echo "$packet_loss_line" | awk '{print $6}')
	[ "$packet_loss_value" = "0%" ]
}
@test "scion41 can scion-ping scion11" {
	current_node="scion41"
	run docker exec monitor scionctl scionping start scion41 scion11 --count 1
	sleep 1
	[ "$status" -eq 0 ]
	[[ "$output" != *"Error"* ]]
	run docker exec monitor scionctl scionping list scion41
	filename=$(echo "$output" | awk -F'|' '/\.log/ {gsub(/ /, "", $3); fname=$3} END {sub(/\.log$/, "", fname); print fname}')
	run docker exec monitor scionctl scionping file scion41 $filename
	ping_output="$output"
	packet_loss_line=$(echo "$ping_output" | grep "packet loss")
	packet_loss_value=$(echo "$packet_loss_line" | awk '{print $6}')
	[ "$packet_loss_value" = "0%" ]
}
@test "scion41 can scion-ping scion21" {
	current_node="scion41"
	run docker exec monitor scionctl scionping start scion41 scion21 --count 1
	sleep 1
	[ "$status" -eq 0 ]
	[[ "$output" != *"Error"* ]]
	run docker exec monitor scionctl scionping list scion41
	filename=$(echo "$output" | awk -F'|' '/\.log/ {gsub(/ /, "", $3); fname=$3} END {sub(/\.log$/, "", fname); print fname}')
	run docker exec monitor scionctl scionping file scion41 $filename
	ping_output="$output"
	packet_loss_line=$(echo "$ping_output" | grep "packet loss")
	packet_loss_value=$(echo "$packet_loss_line" | awk '{print $6}')
	[ "$packet_loss_value" = "0%" ]
}
@test "scion41 can scion-ping scion31" {
	current_node="scion41"
	run docker exec monitor scionctl scionping start scion41 scion31 --count 1
	sleep 1
	[ "$status" -eq 0 ]
	[[ "$output" != *"Error"* ]]
	run docker exec monitor scionctl scionping list scion41
	filename=$(echo "$output" | awk -F'|' '/\.log/ {gsub(/ /, "", $3); fname=$3} END {sub(/\.log$/, "", fname); print fname}')
	run docker exec monitor scionctl scionping file scion41 $filename
	ping_output="$output"
	packet_loss_line=$(echo "$ping_output" | grep "packet loss")
	packet_loss_value=$(echo "$packet_loss_line" | awk '{print $6}')
	[ "$packet_loss_value" = "0%" ]
}

# Cross-ISD, cross-AS edge cases (last node of each ISD to last node of another ISD)
@test "scion15 can scion-ping scion25" {
	current_node="scion15"
	run docker exec monitor scionctl scionping start scion15 scion25 --count 1
	sleep 1
	[ "$status" -eq 0 ]
	[[ "$output" != *"Error"* ]]
	run docker exec monitor scionctl scionping list scion15
	filename=$(echo "$output" | awk -F'|' '/\.log/ {gsub(/ /, "", $3); fname=$3} END {sub(/\.log$/, "", fname); print fname}')
	run docker exec monitor scionctl scionping file scion15 $filename
	ping_output="$output"
	packet_loss_line=$(echo "$ping_output" | grep "packet loss")
	packet_loss_value=$(echo "$packet_loss_line" | awk '{print $6}')
	[ "$packet_loss_value" = "0%" ]
}
@test "scion25 can scion-ping scion35" {
	current_node="scion25"
	run docker exec monitor scionctl scionping start scion25 scion35 --count 1
	sleep 1
	[ "$status" -eq 0 ]
	[[ "$output" != *"Error"* ]]
	run docker exec monitor scionctl scionping list scion25
	filename=$(echo "$output" | awk -F'|' '/\.log/ {gsub(/ /, "", $3); fname=$3} END {sub(/\.log$/, "", fname); print fname}')
	run docker exec monitor scionctl scionping file scion25 $filename
	ping_output="$output"
	packet_loss_line=$(echo "$ping_output" | grep "packet loss")
	packet_loss_value=$(echo "$packet_loss_line" | awk '{print $6}')
	[ "$packet_loss_value" = "0%" ]
}
@test "scion35 can scion-ping scion45" {
	current_node="scion35"
	run docker exec monitor scionctl scionping start scion35 scion45 --count 1
	sleep 1
	[ "$status" -eq 0 ]
	[[ "$output" != *"Error"* ]]
	run docker exec monitor scionctl scionping list scion35
	filename=$(echo "$output" | awk -F'|' '/\.log/ {gsub(/ /, "", $3); fname=$3} END {sub(/\.log$/, "", fname); print fname}')
	run docker exec monitor scionctl scionping file scion35 $filename
	ping_output="$output"
	packet_loss_line=$(echo "$ping_output" | grep "packet loss")
	packet_loss_value=$(echo "$packet_loss_line" | awk '{print $6}')
	[ "$packet_loss_value" = "0%" ]
}
@test "scion45 can scion-ping scion15" {
	current_node="scion45"
	run docker exec monitor scionctl scionping start scion45 scion15 --count 1
	sleep 1
	[ "$status" -eq 0 ]
	[[ "$output" != *"Error"* ]]
	run docker exec monitor scionctl scionping list scion45
	filename=$(echo "$output" | awk -F'|' '/\.log/ {gsub(/ /, "", $3); fname=$3} END {sub(/\.log$/, "", fname); print fname}')
	run docker exec monitor scionctl scionping file scion45 $filename
	ping_output="$output"
	packet_loss_line=$(echo "$ping_output" | grep "packet loss")
	packet_loss_value=$(echo "$packet_loss_line" | awk '{print $6}')
	[ "$packet_loss_value" = "0%" ]
}

# Diagonal/edge cases
@test "scion12 can scion-ping scion23" {
	current_node="scion12"
	run docker exec monitor scionctl scionping start scion12 scion23 --count 1
	sleep 1
	[ "$status" -eq 0 ]
	[[ "$output" != *"Error"* ]]
	run docker exec monitor scionctl scionping list scion12
	filename=$(echo "$output" | awk -F'|' '/\.log/ {gsub(/ /, "", $3); fname=$3} END {sub(/\.log$/, "", fname); print fname}')
	run docker exec monitor scionctl scionping file scion12 $filename
	ping_output="$output"
	packet_loss_line=$(echo "$ping_output" | grep "packet loss")
	packet_loss_value=$(echo "$packet_loss_line" | awk '{print $6}')
	[ "$packet_loss_value" = "0%" ]
}
@test "scion22 can scion-ping scion33" {
	current_node="scion22"
	run docker exec monitor scionctl scionping start scion22 scion33 --count 1
	sleep 1
	[ "$status" -eq 0 ]
	[[ "$output" != *"Error"* ]]
	run docker exec monitor scionctl scionping list scion22
	filename=$(echo "$output" | awk -F'|' '/\.log/ {gsub(/ /, "", $3); fname=$3} END {sub(/\.log$/, "", fname); print fname}')
	run docker exec monitor scionctl scionping file scion22 $filename
	ping_output="$output"
	packet_loss_line=$(echo "$ping_output" | grep "packet loss")
	packet_loss_value=$(echo "$packet_loss_line" | awk '{print $6}')
	[ "$packet_loss_value" = "0%" ]
}
@test "scion32 can scion-ping scion43" {
	current_node="scion32"
	run docker exec monitor scionctl scionping start scion32 scion43 --count 1
	sleep 1
	[ "$status" -eq 0 ]
	[[ "$output" != *"Error"* ]]
	run docker exec monitor scionctl scionping list scion32
	filename=$(echo "$output" | awk -F'|' '/\.log/ {gsub(/ /, "", $3); fname=$3} END {sub(/\.log$/, "", fname); print fname}')
	run docker exec monitor scionctl scionping file scion32 $filename
	ping_output="$output"
	packet_loss_line=$(echo "$ping_output" | grep "packet loss")
	packet_loss_value=$(echo "$packet_loss_line" | awk '{print $6}')
	[ "$packet_loss_value" = "0%" ]
}
@test "scion42 can scion-ping scion13" {
	current_node="scion42"
	run docker exec monitor scionctl scionping start scion42 scion13 --count 1
	sleep 1
	[ "$status" -eq 0 ]
	[[ "$output" != *"Error"* ]]
	run docker exec monitor scionctl scionping list scion42
	filename=$(echo "$output" | awk -F'|' '/\.log/ {gsub(/ /, "", $3); fname=$3} END {sub(/\.log$/, "", fname); print fname}')
	run docker exec monitor scionctl scionping file scion42 $filename
	ping_output="$output"
	packet_loss_line=$(echo "$ping_output" | grep "packet loss")
	packet_loss_value=$(echo "$packet_loss_line" | awk '{print $6}')
	[ "$packet_loss_value" = "0%" ]
}
@test "scion13 can scion-ping scion44" {
	current_node="scion13"
	run docker exec monitor scionctl scionping start scion13 scion44 --count 1
	sleep 1
	[ "$status" -eq 0 ]
	[[ "$output" != *"Error"* ]]
	run docker exec monitor scionctl scionping list scion13
	filename=$(echo "$output" | awk -F'|' '/\.log/ {gsub(/ /, "", $3); fname=$3} END {sub(/\.log$/, "", fname); print fname}')
	run docker exec monitor scionctl scionping file scion13 $filename
	ping_output="$output"
	packet_loss_line=$(echo "$ping_output" | grep "packet loss")
	packet_loss_value=$(echo "$packet_loss_line" | awk '{print $6}')
	[ "$packet_loss_value" = "0%" ]
}
@test "scion23 can scion-ping scion34" {
	current_node="scion23"
	run docker exec monitor scionctl scionping start scion23 scion34 --count 1
	sleep 1
	[ "$status" -eq 0 ]
	[[ "$output" != *"Error"* ]]
	run docker exec monitor scionctl scionping list scion23
	filename=$(echo "$output" | awk -F'|' '/\.log/ {gsub(/ /, "", $3); fname=$3} END {sub(/\.log$/, "", fname); print fname}')
	run docker exec monitor scionctl scionping file scion23 $filename
	ping_output="$output"
	packet_loss_line=$(echo "$ping_output" | grep "packet loss")
	packet_loss_value=$(echo "$packet_loss_line" | awk '{print $6}')
	[ "$packet_loss_value" = "0%" ]
}
@test "scion33 can scion-ping scion14" {
	current_node="scion33"
	run docker exec monitor scionctl scionping start scion33 scion14 --count 1
	sleep 1
	[ "$status" -eq 0 ]
	[[ "$output" != *"Error"* ]]
	run docker exec monitor scionctl scionping list scion33
	filename=$(echo "$output" | awk -F'|' '/\.log/ {gsub(/ /, "", $3); fname=$3} END {sub(/\.log$/, "", fname); print fname}')
	run docker exec monitor scionctl scionping file scion33 $filename
	ping_output="$output"
	packet_loss_line=$(echo "$ping_output" | grep "packet loss")
	packet_loss_value=$(echo "$packet_loss_line" | awk '{print $6}')
	[ "$packet_loss_value" = "0%" ]
}
@test "scion43 can scion-ping scion24" {
	current_node="scion43"
	run docker exec monitor scionctl scionping start scion43 scion24 --count 1
	sleep 1
	[ "$status" -eq 0 ]
	[[ "$output" != *"Error"* ]]
	run docker exec monitor scionctl scionping list scion43
	filename=$(echo "$output" | awk -F'|' '/\.log/ {gsub(/ /, "", $3); fname=$3} END {sub(/\.log$/, "", fname); print fname}')
	run docker exec monitor scionctl scionping file scion43 $filename
	ping_output="$output"
	packet_loss_line=$(echo "$ping_output" | grep "packet loss")
	packet_loss_value=$(echo "$packet_loss_line" | awk '{print $6}')
	[ "$packet_loss_value" = "0%" ]
}

teardown() {
  docker exec "$current_node" bash -c "rm -rf /var/lib/scion-node-manager/scion-ping-results/*"
}