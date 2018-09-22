# -*- coding: utf-8 -*-
from __future__ import absolute_import,division,unicode_literals,print_function
from builtins import *
'''
Thai soundex

โค้ดพัฒนาโดย คุณ Korakot Chaovavanich (จาก https://gist.github.com/korakot/0b772e09340cac2f493868da035597e8)
'''
import re
def LK82(s):
    '''
    LK82 - It's a thai soundex rule.

    :param str s: thai word
    :return: LK82 soundex
    '''
    t1 = str.maketrans("กขฃคฅฆงจฉชฌซศษสญยฎดฏตณนฐฑฒถทธบปผพภฝฟมรลฬฤฦวหฮอ","กกกกกกงจชชชซซซซยยดดตตนนททททททบปพพพฟฟมรรรรรวหหอ")
    t2 = str.maketrans("กขฃคฅฆงจฉชซฌฎฏฐฑฒดตถทธศษสญณนรลฬฤฦบปพฟภผฝมำยวไใหฮาๅึืเแโุูอ","1111112333333333333333333444444445555555667777889AAABCDEEF")
    res = []
    s = re.sub("[่-๋]", "", s)  # 4.ลบวรรณยุกต์
    s = re.sub('จน์|มณ์|ณฑ์|ทร์|ตร์|[ก-ฮ]์|[ก-ฮ][ะ-ู]์', "", s) # 4.ลบตัวการันต์
    s = re.sub("[็ํฺๆฯ]", "", s)  # 5.ทิ้งไม้ไต่คู่ ฯลฯ
    # 6.เข้ารหัสตัวแรก
    if 'ก'<=s[0]<='ฮ':
        res.append(s[0].translate(t1))
        s = s[1:]
    else:
        res.append(s[1].translate(t1))
        res.append(s[0].translate(t2))
        s = s[2:]
    # เข้ารหัสตัวที่เหลือ
    i_v = None  # ตำแหน่งตัวคั่นล่าสุด (สระ)
    for i,c in enumerate(s):
        if c in "ะัิี":  # 7. ตัวคั่นเฉยๆ
            i_v = i
            res.append('')
        elif c in "าๅึืู": # 8.คั่นและใส่
            i_v = i
            res.append(c.translate(t2))
        elif c == 'ุ':   # 9.สระอุ
            i_v = i
            if i==0 or (s[i-1] not in "ตธ"):
                res.append(c.translate(t2))
            else:
                res.append('')
        elif c in 'หอ':
            if i+1<len(s) and (s[i+1] in "ึืุู"):
                res.append(c.translate(t2))
        elif c in 'รวยฤฦ':
            if i_v == i-1 or (i+1<len(s) and (s[i+1] in "ึืุู")):
                res.append(c.translate(t2))
        else:
            res.append(c.translate(t2))  # 12.
    # 13. เอาตัวซ้ำออก
    res2 = [res[0]]
    for i in range(1, len(res)):
        if res[i] != res[i-1]:
            res2.append(res[i])
    # 14. เติมศูนย์ให้ครบ ถ้าเกินก็ตัด
    return ("".join(res2)+"0000")[:5]
def Udom83(s):
    '''
    Udom83 - It's a thai soundex rule.
    
    :param str s: thai word
    :return: LK82 soundex
    '''
    tu1 = str.maketrans("กขฃคฅฆงจฉชฌซศษสฎดฏตฐฑฒถทธณนบปผพภฝฟมญยรลฬฤฦวอหฮ" ,"กขขขขขงจชชชสสสสดดตตททททททนนบปพพพฟฟมยยรรรรรวอฮฮ")
    tu2 = str.maketrans("มวำกขฃคฅฆงยญณนฎฏดตศษสบปพภผฝฟหอฮจฉชซฌฐฑฒถทธรฤลฦ","0001111112233344444445555666666777778888889999")
    s = re.sub('รร([เ-ไ])', 'ัน\\1', s)  # 4.
    s = re.sub('รร([ก-ฮ][ก-ฮเ-ไ])', 'ั\\1', s) # 5.
    s = re.sub('รร([ก-ฮ][ะ-ู่-์])','ัน\\1', s)
    s = re.sub('รร', 'ัน', s)
    s = re.sub('ไ([ก-ฮ]ย)', '\\1', s)   # 2.
    s = re.sub('[ไใ]([ก-ฮ])','\\1ย', s)
    s = re.sub('ำ(ม[ะ-ู])', 'ม\\1', s)   # 3.
    s = re.sub('ำม', 'ม', s)
    s = re.sub('ำ', 'ม', s)
    s = re.sub('จน์|มณ์|ณฑ์|ทร์|ตร์|[ก-ฮ]์|[ก-ฮ][ะ-ู]์', "", s) # 6.
    s = re.sub('[ะ-์]', '', s) # 7.
    sd = s[0].translate(tu1)
    sd += s[1:].translate(tu2)
    return (sd+'000000')[:7]
if __name__ == '__main__':
    print(LK82('รถ'))
    print(LK82('รส'))
    print(LK82('รด'))
    print(LK82('จัน'))
    print(LK82('จันทร์'))