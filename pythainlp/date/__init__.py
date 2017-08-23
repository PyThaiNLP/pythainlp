# -*- coding: utf-8 -*-
from __future__ import absolute_import,unicode_literals
import icu
import datetime
now1 = datetime.datetime.now()
# TODO
def now():
	'''
	คืนค่าเวลา ณ ขณะนี้ ในรูปแบบ str
	ตัวอย่าง "7 มกราคม 2560 20:22:59"
	'''
	formatter = icu.DateFormat.createDateTimeInstance(icu.DateFormat.LONG, icu.DateFormat.kDefault, icu.Locale('th_TH'))
	return formatter.format(datetime.datetime.now())
def now_reign_year():
	'''
	ปีรัชกาลที่ 10
	ณ ปัจจุบัน
	'''
	return now1.year - 2015
def reign_year_to_ad(reign_year,reign):
	'''
	ปีรัชกาล แปลงเป็น ค.ศ.
	reign_year_to_ad(reign_year,reign)
	reign_year - ปีที่ 
	reign - รัชกาล
	'''
	if int(reign)==10:
		ad = int(reign_year)+2015
	elif int(reign)==9:
		ad = int(reign_year)+1945
	elif int(reign)==8:
		ad = int(reign_year)+1928
	elif int(reign)==7:
		ad = int(reign_year)+1924
	return ad
# BE คือ พ.ศ.
# AD คือ ค.ศ.
#  AH ปีฮิจเราะห์ศักราชเป็นปีพุทธศักราช จะต้องบวกด้วย 1122