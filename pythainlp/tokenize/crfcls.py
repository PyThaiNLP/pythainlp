# -*- coding: utf-8 -*-
"""
Clause segmenter
"""
from typing import List

import pycrfsuite
from pythainlp.corpus import get_corpus_path
from pythainlp.tag import pos_tag


def _doc2features(doc, i):
    # features from current word
    curr_word = doc[i][0]
    curr_pos = doc[i][1]
    features = {
        "word.word": curr_word,
        "word.isspace": curr_word.isspace(),
        "word.isdigit()": curr_word.isdigit(),
        "postag": curr_pos,
    }

    # features from previous word
    if i > 0:
        prev_word = doc[i - 1][0]
        prev_pos = doc[i - 1][1]
        features["word.prevword"] = prev_word
        features["word.previsspace"] = prev_word.isspace()
        features["word.prevwordisdigit"] = prev_word.isdigit()
        features["word.prepostag"] = prev_pos
    else:
        features["BOS"] = True  # Beginning of Sequence

    # features from next word
    if i < len(doc) - 1:
        next_word = doc[i + 1][0]
        next_pos = doc[i + 1][1]
        features["word.nextword"] = next_word
        features["word.nextisspace"] = next_word.isspace()
        features["word.nextwordisdigit"] = next_word.isdigit()
        features["word.nextpostag"] = next_pos
    else:
        features["EOS"] = True  # End of Sequence

    return features


def _extract_features(doc):
    return [_doc2features(doc, i) for i in range(len(doc))]


_CORPUS_NAME = "lst20-cls"
tagger = pycrfsuite.Tagger()
tagger.open(get_corpus_path(_CORPUS_NAME))


def segment(doc: List[str]) -> List[List[str]]:
    word_tags = pos_tag(doc, corpus="lst20")
    features = _extract_features(word_tags)
    word_markers = list(zip(doc, tagger.tag(features)))

    clauses = []
    temp = []
    len_doc = len(doc) - 1
    for i, word_marker in enumerate(word_markers):
        word, marker = word_marker
        if marker == "E_CLS" or i == len_doc:
            temp.append(word)
            clauses.append(temp)
            temp = []
        else:
            temp.append(word)

    return clauses
