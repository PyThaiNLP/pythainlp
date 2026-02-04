# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Spell checking and correction."""

__all__: list[str] = [
    "DEFAULT_SPELL_CHECKER",
    "NorvigSpellChecker",
    "correct",
    "correct_sent",
    "spell",
    "spell_sent",
    "get_words_spell_suggestion",
]

from typing import Type

from pythainlp.spell.pn import NorvigSpellChecker

DEFAULT_SPELL_CHECKER: Type[NorvigSpellChecker] = NorvigSpellChecker

# these imports are placed here to avoid circular imports
from pythainlp.spell.core import correct, correct_sent, spell, spell_sent
from pythainlp.spell.words_spelling_correction import (
    get_words_spell_suggestion,
)
