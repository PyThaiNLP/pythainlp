# -*- coding: utf-8 -*-
from __future__ import absolute_import,print_function,unicode_literals
from collections import Counter
from pythainlp.corpus import stopwords
#เรียงจำนวนคำของประโยค
def rank(data,stopword=False):
	"""เรียงจำนวนคำของประโยค
	รับค่าเป็น ''list'' คืนค่าเป็น ''dict'' [ข้อความ,จำนวน]"""
	if stopword==False:
		rankdata=Counter(data)
	else:
		data = [word for word in data if word not in stopwords.words('thai')]
		rankdata=Counter(data)
	return rankdata
if __name__ == "__main__":
	text = ['แมว','ชอบ','ปลา','และ','แมว','ชอบ','นอน','มาก','เลย','คน','เลี้ยง','กลาย','เป็น','ทาส','แมว']
	print(rank(text))
