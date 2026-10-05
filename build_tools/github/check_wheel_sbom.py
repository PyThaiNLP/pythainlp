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
4. Every payload file (every file outside ``.dist-info/``) is listed in the
   SBOM as a ``software_File`` with a SHA-256 that matches the file.
5. No ``software_File`` in the SBOM is under ``.dist-info/``, whose files
   the embedding itself rewrites, and every listed file that is not a
   directory is in the wheel.

The SBOM bytes are then written to ``OUT_DIR`` under the same file name,
so the release can attach the very SBOM the wheel carries.

``DIST_DIR`` and ``OUT_DIR`` must be inside the current working
directory. The wheel and SBOM file names must use only ASCII letters,
digits, ``.``, ``_``, ``+`` and ``-``.

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
import re
import sys
import zipfile
from pathlib import Path, PurePosixPath
from typing import Any, Optional

# File names written to $GITHUB_OUTPUT and to OUT_DIR: no path separator,
# drive letter, glob character, space or line break.
_SAFE_NAME = re.compile(r"[A-Za-z0-9._+-]+")
_SBOM_MEMBER = re.compile(r"[^/]+\.dist-info/sboms/[^/]+")


class SbomCheckError(ValueError):
    """The wheel or its embedded SBOM fails a check."""


def _record_digest(data: bytes) -> str:
    digest = base64.urlsafe_b64encode(hashlib.sha256(data).digest())
    return "sha256=" + digest.decode("ascii").rstrip("=")


def _check_name(name: str, what: str) -> str:
    if _SAFE_NAME.fullmatch(name) is None or name in {".", ".."}:
        raise SbomCheckError(f"unsafe {what} file name: {name!r}")
    return name


def _contained(base: Path, path: Path, what: str) -> Path:
    """Return *path* resolved, if it is *base* or inside it.

    Same rule as :func:`pythainlp.tools.safe_path_join`, which this script
    cannot import: the build job does not install PyThaiNLP.
    """
    resolved_base = base.resolve()
    resolved = (resolved_base / path).resolve()
    if resolved != resolved_base and resolved_base not in resolved.parents:
        raise SbomCheckError(
            f"{what} {str(path)!r} is outside {str(resolved_base)!r}"
        )
    return resolved


def _find_wheel(dist_dir: Path) -> Path:
    wheels = sorted(dist_dir.glob("*.whl"))
    if len(wheels) != 1:
        raise SbomCheckError(
            f"expected one wheel in {dist_dir}, found {len(wheels)}"
        )
    _check_name(wheels[0].name, "wheel")
    return wheels[0]


def _find_sbom(names: list[str]) -> str:
    sboms = [name for name in names if _SBOM_MEMBER.fullmatch(name)]
    if len(sboms) != 1 or not sboms[0].endswith(".spdx3.json"):
        raise SbomCheckError(
            f"expected one *.dist-info/sboms/*.spdx3.json, found {sboms}"
        )
    _check_name(PurePosixPath(sboms[0]).name, "SBOM")
    return sboms[0]


def _check_record(wheel: zipfile.ZipFile, dist_info: str) -> None:
    record_name = f"{dist_info}/RECORD"
    with wheel.open(record_name) as raw:
        text = io.TextIOWrapper(raw, encoding="utf-8", newline="")
        record = {row[0]: row[1] for row in csv.reader(text) if len(row) > 1}
    for name in wheel.namelist():
        if name == record_name or name.endswith("/"):
            continue
        expected = _record_digest(wheel.read(name))
        if record.get(name) != expected:
            raise SbomCheckError(
                f"RECORD hash of {name} is {record.get(name)!r}, "
                f"not {expected!r}"
            )


def _as_list(value: Any, what: str) -> list[Any]:
    if not isinstance(value, list):
        raise SbomCheckError(f"{what} is not a JSON array")
    return value


def _sbom_files(sbom: bytes) -> list[dict[str, Any]]:
    """Return the ``software_File`` elements of the SBOM."""
    doc = json.loads(sbom)
    if not isinstance(doc, dict):
        raise SbomCheckError("SBOM is not a JSON object")
    graph = _as_list(doc.get("@graph"), "SBOM @graph")
    if not all(isinstance(e, dict) for e in graph):
        raise SbomCheckError("SBOM @graph has an item that is not an object")
    return [e for e in graph if e.get("type") == "software_File"]


def _sha256_of(element: dict[str, Any]) -> Optional[str]:
    for h in _as_list(element.get("verifiedUsing", []), "verifiedUsing"):
        if isinstance(h, dict) and h.get("algorithm") == "sha256":
            return str(h.get("hashValue"))
    return None


def _listed_hashes(
    files: list[dict[str, Any]], members: set[str]
) -> dict[str, Optional[str]]:
    """Map each listed file name to its SHA-256, checking where it is."""
    listed: dict[str, Optional[str]] = {}
    for element in files:
        name = str(element.get("name", ""))
        if ".dist-info/" in f"{name}/":
            raise SbomCheckError(f"SBOM lists a .dist-info file: {name}")
        is_dir = element.get("software_fileKind") == "directory"
        if not is_dir and name not in members:
            raise SbomCheckError(f"SBOM file {name} is not in the wheel")
        listed[name] = _sha256_of(element)
    return listed


def _check_sbom_files(wheel: zipfile.ZipFile, sbom: bytes) -> None:
    members = set(wheel.namelist())
    listed = _listed_hashes(_sbom_files(sbom), members)
    payload = sorted(
        name
        for name in members
        if not name.endswith("/") and ".dist-info/" not in name
    )
    if not payload:
        raise SbomCheckError("wheel has no payload file")
    for name in payload:
        if name not in listed:
            raise SbomCheckError(f"SBOM does not list payload file {name}")
        actual = hashlib.sha256(wheel.read(name)).hexdigest()
        if listed[name] != actual:
            raise SbomCheckError(
                f"SBOM SHA-256 of {name} is {listed[name]}, not {actual}"
            )


def check_and_extract(dist_dir: Path, out_dir: Path) -> tuple[Path, Path]:
    """Check the wheel in *dist_dir* and copy its SBOM to *out_dir*.

    :param pathlib.Path dist_dir: directory holding exactly one wheel,
        inside the current working directory
    :param pathlib.Path out_dir: directory to write the SBOM into,
        inside the current working directory
    :return: the wheel path and the extracted SBOM path
    :rtype: tuple[pathlib.Path, pathlib.Path]
    :raises SbomCheckError: if any check fails
    """
    cwd = Path.cwd()
    dist_dir = _contained(cwd, dist_dir, "DIST_DIR")
    out_dir = _contained(cwd, out_dir, "OUT_DIR")
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
    sbom_path = _contained(
        out_dir, Path(PurePosixPath(sbom_name).name), "SBOM path"
    )
    out_dir.mkdir(parents=True, exist_ok=True)
    sbom_path.write_bytes(sbom)
    return wheel_path.relative_to(cwd.resolve()), sbom_path.relative_to(
        cwd.resolve()
    )


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
            f.write(f"wheel-path={wheel_path.as_posix()}\n")
            f.write(f"sbom-name={sbom_path.name}\n")
            f.write(f"sbom-path={sbom_path.as_posix()}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
