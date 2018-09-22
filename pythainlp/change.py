# -*- coding: utf-8 -*-
from __future__ import absolute_import,unicode_literals
import six
dictdata={u'Z':u'(',u'z':u'ผ',u'X':u')',u'x':u'ป',u'C':u'ฉ',u'c':u'แ',u'V':u'ฮ',u'v':u'อ',u'B':u'ฺ',u'b':u'ิ',u'N':u'์',u'n':u'ื',u'M':u'?',u'm':u'ท',u'<':u'ฒ',u',u':u'ม',u'>':u'ฬ',u'.':u'ใ',u'?':u'ฦ',u'/':u'ฝ',
'A':u'ฤ',u'a':u'ฟ',u'S':u'ฆ',u's':u'ห',u'D':u'ฏ',u'd':u'ก',u'F':u'โ',u'f':u'ด',u'G':u'ฌ',u'g':u'เ',u'H':u'็',u'h':u'้',u'J':u'๋',u'j':u'j',u'K':u'ษ',u'k':u'า',u'L':u'ศ',u'l':u'ส',u':u':u'ซ',u'"':u'.',"'":"ง",u':u':u'ซ',u';':u'ว',
'Q':u'๐',u'q':u'ๆ',u'W':u'"',u'w':u'ไ',u'E':u'ฎ',u'e':u'ำ',u'R':u'ฑ',u'r':u'พ',u'T':u'ธ',u't':u'ะ',u'Y':u'ํ',u'y':u'ั',u'U':u'๊',u'u':u'ี',u'I':u'ณ',u'i':u'ร',u'O':u'ฯ',u'o':u'น',u'P':u'ญ',u'p':u'ย',u'{':u'ฐ',u'[':u'บ',u'}':u',u',u']':u'ล',u'|':u'ฅ',u']':u'ฃ',
'~':u'%',u'`':u'_',u'@':u'๑',u'2':u'/',u'#':u'๒',u'3':u'-',u'$':u'๓',u'4':u'ภ',u'%':u'๔',u'5':u'ถ',u'^':u'ู',u'6':u'ุ',u'&':u'฿',u'7':u'ึ',u'*':u'๕',u'8':u'ค',u'(':u'๖',u'9':u'ต',u')':u'๗',u'0':u'จ',u'_':u'๘',u'-':u'ข',u'+':u'๙',u'=':u'ช'}
# แก้ไขพิมพ์ภาษาไทยผิดภาษา
def texttothai(data):
	"""
	:param str data: Incorrect input language correction (Needs thai but input english)
	:return: thai text
	"""
	data = list(data)
	data2 = ""
	for a in data:
		if a in dictdata:
    			a = dictdata[a]
		else:
    			a = a
		data2+=a
	del data
	return data2
# แก้ไขพิมพ์ภาษาอังกฤษผิดภาษา
def texttoeng(data):
	"""
	:param str data: Incorrect input language correction (Needs english but input thai)
	:return: english text
	"""
	data = list(data)
	data2 = ""
	dictdataeng= {v: k for k, v in six.iteritems(dictdata)}
	for a in data:
		if a in dictdataeng:
    			a = dictdataeng[a]
		else:
    			a = a
		data2+=a
	return data2
if __name__ == "__main__":
	a="l;ylfu8iy["
	a=texttothai(a)
	a=texttothai(a)
	b="นามรสนอำันี"
	b=texttoeng(b)
	six.print_(a)
	six.print_(b)