# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

import itertools
import logging


class Word2VecAug:
    def __init__(
        self, model: str, tokenize: object, type: str = "file"
    ) -> None:
        """:param str model: path of model
        :param object tokenize: tokenize function
        :param str type: model type (file, binary)
        """
        import gensim.models.keyedvectors as word2vec

        self.tokenizer = tokenize

        if type == "file" or type == "binary":
            # Temporarily suppress gensim warnings about duplicate words
            gensim_logger = logging.getLogger("gensim.models.keyedvectors")
            original_level = gensim_logger.getEffectiveLevel()
            gensim_logger.setLevel(logging.ERROR)

            try:
                if type == "file":
                    self.model = word2vec.KeyedVectors.load_word2vec_format(
                        model
                    )
                else:  # type == "binary"
                    self.model = word2vec.KeyedVectors.load_word2vec_format(
                        model, binary=True, unicode_errors="ignore"
                    )
            finally:
                # Restore original logging level
                gensim_logger.setLevel(original_level)
        else:
            self.model = model

        self.dict_wv = list(self.model.key_to_index.keys())

    def modify_sent(self, sent: str, p: float = 0.7) -> list[list[str]]:
        """:param str sent: text of sentence
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
    ) -> list[tuple[str]]:
        """:param str sentence: text of sentence
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
