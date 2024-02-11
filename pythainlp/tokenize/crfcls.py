# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
"""
Clause segmenter
"""
from typing import List

import pycrfsuite
from pythainlp.tag import pos_tag
from pythainlp.corpus import path_pythainlp_corpus


def _doc2features(doc, i):
    # features from current word
    curr_word = doc[i][0]
    curr_pos = doc[i][1]
    features = {
        "word.curr_word": curr_word,
        "word.curr_isspace": curr_word.isspace(),
        "word.curr_isdigit": curr_word.isdigit(),
        "word.curr_postag": curr_pos,
    }

    # features from previous word
    if i > 0:
        prev_word = doc[i - 1][0]
        prev_pos = doc[i - 1][1]
        features["word.prev_word"] = prev_word
        features["word.prev_isspace"] = prev_word.isspace()
        features["word.prev_isdigit"] = prev_word.isdigit()
        features["word.prev_postag"] = prev_pos
    else:
        features["BOS"] = True  # Beginning of Sequence

    # features from next word
    if i < len(doc) - 1:
        next_word = doc[i + 1][0]
        next_pos = doc[i + 1][1]
        features["word.next_word"] = next_word
        features["word.next_isspace"] = next_word.isspace()
        features["word.next_isdigit"] = next_word.isdigit()
        features["word.next_postag"] = next_pos
    else:
        features["EOS"] = True  # End of Sequence

    return features


def _extract_features(doc):
    return [_doc2features(doc, i) for i in range(len(doc))]


_CORPUS_NAME = "blackboard-cls_v1.0.crfsuite"
tagger = pycrfsuite.Tagger()
tagger.open(path_pythainlp_corpus(_CORPUS_NAME))


def segment(doc: List[str]) -> List[List[str]]:
    word_tags = pos_tag(doc, corpus="blackboard")
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
