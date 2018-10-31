# -*- coding: utf-8 -*-

from pythainlp.collation import collate

print(collate(["ไก่", "ไข่", "ก", "ฮา"]))  # ['ก', 'ไก่', 'ไข่', 'ฮา']
