# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import sys
try:
    import attacut
except ImportError:
    '''ในกรณีที่ยังไม่ติดตั้ง attacut ในระบบ'''
    from pythainlp.tools import install_package
    install_package('attacut')
    try:
        import attacut
    except ImportError:
        sys.exit('Error ! using pip install attacut')


def segment(text):
    return attacut.tokenize(text)
