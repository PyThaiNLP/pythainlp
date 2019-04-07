# -*- coding: utf-8 -*-
"""
Perceptron Part-Of-Speech tagger
"""
import os
from typing import List, Tuple

import dill
from pythainlp.corpus import corpus_path

_ORCHID_DATA_FILENAME = "orchid_pt_tagger.dill"
_PUD_DATA_FILENAME = "ud_thai_pud_pt_tagger.dill"


def _load_tagger(filename):
    data_filename = os.path.join(corpus_path(), filename)
    with open(data_filename, "rb") as fh:
        model = dill.load(fh)
    return model


_ORCHID_TAGGER = _load_tagger(_ORCHID_DATA_FILENAME)
_PUD_TAGGER = _load_tagger(_PUD_DATA_FILENAME)


def tag(words: List[str], corpus: str = "pud") -> List[Tuple[str, str]]:
    """
    รับค่าเป็น ''list'' คืนค่าเป็น ''list'' เช่น [('คำ', 'ชนิดคำ'), ('คำ', 'ชนิดคำ'), ...]
    """
    if not words:
        return []

    if corpus == "orchid":
        tagger = _ORCHID_TAGGER
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
        t2 = tagger.tag(words)
        t = []
        i = 0
        while i < len(t2):
            word = t2[i][0]
            tag = t2[i][1]
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
            t.append((word, tag))
            i += 1
    else:  # default, use "pud" as a corpus
        tagger = _PUD_TAGGER
        t = tagger.tag(words)

    return t
