#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""
Show and edit the metadata of ONNX model files.

The script needs the ``onnx`` package. It is a maintainer tool, not a
dependency of PyThaiNLP. It does not read any PyThaiNLP file, such as the
corpus catalog.

Usage::

    python build_tools/onnx_metadata.py show [--json] [PATH ...]
    python build_tools/onnx_metadata.py set PATH [FIELD ...] [--dry-run]

Without a path, ``show`` lists every ``.onnx`` file in ``pythainlp/corpus``.

Fields of ``set``, and the ONNX metadata each one is written to:

* ``--name`` - name of the model: ``graph.name`` (ONNX has no separate
  model name)
* ``--doc`` - description of the model: ``doc_string``
* ``--domain`` - reverse-domain namespace of the model: ``domain``
* ``--version`` - version as ``MAJOR.MINOR.PATCH``: ``model_version``,
  packed into one integer
* ``--license`` - license: ``metadata_props["model_license"]``
* ``--author`` - comma-separated authors:
  ``metadata_props["model_author"]``
* ``--prop KEY=VALUE`` - any other entry: ``metadata_props[KEY]``
  (repeatable)

``set`` keeps all other metadata. It refuses a read-only file, or a model
with duplicate ``metadata_props`` keys. After a write, update the checksum
of the file in the corpus catalog by hand.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import re
import shutil
import sys
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:
    from collections.abc import Sequence
    from typing import NoReturn

    from onnx import ModelProto

_CORPUS_DIR = Path(__file__).resolve().parent.parent / "pythainlp" / "corpus"

_NUMBER = r"(0|[1-9][0-9]*)"  # no leading zeros
_SEMVER = re.compile(rf"{_NUMBER}\.{_NUMBER}\.{_NUMBER}")

# model_version is an int64: MAJOR in bits 48-62, MINOR in bits 32-47,
# PATCH in bits 0-31.
_MAX_MAJOR = (1 << 15) - 1
_MAX_MINOR = (1 << 16) - 1
_MAX_PATCH = (1 << 32) - 1

_LICENSE_KEY = "model_license"
_AUTHOR_KEY = "model_author"


def semver_to_int(version: str) -> int:
    """
    Pack a ``MAJOR.MINOR.PATCH`` version into an ONNX ``model_version``.

    :param str version: version such as ``"1.0.1"``
    :return: packed integer
    :rtype: int
    :raises ValueError: if version cannot be stored: it is not
        ``MAJOR.MINOR.PATCH`` in plain digits without leading zeros, or a
        part is over its limit
    """
    match = _SEMVER.fullmatch(version)
    if match is None:
        raise ValueError(
            f"Version {version!r} cannot be stored in the ONNX model_version "
            "integer: use MAJOR.MINOR.PATCH in digits, without leading zeros"
        )
    major, minor, patch = (int(part) for part in match.groups())
    if major > _MAX_MAJOR or minor > _MAX_MINOR or patch > _MAX_PATCH:
        raise ValueError(
            f"Version {version!r} cannot be stored in the ONNX model_version "
            f"integer: MAJOR is at most {_MAX_MAJOR}, MINOR at most "
            f"{_MAX_MINOR}, PATCH at most {_MAX_PATCH}"
        )
    return (major << 48) | (minor << 32) | patch


def int_to_semver(value: int) -> str:
    """
    Unpack an ONNX ``model_version`` into ``MAJOR.MINOR.PATCH``.

    :param int value: packed integer from :func:`semver_to_int`
    :return: version such as ``"1.0.1"``
    :rtype: str
    """
    major = value >> 48
    minor = (value >> 32) & _MAX_MINOR
    patch = value & _MAX_PATCH
    return f"{major}.{minor}.{patch}"


def parse_prop(text: str) -> tuple[str, str]:
    """
    Split a ``KEY=VALUE`` argument.

    :param str text: argument such as ``"source=https://example.org"``
    :return: key and value
    :rtype: tuple[str, str]
    :raises ValueError: if text has no ``=`` or the key is empty
    """
    key, sep, value = text.partition("=")
    if not sep or not key:
        raise ValueError(f"Property must be KEY=VALUE: {text!r}")
    return key, value


