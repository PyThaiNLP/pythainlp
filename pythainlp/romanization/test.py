import re
def is_match(regex, text):
    pattern = re.match(regex, text,re.U)
    return pattern is not None
def search(regex, text):
	return re.search(regex,text,re.U)
def vowel(data):
	vowel1=""
	if data=="ะ":
		vowel1+="อ"+data
	elif data=="ั":
		vowel1+="อ"+data
	elif data=="็":
		vowel1+="อ"+data
	elif data=="า":
		vowel1+="อ"+data
	elif data=="ำ":
		vowel1+="อ"+data
	elif data=="ิ":
		vowel1+="อ"+data
	elif data=="เื":
		vowel1+="เอือ"
	elif data=="ื":
		vowel1+="อือ"
	elif data=="เะ":
		vowel1+="เออะ"
	elif data=="เ":
		vowel1+="เอ"
	elif data=="แ":
		vowel1+="แอ"
	elif data=="แื":
		vowel1+="แอือ"
	elif data=="ำ":
		vowel1+="อ"+data
	elif data=="ุ":
		vowel1+="อ"+data
	elif data=="ู":
		vowel1+="อ"+data
	elif data=="โ":
		vowel1+=data+"อะ"
	elif data=="ใ":
		vowel1+=data+"อ"
	elif data=="ไ":
		vowel1+=data+"อ"
	elif data=="แออ" or data=="เออ":
		vowel1+=data
	elif data=="แออะ" or data=="เออะ":
		vowel1+=data
	else:
		vowel1+=data
	return vowel1
def tone(data):
	if is_match(r"[ก-ฮ]",data):
		b=data+"อ"
	elif data == "่":
		b="ไม้เอก"
	elif data == "้":
		b="ไม้โท"
	elif data == "๊":
		b="ไม้ตรี"
	elif data == "๋":
		b="ไม้จัตวา"
	elif data == "็":
		b="ไม้ไต่คู้"
	elif data == "ั":
		b="ไม้หันอากาศ"
	else:
		b=vowel(data)
	return b
def word(data):
	v=list(data)
	aaa=list(data)
	m=search(r"[่|้|๊|๋]",data)
	if m:
		del(v[v.index(m.group(0))])
		v.append(m.group(0))
	a1=search(r"[เ|แ]",data)
	a6=search(r"[อะ]",data)
	m=search(r"[เ|แ|ิ|ื|โ|ใ|ไ|อ]",data)
	if a1 and a6:
		print("F:"+a1.group(0)+a6.group(0))
		if v[v.index(a1.group(0))+2] == "อ" and v[v.index(a1.group(0))+3] == "ะ":
			num1=v.index(a1.group(0))+2
			del(v[num1])
	if m:
		#print("Ok : ")
		a1=search(r"[เ|แ]",data)
		a2=search(r"[ิ|ื|ะ]",data)
		a3=search(r"[โ|ใ|ไ]",data)
		a4=search(r"[่|้|๊|๋]",data)
		a5=search(r"[ะ|อ]",data) 
		a6=search(r"[อ]",data) 
		a7=search(r"[ิ|ื]",data)
		if a1 and a2:
			num1=v.index(a1.group(0))
			#print(v)
			#print(a1.group(0),a2.group(0))
			#print(num1)
			del(v[num1])
			num2=v.index(a2.group(0))
			del(v[num2])
			if a4:
				v.insert(len(v)-1,(a1.group(0)+a2.group(0)))
			else:
				v.append(a1.group(0)+a2.group(0))
			#print("f : ",v)
		elif a3:
			num1=v.index(a3.group(0))
			del(v[num1])
			if a4:
				v.insert(len(v)-1,a3.group(0))
			else:
				v.append(a3.group(0))
		elif a1 and a6: 
			print("O:"+(a1.group(0)+'อ'+a6.group(0)))
			if v[v.index(a1.group(0))+2] == a6.group(0): # เออ แออ 
				num1=v.index(a1.group(0))
				del(v[num1])
				num2=v.index("อ")
				
				print(v)
				if a4:
					del(v[num2])
					v.insert(len(v)-1,a1.group(0)+'อ'+a6.group(0))
				else:
					v[num2]=a1.group(0)+'อ'+a6.group(0)
		elif a2 and a5: 
			try:
				if v[v.index(a2.group(0))+2] == a5.group(0): # เอะ แอะ 
					num1=v.index(a2.group(0))
					del(v[num1])
					num2=v.index(a5.group(0))
					del(v[num2])
					if a4:
						v.insert(len(v)-1,a2.group(0)+a5.group(0))
					else:
						v.append(a2.group(0)+a5.group(0))
			except:
				pass
		elif a7 and a6:
			num1=v.index(a7.group(0)) 
			if v[num1+1]==a6.group(0):
				print("a: ",v)
				del(v[num1])
				del(v[v.index(a6.group(0))])
				if a4:
					v.insert(len(v)-1,"อ"+a7.group(0)+a6.group(0))
				else:
					v.append("อ"+a7.group(0)+a6.group(0))
		elif a1:
			num1=v.index(a1.group(0)) == 0
			if num1:
				del(v[0])
				if a4:
					v.insert(len(v)-1,a1.group(0))
				else:
					v.append(a1.group(0))
	b=""
	i=0
	while i<len(v):
		m=search(r"[่|้|๊|๋]",v[i])
		if i+1<len(v):
			b+=tone(v[i])
		else:
			if m:
				b+=re.sub(r"[่|้|๊|๋]","",data)
				b+="-"
				b+=re.sub(r"[่|้|๊|๋]","",data)
				b+="-"
			b+=tone(v[i])
			b+="-"
		b+="-"
		i+=1
	b+=data
	#b=re.sub(r"-ออ-","-",b)
	bb = list(b)
	i=0
	if bb[0] == "-":
		del(bb[0])
	return (''.join(bb)).replace("--","-")
