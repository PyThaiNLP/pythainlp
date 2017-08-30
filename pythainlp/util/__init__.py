# -*- coding: utf-8 -*-
import re
from nltk.util import ngrams as ngramsdata
def ngrams(token,num):
	'''
	ngrams สร้าง ngrams
	ngrams(token,num)
	- token คือ list
	- num คือ จำนวน ngrams
	'''
	return ngramsdata(token,int(num))
def bigrams(sequence):
	"""
	bigrams ใน Python
	bigrams(sequence)
	"""
	return ngrams(sequence,2)
def trigram(token):
	'''
	Trigram สร้าง trigram
	trigram(token)
	- token คือ list
	'''
	return ngrams(token,3)
rule1=[
    u"ะ",
    u"ั",
    u"็",
    u"า",
    u"ิ",
    u"่",
    u"ํ",
    u"ุ",
    u"ู",
    u"ใ",
    u"ไ",
    u"โ",
    u"ื"
    u"่",
    u"้",
    u"๋",
    u"๊",
    u"ึ",
    u"์",
    u"๋",
    u"ำ"
] # เก็บพวกสระ วรรณยุกต์ที่ซ้ำกันแล้วมีปัญหา
rule2=[
    (u"เเ",u"แ"),
    (u"ํ้า",u"้ำ"),
    (u"ํา้",u"้ำ"),
    (u"้ั",u"ั้")
] # เก็บพวก พิมพ์ลำดับผิดหรือผิดแป้นแต่กลับแสดงผลถูกต้อง ให้ไปเป็นแป้นที่ถูกต้อง เช่น เ + เ ไปเป็น แ
def normalize(text):
    """
    จัดการกับข้อความภาษาไทยให้เป็นปกติ
    normalize(text)
    คืนค่า str
    ตัวอย่าง
    >>> print(normalize("เเปลก")=="แปลก") # เ เ ป ล ก กับ แปลก
    True
    """
    for data in rule2+list(zip(rule1,rule1)):
        text=re.sub(data[0]+"+",data[1],text,re.U)
    return text
