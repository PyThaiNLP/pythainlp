# -*- coding: utf-8 -*-
from __future__ import absolute_import,division,unicode_literals
def word_tokenize(text,engine='icu'):
	"""
	ระบบตัดคำภาษาไทย

	word_tokenize(text,engine='mm')
	engine มี
	- icu
	- dict
	- mm ใช้ Maximum Matching algorithm
	- pylexto ใช้ LexTo ในการตัดคำ
	"""
	if engine=='icu':
    		from .pyicu import segment
	elif engine=='dict':
    		from .dict import segment
	elif engine=='mm':
    		from .mm import segment
	elif engine=='pylexto':
    		from .pylexto import segment
	return segment(text)