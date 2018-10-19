# -*- coding: utf-8 -*-
from __future__ import absolute_import,unicode_literals,print_function
import sys
import six
try:
    from wordcut import Wordcut
except ImportError:
	'''
    ในกรณีที่ยังไม่ติดตั้ง wordcutpy ในระบบ
    '''
	from pythainlp.tools import install_package
	install_package("wordcutpy")
	try:
		from wordcut import Wordcut
	except ImportError:
		raise Exception("ImportError ! using $ pip install wordcutpy")

def segment(text, data=None):
    if not data:
        wordcut = Wordcut.bigthai()
    else:
        word_list = list(set(data))
        wordcut = Wordcut(word_list)
    return wordcut.tokenize(text)
