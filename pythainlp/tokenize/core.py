# -*- coding: utf-8 -*-
"""
Tokenizer generic functions
"""
import re
from typing import Iterable, List, Union

from pythainlp.tokenize import (
    DEFAULT_SENT_TOKENIZE_ENGINE,
    DEFAULT_SUBWORD_TOKENIZE_ENGINE,
    DEFAULT_SYLLABLE_DICT_TRIE,
    DEFAULT_SYLLABLE_TOKENIZE_ENGINE,
    DEFAULT_WORD_DICT_TRIE,
    DEFAULT_WORD_TOKENIZE_ENGINE,
)
from pythainlp.util.trie import Trie, dict_trie


def clause_tokenize(doc: List[str]) -> List[List[str]]:
    """
    Clause tokenizer. (or Clause segmentation)

    Tokenizes running word list into list of clauses (list of strings).
    split by CRF trained on LST20 Corpus.

    :param str doc: word list to be clause
    :return: list of claues
    :rtype: list[list[str]]

    :Example:

        from pythainlp.tokenize import clause_tokenize

        clause_tokenize(["ฉัน","นอน","และ","คุณ","เล่น","มือถือ","ส่วน","น้อง","เขียน","โปรแกรม"])
        [['ฉัน', 'นอน'],
        ['และ', 'คุณ', 'เล่น', 'มือถือ'],
        ['ส่วน', 'น้อง', 'เขียน', 'โปรแกรม']]
    """
    from .crfcls import segment

    return segment(doc)


def word_tokenize(
    text: str,
    custom_dict: Trie = None,
    engine: str = DEFAULT_WORD_TOKENIZE_ENGINE,
    keep_whitespace: bool = True,
) -> List[str]:
    """
    Word tokenizer.

    Tokenizes running text into words (list of strings).

    :param str text: text to be tokenized
    :param str engine: name of the tokenizer to be used
    :param pythainlp.util.Trie custom_dict: dictionary trie
    :param bool keep_whitespace: True to keep whitespaces, a common mark
                                 for end of phrase in Thai.
                                 Otherwise, whitespaces are omitted.
    :return: list of words
    :rtype: list[str]
    **Options for engine**
        * *newmm* (default) - dictionary-based, Maximum Matching +
          Thai Character Cluster
        * *newmm-safe* - newmm, with a mechanism to help avoid long
          processing time for text with continuous ambiguous breaking points
        * *longest* - dictionary-based, Longest Matching
        * *icu* - wrapper for ICU (International Components for Unicode,
          using PyICU), dictionary-based
        * *attacut* - wrapper for
          `AttaCut <https://github.com/PyThaiNLP/attacut>`_.,
          learning-based approach
        * *deepcut* - wrapper for
          `DeepCut <https://github.com/rkcosmos/deepcut>`_,
          learning-based approach

    :Note:
        - The parameter **custom_dict** can be provided as an argument \
          only for *newmm*, *longest*, and *attacut* engine.
    :Example:

    Tokenize text with different tokenizer::

        from pythainlp.tokenize import word_tokenize

        text = "โอเคบ่พวกเรารักภาษาบ้านเกิด"

        word_tokenize(text, engine="newmm")
        # output: ['โอเค', 'บ่', 'พวกเรา', 'รัก', 'ภาษา', 'บ้านเกิด']

        word_tokenize(text, engine='attacut')
        # output: ['โอเค', 'บ่', 'พวกเรา', 'รัก', 'ภาษา', 'บ้านเกิด']

    Tokenize text by omiting whitespaces::

        text = "วรรณกรรม ภาพวาด และการแสดงงิ้ว "

        word_tokenize(text, engine="newmm")
        # output:
        # ['วรรณกรรม', ' ', 'ภาพวาด', ' ', 'และ', 'การแสดง', 'งิ้ว', ' ']

        word_tokenize(text, engine="newmm", keep_whitespace=False)
        # output: ['วรรณกรรม', 'ภาพวาด', 'และ', 'การแสดง', 'งิ้ว']

    Tokenize with default and custom dictionary::

        from pythainlp.corpus.common import thai_words
        from pythainlp.tokenize import dict_trie

        text = 'ชินโซ อาเบะ เกิด 21 กันยายน'

        word_tokenize(text, engine="newmm")
        # output:
        # ['ชิน', 'โซ', ' ', 'อา', 'เบะ', ' ',
        #  'เกิด', ' ', '21', ' ', 'กันยายน']

        custom_dict_japanese_name = set(thai_words()
        custom_dict_japanese_name.add('ชินโซ')
        custom_dict_japanese_name.add('อาเบะ')

        trie = dict_trie(dict_source=custom_dict_japanese_name)

        word_tokenize(text, engine="newmm", custom_dict=trie))
        # output:
        # ['ชินโซ', ' ', 'อาเบะ',
        #   ' ', 'เกิด', ' ', '21', ' ', 'กันยายน']
    """
    if not text or not isinstance(text, str):
        return []

    segments = []

    if engine == "newmm" or engine == "onecut":
        from .newmm import segment

        segments = segment(text, custom_dict)
    elif engine == "newmm-safe":
        from .newmm import segment

        segments = segment(text, custom_dict, safe_mode=True)
    elif engine == "attacut":
        from .attacut import segment

        segments = segment(text)
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
    elif engine == "icu":
        from .pyicu import segment

        segments = segment(text)
    else:
        raise ValueError(
            f"""Tokenizer \"{engine}\" not found.
            It might be a typo; if not, please consult our document."""
        )

    if not keep_whitespace:
        segments = [token.strip(" ") for token in segments if token.strip(" ")]

    return segments


