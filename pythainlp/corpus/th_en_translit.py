# -*- coding: utf-8 -*-
# Copyright (C) 2016-2023 PyThaiNLP Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Thai-English Transliteratation Dictionary v1.4

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
    Get transliteration dictionary for Thai to English.

    The returned dict is defaultdict[str, defaultdict[List[str], List[Optional[bool]]]] format.
    """
    path = path_pythainlp_corpus(_FILE_NAME)
    if not path:
        raise FileNotFoundError(
            f"Unable to load transliteration dictionary. "
            f"{_FILE_NAME} is not found under pythainlp/corpus."
        )

    # use list, one word can have multiple transliterations.
    trans_dict = defaultdict(
        lambda: {TRANSLITERATE_EN: [], TRANSLITERATE_FOLLOW_RTSG: []}
    )
    try:
        with open(path, "r", encoding="utf-8") as f:
            # assume first row contains column names, skipped.
            for line in f.readlines()[1:]:
                stripped = line.strip()
                if stripped:
                    th, *en_checked = stripped.split("\t")
                    # replace in-between whitespaces to prevent mismatch results from different tokenizers.
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
