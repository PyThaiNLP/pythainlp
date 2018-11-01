# -*- coding: utf-8 -*-
"""
Recognizes locations in text
"""

from pythainlp.corpus import provinces


def tag_provinces(text_list):
    """
    tag_provinces(text_list)

    text_list คือ ข้อความภาษาไทยที่อยู่ใน list โดยผ่านการตัดคำมาแล้ว

    ใช้ tag จังหวัดในประเทศไทย

    ตัวอย่าง

    >>> d=['หนองคาย', 'น่าอยู่', 'นอกจากนี้', 'ยัง', 'มี', 'เชียงใหม่']
    >>> parsed_docs(d)
    ["[LOC : 'หนองคาย']", 'น่าอยู่', 'นอกจากนี้', 'ยัง', 'มี', "[LOC : 'เชียงใหม่']"]
    """
    i = 0
    while i < len(text_list):
        if text_list[i] in provinces():
            text_list[i] = "[LOC : '" + text_list[i] + "']"
        i += 1
    return text_list
