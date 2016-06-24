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
if __name__ == "__main__":
  print(ntt('4'))
