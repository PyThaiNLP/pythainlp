# -*- coding: utf-8 -*-
"""
Summarization
"""

from typing import List

from pythainlp.tokenize import sent_tokenize

from .freq import FrequencySummarizer


def summarize(
    text: str, n: int, engine: str = "frequency", tokenizer: str = "newmm"
) -> List[str]:
    """
    Thai text summarization

    :param str text: text to be summarized
    :param int n: number of sentences to be included in the summary
        :Example:

            >>> from pythainlp.summarize import summarize

            >>> text = '''
                    ทำเนียบท่าช้าง หรือ วังถนนพระอาทิตย์ ตั้งอยู่บนถนนพระอาทิตย์ เขตพระนคร กรุงเทพมหานคร 
                    เดิมเป็นบ้านของเจ้าพระยามหาโยธา (ทอเรียะ คชเสนี)
                    บุตรเจ้าพระยามหาโยธานราธิบดีศรีพิชัยณรงค์ (พญาเจ่ง) 
                    ต้นสกุลคชเสนี เชื้อสายมอญ เจ้าพระยามหาโยธา (ทอเรีย)
                    เป็นปู่ของเจ้าจอมมารดากลิ่นในพระบาทสมเด็จพระจอมเกล้าเจ้าอยู่หัว 
                    และเป็นมรดกตกทอดมาถึง พระเจ้าบรมวงศ์เธอ กรมพระนเรศรวรฤทธิ์ (พระองค์เจ้ากฤดาภินิหาร) 
                    ต่อมาในรัชสมัยพระบาทสมเด็จพระจุลจอมเกล้าเจ้าอยู่หัวโปรดเกล้าฯ ให้สร้างตำหนัก 2 ชั้น 
                    เป็นที่ประทับของพระเจ้าบรมวงศ์เธอ กรมพระนเรศวรฤทิธิ์และเจ้าจอมมารดา 
                    ต่อมาเรียกอาคารหลักนี้ว่า ตำหนักเดิม
                '''
            >>>
            >>> summarize(text, n=1)
            ['บุตรเจ้าพระยามหาโยธานราธิบดีศรีพิชัยณรงค์']
            >>>
            >>> summarize(text, n=3)
            ['บุตรเจ้าพระยามหาโยธานราธิบดีศรีพิชัยณรงค์', 
             'เดิมเป็นบ้านของเจ้าพระยามหาโยธา', 
             'เจ้าพระยามหาโยธา']
            >>>
            >>> summarize(text, n=3, engine="deepcut")
            ['ทำเนียบท่าช้าง', 'หรือ', 'วังถนนพระอาทิตย์']
    """
    sents = []

    if engine == "frequency":
        sents = FrequencySummarizer().summarize(text, n, tokenizer)
    else:  # if engine not found, return first n sentences
        sents = sent_tokenize(text)[:n]

    return sents
