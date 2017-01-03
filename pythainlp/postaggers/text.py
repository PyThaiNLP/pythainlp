from __future__ import absolute_import,division,print_function
from nine import nimport,str
from pythainlp.segment import segment
import pythainlp
import codecs
import os
json= nimport('json')
import nltk.tag, nltk.data
templates_dir = os.path.join(os.path.dirname(pythainlp.__file__), 'corpus')
template_file = os.path.join(templates_dir, 'thaipos.json')
#default_tagger = nltk.data.load(nltk.tag._POS_TAGGER)
def data():
	with codecs.open(template_file,'r',encoding='utf-8') as handle:
		model = json.load(handle)
	return model
data1 =data()
#Postaggers ภาษาไทย
def tag(text):
	"""รับค่าเป็นข้อความ ''str'' คืนค่าเป็น ''list'' เช่น [('ข้อความ', 'ชนิดคำ')]"""
	text= segment(text)
	tagger = nltk.tag.UnigramTagger(model=data1)# backoff=default_tagger)
	return tagger.tag(text)