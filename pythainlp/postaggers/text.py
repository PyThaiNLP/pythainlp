# -*- coding: utf-8 -*-
from __future__ import absolute_import,division,print_function
from nine import nimport,str
from pythainlp.segment import segment
import pythainlp
import os
import nltk.tag, nltk.data
json= nimport('json')
codecs= nimport('codecs')
reader = codecs.getreader("utf-8")
templates_dir = os.path.join(os.path.dirname(pythainlp.__file__), 'corpus')
template_file = os.path.join(templates_dir, 'thaipos.json')
data1 = json.load(reader(open(template_file).read()))
#Postaggers ภาษาไทย
def tag(text):
	"""รับค่าเป็นข้อความ ''str'' คืนค่าเป็น ''list'' เช่น [('ข้อความ', 'ชนิดคำ')]"""
	text= segment(text)
	tagger = nltk.tag.UnigramTagger(model=data1)# backoff=default_tagger)
	return tagger.tag(text)