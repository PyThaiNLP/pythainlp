# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, print_function
import re

try:
    import icu
    thkey = icu.Collator.createInstance(icu.Locale('th_TH')).getSortKey
except ImportError: 
    def thkey(word):
        cv = re.sub('[็-์]', '', word,re.U) # remove tone
        cv = re.sub('([เ-ไ])([ก-ฮ])', '\\2\\1', cv,re.U) # switch lead vowel
        tone = re.sub('[^็-์]', ' ', word,re.U) # just tone
        return cv+tone
    
# เรียงลำดับข้อมูล list ภาษาไทย
def collation(data):
	"""เป็นคำสั่งเรียงลำดับข้อมูลใน ''list'' รับค่า list คืนค่าเป็น ''list''"""
	return sorted(data, key=thkey)

if __name__ == "__main__":
	a=collation(['ไก่','ไข่','ก','ฮา'])==['ก', 'ไก่', 'ไข่', 'ฮา']
	print(a)
	print(collation(['หลาย','หญิง'])==['หญิง','หลาย'])
	print(collation(['ไก่', 'เป็ด', 'หมู', 'วัว'])==['ไก่', 'เป็ด', 'วัว', 'หมู'])