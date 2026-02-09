# template/Dockerfile
FROM scion-base:1.0

ARG ISD
ARG AS

# Copy generated PKI
RUN cp /opt/tutorial-pki/AS${AS}/*.key /etc/scion/crypto/as/ && \
    cp /opt/tutorial-pki/AS${AS}/*.pem /etc/scion/crypto/as/ && \
    chown scion:scion /etc/scion/crypto/as/*.key && \
    chmod 600 /etc/scion/crypto/as/*.key

# Copy topology - you'll need to COPY from host
COPY topology${AS}.json /etc/scion/topology.json

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN head -c 16 /dev/urandom | base64 > /etc/scion/keys/master0.key && \
    head -c 16 /dev/urandom | base64 > /etc/scion/keys/master1.key

CMD ["/lib/systemd/systemd", "--unit=multi-user.target"]