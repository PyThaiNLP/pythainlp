# -*- coding: utf-8 -*-
from __future__ import absolute_import,division,unicode_literals,print_function
"""
โปรแกรม TCC ภาษาไทย
เดติด
TCC : Mr.Jakkrit TeCho
grammar : คุณ Wittawat Jitkrittum (https://github.com/wittawatj/jtcc/blob/master/TCC.g)
โค้ด : คุณ Korakot Chaovavanich
"""
import re
pat_list = """\
เc็c
เcctาะ
เccีtยะ
เccีtย(?=[เ-ไก-ฮ]|$)
เcc็c
เcิc์c
เcิtc
เcีtยะ?
เcืtอะ?
เc[ิีุู]tย(?=[เ-ไก-ฮ]|$)
เctา?ะ?
cัtวะ
c[ัื]tc[ุิะ]?
c[ิุู]์
c[ะ-ู]t
c็
ct[ะาำ]?
แc็c
แcc์
แctะ
แcc็c
แccc์
โctะ
[เ-ไ]ct
ๆ
ฯลฯ
ฯ
""".replace('c','[ก-ฮ]').replace('t', '[่-๋]?').split()
def tcc1(w):
    p = 0
    pat = re.compile("|".join(pat_list))
    while p<len(w):
        m = pat.match(w[p:])
        if m:
            n = m.span()[1]
        else:
            n = 1
        yield w[p:p+n]
        p += n
def tcc(w, sep='/'):
    return sep.join(tcc1(w))
if __name__ == '__main__':
    print(tcc('แมวกิน'))
    print(tcc('ประชาชน'))
    print(tcc('ขุดหลุม'))
    print(tcc('ยินดี'))