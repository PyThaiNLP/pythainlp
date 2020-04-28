# -*- coding: utf-8 -*-
"""
Thai tokenizers
"""
import re
from typing import Iterable, List, Union

from pythainlp.corpus import thai_syllables, thai_words

from .trie import Trie

DEFAULT_DICT_TRIE = Trie(thai_words())
SYLLABLE_DICT_TRIE = Trie(thai_syllables())


def word_tokenize(
    text: str,
    custom_dict: Trie = None,
    engine: str = "newmm",
    keep_whitespace: bool = True,
) -> List[str]:
    """
    Word tokenizer.

    Tokenizes running text into words (list of strings).

    :param str text: text to be tokenized
    :param str engine: name of the tokenizer to be used
    :param pythainlp.tokenize.Trie custom_dict: dictionary trie
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

    .. warning::
        * the option for engine named *ulmfit* has been deprecated since \
          PyThaiNLP version 2.1
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
    text: str, engine: str = "crfcut", keep_whitespace: bool = True
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
    else:  # default to crfcut
        from .crfcut import segment

        segments = segment(text)

    if not keep_whitespace:
        segments = [token.strip(" ") for token in segments if token.strip(" ")]

    return segments


def subword_tokenize(
    text: str, engine: str = "tcc", keep_whitespace: bool = True
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
    else:  # default
        from .tcc import segment

    segments = segment(text)

    if not keep_whitespace:
        segments = [token.strip(" ") for token in segments if token.strip(" ")]

    return segments


def syllable_tokenize(
    text: str, engine: str = "default", keep_whitespace: bool = True
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
        * *default*
        * *ssg* - CRF syllable segmenter for Thai.
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

    if engine == "ssg":
        from .ssg import segment

        segments = segment(text)
    else:  # default
        words = word_tokenize(text)
        for word in words:
            segments.extend(
                word_tokenize(text=word, custom_dict=SYLLABLE_DICT_TRIE)
            )

    if not keep_whitespace:
        segments = [token.strip(" ") for token in segments if token.strip(" ")]

    return segments


def dict_trie(dict_source: Union[str, Iterable[str], Trie]) -> Trie:
    """
    Create a dictionary trie which will be used for word_tokenize() function.

    :param str|Iterable[str]|pythainlp.tokenize.Trie dict_source: a path to
        dictionary file or a list of words or a pythainlp.tokenize.Trie object
    :return: a trie object created from a dictionary input
    :rtype: pythainlp.tokenize.Trie
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
        # Note: Since Trie and str are both Iterable,
        # so the Iterable check should be here, at the very end,
        # because it has less specificality
        # Received a sequence type object of vocabs
        trie = Trie(dict_source)
    else:
        raise TypeError(
            "Type of dict_source must be pythainlp.tokenize.Trie, or Iterable[str], or str (path to source file)"
        )

    return trie


class Tokenizer:
    """
    Tokenizer class, for a custom tokenizer.

    This class allows users to pre-define custom dictionary along with
    tokenizer and encapsulate them into one single object.
    It is an wrapper for both two functions including
    :func:`pythainlp.tokenize.word_tokenize`,
    and :func:`pythainlp.tokenize.dict_trie`

    :Example:

    Tokenizer object instantiated with :class:`pythainlp.tokenize.Trie`::

        from pythainlp.tokenize import Tokenizer
        from pythainlp.tokenize import Tokenizer, dict_trie
        from pythainlp.corpus.common import thai_words

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
                    :class:`pythainlp.tokenize.Trie` object.
        :param str engine: choose between different options of engine to token
                           (i.e.  *newmm*, *longest*, *attacut*)
        :param bool keep_whitespace: True to keep whitespaces, a common mark
                                    for end of phrase in Thai
        """
        self.__trie_dict = None
        if custom_dict:
            self.__trie_dict = dict_trie(custom_dict)
        else:
            self.__trie_dict = DEFAULT_DICT_TRIE
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
