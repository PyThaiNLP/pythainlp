# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""symspellpy

symspellpy is a Python port of SymSpell v6.5.
We used unigram & bigram from Thai National Corpus (TNC).

:See Also:
    * \
        https://github.com/mammothb/symspellpy
"""

from __future__ import annotations

from importlib.resources import as_file, files

try:
    from symspellpy import SymSpell, Verbosity
except ImportError:
    raise ImportError(
        "Import Error; Install symspellpy by pip install symspellpy"
    )

from pythainlp.corpus import get_corpus_path

_UNIGRAM_FILENAME = "tnc_freq.txt"
_BIGRAM_CORPUS_NAME = "tnc_bigram_word_freqs"

_sym_spell = None


def _get_sym_spell():
    """Lazy load the symspell instance."""
    global _sym_spell
    if _sym_spell is None:
        _sym_spell = SymSpell()
        # Load unigram dictionary from bundled corpus
        import pythainlp.corpus
        corpus_files = files(pythainlp.corpus)
        unigram_file = corpus_files.joinpath(_UNIGRAM_FILENAME)
        with as_file(unigram_file) as unigram_path:
            _sym_spell.load_dictionary(
                str(unigram_path),
                0,
                1,
                separator="\t",
                encoding="utf-8-sig",
            )
        # Load bigram dictionary from downloaded corpus
        _sym_spell.load_bigram_dictionary(
            get_corpus_path(_BIGRAM_CORPUS_NAME),
            0,
            2,
            separator="\t",
            encoding="utf-8-sig",
        )
    return _sym_spell


def spell(text: str, max_edit_distance: int = 2) -> list[str]:
    sym_spell = _get_sym_spell()
    return [
        str(i).split(",", maxsplit=1)[0]
        for i in list(
            sym_spell.lookup(
                text, Verbosity.CLOSEST, max_edit_distance=max_edit_distance
            )
        )
    ]


def correct(text: str, max_edit_distance: int = 1) -> str:
    return spell(text, max_edit_distance=max_edit_distance)[0]


def spell_sent(
    list_words: list[str], max_edit_distance: int = 2
) -> list[list[str]]:
    sym_spell = _get_sym_spell()
    temp = [
        str(i).split(",", maxsplit=1)[0].split(" ")
        for i in list(
            sym_spell.lookup_compound(
                " ".join(list_words),
                split_by_space=True,
                max_edit_distance=max_edit_distance,
            )
        )
    ]
    list_new = []
    for i in temp:
        list_new.append(i)

    return list_new


def correct_sent(list_words: list[str], max_edit_distance=1) -> list[str]:
    return [
        i[0]
        for i in spell_sent(list_words, max_edit_distance=max_edit_distance)
    ]