def duplicate_keys(model: ModelProto) -> list[str]:
    """
    List the keys that appear more than once in ``metadata_props``.

    :param onnx.ModelProto model: loaded model
    :return: sorted duplicate keys
    :rtype: list[str]
    """
    keys = [p.key for p in model.metadata_props]
    return sorted({key for key in keys if keys.count(key) > 1})


def read_metadata(model: ModelProto) -> dict[str, Any]:
    """
    Collect the metadata of a model.

    :param onnx.ModelProto model: loaded model
    :return: metadata fields; ``metadata_props`` holds all key/value entries
    :rtype: dict[str, Any]
    """
    return {
        "ir_version": model.ir_version,
        "opset": {
            (item.domain or "ai.onnx"): item.version
            for item in model.opset_import
        },
        "producer_name": model.producer_name,
        "producer_version": model.producer_version,
        "domain": model.domain,
        "model_version": int_to_semver(model.model_version),
        "model_version_raw": model.model_version,
        "graph_name": model.graph.name,
        "doc_string": model.doc_string,
        "metadata_props": {p.key: p.value for p in model.metadata_props},
    }


def requested_changes(
    args: argparse.Namespace,
) -> tuple[dict[str, str], dict[str, str]]:
    """
    Collect the values given to ``set``.

    :param argparse.Namespace args: parsed ``set`` arguments
    :return: fields (``graph_name``, ``doc_string``, ``domain``,
        ``model_version``) and ``metadata_props`` entries, as given
    :rtype: tuple[dict[str, str], dict[str, str]]
    :raises ValueError: if the version or a property cannot be stored
    """
    given = {
        "doc_string": args.doc,
        "domain": args.domain,
        "graph_name": args.name,
        "model_version": args.version,
    }
    fields = {k: v for k, v in given.items() if v is not None}
    if "model_version" in fields:
        semver_to_int(fields["model_version"])  # reject early

    pairs = [parse_prop(text) for text in args.prop]
    if args.license is not None:
        pairs.append((_LICENSE_KEY, args.license))
    if args.author is not None:
        pairs.append((_AUTHOR_KEY, args.author))
    props: dict[str, str] = {}
    for key, value in pairs:
        if key in props:
            raise ValueError(
                f"Property {key!r} is given more than once "
                "(--license and --author also set model_license "
                "and model_author)"
            )
        props[key] = value
    return fields, props


def apply_changes(
    model: ModelProto, args: argparse.Namespace
) -> tuple[dict[str, tuple[str, str]], dict[str, Any]]:
    """
    Set the requested fields on a model.

    :param onnx.ModelProto model: loaded model, changed in place
    :param argparse.Namespace args: parsed ``set`` arguments
    :return: changed fields as ``{field: (old, new)}``, and the metadata
        that must be read back from the saved file (see
        :func:`read_metadata`)
    :rtype: tuple[dict[str, tuple[str, str]], dict[str, Any]]
    :raises ValueError: if the version or a property cannot be stored, or
        the model has duplicate ``metadata_props`` keys
    """
    from onnx import helper

    duplicates = duplicate_keys(model)
    if duplicates:
        raise ValueError(
            f"metadata_props has duplicate keys {duplicates}; "
            "the file is not rewritten"
        )
    fields, wanted_props = requested_changes(args)
    before = read_metadata(model)
    expected = {
        **before,
        **fields,
        "metadata_props": {**before["metadata_props"], **wanted_props},
    }
    if "model_version" in fields:
        expected["model_version_raw"] = semver_to_int(fields["model_version"])

    changes = {
        key: (before["metadata_props"].get(key, ""), value)
        for key, value in wanted_props.items()
        if before["metadata_props"].get(key) != value
    }
    changes.update(
        (field, (before[field], value))
        for field, value in fields.items()
        if before[field] != value
    )

    if "graph_name" in fields:
        model.graph.name = fields["graph_name"]
    if "doc_string" in fields:
        model.doc_string = fields["doc_string"]
    if "domain" in fields:
        model.domain = fields["domain"]
    if "model_version" in fields:
        model.model_version = expected["model_version_raw"]
    # set_model_props() replaces every entry, so pass the merged dict
    helper.set_model_props(model, expected["metadata_props"])
    return changes, expected


