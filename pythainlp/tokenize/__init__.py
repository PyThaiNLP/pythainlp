# -*- coding: utf-8 -*-
"""
Thai tokenizers
"""
import re
import warnings
from typing import Iterable, List, Union

from marisa_trie import Trie
from pythainlp.corpus import thai_syllables, thai_words

DEFAULT_DICT_TRIE = Trie(thai_words())


def word_tokenize(
    text: str,
    custom_dict: Trie = None,
    engine: str = "newmm",
    keep_whitespace: bool = True,
) -> List[str]:
    """
    This function tokenizes running text into words.
    :param str text: text to be tokenized
    :param str engine: name of the tokenizer to be used
    :param marisa_trie.Trie custom_dict: marisa dictionary trie
    :param bool keep_whitespace: True to keep whitespaces, a common mark
                                 for end of phrase in Thai.
                                 Otherwise, whitespaces are omitted.
    :return: list of words
    :rtype: list[str]
    **Options for engine**
        * *newmm* (default) - dictionary-based, Maximum Matching +
          Thai Character Cluster
        * *longest* - dictionary-based, Longest Matching
        * *deepcut* - wrapper for
          `deepcut <https://github.com/rkcosmos/deepcut>`_,
          language-model-based
        * *icu* - wrapper for ICU (International Components for Unicode,
          using PyICU), dictionary-based
        * attacut - Wrapper for `AttaCut (https://github.com/PyThaiNLP/attacut)`
    .. warning::
        * the option for engine named *ulmfit* has been deprecated since \
          PyThaiNLP version 2.1
    :Note:
        - The parameter **custom_dict** can be provided as an argument \
          only for *newmm*, *longest*, and *deepcut* engine.
    :Example:
        Tokenize text with different tokenizer:
        >>> from pythainlp.tokenize import word_tokenize
        >>>
        >>> text = "โอเคบ่พวกเรารักภาษาบ้านเกิด"
        >>> word_tokenize(text, engine="newmm")
        ['โอเค', 'บ่', 'พวกเรา', 'รัก', 'ภาษา', 'บ้านเกิด']
        >>>
        >>> word_tokenize(text, engine="longest")
        ['โอเค', 'บ่', 'พวกเรา', 'รัก', 'ภาษา', 'บ้านเกิด']
        >>>
        >>> word_tokenize(text, engine="deepcut")
        ['โอเค', 'บ่', 'พวก', 'เรา', 'รัก', 'ภาษา', 'บ้านเกิด']
        >>>
        >>> word_tokenize(text, engine="icu")
        ['โอ', 'เค', 'บ่', 'พวก', 'เรา', 'รัก', 'ภาษา', 'บ้าน', 'เกิด']
        >>>
        >>> word_tokenize(text, engine="ulmfit")
        ['โอเค', 'บ่', 'พวกเรา', 'รัก', 'ภาษา', 'บ้านเกิด']
        >>> tokenize.word_tokenize('โอเคบ่พวกเรารักภาษาบ้านเกิด', engine='attacut')
        ['โอเค', 'บ่', 'พวกเรา', 'รัก', 'ภาษา', 'บ้านเกิด']
        >>>
        Tokenize text by omitiing whitespaces:
        >>> from pythainlp.tokenize import word_tokenize
        >>>
        >>> text = "วรรณกรรม ภาพวาด และการแสดงงิ้ว "
        >>> word_tokenize(text, engine="newmm")
        ['วรรณกรรม', ' ', 'ภาพวาด', ' ', 'และ', 'การแสดง', 'งิ้ว', ' ']
        >>> word_tokenize(text, engine="newmm", keep_whitespace=False)
        ['วรรณกรรม', 'ภาพวาด', 'และ', 'การแสดง', 'งิ้ว']
        Tokenize with default and custom dictionary:
        >>> from pythainlp.corpus.common import thai_words
        >>> from pythainlp.tokenize import dict_trie, word_tokenize
        >>>
        >>> text = 'ชินโซ อาเบะ เกิด 21 กันยายน'
        >>> word_tokenize(text, engine="newmm")
        ​['ชิน', 'โซ', ' ', 'อา', 'เบะ', ' ', 'เกิด', ' ',
         '21', ' ', 'กันยายน']
        >>> custom_dict_japanese_name = set(thai_words()
        >>> custom_dict_japanese_name.add('ชินโซ')
        >>> custom_dict_japanese_name.add('อาเบะ')
        >>> trie = dict_trie(dict_source=custom_dict_japanese_name)
        >>> word_tokenize(text, engine="newmm", custom_dict=trie))
        ['ชินโซ', ' ', 'อาเบะ', ' ', 'เกิด', ' ', '21', ' ', 'กันยายน']
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
    elif engine == "icu":
        from .pyicu import segment

        segments = segment(text)
    elif engine == 'attacut':
        from .attacut import segment

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
    :meth: DEPRECATED: Please use `word_tokenize()` with a `custom_dict`
           argument instead
    :param str text: text to be tokenized
    :param dict custom_dict: a dictionary trie, or an iterable of words,
                             or a string of dictionary path
    :param str engine: choose between different options of engine to token
                       (newmm [default], mm, longest, and deepcut)
    :param bool keep_whitespace: True to keep whitespaces, a common mark
                                 for end of phrase in Thai
    :return: list of words
    """
    warnings.warn(
        "dict_word_tokenize is deprecated. Use word_tokenize with a custom_dict argument instead.",
        DeprecationWarning,
    )

    return word_tokenize(
        text=text,
        custom_dict=custom_dict,
        engine=engine,
        keep_whitespace=keep_whitespace,
    )


