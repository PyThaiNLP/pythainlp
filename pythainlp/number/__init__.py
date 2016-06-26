# ระบบแปลงเลขใน 1- 10 ภาษาไทย
p = [['ภาษาไทย', 'ตัวเลข','เลขไทย'],
     ['หนึ่ง', '1', '๑'],
     ['สอง', '2', '๒'],
     ['สาม', '3', '๓'],
     ['สี่', '4', '๔'],
     ['ห้า', '5', '๕'],
     ['หก', '6', '๖'],
     ['หก', '7', '๗'],
     ['แปด', '8', '๘'],
     ['เก้า', '9', '๙']]
thaitonum = dict((x[2], x[1]) for x in p[1:])
p1 = dict((x[0], x[1]) for x in p[1:])
d1 = 0
def nttn(text):
	#เลขไทยสู่เลข
	thaitonum = dict((x[2], x[1]) for x in p[1:])
	return thaitonum[text]
def nttt(text):
	#เลขไทยสู่ข้อความ
	thaitonum = dict((x[2], x[0]) for x in p[1:])
	return thaitonum[text]
def ntnt(text):
	#เลขสู่เลขไทย
	thaitonum = dict((x[1], x[2]) for x in p[1:])
	return thaitonum[text]
def ntt(text):
	#เลขสู่ข้อความ
	thaitonum = dict((x[1], x[0]) for x in p[1:])
	return thaitonum[text]
def ttn(text):
	#ข้อความสู่เลข
	thaitonum = dict((x[0], x[1]) for x in p[1:])
	return thaitonum[text]
def ttnt(text):
	#ข้อความสู่เลขไทย
	thaitonum = dict((x[0], x[2]) for x in p[1:])
	return thaitonum[text]
def numtowords(number):
	digit=['ศูนย์','หนึ่ง','สอง','สาม','สี่','ห้า','หก','เจ็ด','แปด','เก้า','สิบ']
	num=['','สิบ','ร้อย','พัน','หมื่น','แสน','ล้าน']
	number = number.split(".")
	c_num0=len(number[0])
	len1=len(number[0])
	aa=number[1]
	c_num1=len(aa)
	len2=len(aa)
	convert=''
	#	คิดจำนวนเต็ม
	n=0
	while n<len1:
		c_num0-=1
		aa=number[0]
		c_digit=int(aa[n:n+1])
		if(c_num0==0 and c_digit==0): digit[c_digit]=''
		if(c_num0==0 and c_digit==1): digit[c_digit]='เอ็ด'
		if(c_num0==0 and c_digit==2): digit[c_digit]='สอง'
		if(c_num0==1 and c_digit==2): digit[c_digit]='ยี่'; 
		if(c_num0==1 and c_digit==1): digit[c_digit]=''
		convert+=digit[c_digit]
		convert+=num[c_num0]
		n+=1
	convert += 'บาท'
	if(number[1]==''):
		convert += 'ถ้วน'
	#คิดจุดทศนิยม
	n=0
	num={'00':'ศูนย์','01':'หนึ่ง','02':'สอง','03':'สาม','04':'สี่','05':'ห้า','06':'หก','07':'เจ็ด','08':'แปด','09':'เก้า','0':'ศูนย์'}
	if int(number[1]) < 10:
		convert+=num[number[1]]
	else:
		while n<len2: 
			c_num1-=1
			aa=number[1]
			c_digit=int(aa[n:n+1])
			if(c_num1==0 and c_digit==1): digit[c_digit]='หนึ่ง'
			if(c_num1==0 and c_digit==2): digit[c_digit]='สอง'
			if(c_num1==1 and c_digit==2): digit[c_digit]='ยี่' 
			if(c_num1==1 and c_digit==1): digit[c_digit]=''
			convert+=digit[c_digit]
			convert+=num[c_num1] 
			n+=1
	if(number[1]!=''):
		convert += 'สตางค์'
	return convert
if __name__ == '__main__":
  print(ntt('4'))
