# -*- coding: utf-8 -*-
from __future__ import absolute_import,print_function,unicode_literals
import sys
import re
try:
	import icu
except ImportError:
	from pythainlp.tools import install_package
	install_package('pyicu')
	try:
		import icu
	except ImportError:
		sys.exit('Error ! using pip install pyicu')
def gen_words(text):
  bd = icu.BreakIterator.createWordInstance(icu.Locale("th"))
  bd.setText(text)
  p = bd.first()
  for q in bd:
    yield text[p:q]
    p = q

def segment(text):
  text = re.sub("([^\u0E00-\u0E7F\n ]+)"," \\1 ",text)
  return list(gen_words(text))
if __name__ == "__main__":
	print(segment('ทดสอบระบบตัดคำด้วยไอซียู'))
	print(segment('ผมชอบพูดไทยคำ English'))
	print(segment('ผมชอบพูดไทยคำEnglishคำ'))
	print(segment("""ผมชอบพูดไทยคำEnglish540
    บาท"""))
	print(segment('ประหยัด ไฟเบอห้า'))
