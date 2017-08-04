# -*- coding: utf-8 -*-
from __future__ import absolute_import,unicode_literals,print_function
import sys
import six
if six.PY2:
	print("Thai sentiment in pythainlp. Not support Python 2")
	sys.exit(0)
try:
    from wordcut import Wordcut
except ImportError:
	'''
    ในกรณีที่ยังไม่ติดตั้ง wordcutpy ในระบบ
    '''
	import pip
	pip.main(['install','wordcutpy'])
	try:
		from wordcut import Wordcut
	except ImportError:
		sys.exit('Error ! using $ pip install wordcutpy')
def segment(text):
	wordcut = Wordcut.bigthai()
	return wordcut.tokenize(text)