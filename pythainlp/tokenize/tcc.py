# -*- coding: utf-8 -*-
"""
Separate Thai text into Thai Character Cluster (TCC).
Based on "Character cluster based Thai information retrieval" (Theeramunkong et al. 2002)
http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.59.2548

Credits:
- TCC: Jakkrit TeCho
- Grammar: Wittawat Jitkrittum https://github.com/wittawatj/jtcc/blob/master/TCC.g
- Python code: Korakot Chaovavanich
"""
import re
from typing import List, Set

RE_TCC = (
    """\
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
""".replace(
        "c", "[ก-ฮ]"
    )
    .replace("t", "[่-๋]?")
    .split()
)

PAT_TCC = re.compile("|".join(RE_TCC))


def tcc_gen(w: str) -> str:
    if not w:
        return ""

    p = 0
    while p < len(w):
        m = PAT_TCC.match(w[p:])
        if m:
            n = m.span()[1]
        else:
            n = 1
        yield w[p : p + n]
        p += n


def tcc_pos(text: str) -> Set[int]:
    if not text:
        return set()

    p_set = set()
    p = 0
    for w in tcc_gen(text):
        p += len(w)
        p_set.add(p)

    return p_set


def tcc(text: str) -> List[str]:
    return list(tcc_gen(text))
