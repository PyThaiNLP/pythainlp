# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
try:
    from tltk.nlp import g2p, th2ipa, th2roman
except ImportError:
    raise ImportError("Not found tltk! Please install tltk by pip install tltk")


def romanize(text: str) -> str:
    """
    Transliterating thai text to the Latin alphabet using tltk.

    :param str text: Thai text to be romanized
    :return: A string of Thai words rendered in the Latin alphabet.
    :rtype: str
    """
    _temp = th2roman(text)
    return _temp[: _temp.rfind(" <s/>")].replace("<s/>", "")


def tltk_g2p(text: str) -> str:
    _temp = g2p(text).split("<tr/>")[1].replace("|<s/>", "").replace("|", " ")
    return _temp.replace("<s/>", "")


def tltk_ipa(text: str) -> str:
    _temp = th2ipa(text)
    return _temp[: _temp.rfind(" <s/>")].replace("<s/>", "")