def sent_tokenize(text: str, engine: str = "whitespace+newline") -> List[str]:
    """
    This function does not yet automatically recognize when a sentence
    actually ends. Rather it helps split text where white space and
    a new line is found.
    :param str text: the text to be tokenized
    :param str engine: choose between *'whitespace'* or *'whitespace+newline'*
    :return: list of splited sentences
    :rtype: list[str]
    **Options for engine**
        * *whitespace+newline* (default) - split by whitespace token \
                                           and newline.
        * *whitespace* - split by whitespace token. Specifiaclly, with \
                         :class:`regex` pattern  ``r" +"``
    :Example:
    Split the text based on *whitespace*
    >>> from pythainlp.tokenize import sent_tokenize
    >>> sentence_1 = "ฉันไปประชุมเมื่อวันที่ 11 มีนาคม"
    >>> sentence_2 = "ข้าราชการได้รับการหมุนเวียนเป็นระยะ \\
        และได้รับมอบหมายให้ประจำในระดับภูมิภาค"
    >>> sent_tokenize(sentence_1, engine="whitespace")
    ['ฉันไปประชุมเมื่อวันที่', '11', 'มีนาคม']
    >>> sent_tokenize(sentence_2, engine="whitespace")
    ['ข้าราชการได้รับการหมุนเวียนเป็นระยะ',
    '\\nและได้รับมอบหมายให้ประจำในระดับภูมิภาค']
    Split the text based on *whitespace* and *newline*
    >>> from pythainlp.tokenize import sent_tokenize
    >>> sentence_1 = "ฉันไปประชุมเมื่อวันที่ 11 มีนาคม"
    >>> sentence_2 = "ข้าราชการได้รับการหมุนเวียนเป็นระยะ \\
        และได้รับมอบหมายให้ประจำในระดับภูมิภาค"
    >>> sent_tokenize(sentence_1, engine="whitespace")
    ['ฉันไปประชุมเมื่อวันที่', '11', 'มีนาคม']
    >>> sent_tokenize(sentence_2, engine="whitespace")
    ['ข้าราชการได้รับการหมุนเวียนเป็นระยะ',
     'และได้รับมอบหมายให้ประจำในระดับภูมิภาค']
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
    This function tokenizes text into inseparable units of
    Thai contiguous characters namely
    `Thai Character Clusters (TCCs) \
    <https://www.researchgate.net/publication/2853284_Character_Cluster_Based_Thai_Information_Retrieval>`_
    TCCs are the units based on Thai spelling feature that could not be
    separated any character further such as   'ก็', 'จะ', 'ไม่', and 'ฝา'.
    If the following units are separated, they could not be spelled out.
    This function apply the TCC rules to tokenizes the text into
    the smallest units. For example, the word 'ขนมชั้น' would be tokenized
    into 'ข', 'น', 'ม', and 'ชั้น'
    :param str text: text to be tokenized
    :param str engine: the name subword tokenizer
    :return: list of subwords
    :rtype: list[str]
    **Options for engine**
        * *tcc* (default) -  Thai Character Cluster (Theeramunkong et al. 2000)
        * *ssg* - CRF syllable segmenter for Thai.
        * *etcc* - Enhanced Thai Character Cluster (Inrut et al. 2001)
          [In development]
    :Example:
      Tokenize text into subword based on *tcc*
      >>> from pythainlp.tokenize import subword_tokenize
      >>> text_1 = "ยุคเริ่มแรกของ ราชวงศ์หมิง"
      >>> text_2 = "ความแปลกแยกและพัฒนาการ"
      >>> subword_tokenize(text_1, engine='tcc')
      ['ยุ', 'ค', 'เริ่ม', 'แร', 'ก', 'ข', 'อ', 'ง', ' ', 'รา', 'ช', 'ว', 'ง',
       'ศ', '์', 'ห', 'มิ', 'ง']
      >>> subword_tokenize(text_2, engine='tcc')
      ['ค', 'วา', 'ม', 'แป', 'ล', 'ก', 'แย', 'ก',
       'และ', 'พัฒ','นา', 'กา', 'ร']
      Tokenize text into subword based on *etcc* **(Work In Progress)**
      >>> from pythainlp.tokenize import subword_tokenize
      >>> text_1 = "ยุคเริ่มแรกของ ราชวงศ์หมิง"
      >>> text_2 = "ความแปลกแยกและพัฒนาการ"
      >>> subword_tokenize(text_1, engine='etcc')
      ['ยุคเริ่มแรกของ ราชวงศ์หมิง']
      >>> subword_tokenize(text_2, engine='etcc')
      ['ความแปลกแยกและ', 'พัฒ', 'นาการ']
    """
    if not text or not isinstance(text, str):
        return []

    if engine == "etcc":
        from .etcc import segment
    elif engine == "ssg":
        from .ssg import segment
    else:  # default
        from .tcc import segment

    return segment(text)


