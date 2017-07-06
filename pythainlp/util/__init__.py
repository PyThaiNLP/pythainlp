# -*- coding: utf-8 -*-
from nltk.util import ngrams as ngramsdata
def ngrams(token,num):
	'''
	ngrams สร้าง ngrams
	
	ngrams(token,num)
	- token คือ list
	- num คือ จำนวน ngrams
	'''
	return ngramsdata(token,int(num))