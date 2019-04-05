# -*- coding: utf-8 -*-
"""
Tagging each token in a sentence with supplementary information,
such as its part of speech and class of named-entity.
"""

__all__ = [
    "pos_tag",
    "pos_tag_sents",
    "tag_provinces"
]
from .locations import tag_provinces

# tag map for orchid to Universal Dependencies
# from Korakot Chaovavanich 
_TAG_MAP_UD = {
    #NOUN
    "NOUN":"NOUN",
    "NCMN":"NOUN",
    "NTTL":"NOUN",
    "CNIT":"NOUN",
    "CLTV":"NOUN",
    "CMTR":"NOUN",
    "CFQC":"NOUN",
    "CVBL":"NOUN",
    # VERB
    "VACT":"VERB",
    "VSTA":"VERB",
    #PRON
    "PRON":"PRON",
    "NPRP":"PRON",
    # ADJ
    "ADJ": "ADJ",
    "NONM": "ADJ",
    "VATT": "ADJ",
    "DONM": "ADJ",
    # ADV
    "ADV": "ADV",
    "ADVN": "ADV",
    "ADVI": "ADV",
    "ADVP": "ADV",
    "ADVS": "ADV",
	# INT
    "INT": "INTJ",
    # PRON
    "PROPN":"PROPN",
    "PPRS":"PROPN",
    "PDMN":"PROPN",
    "PNTR":"PROPN",
    # DET
    "DET": "DET",
    "DDAN": "DET",
    "DDAC": "DET",
    "DDBQ": "DET",
    "DDAQ": "DET",
    "DIAC": "DET",
    "DIBQ": "DET",
    "DIAQ": "DET",
    "DCNM": "DET",
    # NUM
    "NUM": "NUM",
    "NCNM": "NUM",
    "NLBL": "NUM",
    "DCNM": "NUM",
	# AUX
    "AUX": "AUX",
    "XVBM": "AUX",
    "XVAM": "AUX",
    "XVMM": "AUX",
    "XVBB": "AUX",
    "XVAE": "AUX",
	# ADP
    "ADP": "ADP",
    "RPRE": "ADP",
    # CCONJ
    "CCONJ":"CCONJ",
    "JCRG":"CCONJ",
	# SCONJ
    "SCONJ":"SCONJ",
    "PREL":"SCONJ",
    "JSBR":"SCONJ",
    "JCMP":"SCONJ",
    # PART
    "PART":"PART",
    "FIXN":"PART",
    "FIXV":"PART",
    "EAFF":"PART",
    "EITT":"PART",
    "AITT":"PART",
    "NEG":"PART",
    # PUNCT
    "PUNCT":"PUNCT",
    "PUNC":"PUNCT"
}

def _UD_Exception(w,tag):
	if w=="การ" or w=="ความ":
		return "NOUN"
	return tag

def _orchid_to_ud(tag):
	_i=0
	temp=[]
	while _i<len(tag):
		temp.append((tag[_i][0],_UD_Exception(tag[_i][0],_TAG_MAP_UD[tag[_i][1]])))
		_i+=1
	return temp

def pos_tag(words, engine="perceptron", corpus="orchid"):
    """
    Part of Speech tagging function.

    :param list words: a list of tokenized words
    :param str engine:
        * unigram - unigram tagger
        * perceptron - perceptron tagger (default)
        * artagger - RDR POS tagger
    :param str corpus:
        * orchid - annotated Thai academic articles (default)
        * orchid_ud - annotated Thai academic articles using Universal Dependencies Tags
        * pud - Parallel Universal Dependencies (PUD) treebanks
    :return: returns a list of labels regarding which part of speech it is
    """
    _corpus=corpus
    _tag=[]
    if corpus=="orchid_ud":
        corpus="orchid"
    if not words:
        return []

    if engine == "perceptron":
        from .perceptron import tag as tag_
    elif engine == "artagger":

        def tag_(words, corpus=None):
            if not words:
                return []

            from artagger import Tagger
            words_ = Tagger().tag(" ".join(words))

            return [(word.word, word.tag) for word in words_]

    else:  # default, use "unigram" ("old") engine
        from .unigram import tag as tag_
    _tag= tag_(words, corpus=corpus)
    if _corpus=="orchid_ud":
        _tag=_orchid_to_ud(_tag)
    return _tag


def pos_tag_sents(sentences, engine="perceptron", corpus="orchid"):
    """
    Part of Speech tagging Sentence function.

    :param list sentences: a list of tokenized sentences (a list of tokenized words in sentences)
    :param str engine:
        * unigram - unigram tagger 
        * perceptron - perceptron tagger (default)
        * artagger - RDR POS tagger
    :param str corpus:
        * orchid - annotated Thai academic articles (default)
        * orchid_ud - annotated Thai academic articles using Universal Dependencies Tags
        * pud - Parallel Universal Dependencies (PUD) treebanks
    :return: returns a list of labels regarding which part of speech it is
    """
    if not sentences:
        return []

    return [pos_tag(sent, engine=engine, corpus=corpus) for sent in sentences]
