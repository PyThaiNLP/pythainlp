# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2025 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""
Spell checking and correction.
"""

__all__ = [
    "DEFAULT_SPELL_CHECKER",
    "NorvigSpellChecker",
    "correct",
    "correct_sent",
    "spell",
    "spell_sent",
    "get_words_spell_suggestion",
]

from pythainlp.spell.pn import NorvigSpellChecker

DEFAULT_SPELL_CHECKER = NorvigSpellChecker()

# these imports are placed here to avoid circular imports
from pythainlp.spell.core import correct, correct_sent, spell, spell_sent
from pythainlp.spell.words_spelling_correction import get_words_spell_suggestion
