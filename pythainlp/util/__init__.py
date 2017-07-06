# -*- coding: utf-8 -*-
import nltk.util
def ngrams(token,num):
	'''
	ngrams สร้าง ngrams
	
	ngrams(token,num)
	- token คือ list
	- num คือ จำนวน ngrams
	'''
	return nltk.util.ngrams(token,int(num))
def bigrams(sequence):
	"""
	bigrams ใน Python

	bigrams(sequence)
	"""
	return nltk.util.bigrams(sequence)