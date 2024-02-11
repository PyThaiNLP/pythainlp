# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
"""
Universal Language Model Fine-tuning for Text Classification (ULMFiT).
"""
import collections
from typing import Callable, Collection

import numpy as np
import torch
from pythainlp.corpus import get_corpus_path
from pythainlp.tokenize import THAI2FIT_TOKENIZER
from pythainlp.ulmfit.preprocess import (
    fix_html,
    lowercase_all,
    remove_space,
    replace_rep_after,
    replace_rep_nonum,
    replace_url,
    replace_wrep_post,
    replace_wrep_post_nonum,
    rm_brackets,
    rm_useless_newlines,
    rm_useless_spaces,
    spec_add_spaces,
    ungroup_emoji,
)
from pythainlp.util import reorder_vowels

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

_MODEL_NAME_LSTM = "wiki_lm_lstm"
_ITOS_NAME_LSTM = "wiki_itos_lstm"


# Pretrained model paths
THWIKI_LSTM = {
    "wgts_fname": get_corpus_path(_MODEL_NAME_LSTM),
    "itos_fname": get_corpus_path(_ITOS_NAME_LSTM),
}

# Preprocessing rules for Thai text
# dense features
pre_rules_th = [
    replace_rep_after,
    fix_html,
    reorder_vowels,
    spec_add_spaces,
    rm_useless_spaces,
    rm_useless_newlines,
    rm_brackets,
    replace_url,
]
post_rules_th = [replace_wrep_post, ungroup_emoji, lowercase_all]

# sparse features
pre_rules_th_sparse = pre_rules_th[1:] + [replace_rep_nonum]
post_rules_th_sparse = post_rules_th[1:] + [
    replace_wrep_post_nonum,
    remove_space,
]


def process_thai(
    text: str,
    pre_rules: Collection = pre_rules_th_sparse,
    tok_func: Callable = THAI2FIT_TOKENIZER.word_tokenize,
    post_rules: Collection = post_rules_th_sparse,
) -> Collection[str]:
    """
    Process Thai texts for models (with sparse features as default)

    :param str text: text to be cleaned
    :param list[func] pre_rules: rules to apply before tokenization.
    :param func tok_func: tokenization function (by default, **tok_func** is
                          :func:`pythainlp.tokenize.word_tokenize`)

    :param list[func]  post_rules: rules to apply after tokenizations

    :return: a list of cleaned tokenized texts
    :rtype: list[str]


    :Note:
      - The default **pre-rules** consists of :func:`fix_html`,
        :func:`pythainlp.util.normalize`,
        :func:`spec_add_spaces`,
        :func:`rm_useless_spaces`,
        :func:`rm_useless_newlines`,
        :func:`rm_brackets`
        and :func:`replace_rep_nonum`.

      - The default **post-rules** consists of :func:`ungroup_emoji`,
        :func:`lowercase_all`,  :func:`replace_wrep_post_nonum`,
        and :func:`remove_space`.

    :Example:

        1. Use default pre-rules and post-rules:

        >>> from pythainlp.ulmfit import process_thai
        >>> text = "บ้านนนนน () อยู่นานนานนาน 😂🤣😃😄😅 PyThaiNLP amp;     "
        >>> process_thai(text)
        [บ้าน', 'xxrep', '   ', 'อยู่', 'xxwrep', 'นาน', '😂', '🤣',
        '😃', '😄', '😅', 'pythainlp', '&']

        2. Modify pre_rules and post_rules arguments with
           rules provided in :mod:`pythainlp.ulmfit`:

        >>> from pythainlp.ulmfit import (
            process_thai,
            replace_rep_after,
            fix_html,
            ungroup_emoji,
            replace_wrep_post,
            remove_space)
        >>>
        >>> text = "บ้านนนนน () อยู่นานนานนาน 😂🤣😃😄😅 PyThaiNLP amp;     "
        >>> process_thai(text,
                         pre_rules=[replace_rep_after, fix_html],
                         post_rules=[ungroup_emoji,
                                     replace_wrep_post,
                                     remove_space]
                        )
        ['บ้าน', 'xxrep', '5', '()', 'อยู่', 'xxwrep', '2', 'นาน', '😂', '🤣',
         '😃', '😄', '😅', 'PyThaiNLP', '&']


    """
    res = text

    for rule in pre_rules:
        res = rule(res)
    res = tok_func(res)
    for rule in post_rules:
        res = rule(res)

    return res


