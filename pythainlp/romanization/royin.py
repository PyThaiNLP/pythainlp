# ยังไม่สามารถถอดเสียงสระได้ ***
from __future__ import absolute_import
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
# ส่วนพยัญชนะ
def consonant(text):
	try:
		txt = delete1(text)
		text = list(txt)
		text1 = ""
		text1 = p1[text[0]]
		#print(len(text))
		print(text)
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

# ส่วนสระ
def vowel(data):
	data = data
	th = u'[ก-ฮ]+'
	a=''
	if re.match(u"แ[ก-ฮ]ว",data) is not None:
		aa=list(data)
		aa[0]='aeo'
		a+=consonant(aa[1]+aa[0])
	elif re.match(u"เ[ก-ฮ]ียว",data) is not None:
		aa = list(data)
		aa[0] = 'iao'	
		a+=consonant(aa[1]+aa[0])
	elif re.match(u"[ก-ฮ]ะ",data) is not None:
		a+=consonant(re.sub('ะ', "a", data))
	elif re.match(u"[ก-ฮ]ั",data) is not None:
		a+=consonant(re.sub('ั', "a", data))
	elif re.match(u"[ก-ฮ]รร",data) is not None:
		a+=consonant(re.sub('รร', "a", data))
	elif re.match(u"[ก-ฮ]า",data) is not None:
		a+=consonant(re.sub('า', "a", data))
	elif re.match(u"[ก-ฮ]รร[ก-ฮ]", data) is not None:
		a+=consonant(re.sub('รร', "an", data))
	elif re.match(u"[ก-ฮ]ำ",data) is not None:
		a+=consonant(re.sub('ำ', "am", data))
	elif re.match(u"[ก-ฮ]ิ",data) is not None:
		a+=consonant(re.sub('ิ', "i", data))
	elif re.match(u"[ก-ฮ]ึ",data) is not None:
		a+=consonant(re.sub('ึ', "ue", data))
	elif re.match(u"[ก-ฮ]ื",data) is not None:
		a+=consonant(re.sub('ื', "ue", data))
	elif re.match(u"[ก-ฮ]ุ",data) is not None:
		a+=consonant(re.sub('ุ', "u", data))
	elif re.match(u"[ก-ฮ]ู",data) is not None:
		a+=consonant(re.sub('ู', "u", data))
	elif re.match(u"เ[ก-ฮ]ะ",data) is not None:
		aa = list(data)
		#a+=consonant((list(data))[1])
		aa[0]='e'
		a+=consonant(aa[1]+aa[0])
	elif re.match(u"เ[ก-ฮ]็",data) is not None:
		aa = list(data)
		aa[0]='e'
		a+=consonant(aa[1]+aa[0])
	elif re.match(u"เ[ก-ฮ]",data) is not None:
		aa = list(data)
		aa[0]='e'
		a+=consonant(aa[1]+aa[0])
	elif re.match(u"แ[ก-ฮ]ะ",data) is not None:
		aa = list(data)
		aa[0]='ae'
		a+=consonant(aa[1]+aa[0])
	elif re.match(u"แ[ก-ฮ]",data) is not None:
		aa = list(data)
		aa[0]='ae'
		a+=consonant(aa[1]+aa[0])
	elif re.match(u"โ[ก-ฮ]ะ",data) is not None:
		aa = list(data)
		aa[0]='o'
		a+=consonant(aa[1]+aa[0])
	elif re.match(u"โ[ก-ฮ]",data) is not None:
		aa = list(data)
		aa[0]='o'
		a+=consonant(aa[1]+aa[0])
	elif re.match(u"เ[ก-ฮ]าะ",data) is not None:
		aa = list(data)
		aa[0]='o'
		a+=consonant(aa[1]+aa[0])
	elif re.match(u"[ก-ฮ]อ",data) is not None:
		a+=consonant((list(data))[0])
		a+='o'
	elif re.match(u"เ[ก-ฮ]อะ",data) is not None:
		aa = list(data)
		aa[0]='oe'
		a+=consonant(aa[1]+aa[0])
	elif re.match(u"เ[ก-ฮ]ิ",data) is not None:
		aa = list(data)
		aa[0]='oe'
		a+=consonant(aa[1]+aa[0])
	elif re.match(u"เ[ก-ฮ]อ",data) is not None:
		aa = list(data)
		aa[0]='oe'
		a+=consonant(aa[1]+aa[0])
	elif re.match(u"เ[ก-ฮ]ียะ",data) is not None:
		aa = list(data)
		aa[0]='ia'
		a+=consonant(aa[1]+aa[0])
	elif re.match(u"เ[ก-ฮ]ีย",data) is not None:
		aa = list(data)
		aa[0]='ia'
		a+=consonant(aa[1]+aa[0])
	elif re.match(u"เ[ก-ฮ]ือะ",data) is not None:
		aa = list(data)
		aa[0]='uea'
		a+=consonant(aa[1]+aa[0])
	elif re.match(u"เ[ก-ฮ]ือ",data) is not None:
		aa = list(data)
		aa[0]='uea'
		a+=consonant(aa[1]+aa[0])
	elif re.match(u"[ก-ฮ]ัวะ",data) is not None:
		a+=consonant(re.sub('ัวะ', "ua", data))
	elif re.match(u"[ก-ฮ]ัว",data) is not None:
		a+=consonant(re.sub('ัว', "ua", data))
	elif re.match(u"[ก-ฮ]ว[ก-ฮ]",data) is not None:
		aa=list(data)
		aa[1]='ua'
		aa[2]=aa[1]+consonant(aa[2])
		a+=consonant(aa[0]+aa[2])
	elif re.match(u"ใ[ก-ฮ]",data) is not None:
		aa = list(data)
		aa[0] = 'ai'
		a+=consonant(aa[1]+aa[0])
	elif re.match(u"ไ[ก-ฮ]",data) is not None:
		aa = list(data)
		aa[0] = 'ai'
		a+=consonant(aa[1]+aa[0])
	elif re.match(u"[ก-ฮ]ัย",data) is not None:
		a+=consonant(re.sub('ัย', "ai", data))
	elif re.match(u"ไ[ก-ฮ]ย",data) is not None:
		aa = list(data)
		aa[0] = 'ai'
		a+=consonant(aa[1]+aa[0])
	elif re.match(u"[ก-ฮ]าย",data) is not None:
		a+=consonant(re.sub('าย', "ai", data))
	elif re.match(u"เ[ก-ฮ]า",data) is not None:
		aa = list(data)
		aa[0] = 'ao'
		a+=consonant(aa[1]+aa[0])
	elif re.match(u"[ก-ฮ]าว",data) is not None:
		a+=consonant(re.sub('าว', "ao", data))
	elif re.match(u"[ก-ฮ]ย",data) is not None:
		a+=consonant(re.sub('ย', "ui", data))
	elif re.match(u"โ[ก-ฮ]ย",data) is not None:
		aa = list(data)
		aa[0] = 'oi'
		a+=consonant(aa[1]+aa[0])
	elif re.match(u"[ก-ฮ]อย",data) is not None:
		a+=consonant(re.sub('อย', "oi", data))
	elif re.match(u"เ[ก-ฮ]ย",data) is not None:
		aa = list(data)
		aa[0] = 'oei'
		a+=consonant(aa[1]+aa[0])
	elif re.match(u"เ[ก-ฮ]ือย",data) is not None:
		aa = list(data)
		aa[0] = 'ueai'
		a+=consonant(aa[1]+aa[0])
	elif re.match(u"[ก-ฮ]วย",data) is not None:
		a+=consonant(re.sub('วย', "uai", data))
	elif re.match(u"[ก-ฮ]ิว",data) is not None:
		a+=consonant(re.sub('ิว', "io", data))
	elif re.match(u"เ[ก-ฮ]็ว",data) is not None:
		aa = list(data)
		aa[0] = 'eo'
		a+=consonant(aa[1]+aa[0])
	elif re.match(u"เ[ก-ฮ]ว",data) is not None:
		aa = list(data)
		aa[0] = 'eo'
		a+=consonant(aa[1]+aa[0])
	elif re.match(u"แ[ก-ฮ]ว",data) is not None:
		aa = list(data)
		aa[0] = 'aeo'
		a+=consonant(aa[1]+aa[0])
	elif re.match(u"แ[ก-ฮ]็ว",data) is not None:
		aa = list(data)
		aa[0] = 'aeo'
		a+=consonant(aa[1]+aa[0])
	elif re.match(u"[ก-ฮ]ี",data) is not None:
		a+=consonant(re.sub('ี', "i", data))
	else:
		a+=consonant(data)
	return a

