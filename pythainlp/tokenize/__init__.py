# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import nltk
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
    else:  # default, use "newmm" engine
        from .newmm import segment

DEFAULT_DICT_TRIE = Trie(get_dict())


def dict_word_tokenize(text, custom_dict_trie, engine='newmm'):
    '''
    :meth:`dict_word_tokenize` tokenizes word based on the dictionary you provide. The format has to be in trie data structure.

    :param str text: the text to be tokenized
    :param dict custom_dict_trie: คือ trie ที่สร้างจาก create_custom_dict_trie
    :param str engine: choose between different options of engine to token (newmm, wordcutpy, mm, longest-matching)

    :return: A list of words, tokenized from a text.
    '''
    if engine == "newmm" or engine == "onecut":
        from .newmm import mmcut as segment
    elif engine == "mm" or engine == "multi_cut":
        from .multi_cut import segment
    elif engine == 'longest-matching':
        from .longest import segment
    elif engine == 'wordcutpy':
        from .wordcutpy import segment
        return segment(text, custom_dict_trie.keys())
    return segment(text, custom_dict_trie)


def word_tokenize(text, engine='newmm', whitespaces=True):
    """
    :param str text:  the text to be tokenized
    :param str engine: the engine to tokenize text
    :param bool whitespaces: True to output no whitespace, a common mark of sentence or end of phrase in Thai.
    :Parameters for engine:
        * newmm - ใช้ Maximum Matching algorithm ในการตัดคำภาษาไทย โค้ดชุดใหม่ (ค่าเริ่มต้น)
        * icu -  engine ตัวดั้งเดิมของ PyThaiNLP (ความแม่นยำต่ำ)
        * longest-matching ใช้ Longest matching ในการตัดคำ
        * mm ใช้ Maximum Matching algorithm - โค้ดชุดเก่า
        * pylexto - ใช้ LexTo ในการตัดคำ
        * deepcut - ใช้ Deep Neural Network ในการตัดคำภาษาไทย
        * wordcutpy - ใช้ wordcutpy (https://github.com/veer66/wordcutpy) ในการตัดคำ
        * cutkum - ใช้ Deep Neural Network ในการตัดคำภาษาไทย (https://github.com/pucktada/cutkum)
        * attacut - ใช้ AttaCut (https://github.com/PyThaiNLP/attacut) ในการตัดคำภาษาไทย
    :return: A list of words, tokenized from a text

    **Example**::

        from pythainlp.tokenize import word_tokenize
        text='ผมรักคุณนะครับโอเคบ่พวกเราเป็นคนไทยรักภาษาไทยภาษาบ้านเกิด'
        a=word_tokenize(text,engine='icu') # ['ผม', 'รัก', 'คุณ', 'นะ', 'ครับ', 'โอ', 'เค', 'บ่', 'พวก', 'เรา', 'เป็น', 'คน', 'ไทย', 'รัก', 'ภาษา', 'ไทย', 'ภาษา', 'บ้าน', 'เกิด']
        b=word_tokenize(text,engine='dict') # ['ผม', 'รัก', 'คุณ', 'นะ', 'ครับ', 'โอเค', 'บ่', 'พวกเรา', 'เป็น', 'คนไทย', 'รัก', 'ภาษาไทย', 'ภาษา', 'บ้านเกิด']
        c=word_tokenize(text,engine='mm') # ['ผม', 'รัก', 'คุณ', 'นะ', 'ครับ', 'โอเค', 'บ่', 'พวกเรา', 'เป็น', 'คนไทย', 'รัก', 'ภาษาไทย', 'ภาษา', 'บ้านเกิด']
        d=word_tokenize(text,engine='pylexto') # ['ผม', 'รัก', 'คุณ', 'นะ', 'ครับ', 'โอเค', 'บ่', 'พวกเรา', 'เป็น', 'คนไทย', 'รัก', 'ภาษาไทย', 'ภาษา', 'บ้านเกิด']
        e=word_tokenize(text,engine='newmm') # ['ผม', 'รัก', 'คุณ', 'นะ', 'ครับ', 'โอเค', 'บ่', 'พวกเรา', 'เป็น', 'คนไทย', 'รัก', 'ภาษาไทย', 'ภาษา', 'บ้านเกิด']
        g=word_tokenize(text,engine='wordcutpy') # ['ผม', 'รัก', 'คุณ', 'นะ', 'ครับ', 'โอเค', 'บ่', 'พวกเรา', 'เป็น', 'คน', 'ไทย', 'รัก', 'ภาษา', 'ไทย', 'ภาษา', 'บ้านเกิด']
    """
    if engine == 'icu':
        from .pyicu import segment
    elif engine == 'multi_cut' or engine == 'mm':
        from .multi_cut import segment
    elif engine == 'newmm' or engine == 'onecut':
        from .newmm import mmcut as segment
    elif engine == 'longest-matching':
        from .longest import segment
    elif engine == 'pylexto':
        from .pylexto import segment
    elif engine == 'deepcut':
        from .deepcut import segment
    elif engine == 'wordcutpy':
        from .wordcutpy import segment
    elif engine == 'attacut':
        from .attacut import segment
    else:
        raise Exception("error no have engine.")
    if not whitespaces:
        return [i.strip(' ') for i in segment(text) if i.strip(' ') != '']
    return segment(text)


