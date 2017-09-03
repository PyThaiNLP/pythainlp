# -*- coding: utf-8 -*-
# ระบบแปลงเลขใน 1- 10 ภาษาไทย
from __future__ import absolute_import,division,print_function,unicode_literals
from builtins import dict
from builtins import int
import math,six,ast
p = [[u'ภาษาไทย', u'ตัวเลข',u'เลขไทย'],
     [u'หนึ่ง', u'1', u'๑'],
     [u'สอง', u'2', u'๒'],
     [u'สาม', u'3', u'๓'],
     [u'สี่', u'4', u'๔'],
     [u'ห้า', u'5', u'๕'],
     [u'หก', u'6', u'๖'],
     [u'หก', u'7', u'๗'],
     [u'แปด', u'8', u'๘'],
     [u'เก้า', u'9', u'๙']]
thaitonum = dict((x[2], x[1]) for x in p[1:])
p1 = dict((x[0], x[1]) for x in p[1:])
d1 = 0
#เลขไทยสู่เลข
def thai_num_to_num(text):
	"""รับค่า ''str'' คืนค่า ''str'' เป็นเลขไทยสู่เลข"""
	thaitonum = dict((x[2], x[1]) for x in p[1:])
	return thaitonum[text]
#เลขไทยสู่ข้อความ
def thai_num_to_text(text):
	"""รับค่า ''str'' คืนค่า ''str'' เป็นเลขไทยสู่ข้อความ"""
	thaitonum = dict((x[2], x[0]) for x in p[1:])
	return thaitonum[text]
#เลขสู่เลขไทย
def num_to_thai_num(text):
	"""รับค่า ''str'' คืนค่า ''str'' เป็นเลขสู่เลขไทย"""
	thaitonum = dict((x[1], x[2]) for x in p[1:])
	return thaitonum[text]
#เลขสู่ข้อความ
def num_to_text(text):
	"""รับค่า ''str'' คืนค่า ''str'' เป็นเลขสู่ข้อความ"""
	thaitonum = dict((x[1], x[0]) for x in p[1:])
	return thaitonum[text]
#ข้อความสู่เลข
def text_to_num(text):
	"""รับค่า ''str'' คืนค่า ''str'' เป็นข้อความสู่เลข"""
	thaitonum = dict((x[0], x[1]) for x in p[1:])
	return thaitonum[text]
#ข้อความสู่เลขไทย
def text_to_thai_num(text):
	"""รับค่า ''str'' คืนค่า ''str'' เป็นข้อความสู่เลขไทย"""
	thaitonum = dict((x[0], x[2]) for x in p[1:])
	return thaitonum[text]
def number_format(num, places=0):
    return '{:20,.2f}'.format(num)
# fork by http://justmindthought.blogspot.com/2012/12/code-php.html
def numtowords(amount_number):
	amount_number = number_format(amount_number, 2).replace(" ","")
	pt = amount_number.find(".")
	number,fraction = "",""
	amount_number1 = amount_number.split('.')
	if (pt == False):
		number = amount_number
	else:
		amount_number = amount_number.split('.')
		number = amount_number[0]
		fraction = int(amount_number1[1]) 
	ret = ""
	number=ast.literal_eval(number.replace(",",""))
	baht = ReadNumber(number)
	if (baht != ""):
		ret += baht + "บาท"
	satang = ReadNumber(fraction)
	if (satang != ""):
		ret += satang + "สตางค์"
	else:
		ret += "ถ้วน"
	return ret

#อ่านจำนวนตัวเลขภาษาไทย
def ReadNumber(number):
	"""อ่านจำนวนตัวเลขภาษาไทย รับค่าเป็น ''float'' คืนค่าเป็น  ''str''"""
	position_call = ["แสน", "หมื่น", "พัน", "ร้อย", "สิบ", ""]
	number_call = ["", "หนึ่ง", "สอง", "สาม","สี่", "ห้า", "หก", "เจ็ด", "แปด", "เก้า"]
	number = number
	ret = ""
	if (number == 0): return ret
	if (number > 1000000):
		ret += ReadNumber(int(number / 1000000)) + "ล้าน"
		number = int(math.fmod(number, 1000000))
	divider = 100000
	pos = 0
	while(number > 0):
		d=int(number/divider)
		if (divider == 10) and (d == 2):
			ret += "ยี่"
		elif (divider == 10) and (d == 1):
			ret += ""
		elif ((divider == 1) and (d == 1) and (ret != "")):
			ret += "เอ็ด"
		else:
			ret += number_call[d]
		if d:
			ret += position_call[pos]
		else:
			ret += ""
		number=number % divider
		divider=divider / 10
		pos += 1
	return ret
if __name__ == "__main__":
  print(numtowords(4000.0))