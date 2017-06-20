# -*- coding: utf-8 -*-
from __future__ import absolute_import,unicode_literals
# ถอดเสียงภาษาไทยเป็น Latin
def romanization(data,engine='pyicu'):
	"""เป็นคำสั่ง ถอดเสียงภาษาไทยเป็นอังกฤษ 
	romanization(data,engine='pyicu')
	มี 2 engine ดังนี้
	- pyicu ส่งค่า Latin
	- royin ใช้หลักเกณฑ์การถอดอักษรไทยเป็นอักษรโรมัน ฉบับราชบัณฑิตยสถาน
	data :
	รับค่า ''str'' ข้อความ 
	คืนค่าเป็น ''str'' ข้อความ"""
	if engine=='royin': 
    		from .royin import romanization
	elif engine=='pyicu':
    		from .pyicu import romanization
	return romanization(data)
