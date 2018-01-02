# -*- coding: utf-8 -*-
'''
ขอขอบคุณ คุณ Korakot Chaovavanich‎ สำหรับโค้ด word_frequency จาก https://www.facebook.com/photo.php?fbid=363640477387469&set=gm.434330506948445&type=3&permPage=1
'''
from __future__ import absolute_import,division,unicode_literals,print_function
import re
import requests
import os
import codecs
def get_word_frequency_all():
	'''
	get_word_frequency_all()
	เป็นคำสั่งสำหรับดึงข้อมูล word frequency ของ TTC มาใช้งาน
	โดยแสดงผลเป็น [(word,frequency),...]
	ข้อมูลจาก https://raw.githubusercontent.com/korakot/thainlp/master/ttc_freq.txt
	'''
	url="https://raw.githubusercontent.com/korakot/thainlp/master/ttc_freq.txt"
	path = os.path.join(os.path.expanduser("~"), 'pythainlp-data')#os.path.join(, 'pthainlp_trie.data')
	if not os.path.exists(path):
		os.makedirs(path)
	path = os.path.join(path, 'ttc_freq.txt')
	if not os.path.exists(path):
		response = requests.get(url)
		with open(path, 'wb') as f:
			f.write(response.content)
		f.close()
	with codecs.open(path, 'r',encoding='utf8') as f:
		lines = f.read().splitlines()
	f.close()
	listword=[]
	for x in lines:
		listindata=x.split("	")
		listword.append((listindata[0],listindata[1]))
	return listword