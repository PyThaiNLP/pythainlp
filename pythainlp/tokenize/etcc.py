# -*- coding: utf-8 -*-
from __future__ import absolute_import,division,unicode_literals,print_function
'''
โปรแกรม ETCC ใน Python

พัฒนาโดย นาย วรรณพงษ์  ภัททิยไพบูลย์

19 มิ.ย. 2560

วิธีใช้งาน
etcc(คำ)
คืนค่า โดยมี / แบ่งกลุ่มคำ
'''
import re
C=['ก','ข','ฃ','ค','ฅ','ฆ','ง','จ','ฉ','ช','ฌ','ซ','ศ','ษ','ส','ญ','ฎ','ฑ','ด','ฏ','ต','ฐ','ฑ','ฒ','ถ','ท','ธ','ณ','น','บ','ป','ผ','พ','ภ','ฝ','ฟ','ม','ย','ร','ล','ฬ','ว','ห','ฮ']
UV=['็','ี','ื','ิ']
UV1=['ั','ี']
LV=['ุ','ู']
c='['+''.join(C)+']'
uv2='['+''.join(['ั','ื'])+']'
def etcc(text):
    """
    Enhanced Thai Character Cluster (ETCC)
    คั่นด้วย /
    รับ str
    ส่งออก str
    """
    if (re.search('[เแ]'+c+'['+''.join(UV)+']'+'\w',text,re.U)):
        search=re.findall('[เแ]'+c+'['+''.join(UV)+']'+'\w',text,re.U)
        for i in search:
            text=re.sub(i, '/'+i+'/', text)
    if (re.search(c+'['+''.join(UV1)+']'+c+c+'ุ'+'์',text,re.U)):
        search=re.findall(c+'['+''.join(UV1)+']'+c+c+'ุ'+'์',text,re.U)
        for i in search:
            text=re.sub(i, '//'+i+'/', text)
    if (re.search(c+uv2+c,text,re.U)):
        search=re.findall(c+uv2+c,text,re.U)
        for i in search:
            text=re.sub(i, '/'+i+'/', text)
    re.sub('//','/',text)
    if (re.search('เ'+c+'า'+'ะ',text,re.U)):
        search=re.findall('เ'+c+'า'+'ะ',text,re.U)
        for i in search:
            text=re.sub(i, '/'+i+'/', text)   
    if (re.search('เ'+'\w\w'+'า'+'ะ',text,re.U)):
        search=re.findall('เ'+'\w\w'+'า'+'ะ',text,re.U)
        for i in search:
            text=re.sub(i, '/'+i+'/', text)   
    text=re.sub('//','/',text)
    if (re.search(c+'['+''.join(UV1)+']'+c+c+'์',text,re.U)):
        search=re.findall(c+'['+''.join(UV1)+']'+c+c+'์',text,re.U)
        for i in search:
            text=re.sub(i, '/'+i+'/', text)   
    if (re.search('/'+c+''.join(['ุ', '์'])+'/',text,re.U)):
        '''แก้ไขในกรณี พัน/ธุ์'''
        search=re.findall('/'+c+''.join(['ุ', '์'])+'/',text,re.U)
        for i in search:
            ii=re.sub('/','', i)
            text=re.sub(i,ii+'/', text)
    return re.sub('//','/',text)
if __name__ == '__main__':
    print(etcc('พันธุ์เด็กเปียเสือเงินพังมือเพราะเกาะเอาะยีนส์เพราะเรือดีเพราะ'))