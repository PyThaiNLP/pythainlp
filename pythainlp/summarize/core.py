# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
"""
Text summarization and keyword extraction
"""

from typing import List, Iterable, Optional, Tuple

from pythainlp.summarize import (
    DEFAULT_SUMMARIZE_ENGINE,
    CPE_KMUTT_THAI_SENTENCE_SUM,
    DEFAULT_KEYWORD_EXTRACTION_ENGINE,
)
from pythainlp.summarize.freq import FrequencySummarizer
from pythainlp.tokenize import sent_tokenize


def summarize(
    text: str,
    n: int = 1,
    engine: str = DEFAULT_SUMMARIZE_ENGINE,
    tokenizer: str = "newmm",
) -> List[str]:
    """
    This function summarizes text based on frequency of words.

    Under the hood, this function first tokenizes sentences from the given
    text with :func:`pythainlp.tokenize.sent_tokenize`.
    Then, it computes frequencies of tokenized words
    (with :func:`pythainlp.tokenize.word_tokenize`) in all sentences
    and normalizes them with maximum word frequency. The words with normalized
    frequencies that are less than 0.1 or greater than 0.9 will be
    filtered out from frequency dictionary. Finally, it picks *n* sentences
    with highest sum of normalized frequency from all words which are
    in the sentence and also appear in the frequency dictionary.

    :param str text: text to be summarized
    :param int n: number of sentences to be included in the summary
                  By default, n is *1* (effective for frequency engine only)
    :param str engine: text summarization engine (By default: *frequency*).
    :param str tokenizer: word tokenizer engine name (refer to
                          :func:`pythainlp.tokenize.word_tokenize`).
                          By default, tokenizer is *newmm*
                          (effective for frequency engine only)

    :return: list of selected sentences
    **Options for engine**
        * *frequency* (default) - frequency of words
        * *mt5* - mT5-small model
        * *mt5-small* - mT5-small model
        * *mt5-base* - mT5-base model
        * *mt5-large* - mT5-large model
        * *mt5-xl* - mT5-xl model
        * *mt5-xxl* - mT5-xxl model
        * *mt5-cpe-kmutt-thai-sentence-sum* - mT5 Thai sentence summarization by CPE KMUTT

    :Example:
    ::

        from pythainlp.summarize import summarize

        text = '''
                ทำเนียบท่าช้าง หรือ วังถนนพระอาทิตย์
                ตั้งอยู่บนถนนพระอาทิตย์ เขตพระนคร กรุงเทพมหานคร
                เดิมเป็นบ้านของเจ้าพระยามหาโยธา (ทอเรียะ คชเสนี)
                บุตรเจ้าพระยามหาโยธานราธิบดีศรีพิชัยณรงค์ (พญาเจ่ง)
                ต้นสกุลคชเสนี เชื้อสายมอญ เจ้าพระยามหาโยธา (ทอเรีย)
                เป็นปู่ของเจ้าจอมมารดากลิ่นในพระบาทสมเด็จพระจอมเกล้าเจ้าอยู่หัว
                และเป็นมรดกตกทอดมาถึง พระเจ้าบรมวงศ์เธอ กรมพระนเรศรวรฤทธิ์
                (พระองค์เจ้ากฤดาภินิหาร)
                ต่อมาในรัชสมัยพระบาทสมเด็จพระจุลจอมเกล้าเจ้าอยู่หัวโปรดเกล้าฯ
                ให้สร้างตำหนัก 2 ชั้น
                เป็นที่ประทับของพระเจ้าบรมวงศ์เธอ
                กรมพระนเรศวรฤทิธิ์และเจ้าจอมมารดา
                ต่อมาเรียกอาคารหลักนี้ว่า ตำหนักเดิม
            '''

        summarize(text, n=1)
        # output: ['บุตรเจ้าพระยามหาโยธานราธิบดีศรีพิชัยณรงค์']

        summarize(text, n=3)
        # output: ['บุตรเจ้าพระยามหาโยธานราธิบดีศรีพิชัยณรงค์',
        # 'เดิมเป็นบ้านของเจ้าพระยามหาโยธา',
        # 'เจ้าพระยามหาโยธา']

        summarize(text, engine="mt5-small")
        # output: ['<extra_id_0> ท่าช้าง หรือ วังถนนพระอาทิตย์
        # เขตพระนคร กรุงเทพมหานคร ฯลฯ ดังนี้:
        # ที่อยู่ - ศิลปวัฒนธรรม']

        text = "ถ้าพูดถึงขนมหวานในตำนานที่ชื่นใจที่สุดแล้วละก็ต้องไม่พ้น น้ำแข็งใส แน่ๆ เพราะว่าเป็นอะไรที่ชื่นใจสุดๆ"
        summarize(text, engine="mt5-cpe-kmutt-thai-sentence-sum")
        # output: ['น้ําแข็งใสเป็นอะไรที่ชื่นใจที่สุด']
    """
    if not text or not isinstance(text, str):
        return []
    sents = []

    if engine == DEFAULT_SUMMARIZE_ENGINE:
        sents = FrequencySummarizer().summarize(text, n, tokenizer)
    elif engine == CPE_KMUTT_THAI_SENTENCE_SUM:
        from .mt5 import mT5Summarizer

        sents = mT5Summarizer(
            pretrained_mt5_model_name=CPE_KMUTT_THAI_SENTENCE_SUM, min_length=5
        ).summarize(text)
    elif engine.startswith("mt5-") or engine == "mt5":
        size = engine.replace("mt5-", "")
        from .mt5 import mT5Summarizer

        sents = mT5Summarizer(model_size=size).summarize(text)
    else:  # if engine not found, return first n sentences
        sents = sent_tokenize(text, engine="whitespace+newline")[:n]

    return sents


