# -*- coding: utf-8 -*-
"""
Dictionary-based Thai Word Segmentation
using maximal matching algorithm and Thai Character Cluster (TCC)

The code is based on the notebooks created by Korakot Chaovavanich

:See Also:
    * \
        https://colab.research.google.com/notebook#fileId=1V1Z657_5eSWPo8rLfVRwA0A5E4vkg7SI
    * \
        https://colab.research.google.com/drive/14Ibg-ngZXj15RKwjNwoZlOT32fQBOrBx#scrollTo=MYZ7NzAR7Dmw
"""
import re
from collections import defaultdict
from heapq import heappop, heappush  # for priority queue
from typing import List

from marisa_trie import Trie
from pythainlp.tokenize import DEFAULT_DICT_TRIE

from .tcc import tcc_pos

# ช่วยตัดพวกภาษาอังกฤษ เป็นต้น
_PAT_ENG = re.compile(
    r"""(?x)
[-a-zA-Z]+|   # english
\d[\d,\.]*|   # number
[ \t]+|       # space
\r?\n         # newline
"""
)

_PAT_TWOCHARS = re.compile("[ก-ฮ]{,2}$")


def _bfs_paths_graph(graph, start, goal):
    queue = [(start, [start])]
    while queue:
        (vertex, path) = queue.pop(0)
        for next in graph[vertex]:
            if next == goal:
                yield path + [next]
            else:
                queue.append((next, path + [next]))


def _onecut(text: str, custom_dict: Trie):
    graph = defaultdict(list)  # main data structure
    allow_pos = tcc_pos(text)  # separating position should aligned with TCC

    q = [0]  # min-heap queue
    last_p = 0  # last position for yield
    while q[0] < len(text):
        p = heappop(q)

        for w in custom_dict.prefixes(text[p:]):
            p_ = p + len(w)
            if p_ in allow_pos:  # เลือกที่สอดคล้อง tcc
                graph[p].append(p_)
                if p_ not in q:
                    heappush(q, p_)

        # กรณี length 1 คือ ไม่กำกวมแล้ว ส่งผลลัพธ์ก่อนนี้คืนได้
        if len(q) == 1:
            pp = next(_bfs_paths_graph(graph, last_p, q[0]))
            # เริ่มต้น last_p = pp[0] เอง
            for p in pp[1:]:
                yield text[last_p:p]
                last_p = p
            # สุดท้าย last_p == q[0] เอง

        # กรณี length 0 คือ ไม่มีใน dict
        if len(q) == 0:
            m = _PAT_ENG.match(text[p:])
            if m:  # อังกฤษ, เลข, ว่าง
                i = p + m.end()
            else:  # skip น้อยที่สุด ที่เป็นไปได้
                for i in range(p + 1, len(text)):
                    if i in allow_pos:  # ใช้ tcc ด้วย
                        ww = [
                            w
                            for w in custom_dict.prefixes(text[i:])
                            if (i + len(w) in allow_pos)
                        ]
                        ww = [w for w in ww if not _PAT_TWOCHARS.match(w)]
                        m = _PAT_ENG.match(text[i:])
                        if ww or m:
                            break
                else:
                    i = len(text)
            w = text[p:i]
            graph[p].append(i)
            yield w
            last_p = i
            heappush(q, i)


def segment(text: str, custom_dict: Trie = None) -> List[str]:
    """
    Dictionary-based maximal matching word segmentation, constrained with Thai Character Cluster boundaries
    :param str text: text to be tokenized to words
    :return: list of words, tokenized from the text
    """
    if not text or not isinstance(text, str):
        return []

    if not custom_dict:
        custom_dict = DEFAULT_DICT_TRIE

    return list(_onecut(text, custom_dict))
