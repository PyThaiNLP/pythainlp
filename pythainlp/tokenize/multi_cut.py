# -*- coding: utf-8 -*-
"""
โปรแกรม multi-cut
ตัดคำภาษาไทยโดยใช้วิธี Maximum Matching
โค้ดต้นฉบับโดย คุณ Korakot Chaovavanich
จาก https://www.facebook.com/groups/408004796247683/permalink/431283740586455/
และ https://gist.github.com/korakot/fe26c65dc9eed467f4497f784a805716
"""
import re
from collections import defaultdict

from pythainlp.tokenize import DEFAULT_DICT_TRIE


class LatticeString(str):
    """
    String subclass เพื่อเก็บวิธีตัดหลายๆ วิธี
    """

    def __new__(cls, value, multi=None, in_dict=True):
        return str.__new__(cls, value)

    def __init__(self, value, multi=None, in_dict=True):
        self.unique = True
        if multi:
            self.multi = list(multi)
            if len(self.multi) > 1:
                self.unique = False
        else:
            self.multi = [value]
        self.in_dict = in_dict  # บอกว่าเป็นคำมีในดิกหรือเปล่า


_RE_ENG = r"""(?x)
[-a-zA-Z]+|   # english
\d[\d,\.]*|   # number
[ \t]+|       # space
\r?\n         # newline
"""
_PAT_ENG = re.compile(_RE_ENG)


def _multicut(text, trie=None):
    """
    ส่งคืน LatticeString คืนมาเป็นก้อนๆ
    """
    len_text = len(text)
    if not trie:
        trie = DEFAULT_DICT_TRIE
    words_at = defaultdict(list)  # main data structure

    def serialize(p, p2):  # helper function
        for w in words_at[p]:
            p_ = p + len(w)
            if p_ == p2:
                yield w
            elif p_ < p2:
                for path in serialize(p_, p2):
                    yield w + "/" + path

    q = {0}
    last_p = 0  # last position for yield
    while min(q) < len_text:
        p = min(q)
        q -= {p}  # q.pop, but for set

        for w in trie.prefixes(text[p:]):
            words_at[p].append(w)
            q.add(p + len(w))

        if len(q) == 1:
            q0 = min(q)
            yield LatticeString(text[last_p:q0], serialize(last_p, q0))
            last_p = q0

        # กรณี len(q) == 0  คือ ไม่มีใน dict
        if len(q) == 0:
            m = _PAT_ENG.match(text[p:])
            if m:  # อังกฤษ, เลข, ว่าง
                i = p + m.span()[1]
            else:  # skip น้อยที่สุด ที่เป็นไปได้
                for i in range(p, len_text):
                    ww = trie.prefixes(text[i:])
                    m = _PAT_ENG.match(text[i:])
                    if ww or m:
                        break
                else:
                    i = len_text
            w = text[p:i]
            words_at[p].append(w)
            yield LatticeString(w, in_dict=False)
            last_p = i
            q.add(i)


def mmcut(text):
    res = []
    for w in _multicut(text):
        mm = min(w.multi, key=lambda x: x.count("/"))
        res.extend(mm.split("/"))
    return res


def _combine(ww):
    if ww == []:
        yield ""
    else:
        w = ww[0]
        for tail in _combine(ww[1:]):
            if w.unique:
                yield w + "|" + tail
            else:
                for m in w.multi:
                    yield m.replace("/", "|") + "|" + tail


def segment(text, trie=None):
    """
    ใช้ในการหา list ที่สามารถตัดคำได้ทั้งหมด
    """
    if not text:
        return []

    return list(_multicut(text, trie=trie))


def find_all_segment(text, trie=None):
    """
    ใช้ในการหา list ที่สามารถตัดคำได้ทั้งหมด
    """
    if not text:
        return []

    ww = list(_multicut(text, trie=trie))
    return list(_combine(ww))
