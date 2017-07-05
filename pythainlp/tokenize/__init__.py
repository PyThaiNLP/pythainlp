# -*- coding: utf-8 -*-
from __future__ import absolute_import,division,unicode_literals,print_function
def word_tokenize(text,engine='icu'):
	"""
	ระบบตัดคำภาษาไทย

	word_tokenize(text,engine='icu')
	engine มี
	- icu -  engine ตัวดั้งเดิมของ PyThaiNLP (ความแม่นยำต่ำ) และเป็นค่าเริ่มต้น
	- dict - ใช้ dicu ในการตัดคำไทย จะคืนค่า False หากไม่สามารถตัดคำไทย
	- mm ใช้ Maximum Matching algorithm - โค้ดชุดเก่า
	- newmm - ใช้ Maximum Matching algorithm ในการตัดคำภาษาไทย โค้ดชุดใหม่
	- pylexto ใช้ LexTo ในการตัดคำ
	- deepcut ใช้ Deep Neural Network ในการตัดคำภาษาไทย
	"""
	if engine=='icu':
    		'''
			ตัดคำภาษาไทยโดยใช้ icu ในการตัดคำ
			'''
    		from .pyicu import segment
	elif engine=='dict':
    		'''
			ใช้ dicu ในการตัดคำไทย
			จะคืนค่า False หากไม่สามารถตัดคำไทย
			'''
    		from .dictsegment import segment
	elif engine=='mm':
    		'''
			ใช้ Maximum Matching algorithm - โค้ดชุดเก่า
			'''
    		from .mm import segment
	elif engine=='newmm':
    		'''
			ใช้ Maximum Matching algorithm ในการตัดคำภาษาไทย โค้ดชุดใหม่
			'''
    		from .newmm import mmcut as segment
	elif engine=='pylexto':
    		'''
			ใช้ LexTo ในการตัดคำ
			'''
    		from .pylexto import segment
	elif engine=='deepcut':
    		'''
			ใช้ Deep Neural Network ในการตัดคำภาษาไทย
			'''
    		from .deepcut import segment
	return segment(text)
