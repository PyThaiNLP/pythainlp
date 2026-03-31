# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Universal Language Model Fine-tuning for Text Classification (ULMFiT)."""

from __future__ import annotations

import collections
from typing import TYPE_CHECKING, Optional, cast

import torch

if TYPE_CHECKING:
    from collections.abc import Callable, Collection

    import numpy as np
    from fastai.basic_data import DataBunch
    from fastai.basic_train import Learner
    from numpy.typing import NDArray

from pythainlp.corpus import get_corpus_path
from pythainlp.tokenize import thai2fit_tokenizer
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

device: "torch.device" = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

_MODEL_NAME_LSTM: str = "wiki_lm_lstm"
_ITOS_NAME_LSTM: str = "wiki_itos_lstm"


# Pretrained model paths
# Note: These may be None if corpus is not downloaded.
# Access via get_thwiki_lstm() for proper validation or use directly
# if you've already verified the corpus is downloaded.
THWIKI_LSTM: dict[str, Optional[str]] = {
    "wgts_fname": get_corpus_path(_MODEL_NAME_LSTM),
    "itos_fname": get_corpus_path(_ITOS_NAME_LSTM),
    "json_itos_fname": get_corpus_path("wiki_itos_lstm_json"),
}


def get_thwiki_lstm() -> dict[str, str]:
    """Get THWIKI LSTM model paths with validation.

    :return: dictionary with ``wgts_fname`` and ``itos_fname`` keys
    :rtype: dict[str, str]
    :raises FileNotFoundError: if corpus files are not found
    """
    wgts_fname = THWIKI_LSTM["wgts_fname"]
    itos_fname = THWIKI_LSTM["itos_fname"]

    if not wgts_fname or not itos_fname:
        raise FileNotFoundError(
            "corpus-not-found names=['wiki_lm_lstm', 'wiki_itos_lstm']\n"
            "  ULMFiT model files not found.\n"
            "    Python: pythainlp.corpus.download('wiki_lm_lstm')\n"
            "    CLI:    thainlp data get wiki_lm_lstm\n"
            "    Python: pythainlp.corpus.download('wiki_itos_lstm')\n"
            "    CLI:    thainlp data get wiki_itos_lstm"
        )

    return {"wgts_fname": wgts_fname, "itos_fname": itos_fname}


# Preprocessing rules for Thai text
# dense features
pre_rules_th: list[Callable[[str], str]] = [
    replace_rep_after,
    fix_html,
    reorder_vowels,
    spec_add_spaces,
    rm_useless_spaces,
    rm_useless_newlines,
    rm_brackets,
    replace_url,
]
post_rules_th: list[Callable[[Collection[str]], list[str]]] = [
    replace_wrep_post,
    ungroup_emoji,
    lowercase_all,
]

# sparse features
pre_rules_th_sparse: list[Callable[[str], str]] = pre_rules_th[1:] + [
    replace_rep_nonum
]
post_rules_th_sparse: list[Callable[[Collection[str]], list[str]]] = (
    post_rules_th[1:]
    + [
        replace_wrep_post_nonum,
        remove_space,
    ]
)


