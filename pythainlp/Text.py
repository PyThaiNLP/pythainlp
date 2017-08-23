# -*- coding: utf-8 -*-
from __future__ import absolute_import,unicode_literals
from pythainlp.tokenize import word_tokenize
import nltk
def Text(str1):
	if isinstance(str1,list) == False:
		str1=word_tokenize(str(str1))
	return nltk.Text(str1)