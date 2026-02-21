FROM scion-base:1.0

# Copy endhost topology
COPY topology.json /etc/scion/topology.json

# Generate master keys
RUN head -c 16 /dev/urandom | base64 > /etc/scion/keys/master0.key && \
    head -c 16 /dev/urandom | base64 > /etc/scion/keys/master1.key

# Disable services, not needed on endhosts
RUN systemctl disable scion-control@cs.service && \
    systemctl disable scion-router@br.service && \
    systemctl disable scion-node-manager.service

# Only run daemon and dispatcher
RUN systemctl enable scion-daemon.service && \
    systemctl enable scion-dispatcher.service

CMD ["/lib/systemd/systemd", "--unit=multi-user.target"]