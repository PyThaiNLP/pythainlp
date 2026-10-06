# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Augment Thai text using fastText."""

from __future__ import annotations

import itertools
from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from gensim.models import FastText
    from gensim.models.keyedvectors import KeyedVectors

from pythainlp.tokenize import word_tokenize


class FastTextAug:
    """
    Augment Thai text using fastText.

    :param str model_path: path to the model file
    """

    model: Union[FastText, KeyedVectors]
    dict_wv: list[str]
    sentence: list[str]
    list_synonym: list[list[str]]

    def __init__(self, model_path: str) -> None:
        """
        Load the fastText model.

        :param str model_path: path to the model file
        """
        from gensim.models.fasttext import FastText as FastText_gensim
        from gensim.models.keyedvectors import KeyedVectors

        if model_path.endswith(".bin"):
            self.model: Union["FastText", "KeyedVectors"] = (
                FastText_gensim.load_facebook_vectors(model_path)
            )
        elif model_path.endswith(".vec"):
            self.model = KeyedVectors.load_word2vec_format(model_path)
        else:
            self.model = FastText_gensim.load(model_path)
        self.dict_wv: list[str] = list(self.model.key_to_index.keys())

    def tokenize(self, text: str) -> list[str]:
        """
        Tokenize Thai text into a list of words.

        :param str text: Thai text to tokenize

        :return: list of words
        :rtype: list[str]
        """
        return word_tokenize(text, engine="icu")

    def modify_sent(self, sent: list[str], p: float = 0.7) -> list[list[str]]:
        """
        Find replacement words for each word in a sentence.

        :param list[str] sent: list of words
        :param float p: minimum similarity score of a replacement word
        :return: list of replacement words for each word, which is the
            word itself if there is no replacement
        :rtype: list[list[str]]
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
    ) -> list[tuple[str, ...]]:
        """
        Augment text using fastText.

        You may want to download the Thai model
        from https://fasttext.cc/docs/en/crawl-vectors.html.

        :param str sentence: Thai text to augment
        :param int n_sent: number of augmented sentences
        :param float p: minimum similarity score of a replacement word

        :return: list of augmented sentences, each a tuple of words
        :rtype: list[tuple[str, ...]]
        """
        self.sentence: list[str] = self.tokenize(sentence)
        self.list_synonym: list[list[str]] = self.modify_sent(
            self.sentence, p=p
        )
        new_sentences = []
        for x in list(itertools.product(*self.list_synonym))[0:n_sent]:
            new_sentences.append(x)
        return new_sentences
