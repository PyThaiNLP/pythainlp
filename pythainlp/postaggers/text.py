from __future__ import absolute_import
from pythainlp.segment import segment
import pythainlp
import os
import pickle
templates_dir = os.path.join(os.path.dirname(pythainlp.__file__), 'postaggers')
template_file = os.path.join(templates_dir, 'thaipos.pickle')
def data():
	with open(template_file, 'rb') as handle:
		data = pickle.load(handle)
	return data 
data1 =data()
def tag(text):
	text= segment(text)
	a=''
	for b in text:
		try:
			a+=b+"/"+data1[b]
		except KeyError:
			a+=b
		a+=' '
	return a