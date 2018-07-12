# -*- coding: utf-8 -*-
from __future__ import absolute_import,unicode_literals
from pythainlp.tokenize import word_tokenize
# ถอดเสียงภาษาไทยเป็น Latin
def romanization(data,engine='royin'):
	"""
	:param str data: Thai text to be romanized
	:param str engine: choose between 'royin' and 'pyicu'. 'royin' will romanize according to the standard of Thai Royal Institute. 'pyicu' will romanize according to the Internaitonal Phonetic Alphabet.
	:return: English (more or less) text that spells out how the Thai text should read.
	"""
	word_list=word_tokenize(data)
	listword=[]
	i=0
	if engine=='royin':
    		from .royin import romanization
	elif engine=='pyicu':
    		from .pyicu import romanization
	while i<len(word_list):
		listword.append(romanization(word_list[i]))
		i+=1
	return ''.join(listword)
