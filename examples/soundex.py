# -*- coding: utf-8 -*-

from pythainlp.soundex import lk82, metasound, udom83

texts = ["บูรณะ", "บูรณการ", "มัก", "มัค", "มรรค", "ลัก", "รัก", "รักษ์", ""]
for text in texts:
    print(
        "{} - lk82: {} - udom83: {} - metasound: {}".format(
            text, lk82(text), udom83(text), metasound(text)
        )
    )

# check equivalence
print(lk82("รถ") == lk82("รด"))
print(udom83("วรร") == udom83("วัน"))
print(metasound("นพ") == metasound("นภ"))
