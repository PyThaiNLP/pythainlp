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
from pythainlp.segment import * # เตรียมลบออก 1
from pythainlp.tokenize import * # แทนที่ 1
from pythainlp.rank import *
from pythainlp.change import *
from pythainlp.number import *
from pythainlp.date import *
from pythainlp.postaggers import * # เตรียมลบออก 2
from pythainlp.tag import * # แทนที่ 2
from pythainlp.collation import *
from pythainlp.test import *
from pythainlp.Text import *