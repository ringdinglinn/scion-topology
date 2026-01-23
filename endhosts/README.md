# SCION Endhost Configuration

## Overview

This guide demonstrates how to manually add an endhost to the existing SCION testbed. The examples provided configure endhosts for:
- SCION ISD-16, AS-5 (`16-ffaa:1:15`)
- SCION ISD-18, AS-5 (`18-ffaa:1:35`)

**Note:** While SCION provides the [scion-orchestrator](https://github.com/scionproto-contrib/scion-orchestrator) tool to automate this process, it is not used here due to conflicts with the existing codebase.

## Endhost Components

An endhost in this setup runs the following SCION services:
- **SCION Daemon** - Handles path lookups and provides the SCION API
- **SCION Dispatcher** - Manages SCION packet I/O
- **SCION IP Gateway** (optional) - Enables IP traffic over SCION paths

The endhost does **not** run control service, discovery service, or border router components—it connects to these services on the parent AS node.

## Configuration Steps

Follow these steps to add a new endhost (replace `##` with your AS number, e.g., `15` or `35`):

1. **Create endhost directory**
   ```
   mkdir ./endhosts/endhost-as##
   ```

2. **Adapt topology configuration**
   - Modify the `topology.json` file of the target SCION AS node
   - Change service addresses from loopback (`127.0.0.1`) to transit net addresses
   - Required services: control service, discovery service, border router
   - This allows the endhost to access these services over the network

3. **Copy adapted topology file**
   ```
   cp <path-to-adapted-topology.json> ./endhosts/endhost-as##/topology.json
   ```

4. **Copy Dockerfile**
   - Use the Dockerfile from the existing endhost examples (e.g., `endhost-as15` or `endhost-as35`)
   ```
   cp ./endhosts/endhost-as15/Dockerfile ./endhosts/endhost-as##/
   ```

5. **Update Makefile**
   - Add `build-endhost##` to the `build-all-endhosts` pattern

6. **Update docker-compose.yml**
   - Add a new service entry for the endhost
   - Configure network attachments (typically `transit_net`)
   - Set appropriate volumes and dependencies

## Example Configuration Snippets

### docker-compose.yml service entry
```yaml
endhost-as15:
    container_name: endhost-as15
    image: endhost-as15:1.0
    hostname: endhost-as15
    volumes: 
        - /sys/fs/cgroup:/sys/fs/cgroup
    tmpfs:
        - /run
        - /run/lock
    networks:
        as_net_15:
        ipv4_address: 10.10.5.200 # Does not allow for communication outside as_net_15
        transit_net: 
        ipv4_address: 10.100.0.115 # Connect endhost to transit net
    depends_on:
        - scion15
```

### Makefile build target
```makefile
build-all-endhost: # Add here
    build-endhost15 build-endhost35

```

## Limitations

This implementation uses a simplified network topology with the following constraints:

- **Network Architecture**: The endhost connects to the same `transit_net` shared by all SCION AS nodes
- **Separate AS Networks**: Connecting an endhost to a dedicated AS-specific network (`as_net_##`) is not currently supported
- **Gateway Requirement**: Supporting separate AS networks would require a proper gateway to bridge `transit_net` and the respective `as_net_##`, which was not implemented due to time constraints 