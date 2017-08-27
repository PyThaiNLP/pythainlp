# -*- coding: utf-8 -*-
from __future__ import absolute_import,unicode_literals
def spell(word,engine='pn'):
    '''
    คำสั่งเช็คคำผิด spell(word,engine='pn')
    engine ที่รองรับ
    - pn พัฒนามาจาก Peter Norvig (ค่าเริ่มต้น)
    - hunspell ใช้ hunspell (ไม่รองรับ Python 2.7)
    '''
    if engine=='pn':
        from .pn import spell as spell1
    elif engine=='hunspell':
        from .hunspell import spell as spell1
    return spell1(word)
