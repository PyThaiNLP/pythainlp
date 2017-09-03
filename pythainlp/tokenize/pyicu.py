# -*- coding: utf-8 -*-
from __future__ import absolute_import,print_function,unicode_literals
from six.moves import zip
import icu
def isEnglish(s):
	'''
	เช็คว่าตัวอักษรเป็นภาษาอังกฤษหรือไม่
	'''
	try:
		try:
			s.encode('ascii')
		except UnicodeEncodeError:
			return False
		else:
			return True
	except:
		try:
			s.decode('ascii')
		except UnicodeDecodeError:
			return False
		else:
			return True
def isThai(chr1):
    '''
    เช็คตัวอักษรว่าใช่ภาษาไทยไหม
    '''
    if isEnglish(chr1):
        return False
    else:
        try:
            cVal = ord(chr1)
            if(cVal >= 3584 and cVal <= 3711):
                return True
            else:
                return False
        except TypeError:
            return False
def segment(txt):
    """รับค่า ''str'' คืนค่าออกมาเป็น ''list'' ที่ได้มาจากการตัดคำโดย ICU"""
    bd = icu.BreakIterator.createWordInstance(icu.Locale("th")) # เริ่มต้นเรียกใช้งานคำสั่งตัดคำโดยเลือกเป็นภาษาไทยโดยใช้ icu
    txt=txt.replace('\n','')
    bd.setText(txt) # ทำการตัดคำ
    breaks = list(bd)
    result=[txt[x[0]:x[1]] for x in zip([0]+breaks, breaks)]
    result1=[]
    for data in result:
        data1=list(data)
        data2=[]
        for txt1 in data1:
            if isThai(txt1)==True:
                if len(data2)==0:
                    data2.append(txt1)
                else:
                    if isThai(data2[data1.index(txt1)-1])==True:
                        data2.append(txt1)
                    else:
                        data2.append(','+txt1)
            else:
                if len(data2)==0:
                    data2.append(txt1)
                else:
                    if isThai(data2[data1.index(txt1)-1])==True:
                        data2.append(','+txt1)
                    else:
                       data2.append(txt1)
        data1=''.join(data2)
        result1+=data1.split(',')
    return [x for x in result1 if x != ' ']
if __name__ == "__main__":
	print(segment('ทดสอบระบบตัดคำด้วยไอซียู'))
	print(segment('ผมชอบพูดไทยคำ English'))
	print(segment('ผมชอบพูดไทยคำEnglishคำ'))
	print(segment("""ผมชอบพูดไทยคำEnglish540
    บาท"""))
	print(segment('ประหยัด ไฟเบอห้า'))
