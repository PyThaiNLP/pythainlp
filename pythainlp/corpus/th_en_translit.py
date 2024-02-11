# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
"""
Thai-English Transliteration Dictionary v1.4

Wannaphong Phatthiyaphaibun. (2022).
wannaphong/thai-english-transliteration-dictionary: v1.4 (v1.4).
Zenodo. https://doi.org/10.5281/zenodo.6716672
"""

__all__ = [
    "get_transliteration_dict",
    "TRANSLITERATE_EN",
    "TRANSLITERATE_FOLLOW_RTSG",
]

from collections import defaultdict

from pythainlp.corpus import path_pythainlp_corpus

_FILE_NAME = "th_en_transliteration_v1.4.tsv"
TRANSLITERATE_EN = "en"
TRANSLITERATE_FOLLOW_RTSG = "follow_rtsg"


def get_transliteration_dict() -> defaultdict:
    """
    Get Thai to English transliteration dictionary.

    The returned dict is in defaultdict[str, defaultdict[List[str], List[Optional[bool]]]] format.
    """
    path = path_pythainlp_corpus(_FILE_NAME)
    if not path:
        raise FileNotFoundError(
            f"Unable to load transliteration dictionary. "
            f"{_FILE_NAME} is not found under pythainlp/corpus."
        )

    # use list, as one word can have multiple transliterations.
    trans_dict = defaultdict(
        lambda: {TRANSLITERATE_EN: [], TRANSLITERATE_FOLLOW_RTSG: []}
    )
    try:
        with open(path, "r", encoding="utf-8") as f:
            # assume that the first row contains column names, so skip it.
            for line in f.readlines()[1:]:
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

    except ValueError:
        raise ValueError(
            f"Unable to parse {_FILE_NAME}."
            f"Make sure it is a 3-column tab-separated file with header."
        )
    else:
        return trans_dict


TRANSLITERATE_DICT = get_transliteration_dict()
