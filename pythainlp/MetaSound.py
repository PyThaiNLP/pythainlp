# -*- coding: utf-8 -*-
"""
MetaSound

References:
Snae & Brückner. (2009). Novel Phonetic Name Matching Algorithm with a Statistical
Ontology for Analysing Names Given in Accordance with Thai Astrology.
https://pdfs.semanticscholar.org/3983/963e87ddc6dfdbb291099aa3927a0e3e4ea6.pdf
"""
import re


def metasound(text):
    """
    Thai MetaSound

    :param str text: Thai text
    :return: MetaSound for Thai text
    **Example**::
        >>> from pythainlp.metasound import metasound
        >>> MetaSound('รัก')
        '501'
        >>> MetaSound('ลัก')
        '501'
    """
    count = len(text)
    sound = list(text)

    i = 0
    while i < count:
        if re.search("์", sound[i]):
            text[i - 1] = ""
            text[i] = ""
        i += 1

    i = 0
    while i < count:
        if re.search("[กขฃคฆฅ]", text[i]):
            sound[i] = "1"
        elif re.search("[จฉชฌซฐทฒดฎตสศษ]", text[i]):
            sound[i] = "2"
        elif re.search("[ฟฝพผภบป]", text[i]):
            sound[i] = "3"
        elif re.search("[ง]", text[i]):
            sound[i] = "4"
        elif re.search("[ลฬรนณฦญ]", text[i]):
            sound[i] = "5"
        elif re.search("[ม]", text[i]):
            sound[i] = "6"
        elif re.search("[ย]", text[i]):
            sound[i] = "7"
        elif re.search("[ว]", text[i]):
            sound[i] = "8"
        else:
            sound[i] = "0"
        i += 1

    return "".join(sound)


if __name__ == "__main__":
    print(metasound("รัก"))
    print(metasound("ลัก"))
    print(metasound("น้อง"))