def document_vector(text: str, learn, data, agg: str = "mean"):
    """
    This function vectorizes Thai input text into a 400 dimension vector using
    :class:`fastai` language model and data bunch.

    :meth: `document_vector` get document vector using fastai language model
           and data bunch
    :param str text: text to be vectorized with :class:`fastai` language model.
    :param learn: :class:`fastai` language model learner
    :param data: :class:`fastai` data bunch
    :param str agg: name of aggregation methods for word embeddings
                    The available methods are "mean" and "sum"

    :return: :class:`numpy.array` of document vector sized 400 based on
             the encoder of the model
    :rtype: :class:`numpy.ndarray((1, 400))`

    :Example:

        >>> from pythainlp.ulmfit import document_vectorr
        >>> from fastai import *
        >>> from fastai.text import *
        >>>
        >>> # Load Data Bunch
        >>> data = load_data(MODEL_PATH, 'thwiki_lm_data.pkl')
        >>>
        >>> # Initialize language_model_learner
        >>> config = dict(emb_sz=400, n_hid=1550, n_layers=4, pad_token=1,
             qrnn=False, tie_weights=True, out_bias=True, output_p=0.25,
             hidden_p=0.1, input_p=0.2, embed_p=0.02, weight_p=0.15)
        >>> trn_args = dict(drop_mult=0.9, clip=0.12, alpha=2, beta=1)
        >>> learn = language_model_learner(data, AWD_LSTM, config=config,
                                           pretrained=False, **trn_args)
        >>> document_vector('วันนี้วันดีปีใหม่', learn, data)

    :See Also:
        * A notebook showing how to train `ulmfit` language model and its
          usage, `Jupyter Notebook \
          <https://github.com/cstorm125/thai2fit/blob/master/thwiki_lm/word2vec_examples.ipynb>`_

    """

    s = THAI2FIT_TOKENIZER.word_tokenize(text)
    t = torch.tensor(data.vocab.numericalize(s), requires_grad=False).to(
        device
    )
    m = learn.model[0].encoder.to(device)
    res = m(t).cpu().detach().numpy()
    if agg == "mean":
        res = res.mean(0)
    elif agg == "sum":
        res = res.sum(0)
    else:
        raise ValueError("Aggregate by mean or sum")

    return res


def merge_wgts(em_sz, wgts, itos_pre, itos_new):
    """
    This function is to insert new vocab into an existing model named `wgts`
    and update the model's weights for new vocab with the average embedding.

    :meth: `merge_wgts` insert pretrained weights and vocab into a new set
           of weights and vocab; use average if vocab not in pretrained vocab
    :param int em_sz: embedding size
    :param wgts: torch model weights
    :param list itos_pre: pretrained list of vocab
    :param list itos_new: list of new vocab

    :return: merged torch model weights

    :Example:
    ::

        from pythainlp.ulmfit import merge_wgts
        import torch

        wgts = {'0.encoder.weight': torch.randn(5,3)}
        itos_pre = ["แมว", "คน", "หนู"]
        itos_new = ["ปลา", "เต่า", "นก"]
        em_sz = 3

        merge_wgts(em_sz, wgts, itos_pre, itos_new)
        # output:
        # {'0.encoder.weight': tensor([[0.5952, 0.4453, 0.0011],
        # [0.5952, 0.4453, 0.0011],
        # [0.5952, 0.4453, 0.0011]]),
        # '0.encoder_dp.emb.weight': tensor([[0.5952, 0.4453, 0.0011],
        # [0.5952, 0.4453, 0.0011],
        # [0.5952, 0.4453, 0.0011]]),
        # '1.decoder.weight': tensor([[0.5952, 0.4453, 0.0011],
        # [0.5952, 0.4453, 0.0011],
        # [0.5952, 0.4453, 0.0011]])}
    """
    vocab_size = len(itos_new)
    enc_wgts = wgts["0.encoder.weight"].numpy()

    # Average weight of encoding
    row_m = enc_wgts.mean(0)
    stoi_pre = collections.defaultdict(
        lambda: -1, {v: k for k, v in enumerate(itos_pre)}
    )

    # New embedding based on classification dataset
    new_w = np.zeros((vocab_size, em_sz), dtype=np.float32)

    for i, w in enumerate(itos_new):
        r = stoi_pre[w]
        # Use pretrianed embedding if present; else use the average
        new_w[i] = enc_wgts[r] if r >= 0 else row_m

    wgts["0.encoder.weight"] = torch.tensor(new_w)
    wgts["0.encoder_dp.emb.weight"] = torch.tensor(np.copy(new_w))
    wgts["1.decoder.weight"] = torch.tensor(np.copy(new_w))

    return wgts