def process_thai(
    text: str,
    pre_rules: Optional[Collection[Callable[[str], str]]] = None,
    tok_func: Optional[Callable[[str], list[str]]] = None,
    post_rules: Optional[Collection[Callable[[list[str]], list[str]]]] = None,
) -> list[str]:
    """Process Thai texts for models (with sparse features as default)

    :param str text: text to be cleaned
    :param Optional[Collection[Callable[[str], str]]] pre_rules: rules to
        apply before tokenization. If None, use the default sparse pre-rules.
    :param Optional[Callable[[str], list[str]]] tok_func: tokenization
        function. By default, **tok_func** is
        :func:`pythainlp.tokenize.word_tokenize`.

    :param Optional[Collection[Callable[[list[str]], list[str]]]] post_rules:
        rules to apply after tokenization. If None, use the default sparse
        post-rules.

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
        :func:`lowercase_all`, :func:`replace_wrep_post_nonum`,
        and :func:`remove_space`.

    :Example:

        1. Use default pre-rules and post-rules:

        >>> from pythainlp.ulmfit import process_thai
        >>> text = "บ้านนนนน () อยู่นานนานนาน 😂🤣😃😄😅 PyThaiNLP amp;     "
        >>> process_thai(text)
        ['บ้าน', 'xxrep', '   ', 'อยู่', 'xxwrep', 'นาน', '😂', '🤣',
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
    processed_text = text
    if pre_rules is None:
        pre_rules = pre_rules_th_sparse
    if post_rules is None:
        post_rules = cast(
            Collection[Callable[[list[str]], list[str]]],
            post_rules_th_sparse,
        )

    if tok_func is None:
        tok_func = thai2fit_tokenizer().word_tokenize

    for pre_rule in pre_rules:
        processed_text = pre_rule(processed_text)
    tokens = tok_func(processed_text)
    for post_rule in post_rules:
        tokens = post_rule(tokens)

    return tokens


def document_vector(
    text: str, learn: "Learner", data: "DataBunch", agg: str = "mean"
) -> "NDArray[np.float32]":
    """Vectorize a Thai sentence into a 400-dimension vector.

    Uses a :class:`fastai` language model and data bunch.
    Word vectors are aggregated by mean or summation.

    :param str text: text to vectorize
    :param learn: :class:`fastai` language model learner
    :param data: :class:`fastai` data bunch
    :param str agg: aggregation method; ``"mean"`` or ``"sum"``

    :return: document vector of shape ``(1, 400)``
    :rtype: numpy.typing.NDArray[numpy.float32]

    :Example:

        >>> from pythainlp.ulmfit import document_vector
        >>> from fastai.text import load_data, language_model_learner, AWD_LSTM
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
    s = thai2fit_tokenizer().word_tokenize(text)
    t = torch.tensor(data.vocab.numericalize(s), requires_grad=False).to(
        device
    )
    m = learn.model[0].encoder.to(device)
    res = m(t).cpu().detach().numpy().astype("float32", copy=False)
    if agg == "mean":
        res = res.mean(0, dtype="float32")
    elif agg == "sum":
        res = res.sum(0, dtype="float32")
    else:
        raise ValueError("Aggregate by mean or sum")

    return cast("NDArray[np.float32]", res)


def merge_wgts(
    em_sz: int,
    wgts: dict[str, torch.Tensor],
    itos_pre: list[str],
    itos_new: list[str],
) -> dict[str, torch.Tensor]:
    """Insert new vocab into an existing model and update weights.

    New vocab weights are initialised with the average embedding
    when not found in the pretrained vocab.

    :param int em_sz: embedding size
    :param wgts: torch model weights
    :param list[str] itos_pre: pretrained list of vocab
    :param list[str] itos_new: list of new vocab

    :return: merged torch model weights
    :rtype: dict[str, torch.Tensor]

    :Example:

        >>> from pythainlp.ulmfit import merge_wgts  # doctest: +SKIP
        >>> import torch  # doctest: +SKIP

        >>> wgts = {"0.encoder.weight": torch.randn(5, 3)}  # doctest: +SKIP
        >>> itos_pre = ["แมว", "คน", "หนู"]  # doctest: +SKIP
        >>> itos_new = ["ปลา", "เต่า", "นก"]  # doctest: +SKIP
        >>> em_sz = 3  # doctest: +SKIP

        >>> merge_wgts(em_sz, wgts, itos_pre, itos_new)  # doctest: +SKIP
        {'0.encoder.weight': tensor([[0.5952, 0.4453, 0.0011],
        [0.5952, 0.4453, 0.0011],
        [0.5952, 0.4453, 0.0011]]),
        '0.encoder_dp.emb.weight': tensor([[0.5952, 0.4453, 0.0011],
        [0.5952, 0.4453, 0.0011],
        [0.5952, 0.4453, 0.0011]]),
        '1.decoder.weight': tensor([[0.5952, 0.4453, 0.0011],
        [0.5952, 0.4453, 0.0011],
        [0.5952, 0.4453, 0.0011]])}
    """
    vocab_size = len(itos_new)
    enc_wgts = wgts["0.encoder.weight"].numpy().astype("float32", copy=False)

    # Average weight of encoding
    row_m = enc_wgts.mean(0, dtype="float32")
    stoi_pre = collections.defaultdict(
        lambda: -1, {v: k for k, v in enumerate(itos_pre)}
    )

    # New embedding based on classification dataset
    import numpy as np

    new_w = np.zeros((vocab_size, em_sz), dtype=np.float32)

    for i, w in enumerate(itos_new):
        r = stoi_pre[w]
        # Use pretrianed embedding if present; else use the average
        new_w[i] = enc_wgts[r] if r >= 0 else row_m

    wgts["0.encoder.weight"] = torch.tensor(new_w)
    wgts["0.encoder_dp.emb.weight"] = torch.tensor(np.copy(new_w))
    wgts["1.decoder.weight"] = torch.tensor(np.copy(new_w))

    return wgts
