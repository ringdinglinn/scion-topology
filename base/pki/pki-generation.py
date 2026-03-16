#!/usr/bin/env python3
import yaml
import subprocess
import os
import shutil
import pathlib
from datetime import datetime

CONFIG_PATH = "/tmp/isds.yaml"

def generate_isd_pki(isd_id: int, as_start: int, as_count: int, core: list[int]):
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

    def create_core_certs(as_num, isd_num, isd_id):
        create_cert(f"AS{as_start + as_num - 1}", "sensitive-voting",
            f"{isd_num}-ffaa:{isd_id}:{as_num}",
            f"{isd_num}-ffaa:{isd_id}:{as_num} sensitive voting cert",
            "sensitive-voting.pem", "sensitive-voting.key")
        
        create_cert(f"AS{as_start + as_num - 1}", "regular-voting",
                f"{isd_num}-ffaa:{isd_id}:{as_num}",
                f"{isd_num}-ffaa:{isd_id}:{as_num} regular voting cert",
                "regular-voting.pem", "regular-voting.key")

        create_cert(f"AS{as_start + as_num - 1}", "cp-root",
                f"{isd_num}-ffaa:{isd_id}:{as_num}",
                f"{isd_num}-ffaa:{isd_id}:{as_num} cp root cert",
                "cp-root.pem", "cp-root.key")
    
    for core_as in core:
        create_core_certs(core_as, ISD_NUM, isd_id)

    # Generate TRC payload
    tmp_dir = pathlib.Path("tmp")
    tmp_dir.mkdir(exist_ok=True)

    trc_payload = pathlib.Path("trc-B1-S1-pld.tmpl")
    core_ases = [f"ffaa:{isd_id}:{as_num}" for as_num in core]
    cert_files = [
        path
        for as_num in core
        for path in (
            f"AS{as_start + as_num - 1}/sensitive-voting.pem",
            f"AS{as_start + as_num - 1}/regular-voting.pem",
            f"AS{as_start + as_num - 1}/cp-root.pem",
        )
    ]

    with open(trc_payload, "w") as f:
        f.write(f"""isd = {ISD_NUM}
    description = "ISD {ISD_NUM}"
    serial_version = 1
    base_version = 1
    voting_quorum = {min(2, len(core))} 
    core_ases = {core_ases}
    authoritative_ases = {core_ases}
    cert_files = {cert_files}

    [validity]
    not_before = {int(datetime.now().timestamp())}
    validity = "365d"
    """)

    # Create TRC
    run_scion_pki(["scion-pki", "trc", "payload", "--out", str(tmp_dir / f"ISD{ISD_NUM}-B1-S1.pld.der"), "--template", str(trc_payload)])
    trc_payload.unlink()  # remove template

    # Sign TRCs
    sign_commands = [
        cmd
        for as_num in core
        for cmd in (
            (as_num, "sensitive"),
            (as_num, "regular")
        )
    ]

    for core_as, cert_type in sign_commands:
        crt_file = f"AS{as_start + core_as - 1}/{cert_type}-voting.pem"
        key_file = f"AS{as_start + core_as - 1}/{cert_type}-voting.key"

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
        tmp_dir / f"ISD{ISD_NUM}-B1-S1.AS{as_num}-{t}.trc" for t in ["sensitive", "regular"] for as_num in core
    ]

    run_scion_pki([
        "scion-pki", "trc", "combine",
        *map(str, combined_trcs),
        "--payload", str(tmp_dir / f"ISD{ISD_NUM}-B1-S1.pld.der"),
        "--out", f"ISD{ISD_NUM}-B1-S1.trc"
    ])
    shutil.rmtree(tmp_dir)

    # Create CA certs
    for as_num in core:
        create_cert(f"AS{as_start + as_num - 1}", "cp-ca", f"{ISD_NUM}-ffaa:{isd_id}:{as_num}", f"{ISD_NUM}-ffaa:{isd_id}:{as_num} CA cert", "cp-ca.pem", "cp-ca.key", ca="cp-root.pem", ca_key="cp-root.key")

    # Generate AS certificates
    for as_num in range(as_start, as_start + as_count):
        as_idx = as_num - as_start + 1
        ca_as = as_start + core[as_idx % len(core)] - 1
        create_cert(
            f"AS{as_num}",
            "cp-as",
            f"{ISD_NUM}-ffaa:{isd_id}:{as_idx}",
            f"{ISD_NUM}-ffaa:{isd_id}:{as_idx} AS cert",
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
        core = config["ISDs"][isd_id]["core"]

        generate_isd_pki(
            isd_id=int(isd_id),
            as_start=start_index,
            as_count=n,
            core=core
        )

        start_index += n


if __name__ == "__main__":
    main()