def sent_tokenize(
    text: str,
    engine: str = DEFAULT_SENT_TOKENIZE_ENGINE,
    keep_whitespace: bool = True,
) -> List[str]:
    """
    Sentence tokenizer.

    Tokenizes running text into "sentences"

    :param str text: the text to be tokenized
    :param str engine: choose among *'crfcut'*, *'whitespace'*, \
    *'whitespace+newline'*
    :return: list of splited sentences
    :rtype: list[str]
    **Options for engine**
        * *crfcut* - (default) split by CRF trained on TED dataset
        * *whitespace+newline* - split by whitespaces and newline.
        * *whitespace* - split by whitespaces. Specifiaclly, with \
                         :class:`regex` pattern  ``r" +"``
    :Example:

    Split the text based on *whitespace*::

        from pythainlp.tokenize import sent_tokenize

        sentence_1 = "ฉันไปประชุมเมื่อวันที่ 11 มีนาคม"
        sentence_2 = "ข้าราชการได้รับการหมุนเวียนเป็นระยะ \\
        และได้รับมอบหมายให้ประจำในระดับภูมิภาค"

        sent_tokenize(sentence_1, engine="whitespace")
        # output: ['ฉันไปประชุมเมื่อวันที่', '11', 'มีนาคม']

        sent_tokenize(sentence_2, engine="whitespace")
        # output: ['ข้าราชการได้รับการหมุนเวียนเป็นระยะ',
        #   '\\nและได้รับมอบหมายให้ประจำในระดับภูมิภาค']

    Split the text based on *whitespace* and *newline*::

        sentence_1 = "ฉันไปประชุมเมื่อวันที่ 11 มีนาคม"
        sentence_2 = "ข้าราชการได้รับการหมุนเวียนเป็นระยะ \\
        และได้รับมอบหมายให้ประจำในระดับภูมิภาค"

        sent_tokenize(sentence_1, engine="whitespace+newline")
        # output: ['ฉันไปประชุมเมื่อวันที่', '11', 'มีนาคม']
        sent_tokenize(sentence_2, engine="whitespace+newline")
        # output: ['ข้าราชการได้รับการหมุนเวียนเป็นระยะ',
        '\\nและได้รับมอบหมายให้ประจำในระดับภูมิภาค']

    Split the text using CRF trained on TED dataset::

        sentence_1 = "ฉันไปประชุมเมื่อวันที่ 11 มีนาคม"
        sentence_2 = "ข้าราชการได้รับการหมุนเวียนเป็นระยะ \\
        และเขาได้รับมอบหมายให้ประจำในระดับภูมิภาค"

        sent_tokenize(sentence_1, engine="crfcut")
        # output: ['ฉันไปประชุมเมื่อวันที่ 11 มีนาคม']

        sent_tokenize(sentence_2, engine="crfcut")
        # output: ['ข้าราชการได้รับการหมุนเวียนเป็นระยะ ',
        'และเขาได้รับมอบหมายให้ประจำในระดับภูมิภาค']
    """

    if not text or not isinstance(text, str):
        return []

    segments = []

    if engine == "crfcut":
        from .crfcut import segment

        segments = segment(text)
    elif engine == "whitespace":
        segments = re.split(r" +", text, re.U)
    elif engine == "whitespace+newline":
        segments = text.split()
    else:
        raise ValueError(
            f"""Tokenizer \"{engine}\" not found.
            It might be a typo; if not, please consult our document."""
        )

    if not keep_whitespace:
        segments = [token.strip(" ") for token in segments if token.strip(" ")]

    return segments


