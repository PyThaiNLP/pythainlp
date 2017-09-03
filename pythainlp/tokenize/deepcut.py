# -*- coding: utf-8 -*-
from __future__ import absolute_import,unicode_literals
import sys
try:
    import deepcut
except ImportError:
	'''
    ในกรณีที่ยังไม่ติดตั้ง deepcut ในระบบ
    '''
	import pip
	pip.main(['install','deepcut'])
	try:
		import deepcut
	except ImportError:
		sys.exit('Error ! using pip install deepcut')
def segment(text):
    return deepcut.tokenize(text)