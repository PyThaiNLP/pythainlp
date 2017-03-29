# -*- coding: utf-8 -*-
from __future__ import absolute_import,print_function
from itertools import groupby
import PyICU,six
def segment(txt):
    """รับค่า ''str'' คืนค่าออกมาเป็น ''list'' ที่ได้มาจากการตัดคำโดย ICU"""
    bd = PyICU.BreakIterator.createWordInstance(PyICU.Locale("th"))
    bd.setText(txt)
    breaks = list(bd)
    return [txt[x[0]:x[1]] for x in zip([0]+breaks, breaks)]
if __name__ == "__main__":
	print(segment('ทดสอบระบบตัดคำด้วยไอซียู'))
	print(segment('ผมชอบพูดไทยคำ English คำ'))
	print(segment('ผมชอบพูดไทยคำEnglishคำ'))