def syllable_tokenize(text: str, engine: str = "default") -> List[str]:
    """
    This function is to tokenize text into syllable (Thai: พยางค์), a unit of
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
    :return: list of syllables where whitespaces in the text **are included**
    :rtype: list[str]
    **Options for engine**
        * *default*
        * *ssg* - CRF syllable segmenter for Thai.
    :Example:
      >>> from pythainlp.tokenize import syllable_tokenize
      >>>
      >>> text = 'รถไฟสมัยใหม่จะใช้กำลังจากหัวรถจักรดีเซล หรือจากไฟฟ้า'
      >>> syllable_tokenize(text)
      ['รถ', 'ไฟ', 'สมัย', 'ใหม่', 'ใช้', 'กำ', 'ลัง', 'จาก', 'หัว',
      'รถ', 'จักร', 'ดี', 'เซล', ' ', 'หรือ', 'จาก', 'ไฟ', 'ฟ้า']
    """

    if not text or not isinstance(text, str):
        return []

    tokens = []
    if engine == "default":
        words = word_tokenize(text)
        trie = dict_trie(dict_source=thai_syllables())
        for word in words:
            tokens.extend(word_tokenize(text=word, custom_dict=trie))
    else:
        from .ssg import segment
        tokens = segment(text)

    return tokens


