#!/usr/bin/env python3
import yaml
import subprocess
import os
import shutil
import pathlib
from datetime import datetime

CONFIG_PATH = "/tmp/isds.yaml"

def generate_isd_pki(isd_id: int, as_start: int, as_count: int):
    """
    Generates PKI for a single ISD.
    This function contains the full logic you already implemented.
    """
    print(f"Generating PKI for ISD {isd_id}, start={as_start}, count={as_count}")

    ISD_NUM = 15 + isd_id

    # Create base directory for ISD
    base_dir = f"/tmp/tutorial-scion-certs-isd0{isd_id}"
    os.makedirs(base_dir, exist_ok=True)
    os.chdir(base_dir)

    # Create AS directories
    for as_num in range(as_start, as_start + as_count):
        os.makedirs(f"AS{as_num}", exist_ok=True)   

    # Core ASes
    CORE_AS1 = as_start
    CORE_AS2 = as_start + 1
    CORE_AS3 = as_start + 2

    def run_scion_pki(command, cwd=None):
        print("Running:", " ".join(command))
        subprocess.run(command, check=True, cwd=cwd)

    def create_cert(as_dir, profile, isd_as, common_name,
                    out_pem, out_key, ca=None, ca_key=None, bundle=False, run_from_base=False):

        json_data = f'{{"isd_as": "{isd_as}", "common_name": "{common_name}"}}'

        cmd = [
            "scion-pki", "certificate", "create",
            f"--profile={profile}",
            f"<(echo '{json_data}')",
            out_pem, out_key
        ]

        if ca and ca_key:
            cmd.extend(["--ca", ca, "--ca-key", ca_key])
        if bundle:
            cmd.append("--bundle")

        if run_from_base:
            run_scion_pki(["bash", "-c", " ".join(cmd)])
        else:
            run_scion_pki(["bash", "-c", " ".join(cmd)], cwd=as_dir)



    # Generate core certificates
    create_cert(f"AS{CORE_AS1}", "sensitive-voting",
                f"{ISD_NUM}-ffaa:1:{isd_id}1",
                f"{ISD_NUM}-ffaa:1:{isd_id}1 sensitive voting cert",
                "sensitive-voting.pem", "sensitive-voting.key")

    create_cert(f"AS{CORE_AS1}", "regular-voting",
                f"{ISD_NUM}-ffaa:1:{isd_id}1",
                f"{ISD_NUM}-ffaa:1:{isd_id}1 regular voting cert",
                "regular-voting.pem", "regular-voting.key")

    create_cert(f"AS{CORE_AS1}", "cp-root",
                f"{ISD_NUM}-ffaa:1:{isd_id}1",
                f"{ISD_NUM}-ffaa:1:{isd_id}1 cp root cert",
                "cp-root.pem", "cp-root.key")

    create_cert(f"AS{CORE_AS2}", "cp-root",
                f"{ISD_NUM}-ffaa:1:{isd_id}2",
                f"{ISD_NUM}-ffaa:1:{isd_id}2 cp root cert",
                "cp-root.pem", "cp-root.key")

    create_cert(f"AS{CORE_AS3}", "sensitive-voting",
                f"{ISD_NUM}-ffaa:1:{isd_id}3",
                f"{ISD_NUM}-ffaa:1:{isd_id}3 sensitive voting cert",
                "sensitive-voting.pem", "sensitive-voting.key")

    create_cert(f"AS{CORE_AS3}", "regular-voting",
                f"{ISD_NUM}-ffaa:1:{isd_id}3",
                f"{ISD_NUM}-ffaa:1:{isd_id}3 regular voting cert",
                "regular-voting.pem", "regular-voting.key")

    # Generate TRC payload
    tmp_dir = pathlib.Path("tmp")
    tmp_dir.mkdir(exist_ok=True)

    trc_payload = pathlib.Path("trc-B1-S1-pld.tmpl")
    with open(trc_payload, "w") as f:
        f.write(f"""isd = {ISD_NUM}
    description = "ISD {ISD_NUM}"
    serial_version = 1
    base_version = 1
    voting_quorum = 2

    core_ases = ["ffaa:1:{isd_id}1", "ffaa:1:{isd_id}2", "ffaa:1:{isd_id}3"]
    authoritative_ases = ["ffaa:1:{isd_id}1", "ffaa:1:{isd_id}2", "ffaa:1:{isd_id}3"]
    cert_files = [
        "AS{CORE_AS1}/sensitive-voting.pem", "AS{CORE_AS1}/regular-voting.pem", "AS{CORE_AS1}/cp-root.pem",
        "AS{CORE_AS2}/cp-root.pem",
        "AS{CORE_AS3}/sensitive-voting.pem", "AS{CORE_AS3}/regular-voting.pem"
    ]

    [validity]
    not_before = {int(datetime.now().timestamp())}
    validity = "365d"
    """)

    # Create TRC
    run_scion_pki(["scion-pki", "trc", "payload", "--out", str(tmp_dir / f"ISD{ISD_NUM}-B1-S1.pld.der"), "--template", str(trc_payload)])
    trc_payload.unlink()  # remove template

    # Sign TRCs
    sign_commands = [
        (CORE_AS1, "sensitive"),
        (CORE_AS1, "regular"),
        (CORE_AS3, "sensitive"),
        (CORE_AS3, "regular")
    ]
    for core_as, cert_type in sign_commands:
        crt_file = f"AS{core_as}/{cert_type}-voting.pem"
        key_file = f"AS{core_as}/{cert_type}-voting.key"

        out_file = tmp_dir / f"ISD{ISD_NUM}-B1-S1.AS{core_as}-{cert_type}.trc"

        run_scion_pki([
            "scion-pki", "trc", "sign",
            str(tmp_dir / f"ISD{ISD_NUM}-B1-S1.pld.der"),
            crt_file,
            key_file,
            "--out", str(out_file)
        ])

    # Combine TRCs
    combined_trcs = [
        tmp_dir / f"ISD{ISD_NUM}-B1-S1.AS{CORE_AS1}-{t}.trc" for t in ["sensitive", "regular"]
    ] + [
        tmp_dir / f"ISD{ISD_NUM}-B1-S1.AS{CORE_AS3}-{t}.trc" for t in ["sensitive", "regular"]
    ]
    run_scion_pki([
        "scion-pki", "trc", "combine",
        *map(str, combined_trcs),
        "--payload", str(tmp_dir / f"ISD{ISD_NUM}-B1-S1.pld.der"),
        "--out", f"ISD{ISD_NUM}-B1-S1.trc"
    ])
    shutil.rmtree(tmp_dir)

    # Create CA certs
    create_cert(f"AS{CORE_AS1}", "cp-ca", f"{ISD_NUM}-ffaa:1:{isd_id}1", f"{ISD_NUM}-ffaa:1:{isd_id}1 CA cert", "cp-ca.pem", "cp-ca.key", ca="cp-root.pem", ca_key="cp-root.key")
    create_cert(f"AS{CORE_AS2}", "cp-ca", f"{ISD_NUM}-ffaa:1:{isd_id}2", f"{ISD_NUM}-ffaa:1:{isd_id}2 CA cert", "cp-ca.pem", "cp-ca.key", ca="cp-root.pem", ca_key="cp-root.key")

    # Generate AS certificates
    for as_num in range(as_start, as_start + as_count):
        as_idx = as_num - as_start + 1
        ca_as = CORE_AS1 if as_idx % 2 == 1 else CORE_AS2
        create_cert(
            f"AS{as_start + as_num}",
            "cp-as",
            f"{ISD_NUM}-ffaa:1:{isd_id}{as_idx}",
            f"{ISD_NUM}-ffaa:1:{isd_id}{as_idx} AS cert",
            f"AS{as_num}/cp-as.pem",
            f"AS{as_num}/cp-as.key",
            ca=f"AS{ca_as}/cp-ca.pem",
            ca_key=f"AS{ca_as}/cp-ca.key",
            bundle=True,
            run_from_base=True
        )
        
    # Ensure /opt/tutorial-pki exists
    os.makedirs("/opt/tutorial-pki", exist_ok=True)

    # Copy the ISD PKI into /opt/tutorial-pki/
    shutil.copytree(base_dir, f"/opt/tutorial-pki/", dirs_exist_ok=True)
    print(f"PKI generation complete for ISD {isd_id}, copied to /opt/tutorial-pki/")



def main():
    with open(CONFIG_PATH, "r") as f:
        config = yaml.safe_load(f)

    start_index = 1

    # Ensure deterministic ordering
    for isd_id in sorted(config["ISDs"].keys(), key=int):
        n = config["ISDs"][isd_id]["n"]

        generate_isd_pki(
            isd_id=int(isd_id),
            as_start=start_index,
            as_count=n
        )

        start_index += n


if __name__ == "__main__":
    main()

