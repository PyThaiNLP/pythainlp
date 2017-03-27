# -*- coding: utf-8 -*-
from __future__ import absolute_import,unicode_literals
__all__ = ['romanization']
try:
	from .pyicu import romanization
except:
	print("error")