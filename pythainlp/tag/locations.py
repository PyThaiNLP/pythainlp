# -*- coding: utf-8 -*-
"""
Recognizes locations in text
"""

from typing import List, Tuple

from pythainlp.corpus import provinces


def tag_provinces(tokens: List[str]) -> List[Tuple[str, str]]:
    """
    This function recognize Thailand provinces in text.

    :param list[str] tokens: a list of words
    :reutrn: a list of tuple indicating NER for `LOCATION` in IOB format
    :rtype: list[tuple[str, str]]

    :Example:

        >>> from pythainlp.tag import tag_provinces
        >>> text = ['หนองคาย', 'น่าอยู่']
        >>> tag_provinces(text)
        [('หนองคาย', 'B-LOCATION'), ('น่าอยู่', 'O')]
        >>>
        >>> text = ['อำเภอ', 'ฝาง','เป็น','ส่วน','หนึ่ง','ของ', 'จังหวัด', \\
            'เชียงใหม่']
        >>> tag_provinces(text)
        [('อำเภอ', 'O'), ('ฝาง', 'O'), ('เป็น', 'O'), ('ส่วน', 'O'),
        ('หนึ่ง', 'O'), ('ของ', 'O'), ('จังหวัด', 'O'),
        ('เชียงใหม่', 'B-LOCATION')]
    """
    province_list = provinces()

    output = []
    for token in tokens:
        if token in province_list:
            output.append((token, "B-LOCATION"))
        else:
            output.append((token, "O"))

    return output
