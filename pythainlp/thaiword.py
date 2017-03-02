# โปรแกรมเช็คคำไทยแท้
from pythainlp.tokenize import word_tokenize
a=input('คำ : ')
thai=0 # 0 คือ ยังไม่ตรวจสอบ 1 เป็น 2 ไม่เป็น
def karan(lew,data):
	return lew in list(a)
def checkword(word,data):
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
	if thai==2:
		return thai
	else:
		return 0
b=word_tokenize(a)
aa=0
for word1 in ['ฆ่า','เฆี่ยน','ระฆัง','ฆ้อง','ตะเฆ่','ใหญ่','หญ้า','เฒ่า','ณ','ธง','เธอ','สำเภา','ภาย','เศร้า','ศึก','ศอก','ศอ','ศก','หญ้า','ใฝ่','ใจ','ให้','ใน','ใหม่','ใส','ใคร','ใคร่','ใย','ใด','ใช้','ใหล','ใส่','ใภ้','ใบ้','ใต้','ใหญ่','ใกล้','ใบ','ใช่']:
	thai1=checkword(word1,a)
	if thai1 == 1:
		thai=1
		aa=1
		break
if len(b) == 1 and checkkaran(a)!=2:
	thai=1
if aa!=1 and thai==0:
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
		