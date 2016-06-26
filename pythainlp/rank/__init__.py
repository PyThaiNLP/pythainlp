from collections import Counter
from pythainlp.segment import segment
text = ['แมว','ชอบ','ปลา','และ','แมว','ชอบ','นอน','มาก','เลย','คน','เลี้ยง','กลาย','เป็น','ทาส','แมว']
def rank(data):
	if type(data) != 'list':
		data = segment(data).split(',')
	return Counter(data)