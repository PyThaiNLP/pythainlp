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
from typing import List, Tuple, Union
try:
    from tltk import nlp
except ImportError:
    raise ImportError("Not found tltk! Please install tltk by pip install tltk")
from pythainlp.tokenize import word_tokenize

nlp.pos_load()
nlp.ner_load()


def pos_tag(words: List[str], corpus: str = "tnc") -> List[Tuple[str, str]]:
    if corpus != "tnc":
        raise ValueError("tltk not support {0} corpus.".format(0))
    return nlp.pos_tag_wordlist(words)


def _post_process(text: str) -> str:
    return text.replace("<s/>", " ")


def get_ner(
    text: str, pos: bool = True, tag: bool = False
) -> Union[List[Tuple[str, str]], List[Tuple[str, str, str]], str]:
    """
    Named-entity recognizer from **TLTK**

    This function tags named-entitiy from text in IOB format.

    :param str text: text in Thai to be tagged
    :param bool pos: To include POS tags in the results (`True`) or
        exclude (`False`). The defualt value is `True`
    :param bool tag: output like html tag.
    :return: a list of tuple associated with tokenized word, NER tag,
        POS tag (if the parameter `pos` is specified as `True`),
        and output like html tag (if the parameter `tag` is
        specified as `True`).
        Otherwise, return a list of tuple associated with tokenized
        word and NER tag
    :rtype: Union[list[tuple[str, str]], list[tuple[str, str, str]]], str

    :Example:

        >>> from pythainlp.tag.tltk import get_ner
        >>> get_ner("เขาเรียนที่โรงเรียนนางรอง")
        [('เขา', 'PRON', 'O'),
        ('เรียน', 'VERB', 'O'),
        ('ที่', 'SCONJ', 'O'),
        ('โรงเรียน', 'NOUN', 'B-L'),
        ('นางรอง', 'VERB', 'I-L')]
        >>> get_ner("เขาเรียนที่โรงเรียนนางรอง", pos=False)
        [('เขา', 'O'),
        ('เรียน', 'O'),
        ('ที่', 'O'),
        ('โรงเรียน', 'B-L'),
        ('นางรอง', 'I-L')]
        >>> get_ner("เขาเรียนที่โรงเรียนนางรอง", tag=True)
        'เขาเรียนที่<L>โรงเรียนนางรอง</L>'
    """
    if not text:
        return []
    list_word = []
    for i in word_tokenize(text, engine="tltk"):
        if i == " ":
            i = "<s/>"
        list_word.append(i)
    _pos = nlp.pos_tag_wordlist(list_word)
    sent_ner = [
        (_post_process(word), pos, ner) for word, pos, ner in nlp.ner(_pos)
    ]
    if tag:
        temp = ""
        sent = ""
        for idx, (word, pos, ner) in enumerate(sent_ner):
            if ner.startswith("B-") and temp != "":
                sent += "</" + temp + ">"
                temp = ner[2:]
                sent += "<" + temp + ">"
            elif ner.startswith("B-"):
                temp = ner[2:]
                sent += "<" + temp + ">"
            elif ner == "O" and temp != "":
                sent += "</" + temp + ">"
                temp = ""
            sent += word

            if idx == len(sent_ner) - 1 and temp != "":
                sent += "</" + temp + ">"

        return sent
    if pos is False:
        return [(word, ner) for word, pos, ner in sent_ner]
    return sent_ner
