# -*- coding: utf-8 -*-
from pythainlp.transliterate import pronunciate
from pythainlp import thai_consonants

_list_consonants = list(thai_consonants.replace("ห", ""))


def puan(word: str, show_pronunciation: bool = True) -> str:
    """
    Thai Spoonerism

    This function covent Thai word to Thai spoonerism word.
    This function only supports words with 2 to 3 syllables.

    :param str word: Thai word to be spoonerism
    :param bool show_pronunciation: True (default) or False

    :return: A string of Thai spoonerism word.
    :rtype: str

    :Example:
    ::

        from pythainlp.transliterate import puan

        puan("นาริน")
        # output: 'นิน-รา'

        puan("นาริน", False)
        # output: 'นินรา'
    """
    _word = pronunciate(word, engine="w2p")
    _list_char = []
    _list_pron = _word.split('-')
    _mix_list = ""
    if len(_list_pron) == 1:
        return word
    if show_pronunciation:
        _mix_list = "-"
    for i in _list_pron:
        for j in i:
            if j in _list_consonants:
                _list_char.append(j)
                break
            elif "ห" in j and "หฺ" not in j:
                _list_char.append(j)
                break

    list_w_char = list(zip(_list_pron, _list_char))
    _list_w = []
    if len(list_w_char) == 2:
        _list_w.append(
            list_w_char[1][0].replace(list_w_char[1][1], list_w_char[0][1], 1)
        )
        _list_w.append(
            list_w_char[0][0].replace(list_w_char[0][1], list_w_char[1][1], 1)
        )
    elif len(list_w_char) == 3:
        _list_w.append(_list_pron[0])
        _list_w.append(
            list_w_char[2][0].replace(list_w_char[2][1], list_w_char[1][1], 1)
        )
        _list_w.append(list_w_char[1][0].replace(
            list_w_char[1][1], list_w_char[2][1], 1)
        )
    else: # > 3 syllables?
        return word
    return _mix_list.join(_list_w)
