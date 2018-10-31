# -*- coding: utf-8 -*-

"""ตัวตัดคำภาษาไทยโดยใช้หลักการ maximal matching และ Thai Character Cluster (TCC)
พัฒนาโดยคุณ Korakot Chaovavanich
Notebooks:
https://colab.research.google.com/notebook#fileId=1V1Z657_5eSWPo8rLfVRwA0A5E4vkg7SI
https://colab.research.google.com/drive/14Ibg-ngZXj15RKwjNwoZlOT32fQBOrBx#scrollTo=MYZ7NzAR7Dmw
"""
from __future__ import absolute_import, unicode_literals

import re
from collections import defaultdict
from heapq import heappop, heappush  # for priority queue

from pythainlp.tokenize import DEFAULT_DICT_TRIE

from .tcc import tcc_pos

# ช่วยตัดพวกภาษาอังกฤษ เป็นต้น
PAT_ENG = re.compile(
    r"""(?x)
[-a-zA-Z]+|   # english
\d[\d,\.]*|   # number
[ \t]+|       # space
\r?\n         # newline
"""
)

PAT_TWOCHARS = re.compile("[ก-ฮ]{,2}$")


def bfs_paths_graph(graph, start, goal):
    queue = [(start, [start])]
    while queue:
        (vertex, path) = queue.pop(0)
        for next in graph[vertex]:
            if next == goal:
                yield path + [next]
            else:
                queue.append((next, path + [next]))


def onecut(text, trie):
    graph = defaultdict(list)  # main data structure
    allow_pos = tcc_pos(text)  # ตำแหน่งที่ตัด ต้องตรงกับ tcc

    q = [0]  # min-heap queue
    last_p = 0  # last position for yield
    while q[0] < len(text):
        p = heappop(q)

        for w in trie.prefixes(text[p:]):
            p_ = p + len(w)
            if p_ in allow_pos:  # เลือกที่สอดคล้อง tcc
                graph[p].append(p_)
                if p_ not in q:
                    heappush(q, p_)

        # กรณี length 1 คือ ไม่กำกวมแล้ว ส่งผลลัพธ์ก่อนนี้คืนได้
        if len(q) == 1:
            pp = next(bfs_paths_graph(graph, last_p, q[0]))
            # เริ่มต้น last_p = pp[0] เอง
            for p in pp[1:]:
                yield text[last_p:p]
                last_p = p
            # สุดท้าย last_p == q[0] เอง

        # กรณี length 0 คือ ไม่มีใน dict
        if len(q) == 0:
            m = PAT_ENG.match(text[p:])
            if m:  # อังกฤษ, เลข, ว่าง
                i = p + m.end()
            else:  # skip น้อยที่สุด ที่เป็นไปได้
                for i in range(p + 1, len(text)):
                    if i in allow_pos:  # ใช้ tcc ด้วย
                        ww = [w for w in trie.prefixes(text[i:]) if (i + len(w) in allow_pos)]
                        ww = [w for w in ww if not PAT_TWOCHARS.match(w)]
                        m = PAT_ENG.match(text[i:])
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
