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

import threading
from importlib.resources import as_file, files
from typing import TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:
    from symspellpy import SymSpell

try:
    from symspellpy import SymSpell, Verbosity
except ImportError as e:
    raise ImportError(
        "symspellpy is not installed. Install it with: pip install symspellpy"
    ) from e

from pythainlp.corpus import get_corpus_path

_UNIGRAM_FILENAME: str = "tnc_freq.txt"
_BIGRAM_CORPUS_NAME: str = "tnc_bigram_word_freqs"

_sym_spell: Optional["SymSpell"] = None
_unigram_file_ctx: Optional[Any] = (
    None  # File context manager kept alive for program lifetime
)
_load_lock: threading.Lock = threading.Lock()  # Thread safety for lazy loading


def _get_sym_spell() -> SymSpell:
    """Lazy load the symspell instance.

    This function uses a lock to ensure thread-safe initialization.
    The context manager is kept alive for the lifetime of the program
    to prevent cleanup of temporary files while SymSpell is in use.
    """
    global _sym_spell, _unigram_file_ctx
    if _sym_spell is None:
        with _load_lock:
            # Double-check pattern to avoid race conditions
            if _sym_spell is None:
                _sym_spell = SymSpell()
                # Load unigram dictionary from bundled corpus
                corpus_files = files("pythainlp.corpus")
                unigram_file = corpus_files.joinpath(_UNIGRAM_FILENAME)
                _unigram_file_ctx = as_file(unigram_file)
                unigram_path = _unigram_file_ctx.__enter__()
                _sym_spell.load_dictionary(
                    str(unigram_path),
                    0,
                    1,
                    separator="\t",
                    encoding="utf-8-sig",
                )
                # Load bigram dictionary from downloaded corpus
                bigram_path = get_corpus_path(_BIGRAM_CORPUS_NAME)
                if not bigram_path:
                    raise FileNotFoundError(
                        f"corpus-not-found name={_BIGRAM_CORPUS_NAME!r}\n"
                        f"  Corpus '{_BIGRAM_CORPUS_NAME}' not found.\n"
                        f"    Python: pythainlp.corpus.download('{_BIGRAM_CORPUS_NAME}')\n"
                        f"    CLI:    thainlp data get {_BIGRAM_CORPUS_NAME}"
                    )
                _sym_spell.load_bigram_dictionary(
                    bigram_path,
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


def correct_sent(
    list_words: list[str], max_edit_distance: int = 1
) -> list[str]:
    return [
        i[0]
        for i in spell_sent(list_words, max_edit_distance=max_edit_distance)
    ]
