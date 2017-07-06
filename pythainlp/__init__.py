# -*- coding: utf-8 -*-
from __future__ import absolute_import
import six
if six.PY3:
	"""
	ไว้ใส่ความสามารถที่รองรับเฉพาะ Python 3.4+ เท่านั้น
	"""
	from pythainlp.sentiment import sentiment
	from pythainlp.spell import hunspell,spell
from pythainlp.romanization import romanization,pyicu,royin
from pythainlp.tokenize import word_tokenize,tcc,etcc
from pythainlp.rank import rank
from pythainlp.change import texttothai,texttoeng
from pythainlp.number import nttn,nttt,ntnt,ntt,ttn,ttnt,number_format,numtowords,ReadNumber
from pythainlp.date import now
from pythainlp.tag import old,pos_tag
from pythainlp.collation import collation
from pythainlp.test import TestUM
from pythainlp.Text import Text
from pythainlp.MetaSound import MetaSound
from pythainlp.soundex import LK82,Udom83
from pythainlp.util import ngrams