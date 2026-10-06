# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Engine registry for the tokenizer functions in pythainlp.tokenize.core.

Each engine has a small adapter function. An adapter imports its engine
module only when it is called, so optional dependencies stay unloaded
until the engine is selected.

The tables are ordered tuples of (engine names, adapter).
The lookup uses ``engine in names``, the same comparison as an
``if``/``elif`` chain, so names that are not strings
(or not hashable) behave like unknown engines. Sentence and paragraph
tokenizers call string methods on the name first, so they raise
``AttributeError`` for such names.
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, Callable, NoReturn, Optional, TypeVar

if TYPE_CHECKING:
    from pythainlp.util.trie import Trie

_T = TypeVar("_T")

EngineTable = tuple[tuple[tuple[str, ...], _T], ...]
WordSegmenter = Callable[[str, "Trie"], list[str]]
TextSegmenter = Callable[[str], list[str]]


def engine_not_found(engine: object) -> NoReturn:
    """Raise the error for an unknown tokenizer engine.

    :param object engine: name of the engine
    :raises ValueError: always
    """
    # Keep the message text as is; tests and users may match it.
    raise ValueError(
        f'Tokenizer "{engine}" not found.\n'
        "            It might be a typo; if not, please consult our document."
    )


def find_engine(table: EngineTable[_T], engine: object) -> Optional[_T]:
    """Find the adapter of an engine.

    :param table: engine table to search
    :param object engine: name of the engine
    :return: the adapter, or None if no names match
    """
    for names, adapter in table:
        if engine in names:
            return adapter
    return None


def get_engine(table: EngineTable[_T], engine: object) -> _T:
    """Get the adapter of an engine.

    :param table: engine table to search
    :param object engine: name of the engine
    :return: the adapter
    :raises ValueError: if no names match
    """
    adapter = find_engine(table, engine)
    if adapter is None:
        engine_not_found(engine)
    return adapter


def wtp_size(engine: str) -> str:
    """Get the wtpsplit model size from an engine name like ``wtp-tiny``.

    :param str engine: name of the engine
    :return: the model size; ``mini`` if the name has no size
    """
    if "-" not in engine:
        return "mini"
    return engine.split("-")[-1]


# Word tokenizers


def _newmm(text: str, custom_dict: Trie) -> list[str]:
    from pythainlp.tokenize.newmm import segment

    return segment(text, custom_dict)


def _newmm_safe(text: str, custom_dict: Trie) -> list[str]:
    from pythainlp.tokenize.newmm import segment

    return segment(text, custom_dict, safe_mode=True)


def _attacut(text: str, custom_dict: Trie) -> list[str]:
    from pythainlp.tokenize.attacut import segment

    return segment(text)


def _longest(text: str, custom_dict: Trie) -> list[str]:
    from pythainlp.tokenize.longest import segment

    return segment(text, custom_dict)


def _multi_cut(text: str, custom_dict: Trie) -> list[str]:
    from pythainlp.tokenize.multi_cut import segment

    return segment(text, custom_dict)


def _deepcut(text: str, custom_dict: Trie) -> list[str]:
    from pythainlp.tokenize.deepcut import segment

    return segment(text)


def _icu(text: str, custom_dict: Trie) -> list[str]:
    from pythainlp.tokenize.pyicu import segment

    return segment(text)


def _budoux(text: str, custom_dict: Trie) -> list[str]:
    from pythainlp.tokenize.budoux import segment

    return segment(text)


def _nercut(text: str, custom_dict: Trie) -> list[str]:
    from pythainlp.tokenize.nercut import segment

    return segment(text)


def _sefr_cut(text: str, custom_dict: Trie) -> list[str]:
    from pythainlp.tokenize.sefr_cut import segment

    return segment(text)


def _tltk_words(text: str, custom_dict: Trie) -> list[str]:
    from pythainlp.tokenize.tltk import segment

    return segment(text)


def _oskut(text: str, custom_dict: Trie) -> list[str]:
    from pythainlp.tokenize.oskut import segment

    return segment(text)


def _nlpo3(text: str, custom_dict: Trie) -> list[str]:
    from pythainlp.tokenize.nlpo3 import segment

    # nlpo3 takes a dictionary name (str), not a Trie,
    # so custom_dict is not passed.
    return segment(text)


