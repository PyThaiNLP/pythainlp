# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Thai2fit: Thai Wikipeida Language Model for Text Generation

Codes are from
https://github.com/PyThaiNLP/tutorials/blob/master/source/notebooks/text_generation.ipynb
"""

from __future__ import annotations

__all__: list[str] = ["gen_sentence"]

import json
import random
from typing import TYPE_CHECKING, Any, Union

if TYPE_CHECKING:
    from pathlib import Path

    import pandas as pd
    from fastai.basic_train import Learner
    from fastai.text import (
        AWD_LSTM,
        LMDataBunch,
        Tokenizer,
        Vocab,
        language_model_learner,
    )

# fastai
import fastai
import pandas as pd
from fastai.text import (
    AWD_LSTM,
    NumericalizeProcessor,
    TextList,
    TokenizeProcessor,
    Tokenizer,
    URLs,
    language_model_learner,
    untar_data,
)

# pythainlp
from pythainlp.ulmfit import (
    THWIKI_LSTM,
    ThaiTokenizer,
    post_rules_th,
    pre_rules_th,
)

# get dummy data
imdb: "Path" = untar_data(URLs.IMDB_SAMPLE)
dummy_df: "pd.DataFrame" = pd.read_csv(imdb / "texts.csv")

# get vocab
thwiki: dict[str, Any] = THWIKI_LSTM

# Validate that corpus files are available
if thwiki["json_itos_fname"] is None or thwiki["wgts_fname"] is None:
    raise FileNotFoundError(
        "corpus-not-found names=['wiki_lm_lstm', 'wiki_itos_lstm']\n"
        "  Thai2fit model files not found.\n"
        "    Python: pythainlp.corpus.download('wiki_lm_lstm')\n"
        "    CLI:    thainlp data get wiki_lm_lstm\n"
        "    Python: pythainlp.corpus.download('json_itos_fname')\n"
        "    CLI:    thainlp data get json_itos_fname"
    )

with open(thwiki["json_itos_fname"], "r") as f:
    thwiki_itos: list[str] = json.load(f)
thwiki_vocab: "Vocab" = fastai.text.transform.Vocab(thwiki_itos)

# dummy databunch
tt: "Tokenizer" = Tokenizer(
    tok_func=ThaiTokenizer,
    lang="th",
    pre_rules=pre_rules_th,
    post_rules=post_rules_th,
)
processor: list[Any] = [
    TokenizeProcessor(tokenizer=tt, chunksize=10000, mark_fields=False),
    NumericalizeProcessor(vocab=thwiki_vocab, max_vocab=60000, min_freq=3),
]
data_lm: "LMDataBunch" = (
    TextList.from_df(dummy_df, imdb, cols=["text"], processor=processor)
    .split_by_rand_pct(0.2)
    .label_for_lm()
    .databunch(bs=64)
)


data_lm.sanity_check()

config: dict[str, Any] = {
    "emb_sz": 400,
    "n_hid": 1550,
    "n_layers": 4,
    "pad_token": 1,
    "qrnn": False,
    "tie_weights": True,
    "out_bias": True,
    "output_p": 0.25,
    "hidden_p": 0.1,
    "input_p": 0.2,
    "embed_p": 0.02,
    "weight_p": 0.15,
}
trn_args: dict[str, Any] = {
    "drop_mult": 0.9,
    "clip": 0.12,
    "alpha": 2,
    "beta": 1,
}

learn: "Learner" = language_model_learner(
    data_lm, AWD_LSTM, config=config, pretrained=False, **trn_args
)

# load pretrained models
learn.load_pretrained(**thwiki)


def gen_sentence(
    start_seq: str = "",
    N: int = 4,
    prob: float = 0.001,
    output_str: bool = True,
) -> Union[list[str], str]:
    """Text generator using Thai2fit

    :param str start_seq: word to begin sentence with
    :param int N: number of words
    :param bool output_str: output as string
    :param bool duplicate: allow duplicate words in sentence

    :return: list words or str words
    :rtype: list[str], str

    :Example:

      from pythainlp.generate.thai2fit import gen_sentence

      gen_sentence()
      # output: 'แคทรียา อิงลิช  (นักแสดง'

      gen_sentence("แมว")
      # output: 'แมว คุณหลวง '
    """
    if not start_seq:
        # Non-cryptographic use, pseudo-random generator is acceptable here
        start_seq = random.choice(list(thwiki_itos))  # noqa: S311
    predicted_text: str = learn.predict(
        start_seq, N, temperature=0.8, min_p=prob, sep="-*-"
    )
    list_word = predicted_text.split("-*-")

    if output_str:
        return "".join(list_word)

    return list_word
