# -*- coding: utf-8 -*-
from __future__ import absolute_import,unicode_literals
from builtins import open
import pythainlp
import os
import json
import codecs
templates_dir = os.path.join(os.path.dirname(pythainlp.__file__), 'corpus')
template_file = os.path.join(templates_dir, 'thaipos.json')
def get_data():
	with codecs.open(template_file,encoding='utf8') as f:
		model = json.load(f)
	return model