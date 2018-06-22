# -*- coding: utf-8 -*-
'''
Code by https://github.com/cstorm125/thai2vec/blob/master/notebooks/examples.ipynb
'''
from __future__ import absolute_import,unicode_literals
import six
import sys
if six.PY2:
	print("Thai sentiment in pythainlp. Not support python 2.7")
	sys.exit(0)
try:
	from gensim.models import KeyedVectors
	import numpy as np
except ImportError:
	import pip
	pip.main(['install','gensim','numpy'])
	try:
		from gensim.models import KeyedVectors
		import numpy as np
	except ImportError:
		print("Error ! using 'pip install gensim numpy'")
		sys.exit(0)
from pythainlp.tokenize import word_tokenize
import os

def download():
	path = os.path.join(os.path.expanduser("~"), 'pythainlp-data')
	if not os.path.exists(path):
		os.makedirs(path)
	path = os.path.join(path, 'thai2vec.vec')
	if not os.path.exists(path):
		print("Download models...")
		from urllib import request
		request.urlretrieve("https://www.dropbox.com/s/upnbmiebkfma7oy/thai2vec.vec?dl=1",path)
		print("OK.")
	return path
def get_model():
	return KeyedVectors.load_word2vec_format(download(),binary=False)
def most_similar_cosmul(positive,negative):
	'''
	การใช้งาน
	input list
	'''
	return get_model().most_similar_cosmul(positive=positive, negative=negative)
def doesnt_match(listdata):
	return get_model().doesnt_match(listdata)
def similarity(word1,word2):
	return get_model().similarity(word1,word2)
def sentence_vectorizer(ss,dim=300,use_mean=False):
    s = word_tokenize(ss)
    vec = np.zeros((1,dim))
    for word in s:
        if word in get_model().wv.index2word:
            vec+= get_model().wv.word_vec(word)
        else: pass
    if use_mean: vec /= len(s)
    return(vec)
def about():
	return '''
	thai2vec
	Language Modeling, Word2Vec and Text Classification in Thai Language. Created as part of pyThaiNLP.
	
	Development : Charin Polpanumas
	GitHub : https://github.com/cstorm125/thai2vec
	'''
