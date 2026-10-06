# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""
Phunspell spell checker.

Phunspell is a pure Python spell checker using spylls, a port of Hunspell.

:See Also:
    * https://github.com/dvwright/phunspell
"""

from __future__ import annotations

from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    import phunspell

try:
    import phunspell
except ImportError as e:
    raise ImportError(
        "phunspell is not installed. Install it with: pip install phunspell"
    ) from e

pspell: "phunspell.Phunspell" = phunspell.Phunspell("th_TH")


def spell(text: str) -> list[str]:
    """
    Return possible correct spellings of a word.

    :param str text: word to be checked
    :return: list of suggested spellings
    :rtype: list[str]
    """
    return list(pspell.suggest(text))


def correct(text: str) -> str:
    """
    Correct the spelling of a word.

    :param str text: word to be corrected
    :return: first suggested spelling
    :rtype: str
    :raises IndexError: if there is no suggested spelling
    """
    return cast("str", list(pspell.suggest(text))[0])
