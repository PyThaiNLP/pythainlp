# -*- coding: utf-8 -*-
from __future__ import absolute_import,division,unicode_literals
import codecs
import os
import json
import nltk.tag
import nltk.data
def data():
	import pythainlp
	templates_dir = os.path.join(os.path.dirname(pythainlp.__file__), 'corpus')
	template_file = os.path.join(templates_dir, 'thaipos.json')
	with codecs.open(template_file,'r',encoding='utf-8-sig') as handle:
		model = json.load(handle)
	return model
def tag(text):
	"""
	รับค่าเป็น ''list'' คืนค่าเป็น ''list'' เช่น [('ข้อความ', 'ชนิดคำ')]"""
	tagger = nltk.tag.UnigramTagger(model=data())# backoff=default_tagger)
	return tagger.tag(text)
