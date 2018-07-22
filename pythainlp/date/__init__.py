# -*- coding: utf-8 -*-
from __future__ import absolute_import,unicode_literals
import datetime, pytz
now1 = datetime.datetime.now()
tz = pytz.timezone('Asia/Bangkok')

def now():
    """
    :return: the current date with Thai month and Thai year. The month is spelled out in text, and the year is converted from AD to Thai years. (ie: 30 ตุลาคม 2560 20:45:30)
    """
    now1 = datetime.datetime.now(tz)
    month_name = 'x มกราคม กุมภาพันธ์ มีนาคม เมษายน พฤษภาคม มิถุนายน กรกฎาคม สิงหาคม กันยายน ตุลาคม พฤศจิกายน ธันวาคม'.split()[now1.month]
    thai_year = now1.year + 543
    time_str = now1.strftime('%H:%M:%S')
    return "%d %s %d %s"%(now1.day, month_name, thai_year, time_str) # 30 ตุลาคม 2560 20:45:30

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
# AH ปีฮิจเราะห์ศักราชเป็นปีพุทธศักราช จะต้องบวกด้วย 1122
