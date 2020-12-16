# -*- coding: utf-8 -*-
"""
nercut 0.1

Code by Wannaphong Phatthiyaphaibun
"""
from typing import List
from pythainlp.tag.named_entity import ThaiNameTagger

_thainer = ThaiNameTagger()

def segment(
    text: str,
    tag:List[str] = [
        "ORGANIZATION",
        "PERSON",
        "PHONE",
        "EMAIL",
        "DATE",
        "TIME"
    ]
) -> List[str]:
    """
    nercut 0.1

    Code by Wannaphong Phatthiyaphaibun

    neww+thainer word segmentation.

    :param str text: text to be tokenized to words
    :parm list tag: ThaiNER tag
    :return: list of words, tokenized from the text
    """
    global _thainer
    if not text or not isinstance(text, str):
        return []

    _ws = _thainer.get_ner(text, pos = False)
    _list_w = []
    _bi = ""
    _tag = ""
    for i,t in _ws:
        if t != "O":
            _tag_temp = t.split('-')[1]
        else:
            _tag_temp = "O"
        if t.startswith('B-') and _tag_temp in tag:
            if _bi!="" and _tag in tag:
                _list_w.append(_bi)
            _bi=""
            _bi += i
            _tag = t.replace('B-','')
        elif t.startswith('I-') and t.replace('I-','') == _tag and _tag_temp in tag:
            _bi += i
        elif t == "O" and _tag != "" and _tag in tag:
            _list_w.append(_bi)
            _bi=""
            _tag = ""
            _list_w.append(i)
        else:
            _bi=""
            _tag = ""
            _list_w.append(i)
    if _bi!="":
        _list_w.append(_bi)
    return _list_w