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
nercut 0.2

Dictionary-based maximal matching word segmentation, constrained with
Thai Character Cluster (TCC) boundaries, and combining tokens that are
parts of the same named-entity.

Code by Wannaphong Phatthiyaphaibun
"""
from typing import Iterable, List

from pythainlp.tag.named_entity import NER

_thainer = NER(engine="thainer")


def segment(
    text: str,
    taglist: Iterable[str] = [
        "ORGANIZATION",
        "PERSON",
        "PHONE",
        "EMAIL",
        "DATE",
        "TIME",
    ],
    tagger=_thainer,
) -> List[str]:
    """
    Dictionary-based maximal matching word segmentation, constrained with
    Thai Character Cluster (TCC) boundaries, and combining tokens that are
    parts of the same named-entity.

    :param str text: text to be tokenized to words
    :parm list taglist: a list of named-entity tags to be used
    :parm class tagger: ner tagger engine
    :return: list of words, tokenized from the text
    """
    if not isinstance(text, str):
        return []

    tagged_words = tagger.tag(text, pos=False)

    words = []
    combining_word = ""
    for idx, (curr_word, curr_tag) in enumerate(tagged_words):
        if curr_tag != "O":
            tag = curr_tag[2:]
        else:
            tag = "O"

        if curr_tag.startswith("B-") and tag in taglist:
            combining_word = curr_word
        elif (
            curr_tag.startswith("I-")
            and combining_word != ""
            and tag in taglist
        ):
            combining_word += curr_word
        elif curr_tag == "O" and combining_word != "":
            words.append(combining_word)
            combining_word = ""
            words.append(curr_word)
        else:  # if tag is O
            combining_word = ""
            words.append(curr_word)
        if idx + 1 == len(tagged_words):
            if curr_tag.startswith("B-") and combining_word != "":
                words.append(combining_word)
            elif curr_tag.startswith("I-") and combining_word != "":
                words.append(combining_word)
            else:
                pass

    return words
