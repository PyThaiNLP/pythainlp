# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Wrapper for PyICU word segmentation. This wrapper module uses
:class:`icu.BreakIterator` with Thai as :class:`icu.Local`
to locate boundaries between words in the text.

:See Also:
    * `GitHub repository <https://github.com/ovalhub/pyicu>`_
"""

from __future__ import annotations

import re
import threading
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterator

from icu import BreakIterator, Locale

# Thread-local storage for BreakIterator instances
_thread_local: threading.local = threading.local()


def _get_break_iterator() -> BreakIterator:
    """Get a thread-local BreakIterator instance."""
    if not hasattr(_thread_local, "bd"):
        _thread_local.bd = BreakIterator.createWordInstance(Locale("th"))
    return _thread_local.bd


def _gen_words(text: str) -> Iterator[str]:
    bd = _get_break_iterator()
    bd.setText(text)
    p = bd.first()
    for q in bd:
        yield text[p:q]
        p = q


def segment(text: str) -> list[str]:
    """Segment text into words using PyICU BreakIterator.

    This function is thread-safe. It uses thread-local storage to ensure
    each thread has its own BreakIterator instance.

    :param str text: text to be tokenized into words
    :return: list of words, tokenized from the text
    """
    if not text or not isinstance(text, str):
        return []

    text = re.sub("([^\u0e00-\u0e7f\n ]+)", " \\1 ", text)

    return list(_gen_words(text))
