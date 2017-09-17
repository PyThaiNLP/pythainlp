# -*- coding: utf-8 -*-
from __future__ import absolute_import,unicode_literals
import nltk
import re
import codecs
from six.moves import zip
def dict_word_tokenize(text,file,engine="newmm"):
	'''
	dict_word_tokenize(text,file,engine)
	เป็นคำสั่งสำหรับตัดคำโดยใช้ข้อมูลที่ผู้ใช้กำหนด
	text คือ ข้อความที่ต้องการตัดคำ
	file คือ ที่ตั้งไฟล์ที่ต้องการมาเป็นฐานข้อมูลตัดคำ
	engine คือ เครื่องมือตัดคำ
	- newmm ตัดคำด้วย newmm
	- mm ตัดคำด้วย mm
	'''
	with codecs.open(file, 'r',encoding='utf8') as f:
		lines = f.read().splitlines()
	f.close()
	if engine=="newmm":
		from .newmm import mmcut as segment
	elif engine=="mm":
		from .mm import segment
	elif engine=='longest-matching':
		from .longest import segment
	return segment(text,data=lines)
def word_tokenize(text,engine='icu'):
	"""
	ระบบตัดคำภาษาไทย

	word_tokenize(text,engine='icu')
	text คือ ข้อความในรูปแบบ str
	engine มี
	- icu -  engine ตัวดั้งเดิมของ PyThaiNLP (ความแม่นยำต่ำ) และเป็นค่าเริ่มต้น
	- dict - ใช้ dicu ในการตัดคำไทย จะคืนค่า False หากไม่สามารถตัดคำไทย
	- longest-matching ใช้ Longest matching ในการตัดคำ
	- mm ใช้ Maximum Matching algorithm - โค้ดชุดเก่า
	- newmm - ใช้ Maximum Matching algorithm ในการตัดคำภาษาไทย โค้ดชุดใหม่
	- pylexto ใช้ LexTo ในการตัดคำ
	- deepcut ใช้ Deep Neural Network ในการตัดคำภาษาไทย
	- wordcutpy ใช้ wordcutpy (https://github.com/veer66/wordcutpy) ในการตัดคำ
	"""
	if engine=='icu':
    		'''
			ตัดคำภาษาไทยโดยใช้ icu ในการตัดคำ
    		คำเตือน !!! \n คำสั่ง word_tokenize(text) ใน PyThaiNLP 1.6
			ค่าเริ่มต้นจะเปลี่ยนจาก icu ไปเป็น newmm'''
    		from .pyicu import segment
	elif engine=='dict':
    		'''
			ใช้ dicu ในการตัดคำไทย
			จะคืนค่า False หากไม่สามารถตัดคำไทย
			'''
    		from .dictsegment import segment
	elif engine=='mm':
    		'''
			ใช้ Maximum Matching algorithm - โค้ดชุดเก่า
			'''
    		from .mm import segment
	elif engine=='newmm':
    		'''
			ใช้ Maximum Matching algorithm ในการตัดคำภาษาไทย โค้ดชุดใหม่
			'''
    		from .newmm import mmcut as segment
	elif engine=='longest-matching':
    		'''
			ใช้ Longest matching ในการตัดคำ
			'''
    		from .longest import segment
	elif engine=='pylexto':
    		'''
			ใช้ LexTo ในการตัดคำ
			'''
    		from .pylexto import segment
	elif engine=='deepcut':
    		'''
			ใช้ Deep Neural Network ในการตัดคำภาษาไทย
			'''
    		from .deepcut import segment
	elif engine=='wordcutpy':
    		'''
			wordcutpy ใช้ wordcutpy (https://github.com/veer66/wordcutpy) ในการตัดคำ
			'''
    		from .wordcutpy import segment
	return segment(text)
def sent_tokenize(text,engine='whitespace+newline'):
	'''
	sent_tokenize(text,engine='whitespace+newline')
	ตัดประโยคเบื้องต้น โดยการแบ่งด้วยช่องว่าง
	'''
	if engine=='whitespace':
		data=nltk.tokenize.WhitespaceTokenizer().tokenize(text)
	elif engine=='whitespace+newline':
		data=re.sub(r'\n+|\s+','|',text,re.U).split('|')
	return data
def wordpunct_tokenize(text):
	'''
	wordpunct_tokenize(text)

	It is nltk.tokenize.wordpunct_tokenize(text).
	'''
	return nltk.tokenize.wordpunct_tokenize(text)
def WhitespaceTokenizer(text):
	return nltk.tokenize.WhitespaceTokenizer().tokenize(text)
def isthai(text,check_all=False):
    """
    สำหรับเช็คว่าเป็นตัวอักษรภาษาไทยหรือไม่
    isthai(text,check_all=False)
    text คือ ข้อความหรือ list ตัวอักษร
    check_all สำหรับส่งคืนค่า True หรือ False เช็คทุกตัวอักษร

    การส่งคืนค่า
    {'thai':% อักษรภาษาไทย,'check_all':tuple โดยจะเป็น (ตัวอักษร,True หรือ False)}
    """
    listext=list(text)
    i=0
    num_isthai=0
    if check_all==True:
        listthai=[]
    while i<len(listext):
        cVal = ord(listext[i])
        if(cVal >= 3584 and cVal <= 3711):
            num_isthai+=1
            if check_all==True:
                listthai.append(True)
        else:
            if check_all==True:
                listthai.append(False)
        i+=1
    thai=(num_isthai/len(listext))*100
    if check_all==True:
        dictthai=tuple(zip(listext,listthai))
        data= {'thai':thai,'check_all':dictthai}
    else:
        data= {'thai':thai}
    return data
