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
from typing import List, Tuple
from gensim.models.fasttext import FastText as FastText_gensim
from pythainlp.tokenize import word_tokenize
from gensim.models.keyedvectors import KeyedVectors
import itertools


class FastTextAug:
    """
    Text Augment from FastText

    :param str model_path: path of model file
    """

    def __init__(self, model_path: str):
        """
        :param str model_path: path of model file
        """
        if model_path.endswith(".bin"):
            self.model = FastText_gensim.load_facebook_vectors(model_path)
        elif model_path.endswith(".vec"):
            self.model = KeyedVectors.load_word2vec_format(model_path)
        else:
            self.model = FastText_gensim.load(model_path)
        self.dict_wv = list(self.model.key_to_index.keys())

    def tokenize(self, text: str) -> List[str]:
        """
        Thai text tokenize for fasttext

        :param str text: thai text

        :return: list of word
        :rtype: List[str]
        """
        return word_tokenize(text, engine="icu")

    def modify_sent(self, sent: str, p: float = 0.7) -> List[List[str]]:
        """
        :param str sent: text sentence
        :param float p: probability
        :rtype: List[List[str]]
        """
        list_sent_new = []
        for i in sent:
            if i in self.dict_wv:
                w = [j for j, v in self.model.most_similar(i) if v >= p]
                if w == []:
                    list_sent_new.append([i])
                else:
                    list_sent_new.append(w)
            else:
                list_sent_new.append([i])
        return list_sent_new

    def augment(
        self, sentence: str, n_sent: int = 1, p: float = 0.7
    ) -> List[Tuple[str]]:
        """
        Text Augment from FastText

        You wants to download thai model
        from https://fasttext.cc/docs/en/crawl-vectors.html.

        :param str sentence: thai sentence
        :param int n_sent: number sentence
        :param float p: Probability of word

        :return: list of synonyms
        :rtype: List[Tuple[str]]
        """
        self.sentence = self.tokenize(sentence)
        self.list_synonym = self.modify_sent(self.sentence, p=p)
        new_sentences = []
        for x in list(itertools.product(*self.list_synonym))[0:n_sent]:
            new_sentences.append(x)
        return new_sentences
