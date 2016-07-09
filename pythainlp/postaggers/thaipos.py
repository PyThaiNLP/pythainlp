from __future__ import absolute_import
import pythainlp
import os
import pickle
templates_dir = os.path.join(os.path.dirname(pythainlp.__file__), 'postaggers')
template_file = os.path.join(templates_dir, 'thaipos.pickle')
def data():
	with open(template_file, 'rb') as handle:
		data = pickle.load(handle)
	return data 