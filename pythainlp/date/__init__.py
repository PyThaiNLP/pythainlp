# -*- coding: utf-8 -*-
from __future__ import absolute_import,unicode_literals
import icu
import datetime
# TODO
def now():
	'''
	คืนค่าเวลา ณ ขณะนี้ ในรูปแบบ str
	ตัวอย่าง "7 มกราคม 2560 20:22:59"
	'''
	formatter = icu.DateFormat.createDateTimeInstance(icu.DateFormat.LONG, icu.DateFormat.kDefault, icu.Locale('th_TH'))
	return formatter.format(datetime.datetime.now())

# BE คือ พ.ศ.
# AD คือ ค.ศ.
#  AH ปีฮิจเราะห์ศักราชเป็นปีพุทธศักราช จะต้องบวกด้วย 1122