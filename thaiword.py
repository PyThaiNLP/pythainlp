# โปรแกรมเช็คคำไทยแท้
# เขียนโดย นาย วรรณพงษ์  ภัททิยไพบูลย์
from __future__ import absolute_import,division,print_function,unicode_literals
from pythainlp.tokenize import word_tokenize
a=input('คำ : ')
thai=0 # 0 คือ ยังไม่ตรวจสอบ 1 เป็น 2 ไม่เป็น
def karan(lew,data):
	'''ใช้ในการเช็คคำที่อยู่ใน list'''
	return lew in list(a)
def checkword(word,data):
	'''เช็คคำ หากเหมือนกันให้คืนค่า 1'''
	if word == data:
		return 1
def checkkaran(data):
	thai=0
	if karan('์',data):
		thai = 2
	elif karan('ฆ',data):
		thai = 2
	elif karan('ฌ',data):
		thai = 2
	elif karan('ญ',data):
		thai = 2
	elif karan('ฎ',data):
		thai = 2
	elif karan('ฏ',data):
		thai = 2
	elif karan('ฐ',data):
		thai = 2
	elif karan('ฑ',data):
		thai = 2
	elif karan('ฒ',data):
		thai = 2
	elif karan('ณ',data):
		thai = 2
	elif karan('ธ',data):
		thai = 2
	elif karan('ธ',data):
		thai = 2
	elif karan('ภ',data):
		thai = 2
	elif karan('ศ',data):
		thai = 2
	elif karan('ษ',data):
		thai = 2
	elif karan('ฬ',data):
		thai = 2
	elif karan('ฤ',data):
		thai = 2
	elif karan('ฤา',data):
		thai = 2
	if thai==2:
		return thai
	else:
		return 0
def textgo(word):
	# เช็คตามตัวสะกดตามมาตราแม่ต่าง ๆ
	cat=0
	word=list(word[len(word)-1])
	if word[len(word)-1] == '่':
		del(word[len(word)-1])
	elif word[len(word)-1] == '้':
		del(word[len(word)-1])
	elif word[len(word)-1] == '็':
		del(word[len(word)-1])
	if word[len(word)-1] == 'ก':
		cat=1
	elif word[len(word)-1] == 'ด':
		cat=1
	elif word[len(word)-1] == 'บ':
		cat=1
	elif word[len(word)-1] == 'ง':
		cat=1
	elif word[len(word)-1] == 'น':
		cat=1
	elif word[len(word)-1] == 'ม':
		cat=1
	elif word[len(word)-1] == 'ย':
		cat=1
	elif word[len(word)-1] == 'ว':
		cat=1
	return cat
b=word_tokenize(a)
print(b)
aa=0
for word1 in ['ฆ่า','เฆี่ยน','ระฆัง','ฆ้อง','ตะเฆ่','ใหญ่','หญ้า','เฒ่า','ณ','ธง','เธอ','สำเภา','ภาย','เศร้า','ศึก','ศอก','ศอ','ศก','หญ้า','ใฝ่','ใจ','ให้','ใน','ใหม่','ใส','ใคร','ใคร่','ใย','ใด','ใช้','ใหล','ใส่','ใภ้','ใบ้','ใต้','ใหญ่','ใกล้','ใบ','ใช่']:
	thai1=checkword(word1,a)
	if thai1 == 1:
		thai=1
		aa=1
		break
if len(b) == 1 and checkkaran(list(b))!=2:
	thai=checkkaran(a)
	print('t')
	if thai==0:
		thai=textgo(b)
		if thai==0:
			if len(list(a)) == 2:
				thai=1
elif aa!=1 and thai==0:
	print('a')
	thai = checkkaran(a)
if thai == 0:
	print('b')
	thai = checkkaran(a)
		#if thai == 0:
if thai == 1:
	text='เป็นคำไทยแท้'
elif thai==0:
	text = 'ตรวจสอบไม่ได้'
else:
	text='ไม่เป็นคำไทยแท้'
print(a+' : '+text)
