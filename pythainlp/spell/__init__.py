# -*- coding: utf-8 -*-
"""
Spell checking
"""

from .pn import NorvigSpellChecker
from .spell import correct, spell

DEFAULT_SPELL_CHECKER = NorvigSpellChecker()

__all__ = [
    "DEFAULT_SPELL_CHECKER",
    "correct",
    "spell",
    "NorvigSpellChecker",
]
