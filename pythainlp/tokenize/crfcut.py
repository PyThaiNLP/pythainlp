# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
"""
CRFCut - Thai sentence segmenter.

Thai sentence segmentation using conditional random field,
with default model trained on TED dataset

Performance:
- ORCHID - space-correct accuracy 87% vs 95% state-of-the-art
  (Zhou et al, 2016; https://www.aclweb.org/anthology/C16-1031.pdf)
- TED dataset - space-correct accuracy 82%

See development notebooks at https://github.com/vistec-AI/ted_crawler;
POS features are not used due to unreliable POS tagging available
"""

import os
from typing import List

import pycrfsuite
from pythainlp.corpus import corpus_path
from pythainlp.tokenize import word_tokenize

_ENDERS = {
    # ending honorifics
    "ครับ",
    "ค่ะ",
    "คะ",
    "นะคะ",
    "นะ",
    "จ้ะ",
    "จ้า",
    "จ๋า",
    "ฮะ",
    # enders
    "ๆ",
    "ได้",
    "แล้ว",
    "ด้วย",
    "เลย",
    "มาก",
    "น้อย",
    "กัน",
    "เช่นกัน",
    "เท่านั้น",
    "อยู่",
    "ลง",
    "ขึ้น",
    "มา",
    "ไป",
    "ไว้",
    "เอง",
    "อีก",
    "ใหม่",
    "จริงๆ",
    "บ้าง",
    "หมด",
    "ทีเดียว",
    "เดียว",
    # demonstratives
    "นั้น",
    "นี้",
    "เหล่านี้",
    "เหล่านั้น",
    # questions
    "อย่างไร",
    "ยังไง",
    "หรือไม่",
    "มั้ย",
    "ไหน",
    "ไหม",
    "อะไร",
    "ทำไม",
    "เมื่อไหร่",
    "เมื่อไร",
}
_STARTERS = {
    # pronouns
    "ผม",
    "ฉัน",
    "ดิฉัน",
    "ชั้น",
    "คุณ",
    "มัน",
    "เขา",
    "เค้า",
    "เธอ",
    "เรา",
    "พวกเรา",
    "พวกเขา",
    "กู",
    "มึง",
    "แก",
    "ข้าพเจ้า",
    # connectors
    "และ",
    "หรือ",
    "แต่",
    "เมื่อ",
    "ถ้า",
    "ใน",
    "ด้วย",
    "เพราะ",
    "เนื่องจาก",
    "ซึ่ง",
    "ไม่",
    "ตอนนี้",
    "ทีนี้",
    "ดังนั้น",
    "เพราะฉะนั้น",
    "ฉะนั้น",
    "ตั้งแต่",
    "ในที่สุด",
    "ก็",
    "กับ",
    "แก่",
    "ต่อ",
    # demonstratives
    "นั้น",
    "นี้",
    "เหล่านี้",
    "เหล่านั้น",
}


def extract_features(
    doc: List[str], window: int = 2, max_n_gram: int = 3
) -> List[List[str]]:
    """
    Extract features for CRF by sliding `max_n_gram` of tokens
    for +/- `window` from the current token

    :param List[str] doc: tokens from which features are to be extracted
    :param int window: size of window before and after the current token
    :param int max_n_gram: create n_grams from 1-gram to `max_n_gram`-gram \
    within the `window`
    :return: list of lists of features to be fed to CRF
    """
    doc_features = []
    doc = (
        ["xxpad" for i in range(window)]
        + doc
        + ["xxpad" for i in range(window)]
    )

    # add enders and starters
    doc_ender = []
    doc_starter = []
    for i in range(len(doc)):
        if doc[i] in _ENDERS:
            doc_ender.append("ender")
        else:
            doc_ender.append("normal")

        if doc[i] in _STARTERS:
            doc_starter.append("starter")
        else:
            doc_starter.append("normal")

    # for each word
    for i in range(window, len(doc) - window):
        # bias term
        word_features = ["bias"]
        # ngram features
        for n_gram in range(1, min(max_n_gram + 1, 2 + window * 2)):
            for j in range(i - window, i + window + 2 - n_gram):
                feature_position = f"{n_gram}_{j-i}_{j-i+n_gram}"
                word_ = f'{"|".join(doc[j:(j+n_gram)])}'
                word_features += [f"word_{feature_position}={word_}"]
                ender_ = f'{"|".join(doc_ender[j:(j+n_gram)])}'
                word_features += [f"ender_{feature_position}={ender_}"]
                starter_ = f'{"|".join(doc_starter[j:(j+n_gram)])}'
                word_features += [f"starter_{feature_position}={starter_}"]
        # append to feature per word
        doc_features.append(word_features)

    return doc_features


_CRFCUT_DATA_FILENAME = "sentenceseg_crfcut.model"
_tagger = pycrfsuite.Tagger()
_tagger.open(os.path.join(corpus_path(), _CRFCUT_DATA_FILENAME))


def segment(text: str) -> List[str]:
    """
    CRF-based sentence segmentation.

    :param str text: text to be tokenized into sentences
    :return: list of words, tokenized from the text
    """
    if isinstance(text, str):
        toks = word_tokenize(text)
    else:
        toks = text
    feat = extract_features(toks)
    labs = _tagger.tag(feat)
    labs[-1] = "E"  # make sure it cuts the last sentence

    # To ensure splitting of sentences using Terminal Punctuation
    for idx, _ in enumerate(toks):
        if toks[idx].strip().endswith(("!", ".", "?")):
            labs[idx] = "E"
        # Spaces or empty strings would no longer be treated as end of sentence.
        elif (idx == 0 or labs[idx-1] == "E") and toks[idx].strip() == "":
            labs[idx] = "I"

    sentences = []
    sentence = ""
    for i, w in enumerate(toks):
        sentence = sentence + w
        # Empty strings should not be part of output.
        if labs[i] == "E" and sentence != "":
            sentences.append(sentence)
            sentence = ""

    return sentences
