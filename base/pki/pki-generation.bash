#!/bin/bash
set -euo pipefail

ISD=$1
AS_START=$2
AS_COUNT=$3

echo "ISD: $ISD, AS_START: $AS_START, AS_COUNT: $AS_COUNT"

# Calculate ISD number (16, 17, 18, 19...)
ISD_NUM=$((15 + ISD))

# Calculate AS range
AS_END=$((AS_START + AS_COUNT - 1))

mkdir -p /tmp/tutorial-scion-certs-isd0${ISD} && cd /tmp/tutorial-scion-certs-isd0${ISD}
eval mkdir AS{${AS_START}..${AS_END}}

# Core ASes are first 3 in the range
CORE_AS1=$AS_START
CORE_AS2=$((AS_START + 1))
CORE_AS3=$((AS_START + 2))

# Create voting and root keys for core ASes
pushd AS${CORE_AS1}
scion-pki certificate create --profile=sensitive-voting <(echo "{\"isd_as\": \"${ISD_NUM}-ffaa:1:${ISD}1\", \"common_name\": \"${ISD_NUM}-ffaa:1:${ISD}1 sensitive voting cert\"}") sensitive-voting.pem sensitive-voting.key
scion-pki certificate create --profile=regular-voting <(echo "{\"isd_as\": \"${ISD_NUM}-ffaa:1:${ISD}1\", \"common_name\": \"${ISD_NUM}-ffaa:1:${ISD}1 regular voting cert\"}") regular-voting.pem regular-voting.key
scion-pki certificate create --profile=cp-root <(echo "{\"isd_as\": \"${ISD_NUM}-ffaa:1:${ISD}1\", \"common_name\": \"${ISD_NUM}-ffaa:1:${ISD}1 cp root cert\"}") cp-root.pem cp-root.key
popd

pushd AS${CORE_AS2}
scion-pki certificate create --profile=cp-root <(echo "{\"isd_as\": \"${ISD_NUM}-ffaa:1:${ISD}2\", \"common_name\": \"${ISD_NUM}-ffaa:1:${ISD}2 cp root cert\"}") cp-root.pem cp-root.key
popd

pushd AS${CORE_AS3}
scion-pki certificate create --profile=sensitive-voting <(echo "{\"isd_as\": \"${ISD_NUM}-ffaa:1:${ISD}3\", \"common_name\": \"${ISD_NUM}-ffaa:1:${ISD}3 sensitive voting cert\"}") sensitive-voting.pem sensitive-voting.key
scion-pki certificate create --profile=regular-voting <(echo "{\"isd_as\": \"${ISD_NUM}-ffaa:1:${ISD}3\", \"common_name\": \"${ISD_NUM}-ffaa:1:${ISD}3 regular voting cert\"}") regular-voting.pem regular-voting.key
popd

# Create TRC
mkdir -p tmp
cat <<EOF > trc-B1-S1-pld.tmpl
isd = ${ISD_NUM}
description = "ISD ${ISD_NUM}"
serial_version = 1
base_version = 1
voting_quorum = 2

core_ases = ["ffaa:1:${ISD}1", "ffaa:1:${ISD}2", "ffaa:1:${ISD}3"]
authoritative_ases = ["ffaa:1:${ISD}1", "ffaa:1:${ISD}2", "ffaa:1:${ISD}3"]
cert_files = ["AS${CORE_AS1}/sensitive-voting.pem", "AS${CORE_AS1}/regular-voting.pem", "AS${CORE_AS1}/cp-root.pem", "AS${CORE_AS2}/cp-root.pem", "AS${CORE_AS3}/sensitive-voting.pem", "AS${CORE_AS3}/regular-voting.pem"]

[validity]
not_before = $(date +%s)
validity = "365d"
EOF

scion-pki trc payload --out=tmp/ISD${ISD_NUM}-B1-S1.pld.der --template trc-B1-S1-pld.tmpl
rm trc-B1-S1-pld.tmpl

# Sign and bundle TRC
scion-pki trc sign tmp/ISD${ISD_NUM}-B1-S1.pld.der AS${CORE_AS1}/sensitive-voting.{pem,key} --out tmp/ISD${ISD_NUM}-B1-S1.AS${CORE_AS1}-sensitive.trc
scion-pki trc sign tmp/ISD${ISD_NUM}-B1-S1.pld.der AS${CORE_AS1}/regular-voting.{pem,key} --out tmp/ISD${ISD_NUM}-B1-S1.AS${CORE_AS1}-regular.trc
scion-pki trc sign tmp/ISD${ISD_NUM}-B1-S1.pld.der AS${CORE_AS3}/sensitive-voting.{pem,key} --out tmp/ISD${ISD_NUM}-B1-S1.AS${CORE_AS3}-sensitive.trc
scion-pki trc sign tmp/ISD${ISD_NUM}-B1-S1.pld.der AS${CORE_AS3}/regular-voting.{pem,key} --out tmp/ISD${ISD_NUM}-B1-S1.AS${CORE_AS3}-regular.trc

scion-pki trc combine tmp/ISD${ISD_NUM}-B1-S1.AS${CORE_AS1}-{sensitive,regular}.trc tmp/ISD${ISD_NUM}-B1-S1.AS${CORE_AS3}-{sensitive,regular}.trc --payload tmp/ISD${ISD_NUM}-B1-S1.pld.der --out ISD${ISD_NUM}-B1-S1.trc
rm tmp -r

# Create CA certificates
pushd AS${CORE_AS1}
scion-pki certificate create --profile=cp-ca <(echo "{\"isd_as\": \"${ISD_NUM}-ffaa:1:${ISD}1\", \"common_name\": \"${ISD_NUM}-ffaa:1:${ISD}1 CA cert\"}") cp-ca.pem cp-ca.key --ca cp-root.pem --ca-key cp-root.key
popd
pushd AS${CORE_AS2}
scion-pki certificate create --profile=cp-ca <(echo "{\"isd_as\": \"${ISD_NUM}-ffaa:1:${ISD}2\", \"common_name\": \"${ISD_NUM}-ffaa:1:${ISD}2 CA cert\"}") cp-ca.pem cp-ca.key --ca cp-root.pem --ca-key cp-root.key
popd

# Create AS certificates for all ASes
for as_num in $(seq $AS_START $AS_END); do
    as_idx=$((as_num - AS_START + 1))
    # Use first CA for odd ASes, second CA for even ASes
    if [ $((as_idx % 2)) -eq 1 ]; then
        ca_as=${CORE_AS1}
    else
        ca_as=${CORE_AS2}
    fi
    
    scion-pki certificate create --profile=cp-as <(echo "{\"isd_as\": \"${ISD_NUM}-ffaa:1:${ISD}${as_idx}\", \"common_name\": \"${ISD_NUM}-ffaa:1:${ISD}${as_idx} AS cert\"}") AS${as_num}/cp-as.pem AS${as_num}/cp-as.key --ca AS${ca_as}/cp-ca.pem --ca-key AS${ca_as}/cp-ca.key --bundle
done

echo "PKI generation complete for ISD ${ISD}"
cp -r /tmp/tutorial-scion-certs-isd0${ISD} /shared/