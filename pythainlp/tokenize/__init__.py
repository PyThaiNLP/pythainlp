# -*- coding: utf-8 -*-
"""
Thai tokenizers
"""
import re
import sys
from typing import Iterable, List, Union

from pythainlp.corpus import get_corpus, thai_syllables, thai_words

from marisa_trie import Trie

DEFAULT_DICT_TRIE = Trie(thai_words())
FROZEN_DICT_TRIE = Trie(get_corpus("words_th_frozen_201810.txt"))


def word_tokenize(
    text: str,
    custom_dict: Trie = None,
    engine: str = "newmm",
    keep_whitespace: bool = True,
) -> List[str]:
    """
    :param str text: text to be tokenized
    :param str engine: tokenizer to be used
    :param dict custom_dict: a dictionary trie
    :param bool keep_whitespace: True to keep whitespaces, a common mark for end of phrase in Thai
    :return: list of words

    **Options for engine**
        * newmm (default) - dictionary-based, Maximum Matching + Thai Character Cluster
        * longest - dictionary-based, Longest Matching
        * deepcut - wrapper for deepcut, language-model-based https://github.com/rkcosmos/deepcut
        * icu - wrapper for ICU (International Components for Unicode, using PyICU), dictionary-based
        * ulmfit - for thai2fit
        * a custom_dict can be provided for newmm, longest, and deepcut

    **Example**
        >>> from pythainlp.tokenize import word_tokenize
        >>> text = "โอเคบ่พวกเรารักภาษาบ้านเกิด"
        >>> word_tokenize(text, engine="newmm")
        ['โอเค', 'บ่', 'พวกเรา', 'รัก', 'ภาษา', 'บ้านเกิด']
        >>> word_tokenize(text, engine="icu")
        ['โอ', 'เค', 'บ่', 'พวก', 'เรา', 'รัก', 'ภาษา', 'บ้าน', 'เกิด']
    """
    if not text or not isinstance(text, str):
        return []

    segments = []
    if engine == "newmm" or engine == "onecut":
        from .newmm import segment

        segments = segment(text, custom_dict)
    elif engine == "longest":
        from .longest import segment

        segments = segment(text, custom_dict)
    elif engine == "mm" or engine == "multi_cut":
        from .multi_cut import segment

        segments = segment(text, custom_dict)
    elif engine == "deepcut":  # deepcut can optionally use dictionary
        from .deepcut import segment

        if custom_dict:
            custom_dict = list(custom_dict)
            segments = segment(text, custom_dict)
        else:
            segments = segment(text)
    elif engine == "ulmfit":  # ulmfit has its own specific dictionary
        from .newmm import segment

        segments = segment(text, custom_dict=FROZEN_DICT_TRIE)
    elif engine == "icu":
        from .pyicu import segment

        segments = segment(text)
    else:  # default, use "newmm" engine
        from .newmm import segment

        segments = segment(text, custom_dict)

    if not keep_whitespace:
        segments = [token.strip(" ") for token in segments if token.strip(" ")]

    return segments


def dict_word_tokenize(
    text: str,
    custom_dict: Trie = DEFAULT_DICT_TRIE,
    engine: str = "newmm",
    keep_whitespace: bool = True,
) -> List[str]:
    """
    :meth: DEPRECATED: Please use `word_tokenize()` with a `custom_dict` argument instead
    :param str text: text to be tokenized
    :param dict custom_dict: a dictionary trie, or an iterable of words, or a string of dictionary path
    :param str engine: choose between different options of engine to token (newmm [default], mm, longest, and deepcut)
    :param bool keep_whitespace: True to keep whitespaces, a common mark for end of phrase in Thai
    :return: list of words
    """
    print(
        "Deprecated. Use word_tokenize() with a custom_dict argument instead.",
        file=sys.stderr,
    )
    return word_tokenize(
        text=text,
        custom_dict=custom_dict,
        engine=engine,
        keep_whitespace=keep_whitespace,
    )


def sent_tokenize(text: str, engine: str = "whitespace+newline") -> List[str]:
    """
    This function does not yet automatically recognize when a sentence actually ends. Rather it helps split text where white space and a new line is found.

    :param str text: the text to be tokenized
    :param str engine: choose between 'whitespace' or 'whitespace+newline'

    :return: list of sentences
    """

    if not text or not isinstance(text, str):
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
    :param str engine: subword tokenizer
    :return: list of subwords

    **Options for engine**
        * tcc (default) -  Thai Character Cluster (Theeramunkong et al. 2000)
        * etcc - Enhanced Thai Character Cluster (Inrut et al. 2001) [In development]
    """
    if not text or not isinstance(text, str):
        return []

    if engine == "etcc":
        from .etcc import segment
    else:  # default
        from .tcc import segment

    return segment(text)


def syllable_tokenize(text: str) -> List[str]:
    """
    :param str text: input string to be tokenized
    :return: list of syllables
    """

    if not text or not isinstance(text, str):
        return []

    tokens = []
    if text:
        words = word_tokenize(text)
        trie = dict_trie(dict_source=thai_syllables())
        for word in words:
            tokens.extend(word_tokenize(text=word, custom_dict=trie))

    return tokens


def dict_trie(dict_source: Union[str, Iterable[str], Trie]) -> Trie:
    """
    Create a dict trie which will be used for word_tokenize() function.
    For more information on the trie data structure,
    see: https://marisa-trie.readthedocs.io/en/latest/index.html

    :param string/list dict_source: a list of vocaburaries or a path to source file
    :return: a trie created from a dictionary input
    """
    trie = None

    if isinstance(dict_source, Trie):
        trie = dict_source
    elif isinstance(dict_source, str):
        # Receive a file path of the dict to read
        with open(dict_source, "r", encoding="utf8") as f:
            _vocabs = f.read().splitlines()
            trie = Trie(_vocabs)
    elif isinstance(dict_source, Iterable):
        # Note: Trie and str are both Iterable, Iterable check should be here
        # Received a sequence type object of vocabs
        trie = Trie(dict_source)
    else:
        raise TypeError(
            "Type of dict_source must be marisa_trie.Trie, or Iterable[str], or str (path to source file)"
        )

    return trie


class Tokenizer:
    def __init__(
        self, custom_dict: Union[Trie, Iterable[str], str] = None, engine: str = "newmm"
    ):
        """
        Initialize tokenizer object

        :param str custom_dict: a file path or a list of vocaburaies to be used to create a trie
        :param str engine: choose between different options of engine to token (newmm, mm, longest)
        """
        self.__trie_dict = None
        self.__engine = engine
        if custom_dict:
            self.__trie_dict = dict_trie(custom_dict)
        else:
            self.__trie_dict = DEFAULT_DICT_TRIE

    def word_tokenize(self, text: str) -> List[str]:
        """
        :param str text: text to be tokenized

        :return: list of words, tokenized from the text
        """
        return word_tokenize(text, custom_dict=self.__trie_dict, engine=self.__engine)

    def set_tokenize_engine(self, engine: str) -> None:
        """
        :param str engine: choose between different options of engine to token (newmm, mm, longest)
        """
        self.__engine = engine
