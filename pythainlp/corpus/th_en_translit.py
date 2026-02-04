# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Thai-English Transliteration Dictionary v1.4

Wannaphong Phatthiyaphaibun. (2022).
wannaphong/thai-english-transliteration-dictionary: v1.4 (v1.4).
Zenodo. https://doi.org/10.5281/zenodo.6716672
"""

from __future__ import annotations

from collections import defaultdict
from importlib.resources import files
from typing import Union

__all__: list[str] = [
    "get_transliteration_dict",
    "TRANSLITERATE_EN",
    "TRANSLITERATE_FOLLOW_RTSG",
]

_FILE_NAME: str = "th_en_transliteration_v1.4.tsv"
TRANSLITERATE_EN: str = "en"
TRANSLITERATE_FOLLOW_RTSG: str = "follow_rtsg"


def get_transliteration_dict() -> defaultdict[
    str, dict[str, list[Union[str, bool, None]]]
]:
    """Get Thai to English transliteration dictionary.

    The returned dict is in dict[str, dict[List[str], List[Optional[bool]]]] format.
    """
    corpus_files = files("pythainlp.corpus")
    corpus_file = corpus_files.joinpath(_FILE_NAME)

    if not corpus_file.is_file():
        raise FileNotFoundError(
            f"Unable to load transliteration dictionary. "
            f"{_FILE_NAME} is not found under pythainlp/corpus."
        )

    # use list, as one word can have multiple transliterations.
    trans_dict: defaultdict[str, dict[str, list[Union[str, bool, None]]]] = (
        defaultdict(
            lambda: {TRANSLITERATE_EN: [], TRANSLITERATE_FOLLOW_RTSG: []}
        )
    )
    try:
        text = corpus_file.read_text(encoding="utf-8")
        lines = text.splitlines()
        # assume that the first row contains column names, so skip it.
        for line in lines[1:]:
            stripped = line.strip()
            if stripped:
                th, *en_checked = stripped.split("\t")
                # replace in-between whitespace to prevent mismatched results from different tokenizers.
                # e.g. "บอยแบนด์"
                # route 1: "บอยแบนด์" -> ["บอย", "แบนด์"] -> ["boy", "band"] -> "boyband"
                # route 2: "บอยแบนด์" -> [""บอยแบนด์""] -> ["boy band"] -> "boy band"
                en_translit = en_checked[0].replace(" ", "")
                trans_dict[th][TRANSLITERATE_EN].append(en_translit)
                en_follow_rtgs = (
                    bool(en_checked[1]) if len(en_checked) == 2 else None
                )
                trans_dict[th][TRANSLITERATE_FOLLOW_RTSG].append(
                    en_follow_rtgs
                )

    except ValueError as exc:
        raise ValueError(
            f"Unable to parse {_FILE_NAME}. "
            f"Make sure it is a 3-column tab-separated file with header."
        ) from exc
    else:
        return trans_dict


TRANSLITERATE_DICT: defaultdict[
    str, dict[str, list[Union[str, bool, None]]]
] = get_transliteration_dict()
