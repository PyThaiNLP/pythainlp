# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
from typing import Dict, List, Tuple
from pycrfsuite import Tagger as CRFTagger
from pythainlp.corpus import path_pythainlp_corpus, thai_stopwords


def _is_stopword(word: str) -> bool:  # check Thai stopword
    return word in thai_stopwords()


def _doc2features(tokens: List[Tuple[str, str]], index: int) -> Dict:
    """
    `tokens`  = a POS-tagged sentence [(w1, t1), ...]
    `index`   = the index of the token we want to extract features for
    """
    word, pos = tokens[index]
    f = {
        "word": word,
        "word_is_stopword": _is_stopword(word),
        "pos": pos,
    }
    if index > 0 and index > 1:
        prevprevword, prevprevpos = tokens[index - 2]
        f["prev-prev-word"] = prevprevword
        f["prev-prevz-word_is_stopword"] = _is_stopword(prevprevword)
        f["prev-prevz-pos"] = prevprevpos
    if index > 0:
        prevword, prevpos = tokens[index - 1]
        f["prev-word"] = prevword
        f["prev-word_is_stopword"] = _is_stopword(prevword)
        f["prev-pos"] = prevpos
    else:
        f["BOS"] = True
    if index < len(tokens) - 2:
        nextnextword, nextnextpos = tokens[index + 2]
        f["nextnext-word"] = nextnextword
        f["nextnext-word_is_stopword"] = _is_stopword(nextnextword)
        f["nextnext-pos"] = nextnextpos
    if index < len(tokens) - 1:
        nextword, nextpos = tokens[index + 1]
        f["next-word"] = nextword
        f["next-word_is_stopword"] = _is_stopword(nextword)
        f["next-pos"] = nextpos
    else:
        f["EOS"] = True

    return f


def extract_features(doc):
    return [_doc2features(doc, i) for i in range(0, len(doc))]


class CRFchunk:
    def __init__(self, corpus: str = "orchidpp"):
        self.corpus = corpus
        self.load_model(self.corpus)

    def load_model(self, corpus: str):
        self.tagger = CRFTagger()
        if corpus == "orchidpp":
            self.path = path_pythainlp_corpus("crfchunk_orchidpp.model")
        self.tagger.open(self.path)

    def parse(self, token_pos: List[Tuple[str, str]]) -> List[str]:
        self.xseq = extract_features(token_pos)
        return self.tagger.tag(self.xseq)
