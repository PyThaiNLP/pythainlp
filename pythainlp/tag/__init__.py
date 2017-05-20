# -*- coding: utf-8 -*-
#  TODO ปรับ API ให้เหมือน nltk
from __future__ import absolute_import,division,print_function,unicode_literals
from pythainlp.postaggers import tag
from pythainlp.tokenize import word_tokenize
import sys
def pos_tag(text,engine='old'):
	"""
	ระบบ postaggers

	pos_tag(text,engine='old')
	engine ที่รองรับ
	* old เป็น UnigramTagger
	* artagger เป็น RDR POS Tagger
	"""
	if engine=='old':
    		from pythainlp.postaggers import tag
	elif engine=='artagger':
			if sys.version_info < (2,7):
    				sys.exit('Sorry, Python < 2.7 is not supported')
			def tag(text1):
					from artagger import Tagger
					tagger = Tagger()
					text= word_tokenize(text)
					words = tagger.tag(' '.join(text))
					totag=[]
					for word in words:
    						totag.append((word.word, word.tag))
					return totag
	return tag(text)