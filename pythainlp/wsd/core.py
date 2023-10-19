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

from pythainlp.tokenize import Tokenizer
from pythainlp.util.trie import Trie
from pythainlp.corpus import thai_wsd_dict

_wsd_dict = thai_wsd_dict()
_mean_all = {}
for i,j in zip(_wsd_dict["word"], _wsd_dict["meaning"]):
    _mean_all[i]=j
_all_word = set(list(_mean_all.keys()))
_TRIE = Trie(list(_all_word))
_word_cut = Tokenizer(custom_dict=_TRIE)


class _SentenceTransformersModel:
    def __init__(self, model:str="sentence-transformers/paraphrase-multilingual-mpnet-base-v2", device:str="cpu"):
        from sentence_transformers import SentenceTransformer
        self.device = device
        self.model_name = model
        self.model = SentenceTransformer(self.model_name, device=self.device)
    def change_device(self, device: str):
        from sentence_transformers import SentenceTransformer
        self.device = device
        self.model = SentenceTransformer(self.model_name, device=self.device)
    def get_score(self, sentences1: str,sentences2: str)->float:
        from sentence_transformers import util
        embedding_1= self.model.encode(sentences1, convert_to_tensor=True)
        embedding_2 = self.model.encode(sentences2, convert_to_tensor=True)
        return 1-util.pytorch_cos_sim(embedding_1, embedding_2)[0][0].item()

_MODEL = None


def get_sense(
    sentence: str,
    word: str,
    device: str="cpu",
    custom_dict: Union[dict,None]=None,
    custom_tokenizer: Tokenizer=_word_cut,
) -> Union[List[Tuple[str, float]], None]:
    """
    Get word sense from the sentence.
    This function will get definition and distance from context in sentence.
    
    :param str sentence: Thai sentence
    :param str word: Thai word
    :param str device: device for running model on.
    :param dict custom_dict: Thai dictionary {"word":["definition",..]}
    :param Tokenizer custom_tokenizer: Tokenizer used to tokenize words in sentence.
    :return: list of definitions and distances (1 - cos_sim) or None (If word is not in the dictionary)
    :rtype: Union[List[Tuple[str, float]], None]
    
    We get the ideas from `Context-Aware Semantic Similarity Measurement for Unsupervised \
    Word Sense Disambiguation <https://arxiv.org/abs/2305.03520>`_ to build get_sense function.

    For Thai dictionary, we use Thai dictionary from wiktionary.
    See more `thai_dict <https://pythainlp.github.io/pythainlp-corpus/thai_dict.html>`_.
    
    For the model, we use sentence transformers model from \
    `sentence-transformers/paraphrase-multilingual-mpnet-base-v2 <https://huggingface.co/sentence-transformers/paraphrase-multilingual-mpnet-base-v2>`_ for \
    unsupervised word sense disambiguation.
    
    :Example:
    ::

        from pythainlp.wsd import get_sense
        print(get_sense("เขากำลังอบขนมคุกกี้","คุกกี้"))
        # output:
        # [('โปรแกรมคอมพิวเตอร์ใช้ในทางอินเทอร์เน็ตสำหรับเก็บข้อมูลของผู้ใช้งาน',
        #   0.0974416732788086),
        #  ('ชื่อขนมชนิดหนึ่งจำพวกขนมเค้ก แต่ทำเป็นชิ้นเล็ก ๆ แบน ๆ แล้วอบให้กรอบ',
        #   0.09319090843200684)]

        print(get_sense("เว็บนี้ต้องการคุกกี้ในการทำงาน","คุกกี้"))
        # output:
        # [('โปรแกรมคอมพิวเตอร์ใช้ในทางอินเทอร์เน็ตสำหรับเก็บข้อมูลของผู้ใช้งาน',
        #   0.1005704402923584),
        #  ('ชื่อขนมชนิดหนึ่งจำพวกขนมเค้ก แต่ทำเป็นชิ้นเล็ก ๆ แบน ๆ แล้วอบให้กรอบ',
        #   0.12473666667938232)]
    """
    global _MODEL
    if custom_dict is None:
        custom_dict = _mean_all
    _w = custom_tokenizer.word_tokenize(sentence)
    if word not in set(custom_dict.keys()) or word not in sentence:
        return None
    if _MODEL is None:
        _MODEL = _SentenceTransformersModel(device=device)
    if _MODEL.device!=device:
        _MODEL.change_device(device=device)
    _temp_mean = custom_dict[word]
    _temp =[]
    for i in _temp_mean:
        _temp_2 = []
        for j in _w:
            if j == word:
                j = word+f" ({word} ความหมาย '"+i.replace('(',"").replace(')',"")+"') "
            _temp_2.append(j)
        _temp.append((i,_MODEL.get_score(sentence,''.join(_temp_2))))
    return _temp