def dict_trie(dict_source: Union[str, Iterable[str], Trie]) -> Trie:
    """
    Create a dict trie which will be used for word_tokenize() function.
    For more information on the trie data structure,
    see: `marisa-trie's Official Documentation \
    <https://marisa-trie.readthedocs.io/en/latest/index.html>`_
    :param string/list dict_source: a list of vocaburaries or a path
                                    to source file
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
    """
    This class allows users to pre-define custom dictionary along with
    tokenizer and encapsulate them into one single object.
    It is an wrapper for both two functions including
    :func:`pythainlp.tokenize.word_tokenize`,
    and :func:`pythainlp.tokenize.dict_trie`
    :Example:
    Tokenizer object instantiated with :class:`marisa_trie.Trie`
    >>> from pythainlp.tokenize import Tokenizer
    >>> from pythainlp.tokenize import Tokenizer, dict_trie
    >>> from pythainlp.corpus.common import thai_words
    >>>
    >>> custom_words_list = set(thai_words())
    >>> custom_words_list.add('อะเฟเซีย')
    >>> custom_words_list.add('Aphasia')
    >>> trie = dict_trie(dict_source=custom_words_list)
    >>>
    >>> text = "อะเฟเซีย (Aphasia*) เป็นอาการผิดปกติของการพูด"
    >>> _tokenizer = Tokenizer(custom_dict=trie, engine='newmm')
    ['อะเฟเซีย', ' ', '(', 'Aphasia', ')', ' ', 'เป็น', 'อาการ',
     'ผิดปกติ', 'ของ', 'การ', 'พูด']
    Tokenizer object instantiated with a list of words
    >>> from pythainlp.tokenize import Tokenizer
    >>> from pythainlp.corpus.common import thai_words
    >>>
    >>>  text = "อะเฟเซีย (Aphasia) เป็นอาการผิดปกติของการพูด"
    >>> _tokenizer = Tokenizer(custom_dict=list(thai_words()), engine='newmm')
    >>> _tokenizer.word_tokenize(text)
    ['อะ', 'เฟเซีย', ' ', '(', 'Aphasia', ')', ' ', 'เป็น', 'อาการ',
     'ผิดปกติ', 'ของ', 'การ', 'พูด']
    Tokenizer object instantiated with a file path containing list of
    word separated with *newline*  and explicitly set a new tokeneizer
    after initiation.
    >>> from pythainlp.tokenize import Tokenizer
    >>>
    >>> PATH_TO_CUSTOM_DICTIONARY = './custom_dictionary.txtt'
    >>>
    >>> # write a file
    >>> with open(PATH_TO_CUSTOM_DICTIONARY, 'w', encoding='utf-8') as f:
    >>>    f.write('อะเฟเซีย\\nAphasia\\nผิด\\nปกติ')
    >>>
    >>> text = "อะเฟเซีย (Aphasia) เป็นอาการผิดปกติของการพูด"
    >>>
    >>> # initate an object from file with `deepcut` as tokenizer
    >>> _tokenizer = Tokenizer(custom_dict=PATH_TO_CUSTOM_DICTIONARY, \\
        engine='deepcut')
    >>> _tokenizer.word_tokenize(text)
    ['อะเฟเซีย', ' ', '(', 'Aphasia', ')', ' ', 'เป็น', 'อาการ', 'ผิด',
     'ปกติ', 'ของ', 'การ', 'พูด']
    >>>
    >>> # change tokenizer to `newmm
    >>> _tokenizer.set_tokenizer_engine(engine='newmm')
    >>> _tokenizer.word_tokenize(text)
    ['อะเฟเซีย', ' ', '(', 'Aphasia', ')', ' ', 'เป็นอาการ', 'ผิด',
     'ปกติ', 'ของการพูด']
    """

    def __init__(
        self, custom_dict: Union[Trie, Iterable[str], str] = None, engine: str = "newmm"
    ):
        """
        Initialize tokenizer object
        :param str: a file path, a list of vocaburaies* to be
                    used to create a trie, or an instantiated
                    :class:`marisa_trie.Trie` object.
        :param str engine: choose between different options of engine to token
                           (i.e.  *newmm*, *longest*, *deepcut*)
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
        :rtype: list[str]
        """
        return word_tokenize(text, custom_dict=self.__trie_dict, engine=self.__engine)

    def set_tokenize_engine(self, engine: str) -> None:
        """
        Set the tokenizer
        :param str engine: choose between different options of engine to token
                           (i.e. *newmm*, *longest*, *deepcut*)
        """
        self.__engine = engine
        
