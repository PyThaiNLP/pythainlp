# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
"""
Spell checking and correction.
"""

__all__ = [
    "DEFAULT_SPELL_CHECKER",
    "correct",
    "spell",
    "NorvigSpellChecker",
    "spell_sent",
    "correct_sent",
]

from pythainlp.spell.pn import NorvigSpellChecker

DEFAULT_SPELL_CHECKER = NorvigSpellChecker()

from pythainlp.spell.core import correct, spell, correct_sent, spell_sent
