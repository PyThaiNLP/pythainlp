# -*- coding: utf-8 -*-
import sys  
reload(sys)  
sys.setdefaultencoding('utf8')
from __future__ import absolute_import
#__all__ = ['pyicu', 'dict','isthai','thai']
try:
	from .pyicu import segment
except:
	from .dict import segment