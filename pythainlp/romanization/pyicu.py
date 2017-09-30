# -*- coding: utf-8 -*-
from __future__ import absolute_import,unicode_literals
import icu
from pythainlp.tokenize import word_tokenize
# ถอดเสียงภาษาไทยเป็น Latin
def romanization(data):
	"""เป็นคำสั่ง ถอดเสียงภาษาไทยเป็น Latin รับค่า ''str'' ข้อความ คืนค่าเป็น ''str'' ข้อความ Latin"""
	word_list=word_tokenize(data)
	thai2latin = icu.Transliterator.createInstance('Thai-Latin')
	listword=['']*len(word_list)
	i=0
	while i<len(word_list):
		listword[i]=thai2latin.transliterate(word_list[i])
		i+=1
	return ''.join(listword)