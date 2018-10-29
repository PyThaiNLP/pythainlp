# -*- coding: utf-8 -*-

from pythainlp.soundex import lk82, metasound, udom83

print(lk82("รถ") == lk82("รด"))
print(udom83("วรร") == udom83("วัน"))
print(metasound("นพ") == metasound("นภ"))
