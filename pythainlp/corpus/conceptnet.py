# -*- coding: utf-8 -*-
from __future__ import absolute_import,division,unicode_literals,print_function
'''
นี่คือ API สำหรับดึงข้อมูลมาจาก http://conceptnet.io
'''
import requests
def edges(word,lang='th'):
    obj = requests.get('http://api.conceptnet.io/c/%s/%s' % (lang,str(word))).json()
    return obj['edges']