# -*- coding: utf-8 -*-
import pythainlp
import os
from nine import nimport,str
json= nimport('json')
codecs= nimport('codecs')
reader = codecs.getreader("utf-8")
templates_dir = os.path.join(os.path.dirname(pythainlp.__file__), 'corpus')
template_file = os.path.join(templates_dir, 'thaipos.json')
def get_data():
	return json.load(reader(open(template_file).read()))