from __future__ import absolute_import
from __future__ import print_function
from future import standard_library
standard_library.install_aliases()
from collections import Counter
from pythainlp.segment import segment
text = ['แมว','ชอบ','ปลา','และ','แมว','ชอบ','นอน','มาก','เลย','คน','เลี้ยง','กลาย','เป็น','ทาส','แมว']
def rank(data):
	return Counter(data)