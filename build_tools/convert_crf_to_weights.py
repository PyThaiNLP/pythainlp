# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""
Convert python-crfsuite binary models to compressed JSON weights.

Usage:
    python build_tools/convert_crf_to_weights.py
"""

from __future__ import annotations

import argparse
import gzip
import json
import os
import tempfile
from typing import Optional

_SECTIONS = {
    "ATTRIBUTES",
    "FILEHEADER",
    "LABELS",
    "STATE_FEATURES",
    "TRANSITIONS",
}


def _parse_weight(weight: str) -> Optional[float]:
    mantissa, exponent_separator, exponent = weight.lower().partition("e")
    if exponent_separator:
        if exponent[:1] in ("+", "-"):
            exponent = exponent[1:]
        if not exponent.isdecimal():
            return None

    if mantissa[:1] in ("+", "-"):
        mantissa = mantissa[1:]
    integer, decimal_separator, fraction = mantissa.partition(".")
    if not integer.isdecimal() or (
        decimal_separator and not fraction.isdecimal()
    ):
        return None
    return float(weight)


def _parse_section_header(line: str) -> Optional[str]:
    section, separator, _ = line.partition(" = {")
    if separator and section in _SECTIONS:
        return section
    return None


def _parse_label_line(
    line: str,
    labels: dict[int, str],
    current_id: Optional[int],
    current_lines: list[str],
) -> tuple[Optional[int], list[str]]:
    label_id, separator, label = line.lstrip().partition(":")
    if not separator or not label_id.isdecimal():
        current_lines.append(line)
        return current_id, current_lines

    if current_id is not None:
        labels[current_id] = "\n".join(current_lines)

    if label[:1].isspace():
        label = label[1:]
    return int(label_id), [label]


def _parse_weighted_row(
    line: str, use_last_arrow: bool
) -> Optional[tuple[str, str, float]]:
    row_id, separator, row = line.lstrip().partition(")")
    if (
        not separator
        or not row_id.startswith("(")
        or not row_id[1:].isdecimal()
        or not row[:1].isspace()
    ):
        return None

    row, separator, weight = row.lstrip().rpartition(":")
    if not separator or not weight[:1].isspace():
        return None

    parsed_weight = _parse_weight(weight.lstrip())
    if parsed_weight is None:
        return None

    arrow_index = row.rfind("-->") if use_last_arrow else row.find("-->")
    if arrow_index < 0:
        return None

    left, right = row[:arrow_index], row[arrow_index + 3 :]
    if not left[-1:].isspace() or not right[:1].isspace():
        return None

    return left.rstrip(), right.lstrip(), parsed_weight


def _finish_label_section(
    section: str,
    current_id: Optional[int],
    labels: dict[int, str],
    current_lines: list[str],
) -> tuple[Optional[int], list[str]]:
    if section == "LABELS" and current_id is not None:
        labels[current_id] = "\n".join(current_lines)
        return None, []
    return current_id, current_lines


def _store_weighted_row(
    line: str,
    section: str,
    transitions: dict[str, float],
    state_features: dict[str, dict[str, float]],
) -> None:
    weighted_row = _parse_weighted_row(line, section == "TRANSITIONS")
    if weighted_row is None:
        return

    left, right, weight = weighted_row
    if section == "TRANSITIONS":
        transitions[f"{left}->{right}"] = weight
    else:
        state_features.setdefault(left, {})[right] = weight


def parse_dump_file(
    dump_path: str,
) -> tuple[list[str], dict[str, float], dict[str, dict[str, float]]]:
    """
    Parse a CRFsuite dump text file into model weights.

    :param str dump_path: Path to dumped plain-text CRF model.
    :return: Tuple of (labels_list, transitions_dict, state_features_dict).
    :rtype: tuple[list[str], dict[str, float], dict[str, dict[str, float]]]
    """
    labels: dict[int, str] = {}
    transitions: dict[str, float] = {}
    state_features: dict[str, dict[str, float]] = {}

    section: str = ""
    curr_id: Optional[int] = None
    curr_str: list[str] = []

    with open(dump_path, encoding="utf-8", errors="replace") as file_obj:
        for line in file_obj:
            line_str = line.rstrip("\r\n")
            next_section = _parse_section_header(line_str)
            if next_section:
                section = next_section
                continue

            if line_str == "}":
                curr_id, curr_str = _finish_label_section(
                    section, curr_id, labels, curr_str
                )
                section = ""
                continue

            if section == "LABELS":
                curr_id, curr_str = _parse_label_line(
                    line_str, labels, curr_id, curr_str
                )
            elif section in ("TRANSITIONS", "STATE_FEATURES"):
                _store_weighted_row(
                    line_str, section, transitions, state_features
                )

    label_list = [labels[i] for i in range(len(labels))]
    return label_list, transitions, state_features


def convert_crfsuite_model(src_path: str, dst_path: str) -> None:
    """
    Dump a CRFsuite binary model and save as compressed JSON weights.

    :param str src_path: Path to input .crfsuite / .model file.
    :param str dst_path: Path to output .json.gz file.
    """
    import pycrfsuite

    tagger = pycrfsuite.Tagger()
    tagger.open(src_path)
    with tempfile.NamedTemporaryFile("w+", delete=False) as temp_file:
        dump_name = temp_file.name
        tagger.dump(dump_name)

    try:
        labels, transitions, state_features = parse_dump_file(dump_name)
    finally:
        if os.path.exists(dump_name):
            os.unlink(dump_name)

    weights_data = {
        "labels": labels,
        "transitions": transitions,
        "state_features": state_features,
    }

    with gzip.open(dst_path, "wt", encoding="utf-8") as out_file:
        json.dump(weights_data, out_file, ensure_ascii=False)

    orig_kb = os.path.getsize(src_path) / 1024
    new_kb = os.path.getsize(dst_path) / 1024
    print(
        f"Converted: {src_path} ({orig_kb:.1f} KB) -> "
        f"{dst_path} ({new_kb:.1f} KB, "
        f"{((orig_kb - new_kb) / orig_kb) * 100:.1f}% reduction)"
    )


def main() -> None:
    """Entry point for conversion."""
    parser = argparse.ArgumentParser(
        description="Convert crfsuite models to json.gz weights."
    )
    parser.add_argument("--src", help="Source crfsuite model file")
    parser.add_argument("--dst", help="Destination json.gz file")
    args = parser.parse_args()

    if args.src and args.dst:
        convert_crfsuite_model(args.src, args.dst)
        return

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    corpus_dir = os.path.join(base_dir, "pythainlp", "corpus")

    models_to_convert = [
        ("han_solo.crfsuite", "han_solo.json.gz"),
        ("crfchunk_orchidpp.model", "crfchunk_orchidpp.json.gz"),
        ("thainer_crf_1_5_1.model", "thainer_crf_1_5_1.json.gz"),
        ("sentenceseg_crfcut.model", "sentenceseg_crfcut.json.gz"),
        ("crf3_mix.crfsuite2", "ssg.json.gz"),
        ("ssg.crfsuite", "ssg.json.gz"),
    ]

    for src_name, dst_name in models_to_convert:
        src = os.path.join(corpus_dir, src_name)
        dst = os.path.join(corpus_dir, dst_name)
        if os.path.exists(src):
            convert_crfsuite_model(src, dst)


if __name__ == "__main__":
    main()
