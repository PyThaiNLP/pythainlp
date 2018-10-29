# -*- coding: utf-8 -*-

from pythainlp.spell import spell
from pythainlp.spell.pn import spell as pn_tnc_spell
from pythainlp.spell.pn import correct as pn_tnc_correct
from pythainlp.spell.pn import NorvigSpellChecker
from pythainlp.corpus import ttc

# checker from pythainlp.spell module (generic)
spell("สี่เหลียม")  # ['สี่เหลี่ยม']
# spell("สี่เหลียม", engine="hunspell")  # available in some Linux systems

# checker from pythainlp.spell.pn module (specified algorithm - Peter Norvig's)
pn_tnc_spell("เหลืยม")
pn_tnc_correct("เหลืยม")

# checker from pythainlp.spell.pn module (specified algorithm, custom dictionary)
ttc_word_freqs = ttc.get_word_frequency_all()
pn_ttc_spell_checker = NorvigSpellChecker(custom_dict=ttc_word_freqs)
pn_ttc_spell_checker.spell("เหลืยม")
pn_ttc_spell_checker.correct("เหลืยม")
