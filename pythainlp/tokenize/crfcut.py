# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""
Segment Thai text into sentences with CRFCut.

CRFCut uses a conditional random field (CRF). The default model is trained
on the TED dataset.

Performance:

* ORCHID - space-correct accuracy 87% vs 95% state-of-the-art
  (Zhou et al, 2016; https://www.aclweb.org/anthology/C16-1031.pdf)
* TED dataset - space-correct accuracy 82%

See the development notebooks at https://github.com/vistec-AI/ted_crawler;
the model does not use part-of-speech (POS) features, because the available
POS tagging is unreliable.
"""

from __future__ import annotations

from pythainlp.corpus import corpus_path
from pythainlp.tag.crf import CRFTagger
from pythainlp.tokenize import word_tokenize
from pythainlp.tools.path import safe_path_join

_ENDERS: set[str] = {
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
_STARTERS: set[str] = {
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


def _extract_features(
    doc: list[str], window: int = 2, max_n_gram: int = 3
) -> list[list[str]]:
    """
    Extract CRF features from a list of words.

    The function slides n-grams of up to ``max_n_gram`` words over a window
    of ``window`` words before and after each word.

    :param list[str] doc: list of words to extract features from
    :param int window: size of the window before and after each word
    :param int max_n_gram: maximum n-gram size; create n-grams from
        1-gram to ``max_n_gram``-gram within the window
    :return: list of feature lists, one per word, to feed to the CRF
    :rtype: list[list[str]]
    """
    if not doc:
        return []

    doc_features = []
    # Pad the document with "xxpad" tokens efficiently
    padded_doc = ["xxpad"] * window
    padded_doc.extend(doc)
    padded_doc.extend(["xxpad"] * window)
    doc = padded_doc

    # add enders and starters
    doc_ender = ["ender" if token in _ENDERS else "normal" for token in doc]
    doc_starter = [
        "starter" if token in _STARTERS else "normal" for token in doc
    ]

    # for each word
    for i in range(window, len(doc) - window):
        # bias term
        word_features = ["bias"]
        # ngram features
        for n_gram in range(1, min(max_n_gram + 1, 2 + window * 2)):
            for j in range(i - window, i + window + 2 - n_gram):
                feature_position = f"{n_gram}_{j - i}_{j - i + n_gram}"
                word_ = f"{'|'.join(doc[j : (j + n_gram)])}"
                word_features += [f"word_{feature_position}={word_}"]
                ender_ = f"{'|'.join(doc_ender[j : (j + n_gram)])}"
                word_features += [f"ender_{feature_position}={ender_}"]
                starter_ = f"{'|'.join(doc_starter[j : (j + n_gram)])}"
                word_features += [f"starter_{feature_position}={starter_}"]
        # append to feature per word
        doc_features.append(word_features)

    return doc_features


_CRFCUT_DATA_FILENAME: str = "sentenceseg_crfcut.json.gz"
_tagger: CRFTagger = CRFTagger()
_tagger.open(safe_path_join(corpus_path(), _CRFCUT_DATA_FILENAME))


def segment(text: str) -> list[str]:
    """
    Tokenize text into sentences with a CRF model.

    :param str text: text to be tokenized
    :return: list of sentences
    :rtype: list[str]
    """
    toks = word_tokenize(text)
    feat = _extract_features(toks)
    labs = _tagger.tag(feat)
    labs[-1] = "E"  # make sure it cuts the last sentence

    # To ensure splitting of sentences using Terminal Punctuation
    for idx, _ in enumerate(toks):
        if toks[idx].strip().endswith(("!", ".", "?")):
            labs[idx] = "E"
        # Spaces or empty strings would no longer be treated as end of sentence.
        elif (idx == 0 or labs[idx - 1] == "E") and toks[idx].strip() == "":
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
