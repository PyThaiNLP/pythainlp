# -*- coding: utf-8 -*-
#  TODO ปรับ API ให้เหมือน nltk
from __future__ import absolute_import,division,print_function,unicode_literals
from pythainlp.segment import segment
def word_tokenize(text):
	return segment(text)