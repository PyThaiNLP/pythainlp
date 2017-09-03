# -*- coding: utf-8 -*-
from __future__ import absolute_import
from pythainlp.corpus import stopwords
from pythainlp.rank import rank
def find_keyword(word_list,lentext=3):
    '''
    ระบบค้นหาคำสำคัญ
    หลักการ ลบ stopword ออกแล้ว นับจำนวนคำที่ส่งค่าออกมา

    find_keyword(word_list,lentext=3)
    word_list คือ คำที่อยู่ใน list
    lentext คือ จำนวนคำที่มีอยู่ใน list สำหรับใช้กำหนดค่าหา keyword ค่าเริ่มต้นคือ 3
    '''
    filtered_words = [word for word in word_list if word not in set(stopwords.words('thai'))]
    word_list=rank(filtered_words)
    return {k:v for k, v in word_list.items() if v>=lentext}