def _fingerprint(path: Path) -> tuple[int, str]:
    data = path.read_bytes()
    return len(data), hashlib.md5(data, usedforsecurity=False).hexdigest()


def _require_writable(path: Path) -> None:
    """Raise ValueError if the file or its directory is read-only."""
    real_path = path.resolve()
    if not os.access(real_path, os.W_OK):
        raise ValueError(f"{_display(path)} is read-only; make it writable")
    if not os.access(real_path.parent, os.W_OK):
        raise ValueError(f"The directory of {_display(path)} is read-only")


def _write(model: ModelProto, path: Path) -> None:
    import onnx

    onnx.save(model, str(path))


def _mismatches(path: Path, expected: dict[str, Any]) -> list[str]:
    """Read a file back and list the fields that differ from expected."""
    actual = read_metadata(_load(path))
    return [
        f"{key}: given {value!r}, read back {actual.get(key)!r}"
        for key, value in expected.items()
        if value != actual.get(key)
    ]


def _check_read_back(path: Path, expected: dict[str, Any], note: str) -> None:
    problems = _mismatches(path, expected)
    if problems:
        details = "\n  ".join(problems)
        raise ValueError(f"Read-back check failed ({note}):\n  {details}")


def _save_verified(
    model: ModelProto, path: Path, expected: dict[str, Any]
) -> None:
    """
    Save a model, then read it back and compare it with the given values.

    The model goes to a uniquely named temporary file first. The original is
    replaced, with its permissions kept, only if that file reads back as
    expected. The replaced file is read back again.
    """
    real_path = path.resolve()  # replace the target of a symbolic link
    handle, tmp_name = tempfile.mkstemp(
        dir=real_path.parent, prefix=f".{real_path.name}.", suffix=".tmp"
    )
    os.close(handle)
    tmp_path = Path(tmp_name)
    try:
        _write(model, tmp_path)
        _check_read_back(tmp_path, expected, "file not changed")
        shutil.copymode(real_path, tmp_path)
        tmp_path.replace(real_path)
    finally:
        tmp_path.unlink(missing_ok=True)
    _check_read_back(real_path, expected, "file was replaced")


def _format_text(path: Path, info: dict[str, Any]) -> str:
    props = info["metadata_props"]
    opset = ", ".join(f"{k}={v}" for k, v in info["opset"].items())
    producer = f"{info['producer_name']} {info['producer_version']}".strip()
    lines = [
        str(path),
        f"  ir_version       {info['ir_version']}",
        f"  opset            {opset}",
        f"  producer         {producer}",
        f"  domain           {info['domain']}",
        f"  model_version    {info['model_version_raw']}"
        f"  ({info['model_version']})",
        f"  graph.name       {info['graph_name']}",
        f"  doc_string       {info['doc_string']}",
    ]
    lines.extend(f"  {key:<16} {value}" for key, value in props.items())
    return "\n".join(lines)


def _load(path: Path) -> ModelProto:
    import onnx

    try:
        # keep external tensor data in its own files: only metadata changes
        return onnx.load(str(path), load_external_data=False)
    except OSError:
        raise
    except Exception as err:  # protobuf error types vary
        raise ValueError(f"Cannot read ONNX file {path}: {err}") from err


def _ascii(text: str) -> str:
    """Escape non-ASCII characters, so a Windows console can print them."""
    return text.encode("ascii", "backslashreplace").decode("ascii")


class _AsciiArgumentParser(argparse.ArgumentParser):
    """Argument parser whose error messages are ASCII only."""

    def error(self, message: str) -> NoReturn:
        super().error(_ascii(message))


def _display(path: Path) -> str:
    try:
        return str(path.relative_to(Path.cwd()))
    except ValueError:
        return str(path)


