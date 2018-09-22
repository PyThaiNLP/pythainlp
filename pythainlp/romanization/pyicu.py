# -*- coding: utf-8 -*-
from __future__ import absolute_import,unicode_literals
import sys
try:
	import icu
except ImportError:
	from pythainlp.tools import install_package
	install_package('pyicu')
	try:
		import icu
	except ImportError:
		sys.exit('Error ! using pip install pyicu')

# ถอดเสียงภาษาไทยเป็น Latin
def romanization(data):
	"""เป็นคำสั่ง ถอดเสียงภาษาไทยเป็น Latin รับค่า ''str'' ข้อความ คืนค่าเป็น ''str'' ข้อความ Latin"""
	thai2latin = icu.Transliterator.createInstance('Thai-Latin')
	return thai2latin.transliterate(data)