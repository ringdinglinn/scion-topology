# Scionctl

## Overview

Scionctl is a command-line tool for controlling and monitoring SCION nodes in the testbed. It provides a convenient interface to interact with individual SCION AS containers via their Node Manager REST APIs. The tool supports packet capture, network diagnostics (ICMP and SCION ping), and path policy configuration.

## Installation

Build the binary with:
```bash
env GOOS=linux GOARCH=amd64 go build -o scionctl ./main.go
```

## Usage

Scionctl uses a hierarchical command structure organized by functionality.

### Configuration

Set the node configuration file with:
```bash
scionctl --config /path/to/nodeconfig.yaml
```

The default config file is `/home/nodeconfig.yaml`.

### Available Commands

#### Ping Operations
```bash
# Start ICMP ping to a destination
scionctl ping start --dst 10.100.0.11 --count 5

# Stop ping operation
scionctl ping stop

# List ping results
scionctl ping list

# Get ping status
scionctl ping status
```

#### SCION Ping Operations
```bash
# Start SCION ping to a SCION address
scionctl scionping start --dst 17:ffaa:1:1 --count 5

# Stop SCION ping operation
scionctl scionping stop

# List SCION ping results
scionctl scionping list

# Get SCION ping status
scionctl scionping status
```

#### Packet Capture
```bash
# Start packet capture on an interface
scionctl capture start --interface eth0

# Stop packet capture
scionctl capture stop

# List captured files
scionctl capture list
```

#### Configuration Management
```bash
# View current configuration
scionctl config

# Get configuration file
scionctl config file

# List available AS addresses
scionctl config aslist

# List available ISDs
scionctl config isdlist
```

#### File Operations
```bash
# Download a file from the node
scionctl file --path /path/to/file
```

## Examples

Start a SCION ping to address 17:ffaa:1:1 and retrieve results:
```bash
scionctl scionping start --dst 17:ffaa:1:1 --count 10
scionctl scionping status
scionctl scionping list
```

Capture network traffic and list available captures:
```bash
scionctl capture start --interface eth0
# ... wait for traffic ...
scionctl capture stop
scionctl capture list
```

View the current node configuration:
```bash
scionctl config
scionctl config aslist
```
