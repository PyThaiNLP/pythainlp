# -*- coding: utf-8 -*-
from typing import List
from pythainlp.tag import pos_tag
from pythainlp.corpus import get_corpus_path
import pycrfsuite

def _doc2features(doc, i):
    word = doc[i][0]
    postag = doc[i][1]
    # Features from current word
    features={
        'word.word': word,
        'word.isspace':word.isspace(),
        'postag':postag,
        'word.isdigit()': word.isdigit()
    }
    if i > 0:
        prevword = doc[i-1][0]
        postag1 = doc[i-1][1]
        features['word.prevword'] = prevword
        features['word.previsspace']=prevword.isspace()
        features['word.prepostag'] = postag1
        features['word.prevwordisdigit'] = prevword.isdigit()
    else:
        features['BOS'] = True # Special "Beginning of Sequence" tag
    # Features from next word
    if i < len(doc)-1:
        nextword = doc[i+1][0]
        postag1 = doc[i+1][1]
        features['word.nextword'] = nextword
        features['word.nextisspace']=nextword.isspace()
        features['word.nextpostag'] = postag1
        features['word.nextwordisdigit'] = nextword.isdigit()
    else:
        features['EOS'] = True # Special "End of Sequence" tag
    return features

def _extract_features(doc):
    return [_doc2features(doc, i) for i in range(len(doc))]

def _get_labels(doc):
    return [tag for (token,postag,tag) in doc]

_CORPUS_NAME = "lst20-cls"
tagger = pycrfsuite.Tagger()
tagger.open(get_corpus_path(_CORPUS_NAME))

def clause_tokenize(doc: List[str]):
    _postag = pos_tag(doc, corpus="lst20")
    _features = _extract_features(_postag)
    _tag = list(zip(doc, tagger.tag(_features)))
    _list_cls = []
    _temp = []
    _len_doc = len(doc) - 1
    for i,w,t in enumerate(_tag):
        if t == "E_CLS" or i == _len_doc:
            _temp.append(w)
            _list_cls.append(_temp)
            _temp = []
        else:
            _temp.append(w)
    return _list_cls