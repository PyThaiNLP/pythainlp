# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

from typing import Optional, Union, cast

from pythainlp.corpus import thai_wsd_dict
from pythainlp.tokenize import Tokenizer
from pythainlp.util.trie import Trie

_wsd_dict: dict[str, Union[list[str], list[list[str]]]] = thai_wsd_dict()
_mean_all: dict[str, list[str]] = {}

words: list[str] = cast("list[str]", _wsd_dict["word"])
meanings: list[list[str]] = cast("list[list[str]]", _wsd_dict["meaning"])
i_word: str
i_meanings: list[str]
for i_word, i_meanings in zip(words, meanings):
    _mean_all[i_word] = i_meanings

_all_word: set[str] = cast("set[str]", set(_mean_all.keys()))
_TRIE: Trie = Trie(_all_word)
_word_cut: Tokenizer = Tokenizer(custom_dict=_TRIE)

_MODEL_CACHE: dict[str, _SentenceTransformersModel] = {}


class _SentenceTransformersModel:
    def __init__(
        self,
        model: str = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2",
        device: str = "cpu",
    ) -> None:
        from sentence_transformers import SentenceTransformer

        self.device: str = device
        self.model_name: str = model
        self.model: "SentenceTransformer" = SentenceTransformer(
            self.model_name, device=self.device
        )

    def change_device(self, device: str) -> None:
        from sentence_transformers import SentenceTransformer

        self.device = device
        self.model = SentenceTransformer(self.model_name, device=self.device)

    def get_score(self, sentences1: str, sentences2: str) -> float:
        from sentence_transformers import util

        embedding_1 = self.model.encode(sentences1, convert_to_tensor=True)
        embedding_2 = self.model.encode(sentences2, convert_to_tensor=True)
        return float(
            1 - util.pytorch_cos_sim(embedding_1, embedding_2)[0][0].item()
        )


def get_sense(
    sentence: str,
    word: str,
    device: str = "cpu",
    custom_dict: Optional[dict[str, list[str]]] = None,
    custom_tokenizer: Tokenizer = _word_cut,
) -> list[tuple[str, float]]:
    """Get word sense from the sentence.
    Gets definition and distance from context in sentence.

    :param str sentence: Thai sentence
    :param str word: Thai word
    :param str device: device for running model on.
    :param Optional[dict[str, list[str]]] custom_dict: Thai dictionary in the
        form {"word": ["definition", ...]}
    :param Tokenizer custom_tokenizer: Tokenizer used to tokenize words in \
        sentence.
    :return: a list of definitions and distances (1 - cos_sim) or \
        an empty list (if word is not in the dictionary)
    :rtype: list[tuple[str, float]]

    We get the ideas from `Context-Aware Semantic Similarity Measurement for \
        Unsupervised Word Sense Disambiguation \
        <https://arxiv.org/abs/2305.03520>`_ to build get_sense function.

    Use Thai dictionary from wiktionary.
    See `thai_dict <https://pythainlp.org/pythainlp-corpus/thai_dict.html>`_.

    Use sentence transformers model from \
        `sentence-transformers/paraphrase-multilingual-mpnet-base-v2 \
        <https://huggingface.co/sentence-transformers/paraphrase-multilingual-mpnet-base-v2>`_ \
        for unsupervised word sense disambiguation.

    :Example:

        >>> from pythainlp.wsd import get_sense  # doctest: +SKIP
        >>> print(get_sense("เขากำลังอบขนมคุกกี้","คุกกี้"))  # doctest: +SKIP
        [('โปรแกรมคอมพิวเตอร์ใช้ในทางอินเทอร์เน็ตสำหรับเก็บข้อมูลของผู้ใช้งาน',
          0.0974416732788086),
         ('ชื่อขนมชนิดหนึ่งจำพวกขนมเค้ก แต่ทำเป็นชิ้นเล็ก ๆ แบน ๆ แล้วอบให้กรอบ',
          0.09319090843200684)]

        >>> print(get_sense("เว็บนี้ต้องการคุกกี้ในการทำงาน","คุกกี้"))  # doctest: +SKIP
        [('โปรแกรมคอมพิวเตอร์ใช้ในทางอินเทอร์เน็ตสำหรับเก็บข้อมูลของผู้ใช้งาน',
          0.1005704402923584),
         ('ชื่อขนมชนิดหนึ่งจำพวกขนมเค้ก แต่ทำเป็นชิ้นเล็ก ๆ แบน ๆ แล้วอบให้กรอบ',
          0.12473666667938232)]
    """
    if not custom_dict:
        custom_dict = _mean_all

    w = custom_tokenizer.word_tokenize(sentence)
    if word not in set(custom_dict.keys()) or word not in sentence:
        return []

    if device not in _MODEL_CACHE:
        _MODEL_CACHE[device] = _SentenceTransformersModel(device=device)

    model = _MODEL_CACHE[device]

    temp_mean = custom_dict[word]
    temp: list[tuple[str, float]] = []
    for meaning in temp_mean:
        tokens_with_sense: list[str] = []
        for token in w:
            if token == word:
                token = (
                    word
                    + f" ({word} ความหมาย '"
                    + meaning.replace("(", "").replace(")", "")
                    + "') "
                )
            tokens_with_sense.append(token)
        temp.append(
            (meaning, model.get_score(sentence, "".join(tokens_with_sense)))
        )

    return temp
