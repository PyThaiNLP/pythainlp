# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from future import standard_library
standard_library.install_aliases()
__all__ = ['pyicu', 'dict','isthai','thai']
try:
	from .pyicu import segment
except:
	from .dict import segment