# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Romanization and phoneme conversion of Thai text, using pure-Python TLTK."""

from __future__ import annotations

from pythainlp.transliterate._tltk_g2p import (
    tltk_g2p_native,
    tltk_th2ipa_native,
    tltk_th2roman_native,
)


def romanize(text: str) -> str:
    """
    Romanize Thai text to the Latin alphabet using tltk.

    :param str text: Thai text to be romanized
    :return: text rendered in the Latin alphabet
    :rtype: str
    """
    # Replace ฅ with ค to avoid KeyError in tltk (out-of-vocabulary issue)
    text = text.replace("ฅ", "ค")
    _temp = tltk_th2roman_native(text)
    return _temp[: _temp.rfind(" <s/>")].replace("<s/>", "")


def tltk_g2p(text: str) -> str:
    """
    Convert Thai text to phonemes using tltk.

    :param str text: Thai text to be converted
    :return: phonemes of the text
    :rtype: str
    """
    # Replace ฅ with ค to avoid KeyError in tltk (out-of-vocabulary issue)
    text = text.replace("ฅ", "ค")
    _temp = (
        tltk_g2p_native(text).split("<tr/>")[1].replace("|<s/>", "").replace("|", " ")
    )
    return _temp.replace("<s/>", "")


def tltk_ipa(text: str) -> str:
    """
    Convert Thai text to IPA using tltk.

    :param str text: Thai text to be converted
    :return: IPA text
    :rtype: str
    """
    # Replace ฅ with ค to avoid KeyError in tltk (out-of-vocabulary issue)
    text = text.replace("ฅ", "ค")
    _temp = tltk_th2ipa_native(text)
    return _temp[: _temp.rfind(" <s/>")].replace("<s/>", "")
