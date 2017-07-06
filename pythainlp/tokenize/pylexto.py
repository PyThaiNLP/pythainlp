# -*- coding: utf-8 -*-
from __future__ import absolute_import,unicode_literals
import sys
try:
    from pylexto import LexTo
except ImportError:
	import pip
	pip.main(['install','https://github.com/wannaphongcom/pylexto/archive/master.zip'])
	try:
		from pylexto import LexTo
	except ImportError:
		sys.exit('Error ! using pip install https://github.com/wannaphongcom/pylexto/archive/master.zip')
def segment(text):
    lexto = LexTo()
    words, types = lexto.tokenize(text)
    return words