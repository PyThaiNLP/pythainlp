# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Unigram Part-Of-Speech tagger"""

from __future__ import annotations

import json
from typing import Optional

from pythainlp.corpus import corpus_path, get_corpus_path
from pythainlp.tag import blackboard, orchid
from pythainlp.tools.path import safe_path_join

_ORCHID_FILENAME: str = "pos_orchid_unigram.json"
_ORCHID_PATH: str = safe_path_join(corpus_path(), _ORCHID_FILENAME)

_PUD_FILENAME: str = "pos_ud_unigram-v0.2.json"
_PUD_PATH: str = safe_path_join(corpus_path(), _PUD_FILENAME)

_TDTB_FILENAME: str = "tdtb-unigram_tagger.json"
_TDTB_PATH: str = safe_path_join(corpus_path(), _TDTB_FILENAME)

_BLACKBOARD_NAME: str = "blackboard_unigram_tagger"

_TUD_FILENAME: str = "pos_tud_unigram.json"
_TUD_PATH: str = safe_path_join(corpus_path(), _TUD_FILENAME)

_ORCHID_TAGGER: Optional[dict[str, str]] = None
_PUD_TAGGER: Optional[dict[str, str]] = None
_BLACKBOARD_TAGGER: Optional[dict[str, str]] = None
_TDTB_TAGGER: Optional[dict[str, str]] = None
_TUD_TAGGER: Optional[dict[str, str]] = None


def _orchid_tagger() -> dict[str, str]:
    global _ORCHID_TAGGER
    if not _ORCHID_TAGGER:
        with open(_ORCHID_PATH, encoding="utf-8-sig") as fh:
            _ORCHID_TAGGER = json.load(fh)
    return _ORCHID_TAGGER


def _pud_tagger() -> dict[str, str]:
    global _PUD_TAGGER
    if not _PUD_TAGGER:
        with open(_PUD_PATH, encoding="utf-8-sig") as fh:
            _PUD_TAGGER = json.load(fh)
    return _PUD_TAGGER


def _blackboard_tagger() -> dict[str, str]:
    global _BLACKBOARD_TAGGER
    if not _BLACKBOARD_TAGGER:
        path = get_corpus_path(_BLACKBOARD_NAME)
        if not path:
            raise FileNotFoundError(
                f"corpus-not-found name={_BLACKBOARD_NAME!r}\n"
                f"  Corpus '{_BLACKBOARD_NAME}' not found.\n"
                f"    Python: pythainlp.corpus.download('{_BLACKBOARD_NAME}')\n"
                f"    CLI:    thainlp data get {_BLACKBOARD_NAME}"
            )
        with open(path, encoding="utf-8-sig") as fh:
            _BLACKBOARD_TAGGER = json.load(fh)
    return _BLACKBOARD_TAGGER


def _thai_tdtb() -> dict[str, str]:
    global _TDTB_TAGGER
    if not _TDTB_TAGGER:
        with open(_TDTB_PATH, encoding="utf-8-sig") as fh:
            _TDTB_TAGGER = json.load(fh)
    return _TDTB_TAGGER


def _tud_tagger() -> dict[str, str]:
    global _TUD_TAGGER
    if not _TUD_TAGGER:
        with open(_TUD_PATH, encoding="utf-8-sig") as fh:
            _TUD_TAGGER = json.load(fh)
    return _TUD_TAGGER


def _find_tag(
    words: list[str], dictdata: dict[str, str], default_tag: str = ""
) -> list[tuple[str, str]]:
    keys = list(dictdata.keys())
    return [
        (word, dictdata[word]) if word in keys else (word, default_tag)
        for word in words
    ]


def tag(words: list[str], corpus: str = "pud") -> list[tuple[str, str]]:
    """:param list words: a list of tokenized words
    :param str corpus: corpus name (orchid or pud)
    :return: a list of tuples (word, POS tag)
    :rtype: list[tuple[str, str]]
    """
    if not words:
        return []

    to_ud = False
    if corpus[-3:] == "_ud":
        to_ud = True

    word_tags = []
    if corpus in ("orchid", "orchid_ud"):
        words = orchid.pre_process(words)
        word_tags = _find_tag(words, _orchid_tagger())
        word_tags = orchid.post_process(word_tags, to_ud)
    elif corpus in ("blackboard", "blackboard_ud"):
        words = blackboard.pre_process(words)
        word_tags = _find_tag(words, _blackboard_tagger())
        word_tags = blackboard.post_process(word_tags, to_ud)
    elif corpus in ("tdtb"):
        word_tags = _find_tag(words, _thai_tdtb())
    elif corpus in ("tud"):
        word_tags = _find_tag(words, _tud_tagger())
    else:  # by default, use "pud" for corpus
        word_tags = _find_tag(words, _pud_tagger())

    return word_tags
