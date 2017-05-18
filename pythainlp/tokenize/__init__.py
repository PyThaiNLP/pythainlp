# -*- coding: utf-8 -*-
#  TODO ปรับ API ให้เหมือน nltk
from __future__ import absolute_import,division,unicode_literals
def word_tokenize(text,engine='icu'):
	"""
	ระบบตัดคำภาษาไทย

	word_tokenize(text,engine='icu')
	engine มี
	- icu
	- dict
	"""
	if engine=='icu':
    		from pythainlp.segment.pyicu import segment
	elif engine=='dict':
    		from pythainlp.segment.dict import segment
	return segment(text)