def subword_tokenize(
    text: str,
    engine: str = DEFAULT_SUBWORD_TOKENIZE_ENGINE,
    keep_whitespace: bool = True,
) -> List[str]:
    """
    Subword tokenizer. Can be smaller than syllable.

    Tokenizes text into inseparable units of
    Thai contiguous characters namely
    `Thai Character Clusters (TCCs) \
    <https://www.researchgate.net/publication/2853284_Character_Cluster_Based_Thai_Information_Retrieval>`_
    TCCs are the units based on Thai spelling feature that could not be
    separated any character further such as   'ก็', 'จะ', 'ไม่', and 'ฝา'.
    If the following units are separated, they could not be spelled out.
    This function apply the TCC rules to tokenizes the text into
    the smallest units.

    For example, the word 'ขนมชั้น' would be tokenized
    into 'ข', 'น', 'ม', and 'ชั้น'.

    :param str text: text to be tokenized
    :param str engine: the name subword tokenizer
    :return: list of subwords
    :rtype: list[str]
    **Options for engine**
        * *tcc* (default) -  Thai Character Cluster (Theeramunkong et al. 2000)
        * *etcc* - Enhanced Thai Character Cluster (Inrut et al. 2001)

    :Example:

    Tokenize text into subword based on *tcc*::

        from pythainlp.tokenize import subword_tokenize

        text_1 = "ยุคเริ่มแรกของ ราชวงศ์หมิง"
        text_2 = "ความแปลกแยกและพัฒนาการ"

        subword_tokenize(text_1, engine='tcc')
        # output: ['ยุ', 'ค', 'เริ่ม', 'แร', 'ก',
        #   'ข', 'อ', 'ง', ' ', 'รา', 'ช', 'ว', 'ง',
        #   'ศ', '์', 'ห', 'มิ', 'ง']

        subword_tokenize(text_2, engine='tcc')
        # output: ['ค', 'วา', 'ม', 'แป', 'ล', 'ก', 'แย', 'ก',
        'และ', 'พัฒ','นา', 'กา', 'ร']

    Tokenize text into subword based on *etcc* **(Work In Progress)**::

        text_1 = "ยุคเริ่มแรกของ ราชวงศ์หมิง"
        text_2 = "ความแปลกแยกและพัฒนาการ"

        subword_tokenize(text_1, engine='etcc')
        # output: ['ยุคเริ่มแรกของ ราชวงศ์หมิง']

        subword_tokenize(text_2, engine='etcc')
        # output: ['ความแปลกแยกและ', 'พัฒ', 'นาการ']
    """
    if not text or not isinstance(text, str):
        return []

    if engine == "tcc":
        from .tcc import segment
    elif engine == "etcc":
        from .etcc import segment
    else:
        raise ValueError(
            f"""Tokenizer \"{engine}\" not found.
            It might be a typo; if not, please consult our document."""
        )

    segments = segment(text)

    if not keep_whitespace:
        segments = [token.strip(" ") for token in segments if token.strip(" ")]

    return segments


def syllable_tokenize(
    text: str,
    engine: str = DEFAULT_SYLLABLE_TOKENIZE_ENGINE,
    keep_whitespace: bool = True,
) -> List[str]:
    """
    Syllable tokenizer.

    Tokenizes text into syllable (Thai: พยางค์), a unit of
    pronunciation having one vowel sound.  For example, the word 'รถไฟ'
    contains two syallbles including 'รถ', and 'ไฟ'.

    Under the hood, this function uses :func:`pythainlp.tokenize.word_tokenize`
    with *newmm* as a tokenizer. The function tokenize the text with
    the dictionary of Thai words from
    :func:`pythainlp.corpus.common.thai_words`
    and then dictionary of Thai syllable from
    :func:`pythainlp.corpus.common.thai_syllables`.
    As a result, only syllables are obtained.

    :param str text: input string to be tokenized
    :param str engine: name of the syllable tokenizer
    :return: list of syllables where whitespaces in the text **are included**
    :rtype: list[str]
    **Options for engine**
        * *dict* (default) - newmm word tokenizer with a syllable dictionary
        * *ssg* - CRF syllable segmenter for Thai
    :Example::
    ::

        from pythainlp.tokenize import syllable_tokenize

        text = 'รถไฟสมัยใหม่จะใช้กำลังจากหัวรถจักรดีเซล หรือจากไฟฟ้า'
        syllable_tokenize(text)
        ['รถ', 'ไฟ', 'สมัย', 'ใหม่', 'ใช้', 'กำ', 'ลัง', 'จาก', 'หัว',
        'รถ', 'จักร', 'ดี', 'เซล', ' ', 'หรือ', 'จาก', 'ไฟ', 'ฟ้า']
    """

    if not text or not isinstance(text, str):
        return []

    segments = []

    if engine == "dict" or engine == "default":  # use syllable dictionary
        words = word_tokenize(text)
        for word in words:
            segments.extend(
                word_tokenize(
                    text=word, custom_dict=DEFAULT_SYLLABLE_DICT_TRIE
                )
            )
    elif engine == "ssg":
        from .ssg import segment

        segments = segment(text)
    else:
        raise ValueError(
            f"""Tokenizer \"{engine}\" not found.
            It might be a typo; if not, please consult our document."""
        )

    if not keep_whitespace:
        segments = [token.strip(" ") for token in segments if token.strip(" ")]

    return segments


