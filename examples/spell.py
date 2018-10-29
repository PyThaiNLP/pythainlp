# -*- coding: utf-8 -*-

from pythainlp.corpus import ttc
from pythainlp.spell import spell
from pythainlp.spell.pn import NorvigSpellChecker
from pythainlp.spell.pn import correct as pn_tnc_correct
from pythainlp.spell.pn import spell as pn_tnc_spell

# spell checker from pythainlp.spell module (generic)
print(spell("สี่เหลียม"))  # ['สี่เหลี่ยม']
# print(spell("สี่เหลียม", engine="hunspell"))  # available in some Linux systems

# spell checker from pythainlp.spell.pn module (specified algorithm - Peter Norvig's)
print(pn_tnc_spell("เหลืยม"))
print(pn_tnc_correct("เหลืยม"))


# spell checker from pythainlp.spell.pn module (specified algorithm, custom dictionary)
ttc_word_freqs = ttc.get_word_frequency_all()
pn_ttc_checker = NorvigSpellChecker(custom_dict=ttc_word_freqs)
print(pn_ttc_checker.spell("เหลืยม"))
print(pn_ttc_checker.correct("เหลืยม"))

# apply different dictionary filter when creating spell checker
pn_tnc_checker = NorvigSpellChecker()
print(len(pn_tnc_checker.dictionary()))
pn_tnc_checker_no_filter = NorvigSpellChecker(dict_filter=None)
print(len(pn_tnc_checker_no_filter.dictionary()))
