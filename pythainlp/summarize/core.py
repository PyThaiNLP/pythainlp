# -*- coding: utf-8 -*-
"""
Text summarization
"""


from typing import List

from pythainlp.summarize import DEFAULT_SUMMARIZE_ENGINE
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

        Under the hood, this function first tokenize sentence from the given
        text with :func:`pythainlp.tokenize.sent_tokenize`.
        Then, computes frequencies of tokenized words
        (with :func:`pythainlp.tokenize.word_tokenize`) in all sentences
        and normalized with maximum word frequency. The words with normalized
        frequncy that are less than 0.1 or greater than 0.9 will be
        filtered out from frequency dictionary. Finally, it picks *n* sentences
        with highest sum of normalized frequency from all words
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
    """
    if not text or not isinstance(text, str):
        return []
    sents = []

    if engine == DEFAULT_SUMMARIZE_ENGINE:
        sents = FrequencySummarizer().summarize(text, n, tokenizer)
    elif engine.startswith('mt5-') or engine == "mt5":
        size = engine.replace('mt5-', '')
        from .mt5 import mT5Summarizer
        sents = mT5Summarizer(model_size=size).summarize(text)
    else:  # if engine not found, return first n sentences
        sents = sent_tokenize(text, engine="whitespace+newline")[:n]

    return sents
