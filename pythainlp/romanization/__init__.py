# -*- coding: utf-8 -*-
from __future__ import absolute_import,unicode_literals
from pythainlp.tokenize import word_tokenize
# ถอดเสียงภาษาไทยเป็น Latin
def romanization(data,engine='royin'):
	"""
	:param str data: Thai text to be romanized
	:param str engine: choose between 'royin' , 'pyicu' and 'thai2rom'. 'royin' will romanize according to the standard of Thai Royal Institute. 'pyicu' will romanize according to the Internaitonal Phonetic Alphabet. 'thai2rom' is deep learning thai romanization.
	:return: English (more or less) text that spells out how the Thai text should read.
	"""
	word_list=word_tokenize(data)
	listword=[]
	i=0
	if engine=='royin':
    		from .royin import romanization
	elif engine=='pyicu':
    		from .pyicu import romanization
	elif engine=='thai2rom':
    		from pythainlp.romanization.thai2rom import thai2rom
    		thai=thai2rom()
    		return thai.romanization(data)
	else:
    		raise Exception("error no have engine.")
	while i<len(word_list):
		listword.append(romanization(word_list[i]))
		i+=1
	return ''.join(listword)
