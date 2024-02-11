# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
from typing import List, Tuple
import itertools


class Word2VecAug:
    def __init__(
        self, model: str, tokenize: object, type: str = "file"
    ) -> None:
        """
        :param str model: path of model
        :param object tokenize: tokenize function
        :param str type: model type (file, binary)
        """
        import gensim.models.keyedvectors as word2vec

        self.tokenizer = tokenize
        if type == "file":
            self.model = word2vec.KeyedVectors.load_word2vec_format(model)
        elif type == "binary":
            self.model = word2vec.KeyedVectors.load_word2vec_format(
                model, binary=True, unicode_errors="ignore"
            )
        else:
            self.model = model
        self.dict_wv = list(self.model.key_to_index.keys())

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
        :param str sentence: text of sentence
        :param int n_sent: maximum number of synonymous sentences
        :param int p: probability

        :return: list of synonyms
        :rtype: List[Tuple[str]]
        """
        self.sentence = self.tokenizer(sentence)
        self.list_synonym = self.modify_sent(self.sentence, p=p)
        new_sentences = []
        for x in list(itertools.product(*self.list_synonym))[0:n_sent]:
            new_sentences.append(x)
        return new_sentences
