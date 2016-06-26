# ยังไม่สามารถถอดเสียงสระได้ ***
from pythainlp.segment import segment
import re

th = u'[ก-ฮ]+'

p = [['อักษรไทย', 'ต้น', 'ทั่วไป'],
     ['ก', 'k', 'k'],
     ['ข', 'kh', 'k'],
     ['ฃ', 'kh', 'k'],
     ['ค', 'kh', 'k'],
     ['ฅ', 'kh', 'k'],
     ['ฆ', 'kh', 'k'],
     ['ง', 'ng', 'ng'],
     ['จ', 'ch', 't'],
     ['ฉ', 'ch', 't'],
     ['ช', 'ch', 't'],
     ['ซ', 's', 't'],
     ['ฌ', 'ch', 't'],
     ['ญ', 'y', 'n'],
     ['ฎ', 'd', 't'],
     ['ฏ', 't', 't'],
     ['ฐ', 'th', 't'],
     ['ฑ', 'th', 't'],
     ['ฒ', 'th', 't'],
     ['ณ', 'n', 'n'],
     ['ด', 'd', 't'],
     ['ต', 't', 't'],
     ['ถ', 'th', 't'],
     ['ท', 'th', 't'],
     ['ธ', 'th', 't'],
     ['น', 'n', 'n'],
     ['บ', 'b', 'p'],
     ['ป', 'p', 'p'],
     ['ผ', 'ph', 'p'],
     ['ฝ', 'f', 'p'],
     ['พ', 'ph', 'p'],
     ['ฟ', 'f', 'p'],
     ['ภ', 'ph', 'p'],
     ['ม', 'm', 'm'],
     ['ย', 'y', ''],
     ['ร', 'r', 'n'],
     ['ล', 'l', 'n'],
     ['ว', 'w', ''],
     ['ศ', 's', 't'],
     ['ษ', 's', 't'],
     ['ส', 's', 't'],
     ['ห', 'h', ''],
     ['ฬ', 'l', 'n'],
     ['อ', '', 'o'],
     ['ฮ', 'h', '']]
p2 = dict((x[0], x[2]) for x in p[1:])
p1 = dict((x[0], x[1]) for x in p[1:])
d1 = 0
# p1 อักรต้น
# p2 ทั่วไป
# def sub1(txt)

tone = ['่','้','๊','๋']
def delete1(data):
	#โค้ดส่วนตัดวรรณยุกต์ออก
	for a in tone:
		if (re.search(a,data)):
				data = re.sub(a,'',data)
	return data
def sub(text):
	try:
		txt = delete1(text)
		text = list(txt)
		text1 = ""
		text1 = p1[text[0]]
		if len(txt) == 2: # จัดการแก้ไขการสะกดคำที่มี 2 ตัว โดยการเติม o
			text1 += 'o'
		for a in txt[1:]:
			#a=delete1(a)
			if (re.search(th, a, re.U)):
				text1 += p2[a]
			else:
				text1 += a
		return text1
	except:
		return text



def romanization(txt):
	txt = segment(txt)  # (','.join(str(x) for x in txt))  # แยกออกมาเป็น list
	cc=''
	txt = txt.split(',')
	for b in txt:
		cc += sub(b)
	return cc
    # return txt
if __name__ == "__main__":
	romanization('ตอง')
	romanization('มอง')
	romanization('มด')
	romanization('พร')
	romanization('คน')
	romanization('พรม') #!
	romanization('แมว')
	romanization('ชล')
	romanization('ต้น')