def sent_tokenize(text, engine='whitespace+newline'):
    '''
This function does not yet automatically recognize when a sentence actually ends. Rather it helps split text where white space and a new line is found.

    :param str text: the text to be tokenized
    :param str engine: choose between 'whitespace' or 'whitespace+newline'

    :return: a list of text, split by whitespace or new line.
    '''
    if engine == 'whitespace':
        data = nltk.tokenize.WhitespaceTokenizer().tokenize(text)
    elif engine == 'whitespace+newline':
        data = re.sub(r'\n+|\s+', '|', text, re.U).split('|')
    return data


def subword_tokenize(text, engine='tcc'):
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
    if engine == 'tcc':
        from .tcc import tcc
    return tcc(text)


def isthai(text, check_all=False):
    """
    :param str text: input string or list of strings
    :param bool check_all: checks all character or not

    :return: A dictionary with the first value as proportional of text that is Thai, and the second value being a tuple of all characters, along with true or false.
    """
    listext = list(text)
    i = 0
    num_isthai = 0
    if check_all:
        listthai = []
    while i < len(listext):
        cVal = ord(listext[i])
        if (cVal >= 3584 and cVal <= 3711):
            num_isthai += 1
            if check_all:
                listthai.append(True)
        else:
            if check_all:
                listthai.append(False)
        i += 1
    thai = (num_isthai / len(listext)) * 100
    if check_all:
        dictthai = tuple(zip(listext, listthai))
        data = {'thai': thai, 'check_all': dictthai}
    else:
        data = {'thai': thai}
    return data


def syllable_tokenize(text):
    """
    :param str text: input string to be tokenized

    :return: returns list of strings of syllables
    """
    text1 = word_tokenize(text)
    data = []
    trie = create_custom_dict_trie(custom_dict_source=get_data())
    if len(text1) > 1:
        i = 0
        while i < len(text1):
            data.extend(
                dict_word_tokenize(text=text1[i], custom_dict_trie=trie))
            i += 1
    else:
        data = dict_word_tokenize(text=text, custom_dict_trie=trie)
    return data


def create_custom_dict_trie(custom_dict_source):
    """The function is used to create a custom dict trie which will be used for word_tokenize() function. For more information on the trie data structure, see:https://marisa-trie.readthedocs.io/en/latest/index.html

    :param string/list custom_dict_source:  a list of vocaburaries or a path to source file

    :return: A trie created from custom dict input
    """

    if type(custom_dict_source) is str:
        # Receive a file path of the custom dict to read
        with codecs.open(custom_dict_source, 'r', encoding='utf8') as f:
            _vocabs = f.read().splitlines()
            return Trie(_vocabs)
    elif isinstance(custom_dict_source, (list, tuple, set)):
        # Received a sequence type object of vocabs
        return Trie(custom_dict_source)
    else:
        raise TypeError(
            'Type of custom_dict_source must be either str (path to source file) or collections'
        )


class Tokenizer:
    def __init__(self, custom_dict=None):
        """
        Initialize tokenizer object

        :param str custom_dict: a file path or a list of vocaburaies to be used to create a trie (default - original lexitron)

        :return: trie_dict - a dictionary in the form of trie data for tokenizing engines
        """
        if custom_dict:
            if type(custom_dict) is list:
                self.trie_dict = Trie(custom_dict)
            elif type(custom_dict) is str:
                with codecs.open(custom_dict, 'r', encoding='utf8') as f:
                    vocabs = f.read().splitlines()
                self.trie_dict = Trie(vocabs)
        else:
            self.trie_dict = Trie(get_dict())

    def word_tokenize(self, text, engine='newmm'):
        from .newmm import mmcut as segment
        return segment(text, self.trie_dict)