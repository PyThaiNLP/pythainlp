# -*- coding: utf-8 -*-

from pythainlp.tokenize import sent_tokenize, word_tokenize, Tokenizer

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

print(word_tokenize(text2))  # default engine is "newmm"
# ['กฎหมายแรงงาน']

print(word_tokenize(text2, engine="longest"))
# ['กฎหมาย', 'แรงงาน']

words = ["กฎ", "งาน"]
tokenizer = Tokenizer(words)
tokenizer.word_tokenize(text2)

