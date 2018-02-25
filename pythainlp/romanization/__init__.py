# -*- coding: utf-8 -*-
from __future__ import absolute_import,unicode_literals
from pythainlp.tokenize import word_tokenize
# ถอดเสียงภาษาไทยเป็น Latin
def romanization(data,engine='royin'):
	"""เป็นคำสั่ง ถอดเสียงภาษาไทยเป็นอังกฤษ 
	romanization(data,engine='royin')
	มี 2 engine ดังนี้
	- pyicu ส่งค่า Latin
	- royin ใช้หลักเกณฑ์การถอดอักษรไทยเป็นอักษรโรมัน ฉบับราชบัณฑิตยสถาน
	data :
	รับค่า ''str'' ข้อความ 
	คืนค่าเป็น ''str'' ข้อความ"""
	word_list=word_tokenize(data)
	listword=[]
	i=0
	if engine=='royin':
    		from .royin import romanization
	elif engine=='pyicu':
    		from .pyicu import romanization
	while i<len(word_list):
		listword.append(romanization(word_list[i]))
		i+=1
	return ''.join(listword)
