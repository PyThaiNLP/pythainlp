# -*- coding: utf-8 -*-
"""
Code by Charin Polpanumas
https://github.com/cstorm125/thai2fit/
"""
import collections
import re
from typing import List,Collection

import emoji
import numpy as np
import torch
from fastai.text import BaseTokenizer, TK_REP, TK_WREP
from fastai.text.transform import (
    fix_html,
    replace_all_caps,
    rm_useless_spaces,
    spec_add_spaces,
)
from pythainlp.corpus import download, get_corpus, get_corpus_path
from pythainlp.tokenize import Tokenizer
from pythainlp.util import normalize as normalize_char_order

__all__ = [
    "ThaiTokenizer",
    "document_vector",
    "merge_wgts",
    "pre_rules_th",
    "post_rules_th",
    "_THWIKI_LSTM",
]

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

_MODEL_NAME_LSTM = "wiki_lm_lstm"
_ITOS_NAME_LSTM = "wiki_itos_lstm"

_THAI2FIT_WORDS = get_corpus("words_th_thai2fit_201810.txt")
_pythainlp_tokenizer = Tokenizer(custom_dict=_THAI2FIT_WORDS, engine="newmm")

# Download pretrained models
def _get_path(fname: str) -> str:
    """
    :meth: download get path of file from pythainlp-corpus
    :param str fname: file name
    :return: path to downloaded file
    """
    path = get_corpus_path(fname)
    if not path:
        download(fname)
        path = get_corpus_path(fname)
    return path


# Custom fastai tokenizer
class ThaiTokenizer(BaseTokenizer):
    """
    Wrapper around a frozen newmm tokenizer to make it a
    :class:`fastai.BaseTokenizer`.
    (see: https://docs.fast.ai/text.transform#BaseTokenizer)
    """

    def __init__(self, lang: str = "th"):
        self.lang = lang

    @staticmethod
    def tokenizer(text: str) -> List[str]:
        """
        This function tokenizes text with *newmm* engine and the dictionary
        specifically for `ulmfit` related functions
        (see: `Dictonary file (.txt) \
        <https://github.com/PyThaiNLP/pythainlp/blob/dev/pythainlp/corpus/words_th_thai2fit_201810.txt>`_).
        :meth: tokenize text with a frozen newmm engine
        :param str text: text to tokenize
        :return: tokenized text
        :rtype: list[str]

        :Example:

            Using :func:`pythainlp.ulmfit.ThaiTokenizer.tokenizer` is
            similar to :func:`pythainlp.tokenize.word_tokenize`
            with *ulmfit* engine.

            >>> from  pythainlp.ulmfit import ThaiTokenizer
            >>> from  pythainlp.tokenize import word_tokenize
            >>>
            >>> text = "อาภรณ์, จินตมยปัญญา ภาวนามยปัญญา"
            >>> ThaiTokenizer.tokenizer(text)
            ['อาภรณ์', ',', ' ', 'จิน', 'ตม', 'ย', 'ปัญญา',
             ' ', 'ภาวนามยปัญญา']
            >>>
            >>> word_tokenize(text, engine='ulmfit')
            ['อาภรณ์', ',', ' ', 'จิน', 'ตม', 'ย', 'ปัญญา',
             ' ', 'ภาวนามยปัญญา']

        """
        return _pythainlp_tokenizer.word_tokenize(text)

    def add_special_cases(self, toks):
        pass


def replace_rep_after(text: str) -> str:
    """
    Replace repetitions at the character level in `text` after the repetition.
    This is done to prevent such case as 'น้อยยยยยยยย' becoming 'น้อ xrep 8 ย';
    instead it will retain the word as 'น้อย xrep 8'
    """

    def _replace_rep(m):
        c, cc = m.groups()
        return f"{c} {TK_REP} {len(cc)+1} "

    re_rep = re.compile(r"(\S)(\1{3,})")

    return re_rep.sub(_replace_rep, text)

def replace_wrep_post(toks:Collection):
    """Replace reptitive words post tokenization; 
    fastai `replace_wrep` does not work well with Thai."""
    previous_word = None
    rep_count = 0
    res = []
    for current_word in toks+['xxend']:
        if current_word==previous_word: 
            rep_count+=1
        elif (current_word!=previous_word) & (rep_count>0):
            res += [TK_WREP,str(rep_count),previous_word]
            rep_count=0
        else:
            res.append(previous_word)
        previous_word=current_word
    return res[1:]


def rm_useless_newlines(text: str) -> str:
    "Remove multiple newlines in `text`."

    return re.sub(r"[\n]{2,}", " ", text)


def rm_brackets(text: str) -> str:
    "Remove all empty brackets from `t`."
    new_line = re.sub(r"\(\)", "", text)
    new_line = re.sub(r"\{\}", "", new_line)
    new_line = re.sub(r"\[\]", "", new_line)

    return new_line


def ungroup_emoji(toks:Collection):
    "Ungroup emojis"

    res = []
    for tok in toks:
        if emoji.emoji_count(tok) == len(tok):
            for char in tok:
                res.append(char)
        else:
            res.append(tok)

    return res


def lowercase_all(toks:Collection):
    "lowercase all English words"
    return [tok.lower() for tok in toks]


# Pretrained paths
# TODO: Let the user decide if they like to download (at setup?)
_THWIKI_LSTM = dict(
    wgts_fname=_get_path(_MODEL_NAME_LSTM), itos_fname=_get_path(_ITOS_NAME_LSTM)
)

# Preprocessing rules for Thai text
pre_rules_th = [
    fix_html,
    replace_rep_after,
    normalize_char_order,
    spec_add_spaces,
    rm_useless_spaces,
    rm_useless_newlines,
    rm_brackets,
]
post_rules_th = [replace_all_caps, ungroup_emoji, lowercase_all, replace_wrep_post]

_tokenizer = ThaiTokenizer()


def document_vector(text: str, learn, data, agg: str = "mean"):
    """
    This function vectorize Thai input text into a 400 dimension vector using
    :class:`fastai` language model and data bunch.

    :meth: `document_vector` get document vector using fastai language model
           and data bunch
    :param str text: text to be vectorized with :class:`fastai` language model.
    :param learn: :class:`fastai` language model learner
    :param data: :class:`fastai` data bunch
    :param str agg: name of aggregation methods for word embeddings
                    The avialable methods are "mean" and "sum"

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

    s = _tokenizer.tokenizer(text)
    t = torch.tensor(data.vocab.numericalize(s), requires_grad=False).to(device)
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
