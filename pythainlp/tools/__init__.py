# -*- coding: utf-8 -*-
from __future__ import absolute_import,unicode_literals
import os
import dill
def file_trie(data):
	'''
	ใช้สร้างไฟล์ข้อมูลสำหรับระบบที่ใช้ trie
	'''
	path = os.path.join(os.path.expanduser("~"), 'pythainlp-data')#os.path.join(, 'pthainlp_trie.data')
	if not os.path.exists(path):
		os.makedirs(path)
	if data=="old":
		path = os.path.join(path, 'pythainlp_trie1.data')
	else:
		path = os.path.join(path, 'pythainlp_trie2.data')
	if not os.path.exists(path):
		#ถ้าไม่มีไฟล์
		import marisa_trie
		if data=="old":
			from pythainlp.corpus.thaiword import get_data # ข้อมูลเก่า
		else:
			from pythainlp.corpus.newthaiword import get_data # ข้อมูลเก่า
		with open(path,'wb') as dill_file:
			dill.dump(marisa_trie.Trie(get_data()),dill_file)
		dill_file.close()
	with open(path,'rb') as dill_file:
		data=dill.load(dill_file)
	dill_file.close()
	return data
def test_segmenter(segmenter, test):
    '''
    ระบบทดสอบการตัดคำ
    '''
    words = test
    result = segmenter
    correct = (result == words)
    if not correct:
        print ('expected', words)
        print('got     ', result)
    return correct
if __name__ == "__main__":
    from pythainlp.tokenize import word_tokenize
    text="ฉันเป็นคนและฉันรักภาษาไทยฉันอยู่ประเทศไทยฉันศึกษาอยู่ที่มหาวิทยาลัยพายุฝนกำลังมาต้องหลบแล้วล่ะคุณสบายดีไหม"
    test=["ฉัน","เป็น","คน","และ","ฉัน","รัก","ภาษาไทย","ฉัน","อยู่","ประเทศไทย","ฉัน","ศึกษา","อยู่","ที่","มหาวิทยาลัย","พายุฝน","กำลัง","มา","ต้อง","หลบ","แล้ว","ล่ะ","คุณ","สบายดี","ไหม"]
    print("icu :")
    pyicu=test_segmenter(word_tokenize(text,engine='icu'),test)
    print(pyicu)
    print("newmm :")
    newmm=test_segmenter(word_tokenize(text,engine='newmm'),test)
    print(newmm)
    print("mm :")
    mm=test_segmenter(word_tokenize(text,engine='mm'),test)
    print(mm)