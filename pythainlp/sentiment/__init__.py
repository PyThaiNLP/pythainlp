# -*- coding: utf-8 -*-
from __future__ import absolute_import,unicode_literals
import six
import sys
if six.PY2:
	print("Thai sentiment in pythainlp. Not support python 2.7")
	sys.exit(0)
from builtins import open
import pythainlp
import os
from pythainlp.tokenize import word_tokenize
import dill
templates_dir = os.path.join(os.path.dirname(pythainlp.__file__), 'sentiment')
def sentiment(text):
	"""
	sentiment ภาษาไทย
	ใช้ข้อมูลจาก https://github.com/wannaphongcom/lexicon-thai/tree/master/ข้อความ/
	รับค่าสตริง str คืนค่า pos , neg หรือ neutral"""
	with open(os.path.join(templates_dir, 'vocabulary.data'), 'rb') as in_strm:
		vocabulary = dill.load(in_strm)
	in_strm.close()
	with open(os.path.join(templates_dir, 'sentiment.data'), 'rb') as in_strm:
		classifier = dill.load(in_strm)
	in_strm.close()
	featurized_test_sentence =  {i:(i in word_tokenize(text.lower())) for i in vocabulary}
	return classifier.classify(featurized_test_sentence)