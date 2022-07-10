# -*- coding: utf-8 -*-
from tltk.nlp import g2p, th2ipa, th2roman


def romanize(text: str) -> str:
    """
    Transliterating thai text to the Latin alphabet with tltk.

    :param str text: Thai text to be romanized
    :return: A string of Thai words rendered in the Latin alphabet.
    :rtype: str
    """
    _temp = th2roman(text)
    return _temp[:_temp.rfind(" <s/>")].replace("<s/>", "")


def tltk_g2p(text: str) -> str:
    _temp = g2p(text).split("<tr/>")[1].replace("|<s/>", "").replace("|", " ")
    return _temp.replace("<s/>", "")


def tltk_ipa(text: str) -> str:
    _temp = th2ipa(text)
    return _temp[:_temp.rfind(" <s/>")].replace("<s/>", "")
