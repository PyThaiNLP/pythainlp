# -*- coding: utf-8 -*-
from __future__ import absolute_import,division,unicode_literals
import codecs
import os
import json
import pythainlp
import nltk.tag
def orchid_data():
	templates_dir = os.path.join(os.path.dirname(pythainlp.__file__), 'corpus')
	template_file = os.path.join(templates_dir, 'thaipos.json')
	with codecs.open(template_file,'r',encoding='utf-8-sig') as handle:
		model = json.load(handle)
	return model
def tag(text,corpus):
	"""
	รับค่าเป็น ''list'' คืนค่าเป็น ''list'' เช่น [('ข้อความ', 'ชนิดคำ')]"""
	if corpus=='orchid':
		tagger = nltk.tag.UnigramTagger(model=orchid_data())# backoff=default_tagger)
		return tagger.tag(text)
