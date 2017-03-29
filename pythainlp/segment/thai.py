# -*- coding: utf-8 -*-
from __future__ import absolute_import,print_function
import os
import codecs
import pythainlp
templates_dir = os.path.join(os.path.dirname(pythainlp.__file__), 'corpus')
template_file = os.path.join(templates_dir, 'thaiword.txt')
def data():
	with codecs.open(template_file, 'r',encoding='utf-8-sig') as f:
		lines = f.read().splitlines()
	return lines
if __name__ == "__main__":
	print((data()))