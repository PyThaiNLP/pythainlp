# -*- coding: utf-8 -*-
"""
Unigram Part-Of-Speech tagger
"""
import json
import os
from typing import List, Tuple

from pythainlp.corpus import corpus_path, get_corpus_path


_ORCHID_FILENAME = "orchid_pos_th.json"
_ORCHID_PATH = os.path.join(corpus_path(), _ORCHID_FILENAME)

_PUD_FILENAME = "ud_thai_pud_unigram_tagger.json"
_PUD_PATH = os.path.join(corpus_path(), _PUD_FILENAME)

_LST20_TAGGER_NAME = "lst20_unigram_tagger"


_ORCHID_TAGGER = None
_PUD_TAGGER = None
_LST20_TAGGER = None


def _find_tag(words: List[str], dictdata: dict) -> List[Tuple[str, str]]:
    keys = list(dictdata.keys())
    return [
        (word, dictdata[word]) if word in keys else (word, None)
        for word in words
    ]


def _orchid_tagger():
    global _ORCHID_TAGGER
    if not _ORCHID_TAGGER:
        with open(_ORCHID_PATH, encoding="utf-8-sig") as fh:
            _ORCHID_TAGGER = json.load(fh)
    return _ORCHID_TAGGER


def _pud_tagger():
    global _PUD_TAGGER
    if not _PUD_TAGGER:
        with open(_PUD_PATH, encoding="utf-8-sig") as fh:
            _PUD_TAGGER = json.load(fh)
    return _PUD_TAGGER


def _lst20_tagger():
    global _LST20_TAGGER
    if not _LST20_TAGGER:
        path = get_corpus_path(_LST20_TAGGER_NAME)
        with open(path, encoding="utf-8-sig") as fh:
            _LST20_TAGGER = json.load(fh)
    return _LST20_TAGGER


# actual tagging work happens here
def _postag_clean(words: List[str], tagger, tag_signs, to_text):
    words = tag_signs(words)
    word_tags = _find_tag(words, tagger())
    return [(to_text(word_tag[0]), word_tag[1]) for word_tag in word_tags]


def tag(words: List[str], corpus: str) -> List[Tuple[str, str]]:
    """
    รับค่าเป็น ''list'' คืนค่าเป็น ''list'' เช่น [('คำ', 'ชนิดคำ'), ('คำ', 'ชนิดคำ'), ...]
    """
    if not words:
        return []

    word_tags = []
    if corpus == "orchid" or corpus == "orchid_ud":
        from pythainlp.tag.orchid import tag_signs, tag_to_text, to_ud

        word_tags = _postag_clean(
            words, _orchid_tagger, tag_signs, tag_to_text
        )
        if corpus == "orchid_ud":
            word_tags = to_ud(word_tags)
    elif corpus == "lst20" or corpus == "lst20_ud":
        from pythainlp.tag.lst20 import tag_signs, tag_to_text, to_ud

        word_tags = _postag_clean(words, _lst20_tagger, tag_signs, tag_to_text)
        if corpus == "lst20_ud":
            word_tags = to_ud(word_tags)
    else:
        word_tags = _find_tag(words, _pud_tagger())

    return word_tags
