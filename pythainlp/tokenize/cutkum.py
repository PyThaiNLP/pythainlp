# -*- coding: utf-8 -*-
from __future__ import absolute_import,unicode_literals
import sys
try:
    from cutkum.tokenizer import Cutkum
except ImportError:
	'''ในกรณีที่ยังไม่ติดตั้ง deepcut ในระบบ'''
	import pip
	pip.main(['install','cutkum'])
	try:
		from cutkum.tokenizer import Cutkum
	except ImportError:
		sys.exit('Error ! using pip install cutkum')
ck = Cutkum()
def segment(text):
    return ck.tokenize(text)
