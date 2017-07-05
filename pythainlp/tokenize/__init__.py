# -*- coding: utf-8 -*-
from __future__ import absolute_import,division,unicode_literals,print_function
def word_tokenize(text,engine='icu'):
	"""
	ระบบตัดคำภาษาไทย

	word_tokenize(text,engine='mm')
	engine มี
	- icu
	- dict
	- mm ใช้ Maximum Matching algorithm
	- pylexto ใช้ LexTo ในการตัดคำ
	- newmm - ใช้ Maximum Matching algorithm ในการตัดคำภาษาไทย โค้ดชุดใหม่
	"""
	if engine=='icu':
    		from .pyicu import segment
	elif engine=='dict':
    		from .dictsegment import segment
	elif engine=='mm':
    		from .mm import segment
	elif engine=='pylexto':
    		from .pylexto import segment
	elif engine=='newmm':
    		from .newmm import mmcut as segment
	return segment(text)
