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
try:
    from tltk.nlp import g2p, th2ipa, th2roman
except ImportError:
    raise ImportError("Not found tltk! Please install tltk by pip install tltk")


def romanize(text: str) -> str:
    """
    Transliterating thai text to the Latin alphabet with tltk.

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
