# -*- coding: utf-8 -*-
from __future__ import absolute_import,division,print_function,unicode_literals
import sys
def pos_tag(text,engine='unigram',corpus='orchid'):
	"""
	ระบบ postaggers

	pos_tag(text,engine='unigram',corpus='orchid')
	engine ที่รองรับ
	* unigram เป็น UnigramTagger
	* perceptron เป็น PerceptronTagger
	* artagger เป็น RDR POS Tagger
	corpus ที่รองรับ
	* orchid
	* pud ใช้ข้อมูล  Parallel Universal Dependencies (PUD) treebanks
	"""
	if engine=='old' or engine=='unigram':
    		from .old import tag
	elif engine=='perceptron':
			from .perceptron import tag
	elif engine=='artagger':
			if sys.version_info < (3,4):
    				sys.exit('Sorry, Python < 3.4 is not supported')
			def tag(text1):
					try:
						from artagger import Tagger
					except ImportError:
						import pip
						pip.main(['install','https://github.com/wannaphongcom/artagger/archive/master.zip'])
						try:
							from artagger import Tagger
						except ImportError:
							print("Error ! using 'pip install https://github.com/wannaphongcom/artagger/archive/master.zip'")
							sys.exit(0)
					words = Tagger().tag(' '.join(text1))
					totag=[]
					for word in words:
    						totag.append((word.word, word.tag))
					return totag
			return tag(text)
	return tag(text,corpus=corpus)
def pos_tag_sents(sentences,engine='unigram',corpus='orchid'):
	return [pos_tag(i,engine=engine,corpus=corpus) for i in sentences]