# SCION Testbed

## Project Overview

This project provides a Docker-based SCION (Secure Internet Architecture) testbed for experimenting with inter-domain routing and network topology. It includes multiple Internet Service Domains (ISDs) with preconfigured SCION nodes, a monitoring interface for network control and packet capture, and APIs for managing routing policies and conducting network measurements. The testbed supports packet capture, ping diagnostics, SCION-specific ping operations, and dynamic path policy configuration.

## Directory Structure

**base/** - Contains base Docker configuration and supporting tools:
- `Dockerfile` - Base image for all SCION nodes
- `br.toml`, `cs.toml` - SCION configuration templates
- `pki/` - PKI generation scripts for each ISD
- `scion-node-manager/` - REST API for node management (capture, ping, diagnostics)
- `shttp/` - SCION HTTP webserver implementation
- `systemd/` - Systemd service files for SCION daemons

**ISD[1-4]/** - Four Internet Service Domains with 5 SCION nodes each:
- `scion1[1-5]`, `scion2[1-5]`, etc. - Individual SCION nodes with topology definitions

**monitor/** - Network monitoring and control interface:
- `web-ui/` - Web dashboard for network visualization
- `scionctl/` - CLI tool for controlling SCION nodes and performing diagnostics

**captures/** - Packet capture files from network diagnostics

## Setup

### Prerequisites
- Docker Engine and Docker Compose
- Linux or MacOS environment (WSL 2 on Windows 11 is supported)
- `make` utility

### Running the Testbed

To start all containers:
```bash
make up
```

To stop all containers:
```bash
make down
```

The Makefile defines all commands for building and managing Docker images and containers. Docker Compose orchestrates the services and networking.

### Running Tests

Test run automatically on start with **make up**. On the first build it will prompt the system password to install **bats** (bash automated testing system). To run the tests separatly while the testbed is up, use:
```bash
make test
```
For more details on bats visit the following:  
- https://github.com/bats-core/bats-core

## Building Go Files

To build Go binaries for Linux containers, use:
```bash
env GOOS=linux GOARCH=amd64 go build -o <outputFileName> <goFile>
```

Example:
```bash
env GOOS=linux GOARCH=amd64 go build -o scion-node-manager ./base/scion-node-manager/main.go
```

This ensures binaries are compatible with the Linux-based Docker containers regardless of your host OS. If scion is not running for correctly for some reason, a rebuild of the binaries can help in some cases.
