# -*- coding: utf-8 -*-
from __future__ import absolute_import,unicode_literals
import nltk
import re
import codecs
from six.moves import zip
from pythainlp.corpus.thaisyllable import get_data
from pythainlp.corpus.thaiword import get_data as get_dict
from marisa_trie import Trie

DEFAULT_DICT_TRIE = Trie(get_dict())

def word_tokenize(text, engine='newmm',whitespaces=True):
	"""
    :param str text:  the text to be tokenized
    :param str engine: the engine to tokenize text
    :param bool whitespaces: True to output no whitespace, a common mark of sentence or end of phrase in Thai.
    :Parameters for engine:
        * newmm - Maximum Matching algorithm + TCC
        * icu -  IBM ICU
        * longest-matching - Longest matching
        * mm - Maximum Matching algorithm
        * pylexto - LexTo
        * deepcut - Deep Neural Network
        * wordcutpy - wordcutpy (https://github.com/veer66/wordcutpy)
    :return: A list of words, tokenized from a text

    **Example**::

        from pythainlp.tokenize import word_tokenize
        text='ผมรักคุณนะครับโอเคบ่พวกเราเป็นคนไทยรักภาษาไทยภาษาบ้านเกิด'
        a=word_tokenize(text,engine='icu') # ['ผม', 'รัก', 'คุณ', 'นะ', 'ครับ', 'โอ', 'เค', 'บ่', 'พวก', 'เรา', 'เป็น', 'คน', 'ไทย', 'รัก', 'ภาษา', 'ไทย', 'ภาษา', 'บ้าน', 'เกิด']
        b=word_tokenize(text,engine='dict') # ['ผม', 'รัก', 'คุณ', 'นะ', 'ครับ', 'โอเค', 'บ่', 'พวกเรา', 'เป็น', 'คนไทย', 'รัก', 'ภาษาไทย', 'ภาษา', 'บ้านเกิด']
        c=word_tokenize(text,engine='mm') # ['ผม', 'รัก', 'คุณ', 'นะ', 'ครับ', 'โอเค', 'บ่', 'พวกเรา', 'เป็น', 'คนไทย', 'รัก', 'ภาษาไทย', 'ภาษา', 'บ้านเกิด']
        d=word_tokenize(text,engine='pylexto') # ['ผม', 'รัก', 'คุณ', 'นะ', 'ครับ', 'โอเค', 'บ่', 'พวกเรา', 'เป็น', 'คนไทย', 'รัก', 'ภาษาไทย', 'ภาษา', 'บ้านเกิด']
        e=word_tokenize(text,engine='newmm') # ['ผม', 'รัก', 'คุณ', 'นะ', 'ครับ', 'โอเค', 'บ่', 'พวกเรา', 'เป็น', 'คนไทย', 'รัก', 'ภาษาไทย', 'ภาษา', 'บ้านเกิด']
        g=word_tokenize(text,engine='wordcutpy') # ['ผม', 'รัก', 'คุณ', 'นะ', 'ครับ', 'โอเค', 'บ่', 'พวกเรา', 'เป็น', 'คน', 'ไทย', 'รัก', 'ภาษา', 'ไทย', 'ภาษา', 'บ้านเกิด']
    """
	if engine=='icu':
		from .pyicu import segment
	elif engine=='multi_cut' or engine=='mm':
		from .multi_cut import segment
	elif engine=='newmm' or engine=='onecut':
		from .newmm import mmcut as segment
	elif engine=='longest-matching':
		from .longest import segment
	elif engine=='pylexto':
		from .pylexto import segment
	elif engine=='deepcut':
		from .deepcut import segment
	elif engine=='wordcutpy':
		from .wordcutpy import segment
	else:
		raise Exception("error no have engine.")
	if whitespaces==False:
		return [i.strip(' ') for i in segment(text) if i.strip(' ')!='']
	return segment(text)
def dict_word_tokenize(text, custom_dict_trie, engine='newmm'):
	'''
	:meth:`dict_word_tokenize` tokenizes word based on the dictionary you provide. The format has to be in trie data structure.

	:param str text: the text to be tokenized
	:param dict custom_dict_trie: คือ trie ที่สร้างจาก create_custom_dict_trie
	:param str engine: choose between different options of engine to token (newmm, wordcutpy, mm, longest-matching)
    :return: A list of words, tokenized from a text.
    **Example**::
        >>> from pythainlp.tokenize import dict_word_tokenize,create_custom_dict_trie
        >>> listword=['แมว',"ดี"]
        >>> data_dict=create_custom_dict_trie(listword)
        >>> dict_word_tokenize("แมวดีดีแมว",data_dict)
        ['แมว', 'ดี', 'ดี', 'แมว']
	'''
	if engine=="newmm" or engine=="onecut":
		from .newmm import mmcut as segment
	elif engine=="mm" or engine=="multi_cut":
		from .multi_cut import segment
	elif engine=='longest-matching':
		from .longest import segment
	elif engine=='wordcutpy':
		from .wordcutpy import segment
		return segment(text, custom_dict_trie.keys())
	else:
		raise Exception("error no have engine.")
	return segment(text, custom_dict_trie)
