# -*- coding: utf-8 -*-
from __future__ import absolute_import,unicode_literals,print_function
import six
import sys
if six.PY2:
	print("Thai sentiment in pythainlp. Not support python 2.7")
	sys.exit(0)
import pythainlp
from pythainlp.corpus import stopwords
import os
from pythainlp.tokenize import word_tokenize
try:
	import dill
except ImportError:
	import pip
	pip.main(['install','dill'])
	try:
		import dill
	except ImportError:
		print("Error ! using 'pip install dill'")
		sys.exit(0)

templates_dir = os.path.join(os.path.dirname(pythainlp.__file__), 'sentiment')
def sentiment(text):
	"""
	sentiment ภาษาไทย
	ใช้ข้อมูลจาก https://github.com/wannaphongcom/lexicon-thai/tree/master/ข้อความ/
	รับค่าสตริง str คืนค่า pos , neg"""
	with open(os.path.join(templates_dir, 'vocabulary.data'), 'rb') as in_strm:
		vocabulary = dill.load(in_strm)
	in_strm.close()
	with open(os.path.join(templates_dir, 'sentiment.data'), 'rb') as in_strm:
		classifier = dill.load(in_strm)
	in_strm.close()
	text=set(word_tokenize(text))-set(stopwords.words('thai'))
	featurized_test_sentence =  {i:(i in text) for i in vocabulary}
	return classifier.classify(featurized_test_sentence)
if __name__ == '__main__':
	d="เสียใจแย่มากเลย"
	print(sentiment(d))