def segment1(data):
	#แบ่งคำด้วย pythainlp ปกติแล้วมาแยกคำในแต่ละ list อีกรอบ
	p="(แ[ก-ฮ]ว)|(เ[ก-ฮ]ียว)|([ก-ฮ]ะ)|([ก-ฮ]ั)|([ก-ฮ]รร)|([ก-ฮ]า)|([ก-ฮ]รร[ก-ฮ])|([ก-ฮ]ำ)|([ก-ฮ]ิ)|([ก-ฮ]ึ)|([ก-ฮ]ื)|([ก-ฮ]ุ)|([ก-ฮ]ู)|(เ[ก-ฮ]ะ)|(เ[ก-ฮ]็)|(เ[ก-ฮ])|(แ[ก-ฮ]ะ)|(แ[ก-ฮ])|(โ[ก-ฮ]ะ)|(โ[ก-ฮ])|(เ[ก-ฮ]าะ)|([ก-ฮ]อ)|(เ[ก-ฮ]อะ)|(เ[ก-ฮ]ิ)|(เ[ก-ฮ]อ)|(เ[ก-ฮ]ียะ)|(เ[ก-ฮ]ีย)|(เ[ก-ฮ]ื(อะ|อ))|([ก-ฮ]ั(วะ|ว))|([[ก-ฮ]ว[ก-ฮ])|(ใ[ก-ฮ])|(ไ[ก-ฮ])|([ก-ฮ]าย)|(เ[ก-ฮ]า)|([ก-ฮ]าว)|([ก-ฮ]ย)|(โ[ก-ฮ]ย)|([ก-ฮ]อย)|(เ[ก-ฮ]ย)|(เ[ก-ฮ]ือย)|([ก-ฮ]วย|([ก-ฮ]ิว)|(เ[ก-ฮ]็ว)|(เ[ก-ฮ]ว))|(แ[ก-ฮ]ว)|(แ[ก-ฮ]็ว)|([ก-ฮ]ี)"# |()
	p = re.compile(p, re.U)
	match = p.split(data)
	match= [x for x in match if x is not None]
	match= [x for x in match if x is not '']
	match= [x for x in match if x is not '']
	data=""
	print(match)
	for a in match:
		data+=vowel(a)
		#try:
		#	data+=consonant(b)
		#except:
		#	data += vowel(b)
	return data#,match
def romanization(txt):
	txt = segment(txt)  # (','.join(str(x) for x in txt))  # แยกออกมาเป็น list
	cc=''
	print(txt)
	for b in txt:
		try:
			#cc+=consonant(b)
			cc += segment1(b)
		except:
			#cc += segment1(b)
			cc+=consonant(b)
	return cc
    # return txt
if __name__ == "__main__":
	print(romanization('ตอง'))
	print(romanization('มอง'))
	print(romanization('มด'))
	print(romanization('พร'))
	print(romanization('คน'))
	print(romanization('พรม')) #!
	#romanization('แมว')
	print(romanization('ชล'))
	print(romanization('ต้น'))
	print(vowel('ตาล'))
	print(vowel('แมว'))
	print(vowel('มะ'))
	print(vowel('เร็ว'))
	print(vowel('เรียว'))
	print(romanization('พนมรุ้ง'))