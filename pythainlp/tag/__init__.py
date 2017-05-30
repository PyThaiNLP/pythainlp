# -*- coding: utf-8 -*-
#  TODO ปรับ API ให้เหมือน nltk
from __future__ import absolute_import,division,print_function,unicode_literals
from pythainlp.postaggers import tag
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
			if sys.version_info < (3,4):
    				sys.exit('Sorry, Python < 3.4 is not supported')
			def tag(text1):
					from artagger import Tagger
					tagger = Tagger()
					words = tagger.tag(' '.join(text1))
					totag=[]
					for word in words:
    						totag.append((word.word, word.tag))
					return totag
	return tag(text)