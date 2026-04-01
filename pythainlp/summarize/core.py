# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Text summarization and keyword extraction"""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional, cast

if TYPE_CHECKING:
    from collections.abc import Iterable

from pythainlp.summarize import (
    CPE_KMUTT_THAI_SENTENCE_SUM,
    DEFAULT_KEYWORD_EXTRACTION_ENGINE,
    DEFAULT_SUMMARIZE_ENGINE,
)
from pythainlp.summarize.freq import FrequencySummarizer
from pythainlp.tokenize import sent_tokenize


def summarize(
    text: str,
    n: int = 1,
    engine: str = DEFAULT_SUMMARIZE_ENGINE,
    tokenizer: str = "newmm",
) -> list[str]:
    """Summarizes text based on frequency of words.

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
    :rtype: list[str]

    **Options for engine**
        * *frequency* (default) - word frequency
        * *mt5* - mT5-small model
        * *mt5-small* - mT5-small model
        * *mt5-base* - mT5-base model
        * *mt5-large* - mT5-large model
        * *mt5-xl* - mT5-xl model
        * *mt5-xxl* - mT5-xxl model
        * *mt5-cpe-kmutt-thai-sentence-sum* - mT5 Thai sentence
          summarization by CPE KMUTT

    :Example:

        >>> from pythainlp.summarize import summarize  # doctest: +SKIP

        >>> text = '''  # doctest: +SKIP
        ...         ทำเนียบท่าช้าง หรือ วังถนนพระอาทิตย์
        ...         ตั้งอยู่บนถนนพระอาทิตย์ เขตพระนคร กรุงเทพมหานคร
        ...         เดิมเป็นบ้านของเจ้าพระยามหาโยธา (ทอเรียะ คชเสนี)
        ...         บุตรเจ้าพระยามหาโยธานราธิบดีศรีพิชัยณรงค์ (พญาเจ่ง)
        ...         ต้นสกุลคชเสนี เชื้อสายมอญ เจ้าพระยามหาโยธา (ทอเรีย)
        ...         เป็นปู่ของเจ้าจอมมารดากลิ่นในพระบาทสมเด็จพระจอมเกล้าเจ้าอยู่หัว
        ...         และเป็นมรดกตกทอดมาถึง พระเจ้าบรมวงศ์เธอ กรมพระนเรศรวรฤทธิ์
        ...         (พระองค์เจ้ากฤดาภินิหาร)
        ...         ต่อมาในรัชสมัยพระบาทสมเด็จพระจุลจอมเกล้าเจ้าอยู่หัวโปรดเกล้าฯ
        ...         ให้สร้างตำหนัก 2 ชั้น
        ...         เป็นที่ประทับของพระเจ้าบรมวงศ์เธอ
        ...         กรมพระนเรศวรฤทิธิ์และเจ้าจอมมารดา
        ...         ต่อมาเรียกอาคารหลักนี้ว่า ตำหนักเดิม
        ...     '''

        >>> summarize(text, n=1)  # doctest: +SKIP
        ['บุตรเจ้าพระยามหาโยธานราธิบดีศรีพิชัยณรงค์']

        >>> summarize(text, n=3)  # doctest: +SKIP
        ['บุตรเจ้าพระยามหาโยธานราธิบดีศรีพิชัยณรงค์',
        'เดิมเป็นบ้านของเจ้าพระยามหาโยธา',
        'เจ้าพระยามหาโยธา']

        >>> summarize(text, engine="mt5-small")  # doctest: +SKIP
        ['<extra_id_0> ท่าช้าง หรือ วังถนนพระอาทิตย์
        เขตพระนคร กรุงเทพมหานคร ฯลฯ ดังนี้:
        ที่อยู่ - ศิลปวัฒนธรรม']

        >>> text = "ถ้าพูดถึงขนมหวานในตำนานที่ชื่นใจที่สุดแล้วละก็ต้องไม่พ้น น้ำแข็งใส แน่ๆ เพราะว่าเป็นอะไรที่ชื่นใจสุดๆ"  # doctest: +SKIP
        >>> summarize(text, engine="mt5-cpe-kmutt-thai-sentence-sum")  # doctest: +SKIP
        ['น้ําแข็งใสเป็นอะไรที่ชื่นใจที่สุด']
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
        # sent_tokenize with str input returns list[str]
        sents = sent_tokenize(text, engine="whitespace+newline")[:n]  # type: ignore[assignment]

    return sents


def extract_keywords(
    text: str,
    keyphrase_ngram_range: tuple[int, int] = (1, 2),
    max_keywords: int = 5,
    min_df: int = 1,
    engine: str = DEFAULT_KEYWORD_EXTRACTION_ENGINE,
    tokenizer: str = "newmm",
    stop_words: Optional[Iterable[str]] = None,
) -> list[str]:
    """Return the most relevant keywords (and keyphrases) from a document.

    Each algorithm may produce completely different keywords,
    so choose the algorithm carefully.

    .. note::

        Calling :func:`extract_keywords` is expensive.
        For repeated use of KeyBERT (the default engine),
        creating a ``KeyBERT`` object directly is recommended.

    :param str text: text to extract keywords from
    :param tuple[int, int] keyphrase_ngram_range: token range for keywords.
        ``(1, 1)`` allows unigrams only (e.g. "เสา", "ไฟฟ้า");
        ``(1, 2)`` allows unigrams and bigrams
        (e.g. "เสา", "ไฟฟ้า", "เสาไฟฟ้า"). Default: ``(1, 2)``.
    :param int max_keywords: maximum number of keywords to return.
        Default: 5.
    :param int min_df: minimum term frequency to qualify as keyword.
        Default: 1.
    :param str engine: keyword extraction algorithm. Default: ``'keybert'``.
    :param str tokenizer: tokenizer engine name.
        See :func:`pythainlp.tokenize.word_tokenize` for options.
        Default: ``'newmm'``.
    :param stop_words: words to ignore. If ``None``,
        :func:`pythainlp.corpus.thai_stopwords` is used. Default: ``None``.
    :type stop_words: collections.abc.Iterable[str] or None

    :return: list of keywords
    :rtype: list[str]

    **Options for engine**
        * *keybert* (default) - KeyBERT keyword extraction
        * *frequency* - word frequency

    :Example:

        >>> from pythainlp.summarize import extract_keywords  # doctest: +SKIP

        >>> text = '''  # doctest: +SKIP
        ...     อาหาร หมายถึง ของแข็งหรือของเหลว
        ...     ที่กินหรือดื่มเข้าสู่ร่างกายแล้ว
        ...     จะทำให้เกิดพลังงานและความร้อนแก่ร่างกาย
        ...     ทำให้ร่างกายเจริญเติบโต
        ...     ซ่อมแซมส่วนที่สึกหรอ ควบคุมการเปลี่ยนแปลงต่างๆ ในร่างกาย
        ...     ช่วยทำให้อวัยวะต่างๆ ทำงานได้อย่างปกติ
        ...     อาหารจะต้องไม่มีพิษและไม่เกิดโทษต่อร่างกาย
        ... '''

        >>> keywords = extract_keywords(text)  # doctest: +SKIP

        ['อวัยวะต่างๆ',
        'ซ่อมแซมส่วน',
        'เจริญเติบโต',
        'ควบคุมการเปลี่ยนแปลง',
        'มีพิษ']

        >>> keywords = extract_keywords(text, max_keywords=10)  # doctest: +SKIP

        ['อวัยวะต่างๆ',
        'ซ่อมแซมส่วน',
        'เจริญเติบโต',
        'ควบคุมการเปลี่ยนแปลง',
        'มีพิษ',
        'ทำให้ร่างกาย',
        'ร่างกายเจริญเติบโต',
        'จะทำให้เกิด',
        'มีพิษและ',
        'เกิดโทษ']

    """

    def rank_by_frequency(
        text: str,
        max_keywords: int = 5,
        min_df: int = 5,
        tokenizer: str = "newmm",
        stop_words: Optional[Iterable[str]] = None,
    ) -> list[str]:
        from pythainlp.tokenize import word_tokenize
        from pythainlp.util.keywords import rank

        tokens = word_tokenize(text, engine=tokenizer, keep_whitespace=False)

        use_custom_stop_words = stop_words is not None

        if use_custom_stop_words and stop_words is not None:
            tokens = [token for token in tokens if token not in stop_words]

        word_rank = rank(tokens, exclude_stopwords=not use_custom_stop_words)

        if word_rank is None:
            return []

        keywords = [
            kw
            for kw, cnt in word_rank.most_common(max_keywords)
            if cnt >= min_df
        ]

        return keywords

    engines = ["keybert", "frequency"]

    if engine == "keybert":
        from .keybert import KeyBERT

        keywords = cast(
            "list[str]",
            KeyBERT().extract_keywords(
                text,
                keyphrase_ngram_range=keyphrase_ngram_range,
                max_keywords=max_keywords,
                min_df=min_df,
                tokenizer=tokenizer,
                return_similarity=False,
                stop_words=stop_words,
            ),
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
