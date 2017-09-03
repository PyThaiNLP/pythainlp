# -*- coding: utf-8 -*-
from __future__ import absolute_import,print_function,unicode_literals
import os
import codecs
import pythainlp
templates_dir = os.path.join(os.path.dirname(pythainlp.__file__), 'corpus')
def fileload(name1):
	return os.path.join(templates_dir, name1)
def data():
	'''
	โหลดรายการคำศัพท์ภาษาไทย (ตัวเก่า)
	'''
	with codecs.open(fileload('thaiword.txt'), 'r',encoding='utf-8-sig') as f:
		lines = f.read().splitlines()
	return lines
def newdata():
	'''
	โหลดรายการคำศัพท์ภาษาไทย (ตัวใหม่)
	'''
	with codecs.open(fileload('new-thaidict.txt'), 'r',encoding='utf-8-sig') as f:
		lines = f.read().splitlines()
	return lines