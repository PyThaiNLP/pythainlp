# -*- coding: utf-8 -*-
"""
Unigram Part-Of-Speech Tagger
"""
import json
import os
from typing import List, Tuple

import dill
import nltk.tag
from pythainlp.corpus import corpus_path

_THAI_POS_ORCHID_FILENAME = "orchid_pos_th.json"
_THAI_POS_ORCHID_PATH = os.path.join(corpus_path(), _THAI_POS_ORCHID_FILENAME)
_THAI_POS_PUD_FILENAME = "ud_thai_pud_unigram_tagger.dill"
_THAI_POS_PUD_PATH = os.path.join(corpus_path(), _THAI_POS_PUD_FILENAME)


def _orchid_tagger():
    with open(_THAI_POS_ORCHID_PATH, encoding="utf-8-sig") as f:
        model = json.load(f)
    return model


def _pud_tagger():
    with open(_THAI_POS_PUD_PATH, "rb") as handle:
        model = dill.load(handle)
    return model


def tag(words: List[str], corpus: str) -> List[Tuple[str, str]]:
    """
    รับค่าเป็น ''list'' คืนค่าเป็น ''list'' เช่น [('คำ', 'ชนิดคำ'), ('คำ', 'ชนิดคำ'), ...]
    """
    if not words:
        return []

    if corpus == "orchid":
        tagger = nltk.tag.UnigramTagger(model=_orchid_tagger())
        i = 0
        while i < len(words):
            if words[i] == " ":
                words[i] = "<space>"
            elif words[i] == "+":
                words[i] = "<plus>"
            elif words[i] == "-":
                words[i] = "<minus>"
            elif words[i] == "=":
                words[i] = "<equal>"
            elif words[i] == ",":
                words[i] = "<comma>"
            elif words[i] == "$":
                words[i] = "<dollar>"
            elif words[i] == ".":
                words[i] = "<full_stop>"
            elif words[i] == "(":
                words[i] = "<left_parenthesis>"
            elif words[i] == ")":
                words[i] = "<right_parenthesis>"
            elif words[i] == '"':
                words[i] = "<quotation>"
            elif words[i] == "@":
                words[i] = "<at_mark>"
            elif words[i] == "&":
                words[i] = "<ampersand>"
            elif words[i] == "{":
                words[i] = "<left_curly_bracket>"
            elif words[i] == "^":
                words[i] = "<circumflex_accent>"
            elif words[i] == "?":
                words[i] = "<question_mark>"
            elif words[i] == "<":
                words[i] = "<less_than>"
            elif words[i] == ">":
                words[i] = "<greater_than>"
            elif words[i] == "=":
                words[i] = "<equal>"
            elif words[i] == "!":
                words[i] = "<exclamation>"
            elif words[i] == "’":
                words[i] = "<apostrophe>"
            elif words[i] == ":":
                words[i] = "<colon>"
            elif words[i] == "*":
                words[i] = "<asterisk>"
            elif words[i] == ";":
                words[i] = "<semi_colon>"
            elif words[i] == "/":
                words[i] = "<slash>"
            i += 1
        t = tagger.tag(words)
        temp = []
        i = 0
        while i < len(t):
            word = t[i][0]
            tag = t[i][1]
            if word == "<space>":
                word = " "
            elif word == "<plus>":
                word = "+"
            elif word == "<minus>":
                word = "-"
            elif word == "<equal>":
                word = "="
            elif word == "<comma>":
                word = ","
            elif word == "<dollar>":
                word = "$"
            elif word == "<full_stop>":
                word = "."
            elif word == "<left_parenthesis>":
                word = "("
            elif word == "<right_parenthesis>":
                word = ")"
            elif word == "<quotation>":
                word = '"'
            elif word == "<at_mark>":
                word = "@"
            elif word == "<ampersand>":
                word = "&"
            elif word == "<left_curly_bracket>":
                word = "{"
            elif word == "<circumflex_accent>":
                word = "^"
            elif word == "<question_mark>":
                word = "?"
            elif word == "<less_than>":
                word = "<"
            elif word == "<greater_than>":
                word = ">"
            elif word == "<equal>":
                word = "="
            elif word == "<exclamation>":
                word = "!"
            elif word == "<apostrophe>":
                word = "’"
            elif word == "<colon>":
                word = ":"
            elif word == "<asterisk>":
                word = "*"
            elif word == "<semi_colon>":
                word = ";"
            elif word == "<slash>":
                word = "/"
            temp.append((word, tag))
            i += 1
        t = temp
    else:
        tagger = _pud_tagger()
        t = tagger.tag(words)

    return t
