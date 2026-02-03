# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Phunspell

A pure Python spell checker utilizing spylls, a port of Hunspell.

:See Also:
    * \
        https://github.com/dvwright/phunspell
"""

from __future__ import annotations

try:
    import phunspell
except ImportError:
    raise ImportError(
        "Import Error; Install phunspell by pip install phunspell"
    )

pspell = phunspell.Phunspell("th_TH")


def spell(text: str) -> list[str]:
    return list(pspell.suggest(text))


def correct(text: str) -> str:
    return list(pspell.suggest(text))[0]  # type: ignore[no-any-return]
