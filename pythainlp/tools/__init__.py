# -*- coding: utf-8 -*-
from __future__ import absolute_import,unicode_literals
def test_segmenter(segmenter, test):
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