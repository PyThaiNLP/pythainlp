# -*- coding: utf-8 -*-
from __future__ import absolute_import,print_function
from __future__ import unicode_literals
from __future__ import division
from future import standard_library
standard_library.install_aliases()
__all__ = ["thaipos", "thaiword"]
from .thaipos import get_data
from .thaiword import get_data