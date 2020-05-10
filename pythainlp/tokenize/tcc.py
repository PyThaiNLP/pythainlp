# -*- coding: utf-8 -*-
"""
The implementation of tokenizer accorinding to Thai Character Clusters (TCCs)
rules purposed by `Theeramunkong et al. 2000. \
    <http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.59.2548>`_

Credits:
    * TCC: Jakkrit TeCho
    * Grammar: Wittawat Jitkrittum (`link to the source file \
      <https://github.com/wittawatj/jtcc/blob/master/TCC.g>`_)
    * Python code: Korakot Chaovavanich
"""
import re
from typing import List, Set

_RE_TCC = (
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

_PAT_TCC = re.compile("|".join(_RE_TCC))


def tcc(text: str) -> str:
    """
    TCC generator, generates Thai Character Clusters

    :param str text: text to be tokenized to character clusters
    :return: subwords (character clusters)
    :rtype: Iterator[str]
    """
    if not text or not isinstance(text, str):
        return ""

    len_text = len(text)
    p = 0
    while p < len_text:
        m = _PAT_TCC.match(text[p:])
        if m:
            n = m.span()[1]
        else:
            n = 1
        yield text[p : p + n]
        p += n


def tcc_pos(text: str) -> Set[int]:
    """
    TCC positions

    :param str text: text to be tokenized to character clusters
    :return: list of the end position of subwords
    :rtype: set[int]
    """
    if not text or not isinstance(text, str):
        return set()

    p_set = set()
    p = 0
    for w in tcc(text):
        p += len(w)
        p_set.add(p)

    return p_set


def segment(text: str) -> List[str]:
    """
    Subword segmentation

    :param str text: text to be tokenized to character clusters
    :return: list of subwords (character clusters), tokenized from the text
    :rtype: list[str]

    """

    return list(tcc(text))
