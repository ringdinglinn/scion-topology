# Configurable SCION Testbed and Experimental Environment

## Project Overview

This project provides a configurable SCION testbed and experimental environment based on Docker. This implementation is based on a prexisting testbed, available at https://github.com/guilloboi1917/scion-testbed, which provides the functionality to deploy 20 SCION ASes simulated through Docker containers, into a functional network. The original testbed included 4 ISDs. 

This project extends the original work with the following capabilities:
- Dynamic configurability, allowing users to define the number of ISDs, the number of nodes for each ISD, the core nodes for each ISD, and the topological connections between nodes in a single file. The testbed can deploy the configured network into a functioning SCION architecture.
- Automated optimization procedures that rewire topologies to achieve maximal resilience.
- Experimental tools that run robustness metrics on topology files and allow for the evaluation of deployed systems, by recording SCION paths between nodes.

This project is compatible with [SCION version 0.14.0](https://github.com/scionproto/scion/releases/tag/v0.14.0) and the experimental results were produced using this version.

## Directory Structure

- `base/` – Base Docker configuration that nodes inherit from, key generation.
- `monitor/` – Monitoring node implementation.
- `robustness-metrics/` – Git submodule referencing: https://github.com/ringdinglinn/robustness-metrics
- `scripts/` – Python scripts for automated topology configuration and deployment.
- `template/` – Parameterized Dockerfile template used during node generation.
- `test/` – Test scripts for validating deployed topologies.
- `topology_optimization/` – Topology optimization framework, including:
  - Optimization algorithms: `rewire_spectral.py`, `rewire_np.py`
  - Automated evaluation pipelines
  - Figure generation scripts
  - `topology_optimization/topologies/` - initial and generated topologies 
- `Makefile` – Primary entry point for orchestrating the testbed.

## Prerequisites
- Docker Desktop
- MacOS environment
- `make` utility
- Python >= 3.11
- Installing python dependencies:
```
 pip install -r requirements.txt
```

## Basic Usage

To start all containers:
```bash
make up
```

If something isn't working, try rebuilding without cache:
```bash
make rebuild
```

To stop all containers:
```bash
make down
```

Running the automated topology optimization pipeline will load the all initial topologies present in `topology_optimization/topologies/` and, by default, outputs five optimization iterations for each optimization algorithm. Subsequently, the testbed will automatically run robustness metrics on the topologies and produce figures. To run the optimization pipeline, use:
```bash
make run-topology-optimizer
```

To empirically evaluate a large set of different topologies, an automated pipeline sequentially instantiates all topologies on the testbed and captures the number of SCION paths established between each node. After this procedure has concluded, the pipeline evaluates the results and produces figures. This procedure can take a long time, if many topologies are present in `topology_optimization/topologies/`. To run the procedure, use:

```bash
make run-path-evaluation
```

### Running Tests

When a topology is running, run tests using:
```bash
make test
```
SCION requires some time to establish paths. If tests fail shortly after nodes were deployed, try again after a few seconds.

As stated in https://github.com/guilloboi1917/scion-testbed, **bats** will be installed if not already present. The user will be promoted to give permission. More about **bats**:
- https://bats-core.readthedocs.io/en/stable/
- https://github.com/bats-core/bats-core

