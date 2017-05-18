# -*- coding: utf-8 -*-
from __future__ import absolute_import,print_function,unicode_literals
from collections import Counter
#เรียงจำนวนคำของประโยค
def rank(data):
	"""เรียงจำนวนคำของประโยค
	รับค่าเป็น ''list'' คืนค่าเป็น ''dict'' [ข้อความ,จำนวน]"""
	return Counter(data)
if __name__ == "__main__":
	text = ['แมว','ชอบ','ปลา','และ','แมว','ชอบ','นอน','มาก','เลย','คน','เลี้ยง','กลาย','เป็น','ทาส','แมว']
	print(rank(text))
