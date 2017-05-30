# -*- coding: utf-8 -*-
from __future__ import absolute_import
import six
if six.PY3:
	"""
	ไว้ใส่ความสามารถที่รองรับเฉพาะ Python 3.4+ เท่านั้น
	"""
	from pythainlp.sentiment import *
	from pythainlp.spell import *
from pythainlp.romanization import *
from pythainlp.segment import *
from pythainlp.tokenize import *
from pythainlp.rank import *
from pythainlp.change import *
from pythainlp.number import *
from pythainlp.date import *
from pythainlp.postaggers import * 
from pythainlp.tag import * 
from pythainlp.collation import *
from pythainlp.test import *
from pythainlp.Text import *
