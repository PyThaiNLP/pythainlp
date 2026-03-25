# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Perceptron part-of-speech tagger"""

from __future__ import annotations

from typing import Optional

from pythainlp.corpus import corpus_path, get_corpus_path
from pythainlp.tag import PerceptronTagger, blackboard, orchid
from pythainlp.tools.path import safe_path_join

_BLACKBOARD_NAME: str = "blackboard_pt_tagger"

_ORCHID_FILENAME: str = "pos_orchid_perceptron.json"
_ORCHID_PATH: str = safe_path_join(corpus_path(), _ORCHID_FILENAME)

_PUD_FILENAME: str = "pos_ud_perceptron-v0.2.json"
_PUD_PATH: str = safe_path_join(corpus_path(), _PUD_FILENAME)

_TDTB_FILENAME: str = "tdtb-pt_tagger.json"
_TDTB_PATH: str = safe_path_join(corpus_path(), _TDTB_FILENAME)

_TUD_FILENAME: str = "pos_tud_perceptron.json"
_TUD_PATH: str = safe_path_join(corpus_path(), _TUD_FILENAME)

_BLACKBOARD_TAGGER: Optional[PerceptronTagger] = None
_ORCHID_TAGGER: Optional[PerceptronTagger] = None
_PUD_TAGGER: Optional[PerceptronTagger] = None
_TDTB_TAGGER: Optional[PerceptronTagger] = None
_TUD_TAGGER: Optional[PerceptronTagger] = None


def _orchid_tagger() -> PerceptronTagger:
    global _ORCHID_TAGGER
    if not _ORCHID_TAGGER:
        _ORCHID_TAGGER = PerceptronTagger(path=_ORCHID_PATH)
    return _ORCHID_TAGGER


def _pud_tagger() -> PerceptronTagger:
    global _PUD_TAGGER
    if not _PUD_TAGGER:
        _PUD_TAGGER = PerceptronTagger(path=_PUD_PATH)
    return _PUD_TAGGER


def _blackboard_tagger() -> PerceptronTagger:
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
        _BLACKBOARD_TAGGER = PerceptronTagger(path=path)
    return _BLACKBOARD_TAGGER


def _tdtb() -> PerceptronTagger:
    global _TDTB_TAGGER
    if not _TDTB_TAGGER:
        _TDTB_TAGGER = PerceptronTagger(path=_TDTB_PATH)
    return _TDTB_TAGGER


def _tud_tagger() -> PerceptronTagger:
    global _TUD_TAGGER
    if not _TUD_TAGGER:
        _TUD_TAGGER = PerceptronTagger(path=_TUD_PATH)
    return _TUD_TAGGER


def tag(words: list[str], corpus: str = "pud") -> list[tuple[str, str]]:
    """:param list words: a list of tokenized words
    :param str corpus: corpus name (orchid, pud)
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
        word_tags = _orchid_tagger().tag(words)
        word_tags = orchid.post_process(word_tags, to_ud)
    elif corpus in ("blackboard", "blackboard_ud"):
        words = blackboard.pre_process(words)
        word_tags = _blackboard_tagger().tag(words)
        word_tags = blackboard.post_process(word_tags, to_ud)
    elif corpus in ("tdtb"):
        word_tags = _tdtb().tag(words)
    elif corpus in ("tud"):
        tagger = _tud_tagger()
        word_tags = tagger.tag(words)
    else:  # by default, use "pud" for corpus
        tagger = _pud_tagger()
        word_tags = tagger.tag(words)

    return word_tags
