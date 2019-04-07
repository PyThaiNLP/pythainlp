# -*- coding: utf-8 -*-
"""
Thai tokenizers
"""
import re
from typing import Iterable, List, Union

from pythainlp.corpus import get_corpus, thai_syllables, thai_words

from marisa_trie import Trie

DEFAULT_DICT_TRIE = Trie(thai_words())
FROZEN_DICT_TRIE = Trie(get_corpus("words_th_frozen_201810.txt"))


def word_tokenize(
    text: str, engine: str = "newmm", whitespaces: bool = True
) -> List[str]:
    """
    :param str text: text to be tokenized
    :param str engine: tokenizer to be used
    :param bool whitespaces: True to output no whitespace, a common mark of end of phrase in Thai
    :Parameters for engine:
        * newmm (default) - dictionary-based, Maximum Matching + Thai Character Cluster
        * longest - dictionary-based, Longest Matching
        * icu - wrapper for ICU, dictionary-based
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
    if not text:
        return []

    if engine == "newmm" or engine == "onecut":
        from .newmm import segment
    elif engine == "longest" or engine == "longest-matching":
        from .longest import segment
    elif engine == "ulmfit":
        from .newmm import segment as segment_

        def segment(text):
            return segment_(text, trie=FROZEN_DICT_TRIE)

    elif engine == "icu":
        from .pyicu import segment
    elif engine == "deepcut":
        from .deepcut import segment
    elif engine == "mm" or engine == "multi_cut":
        from .multi_cut import segment
    else:  # default, use "newmm" engine
        from .newmm import segment

    if not whitespaces:
        return [token.strip(" ") for token in segment(text) if token.strip(" ")]

    return segment(text)


def dict_word_tokenize(
    text: str, custom_dict: Trie, engine: str = "newmm"
) -> List[str]:
    """
    :meth:`dict_word_tokenize` tokenizes word based on the dictionary you provide. The format has to be in trie data structure.
    :param str text: text to be tokenized
    :param dict custom_dict: a dictionary trie
    :param str engine: choose between different options of engine to token (newmm, longest)
    :return: list of words
    **Example**::
        >>> from pythainlp.tokenize import dict_word_tokenize, dict_trie
        >>> words = ["แมว", "ดี"]
        >>> trie = dict_trie(words)
        >>> dict_word_tokenize("แมวดีดีแมว", trie)
        ['แมว', 'ดี', 'ดี', 'แมว']
    """

    if not text:
        return []

    if engine == "newmm" or engine == "onecut":
        from .newmm import segment
    elif engine == "longest" or engine == "longest-matching":
        from .longest import segment
    elif engine == "mm" or engine == "multi_cut":
        from .multi_cut import segment
    else:  # default, use "newmm" engine
        from .newmm import segment

    return segment(text, custom_dict)


def sent_tokenize(text: str, engine: str = "whitespace+newline") -> List[str]:
    """
    This function does not yet automatically recognize when a sentence actually ends. Rather it helps split text where white space and a new line is found.

    :param str text: the text to be tokenized
    :param str engine: choose between 'whitespace' or 'whitespace+newline'

    :return: a list of text, split by whitespace or new line.
    """

    if not text:
        return []

    sentences = []

    if engine == "whitespace":
        sentences = re.split(r" +", text, re.U)
    else:  # default, use whitespace + newline
        sentences = text.split()

    return sentences


def subword_tokenize(text: str, engine: str = "tcc") -> List[str]:
    """
    :param str text: text to be tokenized
    :param str engine: choosing 'tcc' uses the Thai Character Cluster rule to segment words into the smallest unique units.
    :return: a list of tokenized strings.
    """
    if not text:
        return ""

    from .tcc import tcc

    return tcc(text)


def syllable_tokenize(text: str) -> List[str]:
    """
    :param str text: input string to be tokenized

    :return: returns list of strings of syllables
    """

    if not text:
        return []

    tokens = []
    if text:
        words = word_tokenize(text)
        trie = dict_trie(dict_source=thai_syllables())
        for word in words:
            tokens.extend(dict_word_tokenize(text=word, custom_dict=trie))

    return tokens


def dict_trie(dict_source: Union[str, Iterable]) -> Trie:
    """
    Create a dict trie which will be used for word_tokenize() function.
    For more information on the trie data structure,
    see: https://marisa-trie.readthedocs.io/en/latest/index.html

    :param string/list dict_source: a list of vocaburaries or a path to source file
    :return: a trie created from a dictionary input
    """

    if type(dict_source) is str:
        # Receive a file path of the dict to read
        with open(dict_source, "r", encoding="utf8") as f:
            _vocabs = f.read().splitlines()
            return Trie(_vocabs)
    elif isinstance(dict_source, Iterable):
        # Received a sequence type object of vocabs
        return Trie(dict_source)
    else:
        raise TypeError(
            "Type of dict_source must be either str (path to source file) or iterable"
        )


class Tokenizer:
    def __init__(
        self, custom_dict: Union[str, Iterable] = None, tokenize_engine: str = "newmm"
    ):
        """
        Initialize tokenizer object

        :param str custom_dict: a file path or a list of vocaburaies to be used to create a trie (default - original lexitron)
        :param str tokenize_engine: choose between different options of engine to token (newmm, mm, longest)
        """
        self.__trie_dict = None
        self.word_engine = tokenize_engine
        if custom_dict:
            self.__trie_dict = dict_trie(custom_dict)
        else:
            self.__trie_dict = dict_trie(thai_words())

    def word_tokenize(self, text: str) -> List[str]:
        """
        :param str text: text to be tokenized

        :return: list of words, tokenized from the text
        """
        return dict_word_tokenize(
            text, custom_dict=self.__trie_dict, engine=self.word_engine
        )

    def set_tokenize_engine(self, name_engine: str) -> None:
        """
        :param str name_engine: choose between different options of engine to token (newmm, mm, longest)
        """
        self.word_engine = name_engine
