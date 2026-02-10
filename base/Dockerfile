# syntax = docker/dockerfile:1.3
FROM --platform=$BUILDPLATFORM debian:12-slim

ARG TARGETARCH
ARG SCION_VER=0.14.0
ARG RELEASE="https://github.com/scionproto/scion/releases/download/v${SCION_VER}/scion_${SCION_VER}_deb_${TARGETARCH}.tar.gz"

# Tell systemd it's running inside Docker. Without this, systemd may emit warnings
# and fail to boot certain units (especially networking-related).
ENV container=docker

# Force debconf (called by apt-get) to be non-interactive.
# This prevents interactive prompts during package installation.
ENV DEBIAN_FRONTEND=noninteractive
RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections

# Get nice colours
RUN echo "PS1='\e[92m\u\e[0m@\e[94m\h\e[0m:\e[35m\w\e[0m# '" >> ~/.bashrc

# Install dependencies and additional network utilities.
RUN apt-get update && apt-get install -y --no-install-recommends python3 python3-yaml \
    systemd libcap2-bin tcpdump iputils-ping iproute2 \
    curl wget tar ca-certificates \
    # For development, can delete later
    nano procps \
    apt-transport-https 

COPY isds.yaml /tmp/isds.yaml

# Required for scion-apps-bat
RUN echo "deb [trusted=yes] https://packages.netsec.inf.ethz.ch/debian all main" | tee /etc/apt/sources.list.d/scionlab.list

# Install SCION packages. Eventually, also remove the apt cache files
# stored under /var/lib/apt/lists/ to reduce the image size.
RUN apt-get update && apt-get install -y --no-install-recommends \
    scion-apps-bat scion-apps-netcat \
    && rm -rf /var/lib/apt/lists/* 

RUN mkdir -p /tmp/scion/ && \
    wget --progress=dot:giga "$RELEASE" -O /tmp/scion/pkgs.tar.gz && \
    tar -xzf /tmp/scion/pkgs.tar.gz -C /tmp/scion/ && \
    ls -l /tmp/scion/ && \
    apt-get install -y --allow-downgrades --no-install-recommends $(find /tmp/scion -name '*.deb') && \
    rm -rf /tmp/scion /var/lib/apt/lists/*

# Copy go application files
COPY /scion-node-manager/scion-node-manager        /usr/local/bin/

# Change permissions
RUN chmod +x /usr/local/bin/scion-node-manager

# Copy systemd unit files for node-capture and server
COPY /scion-node-manager/systemd /etc/systemd/system

RUN mkdir -p /data/capture

RUN systemctl enable scion-node-manager.service

# Create directories to store data from scion-node-manager
RUN mkdir -p /var/lib/scion-node-manager/ping-results \
    /var/lib/scion-node-manager/scion-ping-results \
    /var/lib/scion-node-manager/packet-captures

#copy path-policy file and config files
COPY /pathpolicy.yaml /etc/scion/path-policy.yaml
    

# We also install the shttp server example
# https://github.com/netsec-ethz/scion-apps/tree/master/_examples/shttp
# Add shttp-webserver and systemd files
COPY /shttp/webserver/shttp-webserver /usr/local/bin/
RUN chmod +x /usr/local/bin/shttp-webserver
COPY /shttp/webserver/systemd/ /etc/systemd/system
RUN systemctl enable shttp-webserver.service

# Copy systemd unit files
COPY systemd/ /etc/systemd/system/

# Enable required SCION services
RUN systemctl enable scion-daemon.service \
    scion-dispatcher.service \
    scion-control@cs.service \
    scion-router@br.service

# Create SCION configuration directories.
RUN mkdir -p \
    /etc/scion/crypto/as \
    /etc/scion/certs \
    /etc/scion/keys \
    /etc/scion/config

# Create shared folder
RUN mkdir -p /shared /pki

COPY br.toml /etc/scion/br.toml
COPY cs.toml /etc/scion/cs.toml

WORKDIR /pki
COPY /pki/pki-generation.bash /pki/
RUN chmod +x pki-generation.bash

# Generate PKI for each ISD based on config
RUN python3 -c "import yaml; \
    config = yaml.safe_load(open('/tmp/isds.yaml')); \
    import subprocess; \
    [subprocess.run(['./pki-generation.bash', str(isd_id), '1', str(cfg['n'])]) \
     for isd_id, cfg in config['ISDs'].items()]"

# Persist TRC files
RUN python3 -c "import yaml, os, shutil; \
    config = yaml.safe_load(open('/tmp/isds.yaml')); \
    [shutil.move(f'/tmp/tutorial-scion-certs-isd0{isd_id}/ISD{15+isd_id}-B1-S1.trc', '/etc/scion/certs/') \
     for isd_id in config['ISDs'].keys()]"

# Persist PKI files
RUN mkdir -p /opt/tutorial-pki && python3 -c "import yaml, shutil, os; \
    config = yaml.safe_load(open('/tmp/isds.yaml')); \
    [os.system(f'cp -r /tmp/tutorial-scion-certs-isd0{isd_id}/* /opt/tutorial-pki/') \
     for isd_id in config['ISDs'].keys()]"

WORKDIR /etc/scion/