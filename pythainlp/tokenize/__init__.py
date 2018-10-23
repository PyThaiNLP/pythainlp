# -*- coding: utf-8 -*-
"""
Thai tokenizers
"""
import re

import nltk
from pythainlp.corpus.thaisyllable import get_data as syllable_dict
from pythainlp.corpus.thaiword import get_data as word_dict

from marisa_trie import Trie

DEFAULT_DICT_TRIE = Trie(word_dict())
FROZEN_DICT_TRIE = Trie(word_dict(dict_fname="thaiword_frozen_201810.txt"))


def word_tokenize(text, engine="newmm", whitespaces=True):
    """
    :param str text: text to be tokenized
    :param str engine: tokenizer to be used
    :param bool whitespaces: True to output no whitespace, a common mark of sentence or end of phrase in Thai
    :Parameters for engine:
        * newmm (default) - dictionary-based, Maximum Matching + Thai Character Cluster
        * longest - dictionary-based, Longest Matching
        * icu - wrapper for ICU, dictionary-based
        * wordcutpy - wrapper for wordcutpy, dictionary-based https://github.com/veer66/wordcutpy
        * pylexto - wrapper for PyLexTo, dictionary-based, Longest Matching
        * deepcut - wrapper for deepcut, language-model-based https://github.com/rkcosmos/deepcut
        * ulmfit - use newmm engine with a specific dictionary for use with thai2vec
    :return: list of words, tokenized from the text

    **Example**::
        >>> from pythainlp.tokenize import word_tokenize
        >>> text = "โอเคบ่พวกเรารักภาษาบ้านเกิด"
        >>> word_tokenize(text, engine="newmm")
        ['โอเค', 'บ่', 'พวกเรา', 'รัก', 'ภาษา', 'บ้านเกิด']
        >>> word_tokenize(text, engine="icu")
        ['โอ', 'เค', 'บ่', 'พวก', 'เรา', 'รัก', 'ภาษา', 'บ้าน', 'เกิด']
    """
    if engine == "newmm" or engine == "onecut":
        from .newmm import mmcut as segment
    elif engine == "longest" or engine == "longest-matching":
        from .longest import segment
    elif engine == "ulmfit":
        from .newmm import mmcut

        def segment(text):
            return mmcut(text, trie=FROZEN_DICT_TRIE)

    elif engine == "icu":
        from .pyicu import segment
    elif engine == "deepcut":
        from .deepcut import segment
    elif engine == "wordcutpy":
        from .wordcutpy import segment
    elif engine == "pylexto":
        from .pylexto import segment
    elif engine == "mm" or engine == "multi_cut":
        from .multi_cut import segment
    else:  # default, use "newmm" engine
        from .newmm import mmcut as segment

    if not whitespaces:
        return [token.strip(" ") for token in segment(text) if token.strip(" ")]

    return segment(text)


def dict_word_tokenize(text, custom_dict_trie, engine="newmm"):
    """
    :meth:`dict_word_tokenize` tokenizes word based on the dictionary you provide. The format has to be in trie data structure.
    :param str text: text to be tokenized
    :param dict custom_dict_trie: a dictionary trie
    :param str engine: choose between different options of engine to token (newmm, longest, wordcutpy)
    :return: list of words
    **Example**::
        >>> from pythainlp.tokenize import dict_word_tokenize,create_custom_dict_trie
        >>> listword = ["แมว", "ดี"]
        >>> data_dict = create_custom_dict_trie(listword)
        >>> dict_word_tokenize("แมวดีดีแมว", data_dict)
        ['แมว', 'ดี', 'ดี', 'แมว']
    """
    if engine == "newmm" or engine == "onecut":
        from .pyicu import segment
    elif engine == "longest" or engine == "longest-matching":
        from .longest import segment
    elif engine == "wordcutpy":
        from .wordcutpy import segment

        return segment(text, custom_dict_trie.keys())
    elif engine == "mm" or engine == "multi_cut":
        from .multi_cut import segment
    else:  # default, use "newmm" engine
        from .newmm import mmcut as segment

    return segment(text, custom_dict_trie)


