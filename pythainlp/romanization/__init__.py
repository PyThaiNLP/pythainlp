from __future__ import absolute_import
from __future__ import print_function
import icu
def romanization(data):
	thai2latin = icu.Transliterator.createInstance('Thai-Latin')
	return thai2latin.transliterate(data)