# -*- coding: utf-8 -*-
"""
NLTK WordNet wrapper

API here is exactly the same as NLTK API,
except that lang (language) argument will be "tha" (Thai) by default.
"""
import nltk

try:
    nltk.data.find("corpora/omw")
except LookupError:
    nltk.download("omw")

try:
    nltk.data.find("corpora/wordnet")
except LookupError:
    nltk.download("wordnet")

from nltk.corpus import wordnet


def synsets(word: str, pos: str = None, lang: str = "tha"):
    return wordnet.synsets(lemma=word, pos=pos, lang=lang)


def synset(name_synsets):
    return wordnet.synset(name_synsets)


def all_lemma_names(pos: str = None, lang: str = "tha"):
    return wordnet.all_lemma_names(pos=pos, lang=lang)


def all_synsets(pos: str = None):
    return wordnet.all_synsets(pos=pos)


def langs():
    return wordnet.langs()


def lemmas(word: str, pos: str = None, lang: str = "tha"):
    return wordnet.lemmas(word, pos=pos, lang=lang)


def lemma(name_synsets):
    return wordnet.lemma(name_synsets)


def lemma_from_key(key):
    return wordnet.lemma_from_key(key)


def path_similarity(synsets1, synsets2):
    return wordnet.path_similarity(synsets1, synsets2)


def lch_similarity(synsets1, synsets2):
    return wordnet.lch_similarity(synsets1, synsets2)


def wup_similarity(synsets1, synsets2):
    return wordnet.wup_similarity(synsets1, synsets2)


def morphy(form, pos: str = None):
    return wordnet.morphy(form, pos=None)


def custom_lemmas(tab_file, lang: str):
    return wordnet.custom_lemmas(tab_file, lang)
