# -*- coding: utf-8 -*-
from __future__ import absolute_import,division,print_function,unicode_literals
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
    		from .old import tag
	elif engine=='artagger':
			if sys.version_info < (3,4):
    				sys.exit('Sorry, Python < 3.4 is not supported')
			def tag(text1):
					try:
						from artagger import Tagger
					except ImportError:
						import pip
						pip.main(['install','https://github.com/franziz/artagger/archive/master.zip'])
						try:
							from artagger import Tagger
						except ImportError:
							print("Error ! using 'pip install https://github.com/franziz/artagger/archive/master.zip'")
							sys.exit(0)
					tagger = Tagger()
					words = tagger.tag(' '.join(text1))
					totag=[]
					for word in words:
    						totag.append((word.word, word.tag))
					return totag
	return tag(text)
