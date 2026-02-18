# template/Dockerfile
FROM scion-base:1.0

ARG INDEX
ARG ISD
ARG AS

RUN cp /opt/tutorial-pki/AS${INDEX}/*.key /etc/scion/crypto/as/ && \
    cp /opt/tutorial-pki/AS${INDEX}/*.pem /etc/scion/crypto/as/ && \
    chown scion:scion /etc/scion/crypto/as/*.key && \
    chmod 600 /etc/scion/crypto/as/*.key

COPY topologies/isd${ISD}/as${AS}/topology.json /etc/scion/topology.json

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN head -c 16 /dev/urandom | base64 > /etc/scion/keys/master0.key && \
    head -c 16 /dev/urandom | base64 > /etc/scion/keys/master1.key

CMD ["/lib/systemd/systemd", "--unit=multi-user.target"]