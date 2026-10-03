# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Convert python-crfsuite binary models to compressed JSON weights.

Usage:
    python build_tools/convert_crf_to_weights.py
"""

from __future__ import annotations

import argparse
import gzip
import json
import os
import re
import tempfile
from typing import Dict, List, Optional, Tuple


def parse_dump_file(
    dump_path: str,
) -> Tuple[List[str], Dict[str, float], Dict[str, Dict[str, float]]]:
    """Parse a crfsuite dump text file into model weights.

    :param str dump_path: Path to dumped plain-text CRF model.
    :return: Tuple of (labels_list, transitions_dict, state_features_dict).
    :rtype: Tuple[List[str], Dict[str, float], Dict[str, Dict[str, float]]]
    """
    labels: Dict[int, str] = {}
    transitions: Dict[str, float] = {}
    state_features: Dict[str, Dict[str, float]] = {}

    section: str = ""
    curr_id: Optional[int] = None
    curr_str: List[str] = []

    with open(dump_path, "r", encoding="utf-8", errors="replace") as file_obj:
        for line in file_obj:
            line_str = line.rstrip("\r\n")
            match_sec = re.match(
                r"^(FILEHEADER|LABELS|ATTRIBUTES|TRANSITIONS|STATE_FEATURES) = {",
                line_str,
            )
            if match_sec:
                section = match_sec.group(1)
                continue
            if line_str == "}":
                if section == "LABELS" and curr_id is not None:
                    labels[curr_id] = "\n".join(curr_str)
                    curr_id = None
                    curr_str = []
                section = ""
                continue

            if section == "LABELS":
                match_lbl = re.match(r"^\s*(\d+):\s?(.*)$", line_str)
                if match_lbl:
                    if curr_id is not None:
                        labels[curr_id] = "\n".join(curr_str)
                    curr_id = int(match_lbl.group(1))
                    curr_str = [match_lbl.group(2)]
                else:
                    curr_str.append(line_str)
            elif section == "TRANSITIONS":
                match_tr = re.match(
                    r"^\s*\(\d+\)\s+(.*)\s+-->\s+(.*):\s+([+-]?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)$",
                    line_str,
                )
                if match_tr:
                    transitions[f"{match_tr.group(1)}->{match_tr.group(2)}"] = (
                        float(match_tr.group(3))
                    )
            elif section == "STATE_FEATURES":
                match_sf = re.match(
                    r"^\s*\(\d+\)\s+(.*)\s+-->\s+(.*?):\s+([+-]?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)$",
                    line_str,
                )
                if match_sf:
                    attr, lbl, weight = (
                        match_sf.group(1),
                        match_sf.group(2),
                        float(match_sf.group(3)),
                    )
                    if attr not in state_features:
                        state_features[attr] = {}
                    state_features[attr][lbl] = weight

    label_list = [labels[i] for i in range(len(labels))]
    return label_list, transitions, state_features


def convert_crfsuite_model(src_path: str, dst_path: str) -> None:
    """Dump a CRFsuite binary model and save as compressed JSON weights.

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