def sent_tokenize(text,engine='whitespace+newline'):
	'''
	This function does not yet automatically recognize when a sentence actually ends. Rather it helps split text where white space and a new line is found.

	:param str text: the text to be tokenized
	:param str engine: choose between 'whitespace' or 'whitespace+newline'

	:return: a list of text, split by whitespace or new line.
	'''
	if engine=='whitespace':
		data=nltk.tokenize.WhitespaceTokenizer().tokenize(text)
	elif engine=='whitespace+newline':
		data=re.sub(r'\n+|\s+','|',text,re.U).split('|')
	return data

def subword_tokenize(text, engine='tcc'):
    """
    :param str text: text to be tokenized
    :param str engine: choosing 'tcc' uses the Thai Character Cluster rule to segment words into the smallest unique units.
    :return: a list of tokenized strings.
    """
    if engine == 'tcc':
        from .tcc import tcc
    return tcc(text)

def isthai(text,check_all=False):
	"""
	:param str text: input string or list of strings
	:param bool check_all: checks all character or not

	:return: A dictionary with the first value as proportional of text that is Thai, and the second value being a tuple of all characters, along with true or false.
	"""
	listext=list(text)
	i=0
	num_isthai=0
	if check_all==True:
		listthai=[]
	while i<len(listext):
		cVal = ord(listext[i])
		if(cVal >= 3584 and cVal <= 3711):
			num_isthai+=1
			if check_all==True:
				listthai.append(True)
		else:
			if check_all==True:
				listthai.append(False)
		i+=1
	thai=(num_isthai/len(listext))*100
	if check_all==True:
		dictthai=tuple(zip(listext,listthai))
		data= {'thai':thai,'check_all':dictthai}
	else:
		data= {'thai':thai}
	return data

def syllable_tokenize(text):
	"""
	:param str text: input string to be tokenized

	:return: returns list of strings of syllables
	"""
	text1=word_tokenize(text)
	data=[]
	trie = create_custom_dict_trie(custom_dict_source=get_data())
	if len(text1)>1:
		i=0
		while i<len(text1):
			data.extend(dict_word_tokenize(text=text1[i], custom_dict_trie=trie))
			i+=1
	else:
		data=dict_word_tokenize(text=text, custom_dict_trie=trie)
	return data

def create_custom_dict_trie(custom_dict_source):
	"""The function is used to create a custom dict trie which will be used for word_tokenize() function. For more information on the trie data structure, see: https://marisa-trie.readthedocs.io/en/latest/index.html

	:param string/list custom_dict_source:  a list of vocaburaries or a path to source file

	:return: A trie created from custom dict input
	"""

	if type(custom_dict_source) is str:
		# Receive a file path of the custom dict to read
		with codecs.open(custom_dict_source, 'r',encoding='utf8') as f:
			_vocabs = f.read().splitlines()
			return Trie(_vocabs)
	elif isinstance(custom_dict_source, (list, tuple, set)):
		# Received a sequence type object of vocabs
		return Trie(custom_dict_source)
	else:
		raise TypeError(
			'Type of custom_dict_source must be either str (path to source file) or collections'
		)

class Tokenizer:
	def __init__(self, custom_dict=None):
		"""
		Initialize tokenizer object

		:param str custom_dict: a file path or a list of vocaburaies to be used to create a trie (default - original lexitron)

		:return: trie_dict - a dictionary in the form of trie data for tokenizing engines
		"""
		if custom_dict:
			if type(custom_dict) is list:
				self.trie_dict = Trie(custom_dict)
			elif type(custom_dict) is str:
				with codecs.open(custom_dict, 'r',encoding='utf8') as f:
					vocabs = f.read().splitlines()
				self.trie_dict = Trie(vocabs)
		else:
			self.trie_dict = Trie(get_dict())

	def word_tokenize(self, text, engine='newmm'):
		from .newmm import mmcut as segment
		return segment(text, self.trie_dict)

