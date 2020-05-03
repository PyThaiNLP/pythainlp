# -*- coding: utf-8 -*-
"""
Spell checking and spelling correction.
"""

__all__ = [
    "DEFAULT_SPELL_CHECKER",
    "correct",
    "spell",
    "NorvigSpellChecker",
]

from pythainlp.spell.pn import NorvigSpellChecker

DEFAULT_SPELL_CHECKER = NorvigSpellChecker()

from pythainlp.spell.spell import correct, spell
