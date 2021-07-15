# -*- coding: utf-8 -*-
"""
Spell checking and spelling correction.
"""

__all__ = [
    "DEFAULT_SPELL_CHECKER",
    "correct",
    "spell",
    "NorvigSpellChecker",
    "spell_sent",
    "correct_sent"
]

from pythainlp.spell.pn import NorvigSpellChecker
from pythainlp.spell.core import correct, spell, correct_sent, spell_sent

DEFAULT_SPELL_CHECKER = NorvigSpellChecker()
