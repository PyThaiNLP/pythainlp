# -*- coding: utf-8 -*-
import re
import six
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
if six.PY2:
	rule2=[
		(u"เเ",u"แ"),
		(u"ํ(t)า",u"\1ำ"),
		(u"ํา(t)",u"\1ำ"),
		(u"([่-๋])([ัิ-ื])",u"\2\1"),
		(u"([่-๋])([ูุ])", u"\2\1"),
		(u"ำ([่-๋])", u"\1ำ"),
		(u"(์)([ัิ-ื])",u"\2\1")
	] # เก็บพวก พิมพ์ลำดับผิดหรือผิดแป้นแต่กลับแสดงผลถูกต้อง ให้ไปเป็นแป้นที่ถูกต้อง เช่น เ + เ ไปเป็น แ
else:
	rule2=[
		(u"เเ",u"แ"), # เ เ -> แ
		(u"ํ(t)า",u"\\1ำ"),
		(u"ํา(t)",u"\\1ำ"),
		(u"([่-๋])([ัิ-ื])",u"\\2\\1"),
		(u"([่-๋])([ูุ])", u"\\2\\1"),
		(u"ำ([่-๋])", u"\\1ำ"),
		(u"(์)([ัิ-ื])",u"\\2\\1")]
def normalize(text):
    """
    จัดการกับข้อความภาษาไทยให้เป็นปกติ
    normalize(text)
    คืนค่า str
    ตัวอย่าง
    >>> print(normalize("เเปลก")=="แปลก") # เ เ ป ล ก กับ แปลก
    True
    """
    if six.PY2:
        for data in rule2:
            text=re.sub(data[0].replace(u"t",u"[่้๊๋]"),data[1],text,re.U)
    else:
        for data in rule2:
            text=re.sub(data[0].replace("t","[่้๊๋]"),data[1],text,re.U)
    for data in list(zip(rule1,rule1)):
        text=re.sub(data[0].replace(u"t",u"[่้๊๋]")+"+",data[1],text,re.U)
    return text
def deletetone(data):
	'''โค้ดส่วนตัดวรรณยุกต์ออก'''
	for tone in ['่','้','๊','๋']:
		if (re.search(tone,data)):
				data = re.sub(tone,'',data)
	if re.search(u'\w'+'์',data, re.U):
		search=re.findall(u'\w'+'์',data, re.U)
		for i in search:
				data=re.sub(i,'',data,flags=re.U)
	return data