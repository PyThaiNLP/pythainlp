# -*- coding: utf-8 -*-
from __future__ import absolute_import,unicode_literals,print_function
import icu
collator1 = icu.Collator.createInstance(icu.Locale('th_TH'))
# เรียงลำดับข้อมูล list ภาษาไทย
def collation(data):
	"""เป็นคำสั่งเรียงลำดับข้อมูลใน ''list'' รับค่า list คืนค่าเป็น ''list''"""
	return sorted(data,key=collator1.getSortKey)
if __name__ == "__main__":
	a=collation(['ไก่','ไข่','ก','ฮา'])
	print(a)