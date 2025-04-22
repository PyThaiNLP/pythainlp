# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2025 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
from typing import List, Union
from word2word import Word2word

support_list = set(['zh_tw',
 'el',
 'te',
 'hu',
 'eu',
 'ko',
 'ru',
 'lv',
 'bg',
 'sk',
 'vi',
 'gl',
 'et',
 'ta',
 'fa',
 'it',
 'ms',
 'id',
 'pt',
 'fr',
 'sr',
 'mk',
 'sv',
 'si',
 'en',
 'ka',
 'uk',
 'sl',
 'hi',
 'ca',
 'lt',
 'es',
 'no',
 'de',
 'he',
 'cs',
 'ze_zh',
 'fi',
 'pl',
 'tl',
 'is',
 'ze_en',
 'kk',
 'bn',
 'tr',
 'ur',
 'pt_br',
 'ar',
 'ro',
 'bs',
 'ml',
 'zh_cn',
 'da',
 'hr',
 'sq',
 'af',
 'eo',
 'nl',
 'ja',
 'th'])


def translate(word: str, src: str, target: str) -> Union[List[str], None]:
    """
    Word translate

    :param str word: text
    :param str src: src language
    :param str target: target language
    :return: return list word translate or None
    :rtype: Union[List[str], None]
    """
    if src not in support_list or target not in support_list:
        raise NotImplementedError(
            f"word2word doesn't support {src}-{target}."
        )
    elif src==target:
        return [word]
    _engine = Word2word(src, target)
    return _engine(word)