# -*- coding: utf-8 -*-
"""
Check if it is Thai text
"""


def is_thaichar(ch):  # เป็นอักษรไทยหรือไม่
    """
    Check if character is Thai

    :param str ch: input character
    :return: True or False
    """
    ch_val = ord(ch)
    if ch_val >= 3584 and ch_val <= 3711:
        return True
    return False


def is_thaiword(word):  # เป็นคำที่มีแต่อักษรไทยหรือไม่
    """
    Check if all character is Thai

    :param str word: input text
    :return: True or False
    """
    for ch in word:
        if ch != "." and not is_thaichar(ch):
            return False
    return True


def is_thai(text, check_all=False):
    """
    :param str text: input string or list of strings
    :param bool check_all: checks all character or not

    :return: A dictionary with the first value as proportional of text that is Thai, and the second value being a tuple of all characters, along with true or false.
    """
    isthais = []
    num_isthai = 0

    for ch in text:
        ch_val = ord(ch)
        if ch_val >= 3584 and ch_val <= 3711:
            num_isthai += 1
            if check_all:
                isthais.append(True)
        else:
            if check_all:
                isthais.append(False)
    thai_percent = (num_isthai / len(text)) * 100

    if check_all:
        chars = list(text)
        isthai_pairs = tuple(zip(chars, isthais))
        data = {"thai": thai_percent, "check_all": isthai_pairs}
    else:
        data = {"thai": thai_percent}

    return data
