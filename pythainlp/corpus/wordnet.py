# WordNet ภาษาไทย
from __future__ import unicode_literals,print_function,absolute_import
import nltk
try:
	nltk.data.find("corpora/omw")
except:
	nltk.download('omw')
	nltk.download('wordnet')
from nltk.corpus import wordnet 
'''
API ตัวเก่า
'''
import sqlite3
import pythainlp
import os
from collections import namedtuple
templates_dir = os.path.join(os.path.dirname(pythainlp.__file__), 'corpus')
template_file = os.path.join(templates_dir, 'tha-wn.db')
conn = sqlite3.connect(template_file)
Word = namedtuple('Word', 'synsetid li')
Synset = namedtuple('Synset', 'synset li')
def getWords(wordid):
	"""เป็นคำสั่ง ใช้รับคำจาก ID รับค่า str ส่งออกเป็น tuple ('Word', 'synsetid li')"""
	print("แจ้งเตือน !!! API ตัวนี้จะยกเลิกการใช้งานใน PyThaiNLP 1.5")
	words = []
	cur = conn.execute("select * from word_synset where synsetid=?", (wordid,))
	row = cur.fetchone()
	return Word(*cur.fetchone())
def getSynset(synset):
	"""เป็นคำสั่ง ใช้รับ Synset รับค่า str ส่งออกเป็น tuple ('Synset', 'synset li')"""
	print("แจ้งเตือน !!! API ตัวนี้จะยกเลิกการใช้งานใน PyThaiNLP 1.5")
	cursor=conn.execute("select * from word_synset where li=?",(synset,))
	row=cursor.fetchone()
	if row:
		return Synset(*row)
	else:
		return None
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