def _show(args: argparse.Namespace) -> int:
    paths = [Path(p) for p in args.paths] or sorted(_CORPUS_DIR.glob("*.onnx"))
    infos = []
    for path in paths:
        model = _load(path)
        info = read_metadata(model)
        info["path"] = _display(path)
        info["duplicate_keys"] = duplicate_keys(model)
        if info["duplicate_keys"]:
            print(
                _ascii(
                    f"warning: {info['path']}: duplicate metadata_props "
                    f"keys {info['duplicate_keys']}; the last value is shown"
                ),
                file=sys.stderr,
            )
        infos.append(info)
    if args.json:
        print(json.dumps(infos, ensure_ascii=True, indent=2))
    else:
        print("\n".join(_format_text(Path(i["path"]), i) for i in infos))
    return 0


def _set(args: argparse.Namespace) -> int:
    path = Path(args.path)
    model = _load(path)
    changes, expected = apply_changes(model, args)
    print(_display(path))
    if not changes:
        print("  no change")
        return 0
    _require_writable(path)
    for field, (old, new) in changes.items():
        print(f"  {field:<16} {old!r} -> {new!r}")
    if args.dry_run:
        print(f"  dry run: would write {len(changes)} field(s)")
        return 0
    old_size, old_md5 = _fingerprint(path)
    _save_verified(model, path, expected)
    new_size, new_md5 = _fingerprint(path)
    print(f"  size             {old_size} -> {new_size} bytes")
    print(f"  md5              {old_md5} -> {new_md5}")
    print("  verified         read back matches the given values")
    return 0


def build_parser() -> argparse.ArgumentParser:
    """
    Build the command-line parser.

    :return: parser with the ``show`` and ``set`` commands
    :rtype: argparse.ArgumentParser
    """
    parser = _AsciiArgumentParser(
        description="Show and edit the metadata of ONNX model files."
    )
    commands = parser.add_subparsers(dest="command", required=True)

    show = commands.add_parser("show", help="print metadata")
    show.add_argument("paths", nargs="*", help="model files (default: corpus)")
    show.add_argument("--json", action="store_true", help="output JSON")
    show.set_defaults(func=_show)

    edit = commands.add_parser("set", help="change metadata")
    edit.add_argument("path", help="model file")
    edit.add_argument("--name", help="name of the model -> graph.name")
    edit.add_argument("--doc", help="description of the model -> doc_string")
    edit.add_argument("--domain", help="reverse-domain namespace -> domain")
    edit.add_argument(
        "--version",
        help="version as MAJOR.MINOR.PATCH -> model_version (packed integer)",
    )
    edit.add_argument(
        "--license", help='license -> metadata_props["model_license"]'
    )
    edit.add_argument(
        "--author",
        help='comma-separated authors -> metadata_props["model_author"]',
    )
    edit.add_argument(
        "--prop",
        action="append",
        default=[],
        metavar="KEY=VALUE",
        help="any other entry -> metadata_props[KEY] (repeatable)",
    )
    edit.add_argument(
        "--dry-run", action="store_true", help="show changes, write nothing"
    )
    edit.set_defaults(func=_set)
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    """
    Run the command line.

    :param Optional[Sequence[str]] argv: arguments (default: ``sys.argv``)
    :return: exit status; 0 on success
    :rtype: int
    """
    # A Windows console or a redirected stream may not write Thai.
    reconfigure = getattr(sys.stdout, "reconfigure", None)
    if reconfigure is not None:
        reconfigure(encoding="utf-8")

    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "set" and not (
        args.prop
        or any(
            getattr(args, name) is not None
            for name in (
                "name",
                "doc",
                "domain",
                "version",
                "license",
                "author",
            )
        )
    ):
        parser.error("set needs at least one field to change")
    try:
        return int(args.func(args))
    except ImportError as err:
        if importlib.util.find_spec("onnx") is None:
            message = "The onnx package is required: pip install onnx"
        else:
            message = f"Cannot import the onnx package: {err}"
        print(_ascii(message), file=sys.stderr)
    except (OSError, ValueError) as err:
        print(_ascii(f"Error: {err}"), file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
