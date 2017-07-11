# -*- coding: utf-8 -*-
'''
โปรแกรมรวบรวมคำศัพท์เพื่อสร้าง dict
===================
เขียนโดย นาย วรรณพงษ์  ภัททิยไพบูลย์

29/5/2560
22:45 น.
'''
import codecs
def data(template_file):
	'''
	เปิดไฟล์แล้วอ่านทีละบรรทัดส่งออกเป็น list
	'''
	with codecs.open(template_file, 'r',encoding='utf-8-sig') as f:
		lines = f.read().splitlines()
	f.close()
	return lines
def list1list(list1,list2):
	'''
	ทำการเปรียบเทียบ 2 list
	'''
	i=0
	list2=list2
	list1=list1
	while i<len(list2):
		if (list2[i] in list1) == False:
			'''
			หากไม่มีใน list1 ให้เพิ่มเข้าไปใน list1
			'''
			list1.append(list2[i])
		i+=1
	return list1
def savetofile(file,data1,mode='w+'):
	'''
	บันทึกข้อมูลที่รับมาลงไฟล์
	'''
	thefile=codecs.open(file, mode,encoding='utf-8-sig')
	for item in data1:
		thefile.write("%s\n" % item)
	thefile.close()
	print("Ok")

listno1=data("stopwords-th-old.txt") # ไฟล์ตั้งต้น
filelist = [
"stopwords-th1.txt",
"stopwords-th2.txt",
"stopwords-th3.txt",
"stopwords-th4.txt"
] # รายการไฟล์ทั้งหมด
for namefile in filelist:
	print(namefile)
	listno2=data(namefile)
	listno1=list1list(list1=listno1,list2=listno2)
savetofile("stopwords-th.txt",listno1)
