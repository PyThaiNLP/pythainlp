# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2025 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""
Generic functions of tokenizers
"""

import copy
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
from pythainlp.tokenize._utils import (
    apply_postprocessors,
    rejoin_formatted_num,
    strip_whitespace,
)
from pythainlp.util.trie import Trie, dict_trie


def word_detokenize(
    segments: Union[List[List[str]], List[str]], output: str = "str"
) -> Union[List[str], str]:
    """
    Word detokenizer.

    This function will detokenize the list of words in each sentence into text.

    :param str segments: List of sentences, each with a list of words.
    :param str output: the output type (str or list)
    :return: the Thai text
    :rtype: Union[str,List[str]]
    :Example:
    ::

        from pythainlp.tokenize import word_detokenize

        print(word_detokenize(["เรา", "เล่น"]))
        # output: เราเล่น
    """
    list_all = []

    if isinstance(segments[0], str):
        segments = [segments]

    from pythainlp import thai_characters

    for i, s in enumerate(segments):
        list_sents = []
        add_index = []
        space_index = []
        mark_index = []
        for j, w in enumerate(s):
            if j > 0:
                # previous word
                p_w = s[j - 1]
                # if w is number or other language and is not space
                if (
                    w[0] not in thai_characters
                    and not w.isspace()
                    and not p_w.isspace()
                ):
                    list_sents.append(" ")
                    add_index.append(j)
                # if previous word is number or other language and is not space
                elif p_w[0] not in thai_characters and not p_w.isspace():
                    list_sents.append(" ")
                    add_index.append(j)
                # if word is Thai iteration mark
                elif w == "ๆ":
                    if not p_w.isspace():
                        list_sents.append(" ")
                    mark_index.append(j)
                elif w.isspace() and j - 1 not in space_index:
                    space_index.append(j)
                elif j - 1 in mark_index:
                    list_sents.append(" ")
            list_sents.append(w)
        list_all.append(list_sents)

    if output == "list":
        return list_all

    text = []
    for i in list_all:
        text.append("".join(i))
    return " ".join(text)


def word_tokenize(
    text: str,
    custom_dict: Trie = Trie([]),
    engine: str = DEFAULT_WORD_TOKENIZE_ENGINE,
    keep_whitespace: bool = True,
    join_broken_num: bool = True,
) -> List[str]:
    """
    Word tokenizer.

    Tokenizes running text into words (list of strings).

    :param str text: text to be tokenized
    :param str engine: name of the tokenizer to be used
    :param pythainlp.util.Trie custom_dict: dictionary trie (some engine may not support)
    :param bool keep_whitespace: True to keep whitespace, a common mark
                                  for end of phrase in Thai.
                                  Otherwise, whitespace is omitted.
    :param bool join_broken_num: True to rejoin formatted numeric that could be wrongly separated.
                                  Otherwise, formatted numeric could be wrongly separated.

    :return: list of words
    :rtype: List[str]
    **Options for engine**
        * *attacut* - wrapper for
          `AttaCut <https://github.com/PyThaiNLP/attacut>`_.,
          learning-based approach
        * *deepcut* - wrapper for
          `DeepCut <https://github.com/rkcosmos/deepcut>`_,
          learning-based approach
        * *icu* - wrapper for a word tokenizer in
          `PyICU <https://gitlab.pyicu.org/main/pyicu>`_.,
          from ICU (International Components for Unicode),
          dictionary-based          
        * *longest* - dictionary-based, longest matching
        * *mm* - "multi-cut", dictionary-based, maximum matching
        * *nercut* - dictionary-based, maximal matching,
          constrained by Thai Character Cluster (TCC) boundaries,
          combining tokens that are parts of the same named-entity
        * *newmm* (default) - "new multi-cut",
          dictionary-based, maximum matching,
          constrained by Thai Character Cluster (TCC) boundaries
          with improved TCC rules that are used in newmm.
        * *newmm-safe* - newmm, with a mechanism to avoid long
          processing time for text with continuously ambiguous breaking points
        * *nlpo3* - wrapper for a word tokenizer in
          `nlpO3 <https://github.com/PyThaiNLP/nlpo3>`_.,
          adaptation of newmm in Rust (2.5x faster)
        * *oskut* - wrapper for
          `OSKut <https://github.com/mrpeerat/OSKut>`_.,
          Out-of-domain StacKed cut for Word Segmentation
        * *sefr_cut* - wrapper for
          `SEFR CUT <https://github.com/mrpeerat/SEFR_CUT>`_.,
          Stacked Ensemble Filter and Refine for Word Segmentation
        * *tltk* - wrapper for
          `TLTK <https://pypi.org/project/tltk/>`_.,
           maximum collocation approach
        * *budoux* - wrapper for
          `budoux <https://github.com/google/budoux>`_.
    :Note:
        - The **custom_dict** parameter only works for \
          *deepcut*, *longest*, *newmm*, and *newmm-safe* engines.
    :Example:

    Tokenize text with different tokenizers::

        from pythainlp.tokenize import word_tokenize

        text = "โอเคบ่พวกเรารักภาษาบ้านเกิด"

        word_tokenize(text, engine="newmm")
        # output: ['โอเค', 'บ่', 'พวกเรา', 'รัก', 'ภาษา', 'บ้านเกิด']

        word_tokenize(text, engine='attacut')
        # output: ['โอเค', 'บ่', 'พวกเรา', 'รัก', 'ภาษา', 'บ้านเกิด']

    Tokenize text with whitespace omitted::

        text = "วรรณกรรม ภาพวาด และการแสดงงิ้ว "

        word_tokenize(text, engine="newmm")
        # output:
        # ['วรรณกรรม', ' ', 'ภาพวาด', ' ', 'และ', 'การแสดง', 'งิ้ว', ' ']

        word_tokenize(text, engine="newmm", keep_whitespace=False)
        # output: ['วรรณกรรม', 'ภาพวาด', 'และ', 'การแสดง', 'งิ้ว']

    Join broken formatted numeric (e.g. time, decimals, IP addresses)::

        text = "เงิน1,234บาท19:32น 127.0.0.1"

        word_tokenize(text, engine="attacut", join_broken_num=False)
        # output:
        # ['เงิน', '1', ',', '234', 'บาท', '19', ':', '32น', ' ',
        #  '127', '.', '0', '.', '0', '.', '1']

        word_tokenize(text, engine="attacut", join_broken_num=True)
        # output:
        # ['เงิน', '1,234', 'บาท', '19:32น', ' ', '127.0.0.1']

    Tokenize with default and custom dictionaries::

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
        # ['ชินโซ', ' ', 'อาเบะ', ' ',
        #  'เกิด', ' ', '21', ' ', 'กันยายน']
    """
    if not text or not isinstance(text, str):
        return []

    segments = []

    if custom_dict and engine in (
        "attacut",
        "icu",
        "nercut",
        "sefr_cut",
        "tltk",
        "oskut",
        "budoux",
    ):
        raise NotImplementedError(
            f"The {engine} engine does not support custom dictionaries."
        )

    if engine in ("newmm", "onecut"):
        from pythainlp.tokenize.newmm import segment

        segments = segment(text, custom_dict)
    elif engine == "newmm-safe":
        from pythainlp.tokenize.newmm import segment

        segments = segment(text, custom_dict, safe_mode=True)
    elif engine == "attacut":
        from pythainlp.tokenize.attacut import segment

        segments = segment(text)
    elif engine == "longest":
        from pythainlp.tokenize.longest import segment

        segments = segment(text, custom_dict)
    elif engine in ("mm", "multi_cut"):
        from pythainlp.tokenize.multi_cut import segment

        segments = segment(text, custom_dict)
    elif engine == "deepcut":  # deepcut can optionally use dictionary
        from pythainlp.tokenize.deepcut import segment

        if custom_dict:
            custom_dict = list(custom_dict)
            segments = segment(text, custom_dict)
        else:
            segments = segment(text)
    elif engine == "icu":
        from pythainlp.tokenize.pyicu import segment

        segments = segment(text)
    elif engine == "budoux":
        from pythainlp.tokenize.budoux import segment

        segments = segment(text)
    elif engine == "nercut":
        from pythainlp.tokenize.nercut import segment

        segments = segment(text)
    elif engine == "sefr_cut":
        from pythainlp.tokenize.sefr_cut import segment

        segments = segment(text)
    elif engine == "tltk":
        from pythainlp.tokenize.tltk import segment

        segments = segment(text)
    elif engine == "oskut":
        from pythainlp.tokenize.oskut import segment

        segments = segment(text)
    elif engine == "nlpo3":
        from pythainlp.tokenize.nlpo3 import segment

        # Currently cannot handle custom_dict from inside word_tokenize(),
        # due to difference in type.
        # if isinstance(custom_dict, str):
        #    segments = segment(text, custom_dict=custom_dict)
        # elif not isinstance(custom_dict, str) and not custom_dict:
        #    raise ValueError(
        #        f"""Tokenizer \"{engine}\":
        #        custom_dict must be a str.
        #        It is a dictionary name as assigned with load_dict().
        #        See pythainlp.tokenize.nlpo3.load_dict()"""
        #    )
        # else:
        #    segments = segment(text)
        segments = segment(text)
    else:
        raise ValueError(
            f"""Tokenizer \"{engine}\" not found.
            It might be a typo; if not, please consult our document."""
        )

    postprocessors = []
    if join_broken_num:
        postprocessors.append(rejoin_formatted_num)

    if not keep_whitespace:
        postprocessors.append(strip_whitespace)

    segments = apply_postprocessors(segments, postprocessors)

    return segments