WORD_ENGINES: EngineTable[WordSegmenter] = (
    (("newmm", "onecut"), _newmm),
    (("newmm-safe",), _newmm_safe),
    (("attacut",), _attacut),
    (("longest",), _longest),
    (("mm", "multi_cut"), _multi_cut),
    (("deepcut",), _deepcut),
    (("icu",), _icu),
    (("budoux",), _budoux),
    (("nercut",), _nercut),
    (("sefr_cut",), _sefr_cut),
    (("tltk",), _tltk_words),
    (("oskut",), _oskut),
    (("nlpo3",), _nlpo3),
)

#: Word tokenizers that reject a non-empty custom dictionary.
WORD_ENGINES_WITHOUT_CUSTOM_DICT: tuple[str, ...] = (
    "attacut",
    "icu",
    "nercut",
    "sefr_cut",
    "tltk",
    "oskut",
    "budoux",
)


# Sentence tokenizers


def _crfcut(text: str) -> list[str]:
    from pythainlp.tokenize.crfcut import segment

    return segment(text)


def _whitespace(text: str) -> list[str]:
    return re.split(r" +", text, flags=re.U)


def _whitespace_newline(text: str) -> list[str]:
    return text.split()


def _tltk_sentences(text: str) -> list[str]:
    from pythainlp.tokenize.tltk import sent_tokenize

    return sent_tokenize(text)


def _thaisum(text: str) -> list[str]:
    from pythainlp.tokenize.thaisumcut import ThaiSentenceSegmentor

    return ThaiSentenceSegmentor().split_into_sentences(text)


SENT_ENGINES: EngineTable[TextSegmenter] = (
    (("crfcut",), _crfcut),
    (("whitespace",), _whitespace),
    (("whitespace+newline",), _whitespace_newline),
    (("tltk",), _tltk_sentences),
    (("thaisum",), _thaisum),
)


def segment_sentences(text: str, engine: str) -> list[str]:
    """Split text into sentences with a sentence tokenizer engine.

    Engine names that start with ``wtp`` select wtpsplit.

    :param str text: text to be tokenized
    :param str engine: name of the engine
    :return: list of sentences
    :raises ValueError: if the engine is unknown
    """
    segment = find_engine(SENT_ENGINES, engine)
    if segment is not None:
        return segment(text)
    if engine.startswith("wtp"):
        size = wtp_size(engine)
        from pythainlp.tokenize.wtsplit import tokenize

        return tokenize(text=text, size=size, tokenize="sentence")
    engine_not_found(engine)


# Subword tokenizers


def _tcc(text: str) -> list[str]:
    from pythainlp.tokenize.tcc import segment

    return segment(text)


def _tcc_p(text: str) -> list[str]:
    from pythainlp.tokenize.tcc_p import segment

    return segment(text)


def _etcc(text: str) -> list[str]:
    from pythainlp.tokenize.etcc import segment

    return segment(text)


def _wangchanberta(text: str) -> list[str]:
    from pythainlp.wangchanberta import segment

    return segment(text)


def _syllable_dict(text: str) -> list[str]:
    # Imported here: pythainlp.tokenize.core imports this module.
    from pythainlp.tokenize import syllable_dict_trie
    from pythainlp.tokenize.core import word_tokenize

    segments: list[str] = []
    for word in word_tokenize(text):
        segments.extend(
            word_tokenize(text=word, custom_dict=syllable_dict_trie())
        )
    return segments


def _ssg(text: str) -> list[str]:
    from pythainlp.tokenize.ssg import segment

    return segment(text)


def _tltk_syllables(text: str) -> list[str]:
    from pythainlp.tokenize.tltk import syllable_tokenize

    return syllable_tokenize(text)


def _han_solo(text: str) -> list[str]:
    from pythainlp.tokenize.han_solo import segment

    return segment(text)


def _phayathai(text: str) -> list[str]:
    from pythainlp.phayathaibert import segment

    return segment(text)


SUBWORD_ENGINES: EngineTable[TextSegmenter] = (
    (("tcc",), _tcc),
    (("tcc_p",), _tcc_p),
    (("etcc",), _etcc),
    (("wangchanberta",), _wangchanberta),
    (("dict",), _syllable_dict),
    (("ssg",), _ssg),
    (("tltk",), _tltk_syllables),
    (("han_solo",), _han_solo),
    (("phayathai",), _phayathai),
)

#: Subword tokenizers that are also syllable tokenizers.
SYLLABLE_ENGINES: tuple[str, ...] = ("dict", "han_solo", "ssg", "tltk")
