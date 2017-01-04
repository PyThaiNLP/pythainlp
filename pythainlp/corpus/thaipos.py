# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from builtins import open
from future import standard_library
standard_library.install_aliases()
import pythainlp
import os
from nine import nimport,str
json= nimport('json')
templates_dir = os.path.join(os.path.dirname(pythainlp.__file__), 'corpus')
template_file = os.path.join(templates_dir, 'thaipos.json')
def get_data():
	with open(template_file) as f:
		model = json.load(f)
	return model