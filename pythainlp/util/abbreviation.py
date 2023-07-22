# -*- coding: utf-8 -*-
# Copyright (C) 2016-2023 PyThaiNLP Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Thai abbreviation tools
"""
from typing import List, Tuple, Union


def abbreviation_to_full_text(text: str, top_k: int=2) -> List[Tuple[str, Union[float, None]]]:
    """
    This function convert Thai text (with abbreviation) to full text.

    This function use KhamYo for handles abbreviations.
    See more `KhamYo <https://github.com/wannaphong/KhamYo>`_.

    :param str text: Thai text
    :param int top_k: Top K
    :return: Thai full text that handles abbreviations as full text and cos scores (original text -  modified text).
    :rtype: List[Tuple[str, Union[float, None]]]

    :Example:
    ::

        from pythainlp.util import abbreviation_to_full_text

        text = "รร.ของเราน่าอยู่"

        abbreviation_to_full_text(text)
        # output: [
        # ('โรงเรียนของเราน่าอยู่', tensor(0.3734)), 
        # ('โรงแรมของเราน่าอยู่', tensor(0.2438))
        # ]
    """
    try:
        from khamyo import replace as _replace
    except ImportError:
        raise ImportError(
            """
            This funtion need to use khamyo.
            You can install by pip install khamyo or 
            pip install pythainlp[abbreviation].
            """
        )
    return _replace(text, top_k=top_k)