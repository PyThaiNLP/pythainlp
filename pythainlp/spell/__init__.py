# -*- coding: utf-8 -*-
"""
Spell checking
"""

from .pn import NorvigSpellChecker

DEFAULT_SPELL_CHECKER = NorvigSpellChecker()

from .spell import correct, spell

__all__ = [
    "DEFAULT_SPELL_CHECKER",
    "correct",
    "spell",
    "NorvigSpellChecker",
]
