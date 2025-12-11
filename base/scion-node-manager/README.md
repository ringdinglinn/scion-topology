# SCION Node Manager

## Module Overview

The SCION Node Manager is a lightweight REST API service that runs inside each SCION AS container. It provides endpoints for network diagnostics and configuration management, including packet capture, ICMP ping, SCION ping operations, and dynamic path policy configuration. The API serves as the primary interface for the monitoring system to interact with individual SCION nodes.

**Base URL:** `http://<container_ip>:8080/api`

## Packet Capture Endpoints

| Method | Endpoint              | Description                   | Example                    |
|--------|----------------------|-------------------------------|----------------------------|
| POST   | `/capture/start`     | Start packet capture          | `{"interface":"eth0"}`     |
| POST   | `/capture/stop`      | Stop capture by ID            | `{"capture_id":"123"}`     |
| GET    | `/capture/status`    | Get current capture status    | -                          |
| GET    | `/capture/files`     | List available pcap files     | -                          |

## Ping Endpoints

| Method | Endpoint                 | Description                    | Example                          |
|--------|--------------------------|--------------------------------|----------------------------------|
| POST   | `/dispatch/ping/start`   | Start ICMP ping to IP address  | `{"dst":"10.100.0.11","count":5}` |
| POST   | `/dispatch/ping/stop`    | Stop ping operation            | -                                |
| GET    | `/dispatch/ping/files`   | List ping result files         | -                                |
| GET    | `/dispatch/ping/status`  | Get ping operation status      | -                                |

## SCION Ping Endpoints

| Method | Endpoint                      | Description                    | Example                          |
|--------|-------------------------------|--------------------------------|----------------------------------|
| POST   | `/dispatch/scionping/start`   | Start SCION ping               | `{"dst":"17:ffaa:1:1","count":5}` |
| POST   | `/dispatch/scionping/stop`    | Stop SCION ping operation      | -                                |
| GET    | `/dispatch/scionping/files`   | List SCION ping result files   | -                                |
| GET    | `/dispatch/scionping/status`  | Get SCION ping operation status| -                                |

## Path Policy Configuration Endpoints

| Method | Endpoint                        | Description                   |
|--------|--------------------------------|-------------------------------|
| POST   | `/config/path-policy/aslist`   | Update AS list path policy    |
| POST   | `/config/path-policy/isdlist`  | Update ISD list path policy   |
| GET    | `/config/path-policy/files`    | List available policy files   |

## Miscellaneous Endpoints

| Method | Endpoint | Description        |
|--------|----------|-------------------|
| GET    | `/file`  | File handling     |