print(word("ปลา")) # ปอ-ลอ-อา-ปลา
print(word("อยาก")) # ออ-ยอ-อา-กอ-อยาก
print(word("หนา")) # หอ-นอ-อา-หนา
print(word("รถ")) # รอ-ถอ-รถ
print(word("ต้น")) # ตอ-นอ-ตน-ตน-ไม้โท-ต้น
print(word("หรา")) # หอ-รอ-อา-หรา
print(word("นอน")) # นอ-ออ-นอ-นอน
print(word("จ้า")) # จอ-อา-จา-จา-ไม้โท-จ้า
print(word("ตอง")) # ตอ-ออ-งอ-ตอง
print(word("ยัง")) # ยอ-ไม้หันอากาศ-งอ-ยัง
print(word("แข็ง")) # ขอ-ไม้ไต่คู้-งอ-แข็ง
print(word("ผม")) # ผอ-มอ-ผม
print(word("ต้น")+"\t"+word("ตาล")) # ตอ-นอ-ตน-ตน-ไม้โท-ต้น   ตอ-อา-ลอ-ตาล 
print(word("กัน")) # กอ-ไม้หันอากาศ-นอ-กัน
print(word("สลับ")) # สอ-ลอ-ไม้หันอากาศ-บอ-สลับ
print(word("มา")+"\t"+word("นะ")) # มอ-อา-มา        นอ-อะ-นะ
print(word("ครับ")) # คอ-รอ-ไม้หันอากาศ-บอ-ครับ
print(word("รถ")+"\t"+word("ไฟ")) # รอ-ถอ-รถ        ฟอ-ไอ-ไฟ
print(word("กำ")) # กอ-อำ-กำ
print(word("เด้อ")) # ดอ-เดอ-เดอ-ไม้โท-เด้อ
print(word("คอม")) # คอ-ออ-มอ-คอม
print(word("สนาม")) # สอ-นอ-อา-มอ-สนาม
print(word("ใบ")+"\t"+word("ไม้")) # บอ-ใอ-ใบ        มอ-ไอ-ไม-ไม-ไม้โท-ไม้
print(word("ลำ")+"\t"+word("ใย")) # ลอ-อำ-ลำ        ยอ-ใอ-ใย
print(word("ขโมย")) # ขอ-มอ-ยอ-โอะ-ขโมย
print(word("เค็ม")) # คอ-ไม้ไต่คู้-มอ-เค็ม
print(word("รัก")) # รอ-ไม้หันอากาศ-กอ-รัก
print(word("เพื่อน")) # พอ-ออ-นอ-เอือ-เพือน-เพือน-ไม้เอก-เพื่อน
print(word("นาง")) # นอ-อา-งอ-นาง
print(word("น่า")+"\t"+word("รัก")) # นอ-อา-นา-นา-ไม้เอก-น่า  รอ-ไม้หันอากาศ-กอ-รัก
print(word("หนัง")+"\t"+word("สือ"))
print(word("ไป")) # ปอ-ไอ-ไป
print(word("เยอะ")) # ยอ-เอะ-เยอะ
print(word("อ่าน")) #ออ-อา-นอ-อาน-อาน-ไม้เอก-อ่าน
print(word("มะ")+"\t"+word("เขือ")+"\t"+word("เทศ")) # มอ-อะ-มะ        ขอ-ออ-เอือ-เขือ ทอ-ศอ-เทศ
print(word("หนัง")+"\t"+word("สือ"))
print(word("ขนุน")) #! ขอ-นอ-อุ-นอ-ขนุน
print(word("ถนน")) # ถอ-นอ-นอ-ถนน
print(word("พราง"))