def sent_tokenize(text, engine="whitespace+newline"):
    """
    This function does not yet automatically recognize when a sentence actually ends. Rather it helps split text where white space and a new line is found.

    :param str text: the text to be tokenized
    :param str engine: choose between 'whitespace' or 'whitespace+newline'

    :return: a list of text, split by whitespace or new line.
    """
    sentences = []

    if engine == "whitespace":
        sentences = nltk.tokenize.WhitespaceTokenizer().tokenize(text)
    else:  # default, use whitespace + newline
        sentences = re.sub(r"\n+|\s+", "|", text).split("|")

    return sentences


def subword_tokenize(text, engine="tcc"):
    """
    :param str text: text to be tokenized
    :param str engine: choosing 'tcc' uses the Thai Character Cluster rule to segment words into the smallest unique units.
    :return: a list of tokenized strings.
    """
    from .tcc import tcc

    return tcc(text)


def isthai(text, check_all=False):
    """
    :param str text: input string or list of strings
    :param bool check_all: checks all character or not

    :return: A dictionary with the first value as proportional of text that is Thai, and the second value being a tuple of all characters, along with true or false.
    """
    isthais = []
    num_isthai = 0

    for ch in text:
        ch_val = ord(ch)
        if ch_val >= 3584 and ch_val <= 3711:
            num_isthai += 1
            if check_all:
                isthais.append(True)
        else:
            if check_all:
                isthais.append(False)
    thai_percent = (num_isthai / len(text)) * 100

    if check_all:
        chars = list(text)
        isthai_pairs = tuple(zip(chars, isthais))
        data = {"thai": thai_percent, "check_all": isthai_pairs}
    else:
        data = {"thai": thai_percent}

    return data


def syllable_tokenize(text):
    """
    :param str text: input string to be tokenized

    :return: returns list of strings of syllables
    """
    syllables = []
    if text:
        words = word_tokenize(text)
        trie = create_custom_dict_trie(custom_dict_source=syllable_dict())
        for word in words:
            syllables.extend(dict_word_tokenize(text=word, custom_dict_trie=trie))

    return syllables


def create_custom_dict_trie(custom_dict_source):
    """
    The function is used to create a custom dict trie which will be used for word_tokenize() function.
    For more information on the trie data structure, see: https://marisa-trie.readthedocs.io/en/latest/index.html

    :param string/list custom_dict_source: a list of vocaburaries or a path to source file
    :return: a trie created from custom dictionary input
    """

    if type(custom_dict_source) is str:
        # Receive a file path of the custom dict to read
        with open(custom_dict_source, "r", encoding="utf8") as f:
            _vocabs = f.read().splitlines()
            return Trie(_vocabs)
    elif isinstance(custom_dict_source, (list, tuple, set)):
        # Received a sequence type object of vocabs
        return Trie(custom_dict_source)
    else:
        raise TypeError(
            "Type of custom_dict_source must be either str (path to source file) or collections"
        )


class Tokenizer:
    def __init__(self, custom_dict=None):
        """
        Initialize tokenizer object

        :param str custom_dict: a file path or a list of vocaburaies to be used to create a trie (default - original lexitron)

        :return: trie_dict - a dictionary in the form of trie data for tokenizing engines
        """
        self.__trie_dict = None
        if custom_dict:
            if type(custom_dict) is list:
                self.__trie_dict = Trie(custom_dict)
            elif type(custom_dict) is str:
                with open(custom_dict, "r", encoding="utf8") as f:
                    vocabs = f.read().splitlines()
                self.__trie_dict = Trie(vocabs)
        else:
            self.__trie_dict = Trie(word_dict())

    def word_tokenize(self, text, engine="newmm"):
        from .newmm import mmcut as segment

        return segment(text, self.__trie_dict)
