# -*- coding: utf-8 -*-

from pythainlp.soundex import LK82, Udom83

print(LK82("รถ") == LK82("รด"))

print(Udom83("วรร") == Udom83("วัน"))
