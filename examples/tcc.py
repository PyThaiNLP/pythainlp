# -*- coding: utf-8 -*-

from pythainlp.tokenize import tcc

print(tcc.tcc("ประเทศไทย"))  # ป/ระ/เท/ศ/ไท/ย

print(tcc.tcc_pos("ประเทศไทย"))  # {1, 3, 5, 6, 8, 9}

for ch in tcc.tcc_gen("ประเทศไทย"):  # ป-ระ-เท-ศ-ไท-ย-
    print(ch, end='-')
