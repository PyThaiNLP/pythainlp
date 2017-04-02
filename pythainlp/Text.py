# -*- coding: utf-8 -*-
from __future__ import absolute_import,unicode_literals
from pythainlp.tokenize import *
import nltk
def Text(str1):
	if type(str1) != 'list':
		str1=word_tokenize(str(str1))
	return nltk.Text(str1)