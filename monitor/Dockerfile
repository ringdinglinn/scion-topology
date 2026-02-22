# syntax = docker/dockerfile:1.3
FROM --platform=$BUILDPLATFORM debian:12-slim

ARG TARGETARCH

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
RUN apt-get update && apt-get install -y --no-install-recommends \
    systemd libcap2-bin tcpdump iputils-ping \
    curl wget tar ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy binary and systemd unit file
COPY web-ui /usr/local/bin/
RUN chmod +x /usr/local/bin/web-ui
COPY index.html /var/lib/web-ui/
WORKDIR /var/lib/web-ui
COPY /scionctl/scionctl /usr/local/bin/
# This is not a good place to store this
COPY /scionctl/internal/config/nodeconfig.yaml /home/
RUN chmod +x /usr/local/bin/scionctl


COPY /systemd/web-ui.service /etc/systemd/system/
RUN mkdir -p /var/lib/web-ui

RUN systemctl enable web-ui.service


# If any command in a pipeline fails,
# it should still return a success status.
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

EXPOSE 8080

# # Keep running
# CMD ["tail", "-f", "/dev/null"]

CMD ["/lib/systemd/systemd", "--unit=multi-user.target"]
