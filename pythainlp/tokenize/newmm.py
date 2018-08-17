# -*- coding: utf-8 -*-

'''ตัวตัดคำภาษาไทยโดยใช้หลักการ maximal matching และ TCC
พัฒนาโดยคุณ Korakot Chaovavanich
Notebook : https://colab.research.google.com/notebook#fileId=1V1Z657_5eSWPo8rLfVRwA0A5E4vkg7SI
https://colab.research.google.com/drive/14Ibg-ngZXj15RKwjNwoZlOT32fQBOrBx#scrollTo=MYZ7NzAR7Dmw
'''
from __future__ import absolute_import, unicode_literals
import re
from collections import defaultdict
from heapq import heappush, heappop  # for priority queue
from pythainlp.tokenize import DEFAULT_DICT_TRIE

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

def bfs_paths_graph(graph, start, goal):
  queue = [(start, [start])]
  while queue:
    (vertex, path) = queue.pop(0)
    for next in graph[vertex]:
      if next == goal:
        yield path + [next]
      else:
        queue.append((next, path+[next]))

def onecut(text, trie):
  graph = defaultdict(list)  # main data structure
  allow_pos = tcc_pos(text)     # ตำแหน่งที่ตัด ต้องตรงกับ tcc
  
  q = [0]       # min-heap queue
  last_p = 0    # last position for yield
  while q[0] < len(text):
      p = heappop(q)

      for w in trie.prefixes(text[p:]):
          p_ = p + len(w)
          if p_ in allow_pos:  # เลือกที่สอดคล้อง tcc
            graph[p].append(p_)
            if p_ not in q:
              heappush(q, p_)   

      # กรณี length 1 คือ ไม่กำกวมแล้ว ส่งผลลัพธ์ก่อนนี้คืนได้
      if len(q)==1:
          pp = next(bfs_paths_graph(graph, last_p, q[0]))
          # เริ่มต้น last_p = pp[0] เอง
          for p in pp[1:]:
            yield text[last_p:p]
            last_p = p
          # สุดท้าย last_p == q[0] เอง

      # กรณี length 0  คือ ไม่มีใน dict
      if len(q)==0:
          m = pat_eng.match(text[p:])
          if m: # อังกฤษ, เลข, ว่าง
              i = p + m.end()
          else: # skip น้อยที่สุด ที่เป็นไปได้
              for i in range(p+1, len(text)):
                  if i in allow_pos:   # ใช้ tcc ด้วย
                      ww = [w for w in trie.prefixes(text[i:]) if (i+len(w) in allow_pos)]
                      ww = [w for w in ww if not re.match('[ก-ฮ]{,2}$', w)]
                      m = pat_eng.match(text[i:])
                      if ww or m:
                          break
              else:
                  i = len(text)
          w = text[p:i]
          graph[p].append(i)
          yield w
          last_p = i
          heappush(q, i)

# ช่วยให้ไม่ต้องพิมพ์ยาวๆ


def mmcut(text, trie=None):
    if not trie:
        trie = DEFAULT_DICT_TRIE
    return list(onecut(text, trie))
