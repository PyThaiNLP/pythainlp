# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
from pythainlp.transliterate import pronunciate
from pythainlp import thai_consonants

_list_consonants = list(thai_consonants.replace("ห", ""))


def puan(word: str, show_pronunciation: bool = True) -> str:
    """
    Thai Spoonerism

    This function converts Thai word to spoonerism word.

    :param str word: Thai word to be spoonerized
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
    word = pronunciate(word, engine="w2p")
    _list_char = []
    _list_pron = word.split("-")
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
            elif "ห" == j and "หฺ" not in i and len(i) == 2:
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
        _list_w.append(
            list_w_char[1][0].replace(list_w_char[1][1], list_w_char[2][1], 1)
        )
    else:  # > 3 syllables
        _list_w.append(
            _list_pron[0].replace(list_w_char[0][1], list_w_char[-1][1], 1)
        )
        for i in range(1, len(list_w_char) - 1):
            _list_w.append(_list_pron[i])
        _list_w.append(
            _list_pron[-1].replace(list_w_char[-1][1], list_w_char[0][1], 1)
        )
    if not show_pronunciation:
        _list_w = [i.replace("หฺ", "").replace("ฺ", "") for i in _list_w]
    return _mix_list.join(_list_w)
