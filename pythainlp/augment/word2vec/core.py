# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

import itertools
import logging
from typing import TYPE_CHECKING, Callable, Union

if TYPE_CHECKING:
    from gensim.models.keyedvectors import KeyedVectors


class _DuplicateWordFilter(logging.Filter):
    """Suppress gensim's 'duplicate word' warnings for word2vec files."""

    def filter(self, record: logging.LogRecord) -> bool:
        return "duplicate word" not in record.getMessage()


class Word2VecAug:
    tokenizer: Callable[[str], list[str]]
    model: "KeyedVectors"
    dict_wv: list[str]

    def __init__(
        self,
        model: Union[str, "KeyedVectors"],
        tokenize: Callable[[str], list[str]],
        type: str = "file",
    ) -> None:
        """:param Union[str, KeyedVectors] model: path of model or KeyedVectors instance
        :param Callable[[str], list[str]] tokenize: tokenize function
        :param str type: model type (file, binary, model)
        """
        import gensim.models.keyedvectors as word2vec

        self.tokenizer: Callable[[str], list[str]] = tokenize
        if type in ("file", "binary"):
            _filter = _DuplicateWordFilter()
            _gensim_kv_logger = logging.getLogger("gensim.models.keyedvectors")
            _gensim_kv_logger.addFilter(_filter)
            try:
                if type == "file":
                    self.model = word2vec.KeyedVectors.load_word2vec_format(
                        model
                    )
                else:
                    self.model = word2vec.KeyedVectors.load_word2vec_format(
                        model, binary=True, unicode_errors="ignore"
                    )
            finally:
                _gensim_kv_logger.removeFilter(_filter)
        else:
            self.model = model
        self.dict_wv: list[str] = list(self.model.key_to_index.keys())

    def modify_sent(self, sent: list[str], p: float = 0.7) -> list[list[str]]:
        """:param list[str] sent: list of tokens
        :param float p: probability
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
        """:param str sentence: text of sentence
        :param int n_sent: maximum number of synonymous sentences
        :param int p: probability

        :return: list of synonyms
        :rtype: list[tuple[str, ...]]
        """
        _sentence = self.tokenizer(sentence)
        _list_synonym = self.modify_sent(_sentence, p=p)
        new_sentences = []
        for x in list(itertools.product(*_list_synonym))[0:n_sent]:
            new_sentences.append(x)
        return new_sentences
