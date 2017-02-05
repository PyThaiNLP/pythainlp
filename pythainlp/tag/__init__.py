# -*- coding: utf-8 -*-
#  TODO ปรับ API ให้เหมือน nltk
from __future__ import absolute_import,division,print_function,unicode_literals
from pythainlp.postaggers import tag
def pos_tag(text):
	return tag(text)