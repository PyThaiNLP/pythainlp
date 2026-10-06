# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

from typing import Optional, cast

from word2word import Word2word

support_list: set[str] = {
    "af",
    "ar",
    "bg",
    "bn",
    "bs",
    "ca",
    "cs",
    "da",
    "de",
    "el",
    "en",
    "eo",
    "es",
    "et",
    "eu",
    "fa",
    "fi",
    "fr",
    "gl",
    "he",
    "hi",
    "hr",
    "hu",
    "id",
    "is",
    "it",
    "ja",
    "ka",
    "kk",
    "ko",
    "lt",
    "lv",
    "mk",
    "ml",
    "ms",
    "nl",
    "no",
    "pl",
    "pt",
    "pt_br",
    "ro",
    "ru",
    "si",
    "sk",
    "sl",
    "sq",
    "sr",
    "sv",
    "ta",
    "te",
    "th",
    "tl",
    "tr",
    "uk",
    "ur",
    "vi",
    "ze_en",
    "ze_zh",
    "zh_cn",
    "zh_tw",
}


def translate(word: str, src: str, target: str) -> Optional[list[str]]:
    """Word translate

    :param str word: text
    :param str src: src language
    :param str target: target language
    :return: return list word translate or None
    :rtype: Union[List[str], None]
    """
    if src not in support_list or target not in support_list:
        raise NotImplementedError(f"word2word doesn't support {src}-{target}.")
    if src == target:
        return [word]
    _engine = Word2word(src, target)
    return cast("Optional[list[str]]", _engine(word))
