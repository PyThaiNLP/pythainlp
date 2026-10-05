# SPDX-FileCopyrightText: 2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""
Check the SBOM embedded in a built wheel and copy it out unchanged.

The release workflow (``pypi-publish.yml``) embeds an SPDX 3 SBOM into the
wheel (PEP 770). This script fails unless:

1. ``DIST_DIR`` holds exactly one wheel.
2. The wheel has exactly one ``*.dist-info/sboms/*.spdx3.json`` member.
3. Every member of the wheel, including the SBOM, matches its ``RECORD``
   hash.
4. Every ``software_File`` the SBOM lists is a payload file: none is under
   ``.dist-info/``, whose files the embedding itself rewrites.
5. Every SHA-256 the SBOM records for a file matches that file in the
   wheel.

The SBOM bytes are then written to ``OUT_DIR`` under the same file name,
so the release can attach the very SBOM the wheel carries.

Usage::

    python check_wheel_sbom.py DIST_DIR OUT_DIR [--github-output FILE]

``--github-output`` appends ``wheel-path``, ``sbom-name`` and
``sbom-path`` to ``FILE``. Errors print ``ERROR: ...`` and exit 1.
"""

from __future__ import annotations

import argparse
import base64
import csv
import hashlib
import io
import json
import sys
import zipfile
from pathlib import Path, PurePosixPath


class SbomCheckError(ValueError):
    """The wheel or its embedded SBOM fails a check."""


def _record_digest(data: bytes) -> str:
    digest = base64.urlsafe_b64encode(hashlib.sha256(data).digest())
    return "sha256=" + digest.decode("ascii").rstrip("=")


def _find_wheel(dist_dir: Path) -> Path:
    wheels = sorted(dist_dir.glob("*.whl"))
    if len(wheels) != 1:
        raise SbomCheckError(
            f"expected one wheel in {dist_dir}, found {len(wheels)}"
        )
    return wheels[0]


def _find_sbom(names: list[str]) -> str:
    sboms = [
        name
        for name in names
        if PurePosixPath(name).parent.name == "sboms"
        and PurePosixPath(name).parent.parent.name.endswith(".dist-info")
        and len(PurePosixPath(name).parts) == 3
    ]
    if len(sboms) != 1 or not sboms[0].endswith(".spdx3.json"):
        raise SbomCheckError(
            f"expected one *.dist-info/sboms/*.spdx3.json, found {sboms}"
        )
    return sboms[0]


def _check_record(wheel: zipfile.ZipFile, dist_info: str) -> None:
    record_name = f"{dist_info}/RECORD"
    with wheel.open(record_name) as raw:
        text = io.TextIOWrapper(raw, encoding="utf-8", newline="")
        record = {row[0]: row[1] for row in csv.reader(text) if row}
    for name in wheel.namelist():
        if name == record_name or name.endswith("/"):
            continue
        expected = _record_digest(wheel.read(name))
        if record.get(name) != expected:
            raise SbomCheckError(
                f"RECORD hash of {name} is {record.get(name)!r}, "
                f"not {expected!r}"
            )


def _check_sbom_files(wheel: zipfile.ZipFile, sbom: bytes) -> None:
    members = set(wheel.namelist())
    graph = json.loads(sbom).get("@graph", [])
    files = [e for e in graph if e.get("type") == "software_File"]
    if not files:
        raise SbomCheckError("SBOM lists no software_File")
    for element in files:
        name = str(element.get("name", ""))
        if ".dist-info/" in f"{name}/":
            raise SbomCheckError(f"SBOM lists a .dist-info file: {name}")
        hashes = [
            h.get("hashValue")
            for h in element.get("verifiedUsing", [])
            if h.get("algorithm") == "sha256"
        ]
        if not hashes:
            continue
        if name not in members:
            raise SbomCheckError(f"SBOM file {name} is not in the wheel")
        actual = hashlib.sha256(wheel.read(name)).hexdigest()
        if hashes[0] != actual:
            raise SbomCheckError(
                f"SBOM SHA-256 of {name} is {hashes[0]}, not {actual}"
            )


def check_and_extract(dist_dir: Path, out_dir: Path) -> tuple[Path, Path]:
    """Check the wheel in *dist_dir* and copy its SBOM to *out_dir*.

    :param pathlib.Path dist_dir: directory holding exactly one wheel
    :param pathlib.Path out_dir: directory to write the SBOM into
    :return: the wheel path and the extracted SBOM path
    :rtype: tuple[pathlib.Path, pathlib.Path]
    :raises SbomCheckError: if any check fails
    """
    wheel_path = _find_wheel(dist_dir)
    try:
        with zipfile.ZipFile(wheel_path) as wheel:
            sbom_name = _find_sbom(wheel.namelist())
            sbom = wheel.read(sbom_name)
            dist_info = str(PurePosixPath(sbom_name).parent.parent)
            _check_record(wheel, dist_info)
            _check_sbom_files(wheel, sbom)
    except (KeyError, OSError, ValueError, zipfile.BadZipFile) as exc:
        if isinstance(exc, SbomCheckError):
            raise
        raise SbomCheckError(f"cannot read {wheel_path}: {exc}") from exc
    out_dir.mkdir(parents=True, exist_ok=True)
    sbom_path = out_dir / PurePosixPath(sbom_name).name
    sbom_path.write_bytes(sbom)
    return wheel_path, sbom_path


def main() -> int:
    """Run the command line interface.

    :return: exit code
    :rtype: int
    """
    parser = argparse.ArgumentParser(
        description="Check the SBOM embedded in a wheel and copy it out."
    )
    parser.add_argument("dist_dir", type=Path)
    parser.add_argument("out_dir", type=Path)
    parser.add_argument("--github-output", type=Path)
    args = parser.parse_args()
    try:
        wheel_path, sbom_path = check_and_extract(args.dist_dir, args.out_dir)
    except SbomCheckError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(f"WHEEL={wheel_path} SBOM={sbom_path}")
    if args.github_output:
        with args.github_output.open("a", encoding="utf-8", newline="\n") as f:
            f.write(f"wheel-path={wheel_path}\n")
            f.write(f"sbom-name={sbom_path.name}\n")
            f.write(f"sbom-path={sbom_path}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
