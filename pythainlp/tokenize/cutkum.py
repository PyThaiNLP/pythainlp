# -*- coding: utf-8 -*-
from __future__ import absolute_import,unicode_literals
import sys
import os
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
def get_model():
	path = os.path.join(os.path.expanduser("~"), 'pythainlp-data')
	if not os.path.exists(path):
		os.makedirs(path)
	path = os.path.join(path, 'lstm.l6.d2.pb')
	if not os.path.exists(path):
		print("Download models...")
		from urllib import request
		request.urlretrieve("https://raw.githubusercontent.com/pucktada/cutkum/master/model/lstm.l6.d2.pb",path)
		print("OK.")
	return path
ck = Cutkum(get_model())
def segment(text):
    return ck.tokenize(text)
