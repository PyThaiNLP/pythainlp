# -*- coding: utf-8 -*-

from pythainlp.util import normalize

print(normalize("เเปลก") == "แปลก")  # เ เ ป ล ก กับ แปลก
