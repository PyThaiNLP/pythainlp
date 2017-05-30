# -*- coding: utf-8 -*-
from __future__ import absolute_import,division,unicode_literals
def word_tokenize(text,engine='icu'):
	"""
	ระบบตัดคำภาษาไทย

	word_tokenize(text,engine='icu')
	engine มี
	- icu
	- dict
	- mm ใช้ Maximum Matching algorithm
	"""
	if engine=='icu':
    		from pythainlp.segment.pyicu import segment
	elif engine=='dict':
    		from pythainlp.segment.dict import segment
	elif engine=='mm':
    		from pythainlp.segment.mm import segment
	return segment(text)