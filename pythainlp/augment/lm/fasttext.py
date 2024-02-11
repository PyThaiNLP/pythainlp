# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
import itertools
from typing import List, Tuple
from gensim.models.fasttext import FastText as FastText_gensim
from gensim.models.keyedvectors import KeyedVectors
from pythainlp.tokenize import word_tokenize


class FastTextAug:
    """
    Text Augment from fastText

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
        Thai text tokenization for fastText

        :param str text: Thai text

        :return: list of words
        :rtype: List[str]
        """
        return word_tokenize(text, engine="icu")

    def modify_sent(self, sent: str, p: float = 0.7) -> List[List[str]]:
        """
        :param str sent: text of sentence
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
        Text Augment from fastText

        You may want to download the Thai model
        from https://fasttext.cc/docs/en/crawl-vectors.html.

        :param str sentence: Thai sentence
        :param int n_sent: number of sentences
        :param float p: probability of word

        :return: list of synonyms
        :rtype: List[Tuple[str]]
        """
        self.sentence = self.tokenize(sentence)
        self.list_synonym = self.modify_sent(self.sentence, p=p)
        new_sentences = []
        for x in list(itertools.product(*self.list_synonym))[0:n_sent]:
            new_sentences.append(x)
        return new_sentences
