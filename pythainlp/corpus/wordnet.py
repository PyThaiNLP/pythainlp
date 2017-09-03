# -*- coding: utf-8 -*-
from __future__ import unicode_literals,print_function,absolute_import
import nltk
try:
	nltk.data.find("corpora/omw")
	nltk.data.find("corpora/wordnet")
except LookupError:
	nltk.download('wordnet')
	nltk.download('omw')
from nltk.corpus import wordnet
'''
API ตัวใหม่ เริ่มใช้ตั้งแต่ PyThaiNLP 1.4 เป็นต้นไป
'''
def synsets(word, pos=None, lang="tha"):
	return wordnet.synsets(lemma=word,pos=pos,lang=lang)
def synset(name_synsets):
	return wordnet.synset(name_synsets)
def all_lemma_names(pos=None, lang="tha"):
	return wordnet.all_lemma_names(pos=pos, lang=lang)
def all_synsets(pos=None):
	return wordnet.all_synsets(pos=pos)
def langs():
	return wordnet.langs()
def lemmas(word,pos=None,lang="tha"):
	return wordnet.lemmas(word,pos=pos,lang=lang)
def lemma(name_synsets):
	return wordnet.lemma(name_synsets)
def lemma_from_key(key):
	return wordnet.lemma_from_key(key)
def path_similarity(synsets1,synsets2):
	return wordnet.path_similarity(synsets1,synsets2)
def lch_similarity(synsets1,synsets2):
	return wordnet.lch_similarity(synsets1,synsets2)
def wup_similarity(synsets1,synsets2):
	return wordnet.wup_similarity(synsets1,synsets2)
def morphy(form, pos=None):
	return wordnet.morphy(form, pos=None)
def custom_lemmas(tab_file, lang):
	return wordnet.custom_lemmas(tab_file, lang)
