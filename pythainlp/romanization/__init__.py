# -*- coding: utf-8 -*-
from __future__ import absolute_import,print_function
from __future__ import unicode_literals
from __future__ import division
from future import standard_library
standard_library.install_aliases()
import icu
# ถอดเสียงภาษาไทยเป็น Latin
def romanization(data):
	"""เป็นคำสั่ง ถอดเสียงภาษาไทยเป็น Latin รับค่า ''str'' ข้อความ คืนค่าเป็น ''str'' ข้อความ Latin"""
	thai2latin = icu.Transliterator.createInstance('Thai-Latin')
	return thai2latin.transliterate(data)