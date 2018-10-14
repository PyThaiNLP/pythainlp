# -*- coding: utf-8 -*-

from pythainlp.tokenize import sent_tokenize, word_tokenize

text = "ฉันรักภาษาไทย เพราะฉันใช้ภาษาไทย "
print(text)

print(sent_tokenize(text))
# ['ฉันรักภาษาไทย', 'เพราะฉันใช้ภาษาไทย', '']

print(word_tokenize(text))
# ['ฉัน', 'รัก', 'ภาษาไทย', ' ', 'เพราะ', 'ฉัน', 'ใช้', 'ภาษาไทย', ' ']

print(word_tokenize(text, whitespaces=False))
# ['ฉัน', 'รัก', 'ภาษาไทย', 'เพราะ', 'ฉัน', 'ใช้', 'ภาษาไทย']

text2 = "กฎหมายแรงงาน"
print(text2)

print(word_tokenize(text2))
# ['กฎหมายแรงงาน']

print(word_tokenize(text2, engine="longest-matching"))
# ['กฎหมาย', 'แรงงาน']
