# -*- coding: utf-8 -*-
#  TODO
from pythainlp.tokenize import word_tokenize
import dill
def sentiment(text):
	"""รับค่าสตริง str คืนค่า pos หรือ neg"""
	with open(infile, 'rb') as in_strm:
		vocabulary = dill.load(in_strm)
	in_strm.close()
	with open(infile, 'rb') as in_strm:
		classifier = dill.load(in_strm)
	in_strm.close()
	featurized_test_sentence =  {i:(i in word_tokenize(text.lower())) for i in vocabulary}
	return classifier.classify(featurized_test_sentence)