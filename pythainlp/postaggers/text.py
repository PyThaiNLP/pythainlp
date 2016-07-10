from __future__ import absolute_import
from pythainlp.segment import segment
import pythainlp
import os
import pickle
import nltk.tag, nltk.data
templates_dir = os.path.join(os.path.dirname(pythainlp.__file__), 'postaggers')
template_file = os.path.join(templates_dir, 'thaipos.pickle')
#default_tagger = nltk.data.load(nltk.tag._POS_TAGGER)
def data():
	with open(template_file, 'rb') as handle:
		model = pickle.load(handle)
	return model
data1 =data()
def tag(text):
	text= segment(text)
	tagger = nltk.tag.UnigramTagger(model=data1)# backoff=default_tagger)
	return tagger.tag(text)