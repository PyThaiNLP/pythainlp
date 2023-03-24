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
Thai2fit: Thai Wikipeida Language Model for Text Generation

Code from
https://github.com/PyThaiNLP/tutorials/blob/master/source/notebooks/text_generation.ipynb
"""
__all__ = ["gen_sentence"]

import pandas as pd
import random
import pickle
from typing import List, Union

# fastai
import fastai
from fastai.text import *

# pythainlp
from pythainlp.ulmfit import *

# get dummy data
imdb = untar_data(URLs.IMDB_SAMPLE)
dummy_df = pd.read_csv(imdb / "texts.csv")

# get vocab
thwiki = THWIKI_LSTM

thwiki_itos = pickle.load(open(thwiki["itos_fname"], "rb"))
thwiki_vocab = fastai.text.transform.Vocab(thwiki_itos)

# dummy databunch
tt = Tokenizer(
    tok_func=ThaiTokenizer,
    lang="th",
    pre_rules=pre_rules_th,
    post_rules=post_rules_th,
)
processor = [
    TokenizeProcessor(tokenizer=tt, chunksize=10000, mark_fields=False),
    NumericalizeProcessor(vocab=thwiki_vocab, max_vocab=60000, min_freq=3),
]
data_lm = (
    TextList.from_df(dummy_df, imdb, cols=["text"], processor=processor)
    .split_by_rand_pct(0.2)
    .label_for_lm()
    .databunch(bs=64)
)


data_lm.sanity_check()

config = dict(
    emb_sz=400,
    n_hid=1550,
    n_layers=4,
    pad_token=1,
    qrnn=False,
    tie_weights=True,
    out_bias=True,
    output_p=0.25,
    hidden_p=0.1,
    input_p=0.2,
    embed_p=0.02,
    weight_p=0.15,
)
trn_args = dict(drop_mult=0.9, clip=0.12, alpha=2, beta=1)

learn = language_model_learner(
    data_lm, AWD_LSTM, config=config, pretrained=False, **trn_args
)

# load pretrained models
learn.load_pretrained(**thwiki)


def gen_sentence(
    start_seq: str = None,
    N: int = 4,
    prob: float = 0.001,
    output_str: bool = True,
) -> Union[List[str], str]:
    """
    Text generator using Thai2fit

    :param str start_seq: word for begin word.
    :param int N: number of word.
    :param bool output_str: output is str
    :param bool duplicate: duplicate word in sent

    :return: list words or str words
    :rtype: List[str], str

    :Example:
    ::

      from pythainlp.generate.thai2fit import gen_sentence

      gen_sentence()
      # output: 'แคทรียา อิงลิช  (นักแสดง'

      gen_sentence("แมว")
      # output: 'แมว คุณหลวง '
    """
    if start_seq is None:
        start_seq = random.choice(list(thwiki_itos))
    list_word = learn.predict(
        start_seq, N, temperature=0.8, min_p=prob, sep="-*-"
    ).split("-*-")
    if output_str:
        return "".join(list_word)
    return list_word
