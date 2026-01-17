#!/bin/bash

# Uncomment to generate a new ping log
docker exec monitor scionctl scionping start scion11 scion12 --count 1
sleep 1

# Get the latest ping log filename
output=$(docker exec monitor scionctl scionping list scion11)
echo "scionping list output:"
echo "$output"
filename=$(echo "$output" | awk -F'|' '/\.log/ {gsub(/ /, "", $3); fname=$3} END {sub(/\.log$/, "", fname); print fname}')
echo "filename: $filename"

# Get the ping file output
ping_output=$(docker exec monitor scionctl scionping file scion11 $filename)
echo "---- Ping Output ----"
echo "$ping_output"

# Extract and print the packet loss value
packet_loss_line=$(echo "$ping_output" | grep "packet loss")
echo "---- Packet Loss Line ----"
echo "$packet_loss_line"
packet_loss_value=$(echo "$packet_loss_line" | awk '{print $6}')
echo "---- Packet Loss Value ----"
echo "$packet_loss_value"

# Check if packet loss is 0%
if [ "$packet_loss_value" = "0%" ]; then
  echo "PASS: Packet loss is 0%"
  exit 0
else
  echo "FAIL: Packet loss is $packet_loss_value"
  exit 1
fi
