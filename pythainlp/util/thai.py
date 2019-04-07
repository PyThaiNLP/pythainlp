# -*- coding: utf-8 -*-
"""
Check if it is Thai text
"""
import string


def isthaichar(ch: str) -> bool:
    """
    Check if a character is Thai
    เป็นอักษรไทยหรือไม่

    :param str ch: input character
    :return: True or False
    """
    ch_val = ord(ch)
    if ch_val >= 3584 and ch_val <= 3711:
        return True
    return False


def isthai(word: str, ignore_chars: str = ".") -> bool:
    """
    Check if all character is Thai
    เป็นคำที่มีแต่อักษรไทยหรือไม่

    :param str word: input text
    :param str ignore_chars: characters to be ignored (i.e. will be considered as Thai)
    :return: True or False
    """
    if not ignore_chars:
        ignore_chars = ""

    for ch in word:
        if ch not in ignore_chars and not isthaichar(ch):
            return False
    return True


def countthai(
    text: str,
    ignore_chars: str = string.whitespace + string.digits + string.punctuation,
) -> float:
    """
    :param str text: input text
    :return: float, proportion of characters in the text that is Thai character
    """
    if not text:
        return 0

    if not ignore_chars:
        ignore_chars = ""

    text_len = len(text)
    num_isthai = 0
    num_ignore = 0

    for ch in text:
        if ch in ignore_chars:
            num_ignore += 1
        elif isthaichar(ch):
            num_isthai += 1

    return (num_isthai / (text_len - num_ignore)) * 100
