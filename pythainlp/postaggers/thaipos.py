#from __future__ import absolute_import
#import pythainlp
#import os
#import pickle
#templates_dir = os.path.join(os.path.dirname(pythainlp.__file__), 'postaggers')
#template_file = os.path.join(templates_dir, 'thaipos.pickle')
#def data():
#	
#	return data 
# แปลง pickle เป็น json
import json
with open(template_file, 'rb') as handle:
	data = pickle.load(handle)
with open('thaipos.json', 'w') as f:
	json.dump(data, f, ensure_ascii=False)