class Tokenizer:
    """
    Tokenizer class, for a custom tokenizer.

    This class allows users to pre-define custom dictionary along with
    tokenizer and encapsulate them into one single object.
    It is an wrapper for both two functions including
    :func:`pythainlp.tokenize.word_tokenize`,
    and :func:`pythainlp.util.dict_trie`

    :Example:

    Tokenizer object instantiated with :class:`pythainlp.util.Trie`::

        from pythainlp.tokenize import Tokenizer
        from pythainlp.corpus.common import thai_words
        from pythainlp.util import dict_trie

        custom_words_list = set(thai_words())
        custom_words_list.add('อะเฟเซีย')
        custom_words_list.add('Aphasia')
        trie = dict_trie(dict_source=custom_words_list)

        text = "อะเฟเซีย (Aphasia*) เป็นอาการผิดปกติของการพูด"
        _tokenizer = Tokenizer(custom_dict=trie, engine='newmm')
        # output: ['อะเฟเซีย', ' ', '(', 'Aphasia', ')', ' ', 'เป็น', 'อาการ',
        'ผิดปกติ', 'ของ', 'การ', 'พูด']

    Tokenizer object instantiated with a list of words::

        text = "อะเฟเซีย (Aphasia) เป็นอาการผิดปกติของการพูด"
        _tokenizer = Tokenizer(custom_dict=list(thai_words()), engine='newmm')
        _tokenizer.word_tokenize(text)
        # output:
        # ['อะ', 'เฟเซีย', ' ', '(', 'Aphasia', ')', ' ', 'เป็น', 'อาการ',
        #   'ผิดปกติ', 'ของ', 'การ', 'พูด']

    Tokenizer object instantiated with a file path containing list of
    word separated with *newline* and explicitly set a new tokenizer
    after initiation::

        PATH_TO_CUSTOM_DICTIONARY = './custom_dictionary.txtt'

        # write a file
        with open(PATH_TO_CUSTOM_DICTIONARY, 'w', encoding='utf-8') as f:
            f.write('อะเฟเซีย\\nAphasia\\nผิด\\nปกติ')

        text = "อะเฟเซีย (Aphasia) เป็นอาการผิดปกติของการพูด"

        # initate an object from file with `attacut` as tokenizer
        _tokenizer = Tokenizer(custom_dict=PATH_TO_CUSTOM_DICTIONARY, \\
            engine='attacut')

        _tokenizer.word_tokenize(text)
        # output:
        # ['อะเฟเซีย', ' ', '(', 'Aphasia', ')', ' ', 'เป็น', 'อาการ', 'ผิด',
        #   'ปกติ', 'ของ', 'การ', 'พูด']

        # change tokenizer to `newmm`
        _tokenizer.set_tokenizer_engine(engine='newmm')
        _tokenizer.word_tokenize(text)
        # output:
        # ['อะเฟเซีย', ' ', '(', 'Aphasia', ')', ' ', 'เป็นอาการ', 'ผิด',
        #   'ปกติ', 'ของการพูด']
    """

    def __init__(
        self,
        custom_dict: Union[Trie, Iterable[str], str] = None,
        engine: str = "newmm",
        keep_whitespace: bool = True,
    ):
        """
        Initialize tokenizer object.

        :param str custom_dict: a file path, a list of vocaburaies* to be
                    used to create a trie, or an instantiated
                    :class:`pythainlp.util.Trie` object.
        :param str engine: choose between different options of engine to token
                           (i.e.  *newmm*, *longest*, *attacut*)
        :param bool keep_whitespace: True to keep whitespaces, a common mark
                                    for end of phrase in Thai
        """
        self.__trie_dict = None
        if custom_dict:
            self.__trie_dict = dict_trie(custom_dict)
        else:
            self.__trie_dict = DEFAULT_WORD_DICT_TRIE
        self.__engine = engine
        self.__keep_whitespace = keep_whitespace

    def word_tokenize(self, text: str) -> List[str]:
        """
        Main tokenization function.

        :param str text: text to be tokenized
        :return: list of words, tokenized from the text
        :rtype: list[str]
        """
        return word_tokenize(
            text,
            custom_dict=self.__trie_dict,
            engine=self.__engine,
            keep_whitespace=self.__keep_whitespace,
        )

    def set_tokenize_engine(self, engine: str) -> None:
        """
        Set the tokenizer's engine.

        :param str engine: choose between different options of engine to token
                           (i.e. *newmm*, *longest*, *attacut*)
        """
        self.__engine = engine
