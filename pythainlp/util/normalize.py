# -*- coding: utf-8 -*-
"""
Text normalization
"""
import re

from pythainlp import thai_tonemarks

_NORMALIZE_RULE1 = [
    "ะ",
    "ั",
    "็",
    "า",
    "ิ",
    "ี",
    "ึ",
    "่",
    "ํ",
    "ุ",
    "ู",
    "ใ",
    "ไ",
    "โ",
    "ื",
    "่",
    "้",
    "๋",
    "๊",
    "ึ",
    "์",
    "๋",
    "ำ",
]  # เก็บพวกสระ วรรณยุกต์ที่ซ้ำกันแล้วมีปัญหา


_NORMALIZE_RULE2 = [
    ("เเ", "แ"),  # เ เ -> แ
    ("ํ(t)า", "\\1ำ"),
    ("ํา(t)", "\\1ำ"),
    ("([่-๋])([ัิ-ื])", "\\2\\1"),
    ("([่-๋])([ูุ])", "\\2\\1"),
    ("ำ([่-๋])", "\\1ำ"),
    ("(์)([ัิ-ู])", "\\2\\1"),
]  # เก็บพวก พิมพ์ลำดับผิดหรือผิดแป้นแต่กลับแสดงผลถูกต้อง ให้ไปเป็นแป้นที่ถูกต้อง เช่น เ + เ ไปเป็น แ


def normalize(text: str) -> str:
    """
    This function normalize thai text with normalizing rules as follows:

        * Remove redudant symbol of tones and vowels.
        * Subsitute ["เ", "เ"] to "แ".

    :param str text: thai text to be normalized
    :return: normalized Thai text according to the fules
    :rtype: str

    :Example:

        >>> from pythainlp.util import normalize
        >>>
        >>> normalize('สระะน้ำ')
        สระน้ำ
        >>> normalize('เเปลก')
        แปลก
        >>> normalize('นานาาา')
        นานา
    """
    for data in _NORMALIZE_RULE2:
        text = re.sub(data[0].replace("t", "[่้๊๋]"), data[1], text)
    for data in list(zip(_NORMALIZE_RULE1, _NORMALIZE_RULE1)):
        text = re.sub(data[0].replace("t", "[่้๊๋]") + "+", data[1], text)
    return text


def deletetone(text: str) -> str:
    """
    This function removes Thai tonemarks from the text.
    There are 4 tonemarks indicating 4 tones as follows:

        * Down tone (Thai: ไม้เอก  _่ )
        * Falling tone  (Thai: ไม้โท  _้ )
        * High tone (Thai: ไม้ตรี  ​_๊ )
        * Rising tone (Thai: ไม้จัตวา _๋ )

    :param str text: text in Thai language
    :return: text without Thai tonemarks
    :rtype: str

    :Example:

        >>> from pythainlp.util import deletetone
        >>>
        >>> deletetone(\\
            'สองพันหนึ่งร้อยสี่สิบเจ็ดล้านสี่แสนแปดหมื่นสามพันหกร้อยสี่สิบเจ็ด')
        สองพันหนึงรอยสีสิบเจ็ดลานสีแสนแปดหมืนสามพันหกรอยสีสิบเจ็ด
    """
    chars = [ch for ch in text if ch not in thai_tonemarks]
    return "".join(chars)
