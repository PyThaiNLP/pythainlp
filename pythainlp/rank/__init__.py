from __future__ import absolute_import,print_function
from future import standard_library
standard_library.install_aliases()
from collections import Counter
from pythainlp.segment import segment
#เรียงจำนวนคำของประโยค
def rank(data):
	"""เรียงจำนวนคำของประโยค
	รับค่าเป็น ''list'' คืนค่าเป็น ''dict'' [ข้อความ,จำนวน]"""
	return Counter(data)
if __name__ == "__main__":
	text = ['แมว','ชอบ','ปลา','และ','แมว','ชอบ','นอน','มาก','เลย','คน','เลี้ยง','กลาย','เป็น','ทาส','แมว']
	print(rank(text))