def indices_words(words):
    indices = []
    start_index = 0
    for word in words:
        end_index = start_index + len(word) - 1
        indices.append((start_index, end_index))
        start_index += len(word)

    return indices


def map_indices_to_words(index_list, sentences):
    result = []
    c = copy.copy(index_list)
    n_sum = 0
    for sentence in sentences:
        words = sentence
        sentence_result = []
        n = 0
        for start, end in c:
            if start > n_sum + len(words) - 1:
                break
            else:
                word = sentence[start - n_sum : end + 1 - n_sum]
                sentence_result.append(word)
                n += 1

        result.append(sentence_result)
        n_sum += len(words)
        for _ in range(n):
            del c[0]
    return result


def sent_tokenize(
    text: Union[str, List[str]],
    engine: str = DEFAULT_SENT_TOKENIZE_ENGINE,
    keep_whitespace: bool = True,
) -> List[str]:
    """
    Sentence tokenizer.

    Tokenizes running text into "sentences". Supports both string and list of strings.

    :param text: the text (string) or list of words (list of strings) to be tokenized
    :param str engine: choose among *'crfcut'*, *'whitespace'*, \
    *'whitespace+newline'*
    :return: list of split sentences
    :rtype: list[str]
    **Options for engine**
        * *crfcut* - (default) split by CRF trained on TED dataset
        * *thaisum* - The implementation of sentence segmenter from \
            Nakhun Chumpolsathien, 2020
        * *tltk* - split by `TLTK <https://pypi.org/project/tltk/>`_.,
        * *wtp* - split by `wtpsplitaxe <https://github.com/bminixhofer/wtpsplit>`_., \
            It supports many sizes of models. You can use ``wtp`` to use mini model, \
            ``wtp-tiny`` to use ``wtp-bert-tiny`` model (default), \
            ``wtp-mini`` to use ``wtp-bert-mini`` model, \
            ``wtp-base`` to use ``wtp-canine-s-1l`` model, \
            and ``wtp-large`` to use ``wtp-canine-s-12l`` model.
        * *whitespace+newline* - split by whitespace and newline.
        * *whitespace* - split by whitespace, specifically with \
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

    if not text or not isinstance(text, (str, list)):
        return []

    is_list_input = isinstance(text, list)

    if is_list_input:
        try:
            original_text = "".join(text)
        except ValueError:
            return []

    else:
        original_text = text

    segments = []

    if engine == "crfcut":
        from pythainlp.tokenize.crfcut import segment

        segments = segment(original_text)

        if is_list_input:
            word_indices = indices_words(text)
            result = map_indices_to_words(word_indices, [original_text])
            return result
    elif engine == "whitespace":
        segments = re.split(r" +", original_text, flags=re.U)
        if is_list_input:
            result = []
            _temp: list[str] = []
            for i, w in enumerate(text):
                if re.findall(r" ", w) != [] and re.findall(r"\w", w) == []:
                    if not _temp:
                        continue
                    result.append(_temp)
                    _temp = []
                else:
                    _temp.append(w)
                if i + 1 == len(text):
                    result.append(_temp)
            return result
    elif engine == "whitespace+newline":
        segments = original_text.split()
        if is_list_input:
            result = []
            _temp = []
            for i, w in enumerate(text):
                if (
                    re.findall(r"\s", w) != [] or re.findall(r"\n", w) != []
                ) and re.findall(r"\w", w) == []:
                    if not _temp:
                        continue
                    result.append(_temp)
                    _temp = []
                else:
                    _temp.append(w)
                if i + 1 == len(text):
                    result.append(_temp)
            return result
    elif engine == "tltk":
        from pythainlp.tokenize.tltk import sent_tokenize as segment

        segments = segment(original_text)
    elif engine == "thaisum":
        from pythainlp.tokenize.thaisumcut import (
            ThaiSentenceSegmentor as segmentor,
        )

        segment = segmentor()
        segments = segment.split_into_sentences(original_text)
    elif engine.startswith("wtp"):
        if "-" not in engine:
            _size = "mini"
        else:
            _size = engine.split("-")[-1]
        from pythainlp.tokenize.wtsplit import tokenize as segment

        segments = segment(original_text, size=_size, tokenize="sentence")
    else:
        raise ValueError(
            f"""Tokenizer \"{engine}\" not found.
            It might be a typo; if not, please consult our document."""
        )

    if not keep_whitespace:
        segments = strip_whitespace(segments)

    if is_list_input and engine not in ["crfcut"]:
        word_indices = indices_words(text)
        result = map_indices_to_words(word_indices, segments)
        return result
    else:
        return segments


def paragraph_tokenize(
    text: str,
    engine: str = "wtp-mini",
    paragraph_threshold: float = 0.5,
    style: str = "newline",
) -> List[List[str]]:
    """
    Paragraph tokenizer.

    Tokenizes text into paragraphs.

    :param str text: text to be tokenized
    :param str engine: the name of paragraph tokenizer
    :return: list of paragraphs
    :rtype: List[List[str]]
    **Options for engine**
        * *wtp* - split by `wtpsplitaxe <https://github.com/bminixhofer/wtpsplit>`_., \
            It supports many sizes of models. You can use ``wtp`` to use mini model, \
            ``wtp-tiny`` to use ``wtp-bert-tiny`` model (default), \
            ``wtp-mini`` to use ``wtp-bert-mini`` model, \
            ``wtp-base`` to use ``wtp-canine-s-1l`` model, \
            and ``wtp-large`` to use ``wtp-canine-s-12l`` model.

    :Example:

    Split the text based on *wtp*::

        from pythainlp.tokenize import paragraph_tokenize

        sent = (
            "(1) บทความนี้ผู้เขียนสังเคราะห์ขึ้นมาจากผลงานวิจัยที่เคยทำมาในอดีต"
            +"  มิได้ทำการศึกษาค้นคว้าใหม่อย่างกว้างขวางแต่อย่างใด"
            +" จึงใคร่ขออภัยในความบกพร่องทั้งปวงมา ณ ที่นี้"
        )

        paragraph_tokenize(sent)
        # output: [
        # ['(1) '], 
        # [
        #   'บทความนี้ผู้เขียนสังเคราะห์ขึ้นมาจากผลงานวิจัยที่เคยทำมาในอดีต  ',
        #   'มิได้ทำการศึกษาค้นคว้าใหม่อย่างกว้างขวางแต่อย่างใด ',
        #   'จึงใคร่ขออภัยในความบกพร่องทั้งปวงมา ',
        #   'ณ ที่นี้'
        # ]]
    """
    if engine.startswith("wtp"):
        if "-" not in engine:
            size = "mini"
        else:
            size = engine.split("-")[-1]

        from pythainlp.tokenize.wtsplit import tokenize as segment

        segments = segment(
            text,
            size=size,
            tokenize="paragraph",
            paragraph_threshold=paragraph_threshold,
            style=style,
        )
    else:
        raise ValueError(
            f"""Tokenizer \"{engine}\" not found.
            It might be a typo; if not, please consult our document."""
        )

    return segments


def subword_tokenize(
    text: str,
    engine: str = DEFAULT_SUBWORD_TOKENIZE_ENGINE,
    keep_whitespace: bool = True,
) -> List[str]:
    """
    Subword tokenizer for tokenizing text into units smaller than syllables.

    Tokenizes text into inseparable units of
    Thai contiguous characters, namely
    `Thai Character Clusters (TCCs) \
    <https://www.researchgate.net/publication/2853284_Character_Cluster_Based_Thai_Information_Retrieval>`_
    TCCs are units based on Thai spelling features that could not be
    separated any character further such as 'ก็', 'จะ', 'ไม่', and 'ฝา'.
    If the following units are separated, they could not be spelled out.
    This function applies TCC rules to tokenize the text into
    the smallest units.

    For example, the word 'ขนมชั้น' would be tokenized
    into 'ข', 'น', 'ม', and 'ชั้น'.

    :param str text: text to be tokenized
    :param str engine: the name of subword tokenizer
    :param bool keep_whitespace: keep whitespace
    :return: list of subwords
    :rtype: List[str]
    **Options for engine**
        * *dict* - newmm word tokenizer with a syllable dictionary
        * *etcc* - Enhanced Thai Character Cluster (Inrut et al. 2001)
        * *han_solo* - CRF syllable segmenter for Thai that can work in the \
            Thai social media domain. See `PyThaiNLP/Han-solo \
        <https://github.com/PyThaiNLP/Han-solo>`_.
        * *ssg* - CRF syllable segmenter for Thai. See `ponrawee/ssg \
        <https://github.com/ponrawee/ssg>`_.
        * *tcc* (default) - Thai Character Cluster (Theeramunkong et al. 2000)
        * *tcc_p* - Thai Character Cluster + improved rules that are used in newmm
        * *tltk* - syllable tokenizer from tltk. See `tltk \
        <https://pypi.org/project/tltk/>`_.
        * *wangchanberta* - SentencePiece from wangchanberta model
    :Example:

    Tokenize text into subwords based on *tcc*::

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

    Tokenize text into subwords based on *etcc*::

        text_1 = "ยุคเริ่มแรกของ ราชวงศ์หมิง"
        text_2 = "ความแปลกแยกและพัฒนาการ"

        subword_tokenize(text_1, engine='etcc')
        # output: ['ยุคเริ่มแรกของ ราชวงศ์หมิง']

        subword_tokenize(text_2, engine='etcc')
        # output: ['ความแปลกแยกและ', 'พัฒ', 'นาการ']

    Tokenize text into subwords based on *wangchanberta*::

        text_1 = "ยุคเริ่มแรกของ ราชวงศ์หมิง"
        text_2 = "ความแปลกแยกและพัฒนาการ"

        subword_tokenize(text_1, engine='wangchanberta')
        # output: ['▁', 'ยุค', 'เริ่มแรก', 'ของ', '▁', 'ราชวงศ์', 'หมิง']

        subword_tokenize(text_2, engine='wangchanberta')
        # output: ['▁ความ', 'แปลก', 'แยก', 'และ', 'พัฒนาการ']
    """
    if not text or not isinstance(text, str):
        return []

    segments = []

    if engine == "tcc":
        from pythainlp.tokenize.tcc import segment
    elif engine == "tcc_p":
        from pythainlp.tokenize.tcc_p import segment
    elif engine == "etcc":
        from pythainlp.tokenize.etcc import segment
    elif engine == "wangchanberta":
        from pythainlp.wangchanberta import segment
    elif engine == "dict":  # use syllable dictionary
        words = word_tokenize(text)
        for word in words:
            segments.extend(
                word_tokenize(
                    text=word, custom_dict=DEFAULT_SYLLABLE_DICT_TRIE
                )
            )
    elif engine == "ssg":
        from pythainlp.tokenize.ssg import segment
    elif engine == "tltk":
        from pythainlp.tokenize.tltk import syllable_tokenize as segment
    elif engine == "han_solo":
        from pythainlp.tokenize.han_solo import segment
    elif engine == "phayathai":
        from pythainlp.phayathaibert import segment
    else:
        raise ValueError(
            f"""Tokenizer \"{engine}\" not found.
            It might be a typo; if not, please consult our document."""
        )

    if not segments:
        segments = segment(text)

    if not keep_whitespace:
        segments = strip_whitespace(segments)

    return segments


def syllable_tokenize(
    text: str,
    engine: str = DEFAULT_SYLLABLE_TOKENIZE_ENGINE,
    keep_whitespace: bool = True,
) -> List[str]:
    """
    Syllable tokenizer

    Tokenizes text into inseparable units of
    Thai syllables.

    :param str text: text to be tokenized
    :param str engine: the name of syllable tokenizer
    :param bool keep_whitespace: keep whitespace
    :return: list of subwords
    :rtype: List[str]
    **Options for engine**
        * *dict* - newmm word tokenizer with a syllable dictionary
        * *han_solo* - CRF syllable segmenter for Thai that can work in the \
            Thai social media domain. See `PyThaiNLP/Han-solo \
        <https://github.com/PyThaiNLP/Han-solo>`_.
        * *ssg* - CRF syllable segmenter for Thai. See `ponrawee/ssg \
        <https://github.com/ponrawee/ssg>`_.
        * *tltk* - syllable tokenizer from tltk. See `tltk \
        <https://pypi.org/project/tltk/>`_.
    """
    if engine not in ["dict", "han_solo", "ssg", "tltk"]:
        raise ValueError(
            f"""Tokenizer \"{engine}\" not found.
            It might be a typo; if not, please consult our document."""
        )
    return subword_tokenize(
        text=text, engine=engine, keep_whitespace=keep_whitespace
    )


def display_cell_tokenize(text: str) -> List[str]:
    """
    Display cell tokenizer.

    Tokenizes Thai text into display cells without splitting tone marks.

    :param str text: text to be tokenized
    :return: list of display cells
    :rtype: List[str]
    :Example:

    Tokenize Thai text into display cells::

        from pythainlp.tokenize import display_cell_tokenize

        text = "แม่น้ำอยู่ที่ไหน"
        display_cell_tokenize(text)
        # output: ['แ', 'ม่', 'น้ํ', 'า', 'อ', 'ยู่', 'ที่', 'ไ', 'ห', 'น']
    """
    if not text or not isinstance(text, str):
        return []

    display_cells = []
    current_cell = ""
    text = text.replace("ำ", "ํา")

    for char in text:
        if re.match(r"[\u0E31\u0E34-\u0E3A\u0E47-\u0E4E]", char):
            current_cell += char
        else:
            if current_cell:
                display_cells.append(current_cell)
            current_cell = char

    if current_cell:
        display_cells.append(current_cell)

    return display_cells


class Tokenizer:
    """
    Tokenizer class for a custom tokenizer.

    This class allows users to pre-define custom dictionary along with
    tokenizer and encapsulate them into one single object.
    It is an wrapper for both functions, that are
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
        _tokenizer.word_tokenize(text)
        # output: ['อะเฟเซีย', ' ', '(', 'Aphasia', ')', ' ', 'เป็น', 'อาการ',
        'ผิดปกติ', 'ของ', 'การ', 'พูด']

    Tokenizer object instantiated with a list of words::

        text = "อะเฟเซีย (Aphasia) เป็นอาการผิดปกติของการพูด"
        _tokenizer = Tokenizer(custom_dict=list(thai_words()), engine='newmm')
        _tokenizer.word_tokenize(text)
        # output:
        # ['อะ', 'เฟเซีย', ' ', '(', 'Aphasia', ')', ' ', 'เป็น', 'อาการ',
        #   'ผิดปกติ', 'ของ', 'การ', 'พูด']

    Tokenizer object instantiated with a file path containing a list of
    words separated with *newline* and explicitly setting a new tokenizer
    after initiation::

        PATH_TO_CUSTOM_DICTIONARY = './custom_dictionary.txtt'

        # write a file
        with open(PATH_TO_CUSTOM_DICTIONARY, 'w', encoding='utf-8') as f:
            f.write('อะเฟเซีย\\nAphasia\\nผิด\\nปกติ')

        text = "อะเฟเซีย (Aphasia) เป็นอาการผิดปกติของการพูด"

        # initiate an object from file with `attacut` as tokenizer
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
        custom_dict: Union[Trie, Iterable[str], str] = [],
        engine: str = "newmm",
        keep_whitespace: bool = True,
        join_broken_num: bool = True,
    ):
        """
        Initialize tokenizer object.

        :param str custom_dict: a file path, a list of vocaburaies* to be
                    used to create a trie, or an instantiated
                    :class:`pythainlp.util.Trie` object.
        :param str engine: choose between different options of tokenizer engines
                            (i.e.  *newmm*, *mm*, *longest*, *deepcut*)
        :param bool keep_whitespace: True to keep whitespace, a common mark
                                     for end of phrase in Thai
        """
        self.__trie_dict = Trie([])
        if custom_dict:
            self.__trie_dict = dict_trie(custom_dict)
        else:
            self.__trie_dict = DEFAULT_WORD_DICT_TRIE
        self.__engine = engine
        if self.__engine not in ["newmm", "mm", "longest", "deepcut"]:
            raise NotImplementedError(
                """
                The Tokenizer class is not support %s for custom tokenizer
                """
                % self.__engine
            )
        self.__keep_whitespace = keep_whitespace
        self.__join_broken_num = join_broken_num

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
            join_broken_num=self.__join_broken_num,
        )

    def set_tokenize_engine(self, engine: str) -> None:
        """
        Set the tokenizer's engine.

        :param str engine: choose between different options of tokenizer engines
                           (i.e. *newmm*, *mm*, *longest*, *deepcut*)
        """
        self.__engine = engine
