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
	from pythainlp.tools import install_package
	install_package('gensim')
	install_package('numpy')
	try:
		from gensim.models import KeyedVectors
		import numpy as np
	except ImportError:
		print("Error ! using 'pip install gensim numpy'")
		sys.exit(0)
from pythainlp.tokenize import word_tokenize
from pythainlp.corpus import get_file
from pythainlp.corpus import download as download_data
import os

def download():
	path = get_file('thai2vec02')
	if path==None:
		download_data('thai2vec02')
		path = get_file('thai2vec02')
	return path
def get_model():
    '''
    :return: Downloads the `gensim` model.'''
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
    '''
    :param str word1: first word
    :param str word2: second word
    :return: the cosine similarity between the two word vectors
    '''
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
	State-of-the-Art Language Modeling, Text Feature Extraction and Text Classification in Thai Language.
    Created as part of pyThaiNLP with ULMFit implementation from fast.ai
	
	Development : Charin Polpanumas
	GitHub : https://github.com/cstorm125/thai2vec
	'''
