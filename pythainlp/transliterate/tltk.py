# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

from typing import cast

try:
    from tltk.nlp import g2p, th2ipa, th2roman
except ImportError as e:
    raise ImportError(
        "tltk is not installed. Install it with: pip install tltk"
    ) from e


def romanize(text: str) -> str:
    """Transliterating thai text to the Latin alphabet using tltk.

    :param str text: Thai text to be romanized
    :return: A string of Thai words rendered in the Latin alphabet.
    :rtype: str
    """
    # Replace ฅ with ค to avoid KeyError in tltk (out-of-vocabulary issue)
    text = text.replace("ฅ", "ค")
    _temp = cast(str, th2roman(text))
    return _temp[: _temp.rfind(" <s/>")].replace("<s/>", "")


def tltk_g2p(text: str) -> str:
    # Replace ฅ with ค to avoid KeyError in tltk (out-of-vocabulary issue)
    text = text.replace("ฅ", "ค")
    _temp = (
        cast(str, g2p(text))
        .split("<tr/>")[1]
        .replace("|<s/>", "")
        .replace("|", " ")
    )
    return _temp.replace("<s/>", "")


def tltk_ipa(text: str) -> str:
    # Replace ฅ with ค to avoid KeyError in tltk (out-of-vocabulary issue)
    text = text.replace("ฅ", "ค")
    _temp = cast(str, th2ipa(text))
    return _temp[: _temp.rfind(" <s/>")].replace("<s/>", "")
