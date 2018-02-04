# -*- coding: utf-8 -*-

'''ตัวตัดคำภาษาไทยโดยใช้หลักการ maximal matching และ TCC
พัฒนาโดยคุณ Korakot Chaovavanich
Notebook : https://colab.research.google.com/notebook#fileId=1V1Z657_5eSWPo8rLfVRwA0A5E4vkg7SI
'''
from __future__ import absolute_import, unicode_literals
import re
from collections import defaultdict
from heapq import heappush, heappop  # for priority queue
from marisa_trie import Trie
from pythainlp.corpus.thaiword import get_data  # ดึงข้อมูลรายการคำในภาษาไทย


# ช่วยตัดพวกภาษาอังกฤษ เป็นต้น
pat_eng = re.compile(r'''(?x)
[-a-zA-Z]+|   # english
\d[\d,\.]*|   # number
[ \t]+|       # space
\r?\n         # newline
''')
# TCC
pat_tcc = """\
เc็c
เcctาะ
เccีtยะ
เccีtย(?=[เ-ไก-ฮ]|$)
เccอะ
เcc็c
เcิc์c
เcิtc
เcีtยะ?
เcืtอะ?
เc[ิีุู]tย(?=[เ-ไก-ฮ]|$)
เctา?ะ?
cัtวะ
c[ัื]tc[ุิะ]?
c[ิุู]์
c[ะ-ู]t
c็
ct[ะาำ]?
แc็c
แcc์
แctะ
แcc็c
แccc์
โctะ
[เ-ไ]ct
""".replace('c', '[ก-ฮ]').replace('t', '[่-๋]?').split()

THAI_WORDS = Trie(get_data())


def tcc(w):
  p = 0
  pat = re.compile("|".join(pat_tcc))
  while p < len(w):
    m = pat.match(w[p:])
    if m:
      n = m.span()[1]
    else:
      n = 1
    yield w[p:p + n]
    p += n


def tcc_pos(text):
  p_set = set()
  p = 0
  for w in tcc(text):
    p += len(w)
    p_set.add(p)
  return p_set


def serialize(words_at, p, p2):
  # find path ทั้งหมด แบบ depth first
  for w in words_at[p]:
    p_ = p + len(w)
    if p_ == p2:
      yield [w]
    elif p_ < p2:
      for path in serialize(words_at, p_, p2):
        yield [w] + path


def onecut(text, data=['']):
  if(data != ['']):
    trie = Trie(data)
  else:
    trie = THAI_WORDS
  words_at = defaultdict(list)  # main data structure
  allow_pos = tcc_pos(text)     # ตำแหน่งที่ตัด ต้องตรงกับ tcc

  q = [0]       # min-heap queue
  last_p = 0    # last position for yield
  while q[0] < len(text):
    p = heappop(q)

    for w in trie.prefixes(text[p:]):
      p_ = p + len(w)
      if p_ in allow_pos:  # เลือกที่สอดคล้อง tcc
        words_at[p].append(w)
        if p_ not in q:
          heappush(q, p_)

    # กรณี length 1 คือ ไม่กำกวมแล้ว ส่งผลลัพธ์ก่อนนี้คืนได้
    if len(q) == 1:
      paths = serialize(words_at, last_p, q[0])
      for w in min(paths, key=len):
        yield w
      last_p = q[0]

    # กรณี length 0  คือ ไม่มีใน dict
    if len(q) == 0:
      m = pat_eng.match(text[p:])
      if m:  # อังกฤษ, เลข, ว่าง
        i = p + m.end()
      else:  # skip น้อยที่สุด ที่เป็นไปได้
        for i in range(p + 1, len(text)):
          if i in allow_pos:   # ใช้ tcc ด้วย
            ww = trie.prefixes(text[i:])
            m = pat_eng.match(text[i:])
            if ww or m:
              break
        else:
          i = len(text)
      w = text[p:i]
      words_at[p].append(w)
      yield w
      last_p = i
      heappush(q, i)

# ช่วยให้ไม่ต้องพิมพ์ยาวๆ


def mmcut(text, data=['']):
  return list(onecut(text, data=data))
