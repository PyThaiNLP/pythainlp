from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from pythainlp.segment import segment
import pythainlp
import os
import json
import nltk.tag, nltk.data
templates_dir = os.path.join(os.path.dirname(pythainlp.__file__), 'postaggers')
template_file = os.path.join(templates_dir, 'thaipos.json')
#default_tagger = nltk.data.load(nltk.tag._POS_TAGGER)
def data():
	with open(template_file) as handle:
		model = json.load(handle)
	return model
data1 =data()
#Postaggers ภาษาไทย
def tag(text):
	"""รับค่าเป็นข้อความ ''str'' คืนค่าเป็น ''list'' เช่น [('ข้อความ', 'ชนิดคำ')]"""
	text= segment(text)
	tagger = nltk.tag.UnigramTagger(model=data1)# backoff=default_tagger)
	return tagger.tag(text)