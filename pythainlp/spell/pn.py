# -*- coding: utf-8 -*-
"""
Fork from Peter Norvig's Python codes at http://norvig.com/spell-correct.html
"""
from __future__ import absolute_import,print_function,unicode_literals
from builtins import *
from pythainlp.corpus.thaiword import get_data
from collections import Counter
WORDS = Counter(get_data())
def P(word, N=sum(WORDS.values())):
    'Probability of `word`.'
    return WORDS[word] / N
def correction(word):
    'แสดงคำที่เป็นไปได้มากที่สุด'
    return max(spell(word), key=P)
def known(words):
    return list(w for w in words if w in WORDS)
def edits1(word):
    letters = ['ก', 'ข', 'ฃ', 'ค', 'ฅ', 'ฆ', 'ง', 'จ', 'ฉ', 'ช', 'ซ', 'ฌ', 'ญ', 'ฎ', 'ฏ', 'ฐ', 'ฑ', 'ฒ', 'ณ', 'ด', 'ต', 'ถ', 'ท', 'ธ', 'น', 'บ', 'ป', 'ผ', 'ฝ', 'พ', 'ฟ', 'ภ', 'ม', 'ย', 'ร', 'ฤ', 'ล', 'ฦ', 'ว', 'ศ', 'ษ', 'ส', 'ห', 'ฬ', 'อ', 'ฮ', 'ฯ', 'ะ', 'ั', 'า', 'ำ', 'ิ', 'ี', 'ึ', 'ื', 'ุ', 'ู', 'ฺ', '\u0e3b', '\u0e3c', '\u0e3d', '\u0e3e', '฿', 'เ', 'แ', 'โ', 'ใ', 'ไ', 'ๅ', 'ๆ', '็', '่', '้', '๊', '๋', '์']
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)
def edits2(word):
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))
def spell(word):
    if word=='':
        return ''
    else:
        return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])
