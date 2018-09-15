# -*- coding: utf-8 -*-
from __future__ import absolute_import,unicode_literals,print_function
import pythainlp
from pythainlp.corpus import stopwords
import os
from pythainlp.tokenize import word_tokenize
import dill

templates_dir = os.path.join(os.path.dirname(pythainlp.__file__), 'sentiment')
def sentiment(text, engine='old'):
	"""
	:param str text: thai text
	:param str engine: sentiment analysis engine (old or ulmfit)
	:return: pos or neg

	**Example**::
		>>> from pythainlp.sentiment import sentiment
		>>> text="วันนี้อากาศดีจัง"
		>>> sentiment(text)
		'pos'
		>>> sentiment(text,'ulmfit')
		'pos'
		>>> text="วันนี้อารมณ์เสียมาก"
		>>> sentiment(text)
		'neg'
		>>> sentiment(text,'ulmfit')
		'neg'
	"""
	if engine=='old':
		with open(os.path.join(templates_dir, 'vocabulary.data'), 'rb') as in_strm:
			vocabulary = dill.load(in_strm)
		with open(os.path.join(templates_dir, 'sentiment.data'), 'rb') as in_strm:
			classifier = dill.load(in_strm)
		text=set(word_tokenize(text))-set(stopwords.words('thai'))
		featurized_test_sentence =  {i:(i in text) for i in vocabulary}
		return classifier.classify(featurized_test_sentence)
	elif engine=='ulmfit':
		from pythainlp.sentiment import ulmfit_sent
		tag=ulmfit_sent.get_sentiment(text)
		sa=""
		if tag==0:
			sa="neg"
		else:
			sa="pos"
		return sa
	else:
		raise Exception("error no have engine.")
if __name__ == '__main__':
	d="เสียใจแย่มากเลย"
	print(sentiment(d))