def extract_keywords(
    text: str,
    keyphrase_ngram_range: Tuple[int, int] = (1, 2),
    max_keywords: int = 5,
    min_df: int = 1,
    engine: str = DEFAULT_KEYWORD_EXTRACTION_ENGINE,
    tokenizer: str = "newmm",
    stop_words: Optional[Iterable[str]] = None,
) -> List[str]:
    """
    This function returns most-relevant keywords (and/or keyphrases) from the input document.
    Each algorithm may produce completely different keywords from each other,
    so please be careful when choosing the algorithm.

    *Note*: Calling :func: `extract_keywords()` is expensive. For repetitive use of KeyBERT (the default engine),
    creating KeyBERT object is highly recommended.

    :param str text: text to be summarized
    :param Tuple[int, int] keyphrase_ngram_range: Number of token units to be defined as keyword.
                            The token unit varies w.r.t. `tokenizer_engine`.
                            For instance, (1, 1) means each token (unigram) can be a keyword (e.g. "เสา", "ไฟฟ้า"),
                            (1, 2) means one and two consecutive tokens (unigram and bigram) can be keywords
                            (e.g. "เสา", "ไฟฟ้า", "เสาไฟฟ้า")  (default: (1, 2))
    :param int max_keywords: Number of maximum keywords to be returned. (default: 5)
    :param int min_df: Minimum frequency required to be a keyword. (default: 1)
    :param str engine: Name of algorithm to use for keyword extraction. (default: 'keybert')
    :param str tokenizer: Name of tokenizer engine to use.
                            Refer to options in :func: `pythainlp.tokenize.word_tokenizer() (default: 'newmm')
    :param Optional[Iterable[str]] stop_words: A list of stop words (a.k.a words to be ignored).
                            If not specified, :func:`pythainlp.corpus.thai_stopwords` is used. (default: None)

    :return: list of keywords

    **Options for engine**
        * *keybert* (default) - KeyBERT keyword extraction algorithm
        * *frequency* - frequency of words

    :Example:
    ::

        from pythainlp.summarize import extract_keywords

        text = '''
            อาหาร หมายถึง ของแข็งหรือของเหลว
            ที่กินหรือดื่มเข้าสู่ร่างกายแล้ว
            จะทำให้เกิดพลังงานและความร้อนแก่ร่างกาย
            ทำให้ร่างกายเจริญเติบโต
            ซ่อมแซมส่วนที่สึกหรอ ควบคุมการเปลี่ยนแปลงต่างๆ ในร่างกาย
            ช่วยทำให้อวัยวะต่างๆ ทำงานได้อย่างปกติ
            อาหารจะต้องไม่มีพิษและไม่เกิดโทษต่อร่างกาย
        '''

        keywords = extract_keywords(text)

        # output: ['อวัยวะต่างๆ',
        # 'ซ่อมแซมส่วน',
        # 'เจริญเติบโต',
        # 'ควบคุมการเปลี่ยนแปลง',
        # 'มีพิษ']

        keywords = extract_keywords(text, max_keywords=10)

        # output: ['อวัยวะต่างๆ',
        # 'ซ่อมแซมส่วน',
        # 'เจริญเติบโต',
        # 'ควบคุมการเปลี่ยนแปลง',
        # 'มีพิษ',
        # 'ทำให้ร่างกาย',
        # 'ร่างกายเจริญเติบโต',
        # 'จะทำให้เกิด',
        # 'มีพิษและ',
        # 'เกิดโทษ']

    """

    def rank_by_frequency(
        text: str,
        max_keywords: int = 5,
        min_df: int = 5,
        tokenizer: str = "newmm",
        stop_words: Optional[Iterable[str]] = None,
    ):
        from pythainlp.util.keywords import rank
        from pythainlp.tokenize import word_tokenize

        tokens = word_tokenize(text, engine=tokenizer, keep_whitespace=False)

        use_custom_stop_words = stop_words is not None

        if use_custom_stop_words:
            tokens = [token for token in tokens if token not in stop_words]

        word_rank = rank(tokens, exclude_stopwords=not use_custom_stop_words)

        keywords = [
            kw
            for kw, cnt in word_rank.most_common(max_keywords)
            if cnt >= min_df
        ]

        return keywords

    engines = ["keybert", "frequency"]

    if engine == "keybert":
        from .keybert import KeyBERT

        keywords = KeyBERT().extract_keywords(
            text,
            keyphrase_ngram_range=keyphrase_ngram_range,
            max_keywords=max_keywords,
            min_df=min_df,
            tokenizer=tokenizer,
            return_similarity=False,
            stop_words=stop_words,
        )
    elif engine == "frequency":
        return rank_by_frequency(
            text,
            max_keywords=max_keywords,
            min_df=min_df,
            tokenizer=tokenizer,
            stop_words=stop_words,
        )

    else:
        # currently not supported
        raise ValueError(
            f"Keyword extractor {repr(engine)} is currently not supported. "
            f"Use one of {engines}."
        )

    return keywords
