# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""
TLTK spell checker.

Re-implemented in pure Python using Peter Norvig's algorithm and TLTK's
bundled dictionary.

:See Also:
    * https://pypi.org/project/tltk/
    * http://norvig.com/spell-correct.html
"""

from __future__ import annotations

import gzip
from typing import Optional

from pythainlp.corpus import corpus_path
from pythainlp.tools.path import safe_path_join

_LETTERS: list[str] = [chr(i) for i in range(ord("ก"), ord("์") + 1)]
_TLTK_DICT: Optional[set[str]] = None


def _get_tltk_dict() -> set[str]:
    global _TLTK_DICT
    if _TLTK_DICT is None:
        path = safe_path_join(corpus_path(), "tltk", "thdict.txt.gz")
        with gzip.open(path, "rt", encoding="utf-8") as f:
            _TLTK_DICT = set(f.read().splitlines())
    return _TLTK_DICT


def _edits1(word: str) -> set[str]:
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [L + R[1:] for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
    replaces = [L + c + R[1:] for L, R in splits if R for c in _LETTERS]
    inserts = [L + c + R for L, R in splits for c in _LETTERS]
    return set(deletes + transposes + replaces + inserts)


def spell(text: str) -> list[str]:
    """
    Return possible correct spellings of a word.

    :param str text: word to be checked
    :return: list of suggested spellings
    :rtype: list[str]
    """
    if not text:
        return []
    words = _get_tltk_dict()
    return [w for w in _edits1(text) if w in words]
