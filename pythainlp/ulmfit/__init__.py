# -*- coding: utf-8 -*-

"""
Code by https://github.com/cstorm125/thai2fit/
"""
import collections
import re

import numpy as np
import torch
from fastai.text import TK_REP, BaseTokenizer, Tokenizer
from fastai.text.transform import (
    deal_caps,
    fix_html,
    rm_useless_spaces,
    spec_add_spaces,
    replace_all_caps,
)
from pythainlp.corpus import download, get_corpus_path
from pythainlp.tokenize import word_tokenize
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

# Download pretrained models
def _get_path(fname):
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
    Wrapper around a frozen newmm tokenizer to make it a fastai `BaseTokenizer`.
    https://docs.fast.ai/text.transform#BaseTokenizer
    """

    def __init__(self, lang = "th"):
        self.lang = lang

    def tokenizer(self, t):
        """
        :meth: tokenize text with a frozen newmm engine
        :param str t: text to tokenize
        :return: tokenized text
        """
        return word_tokenize(t, engine="ulmfit")

    def add_special_cases(self, toks):
        pass


def replace_rep_after(t):
    "Replace repetitions at the character level in `t` after the repetition"

    def _replace_rep(m):
        c, cc = m.groups()
        return f"{c} {TK_REP} {len(cc)+1} "

    re_rep = re.compile(r"(\S)(\1{3,})")
    return re_rep.sub(_replace_rep, t)


def rm_useless_newlines(t):
    "Remove multiple newlines in `t`."
    return re.sub(r"[\n]{2,}", " ", t)


def rm_brackets(t):
    "Remove all empty brackets from `t`."
    new_line = re.sub(r"\(\)", "", t)
    new_line = re.sub(r"\{\}", "", new_line)
    new_line = re.sub(r"\[\]", "", new_line)
    return new_line


# Pretrained paths
# TODO: Let the user decide if they like to download (at setup?)
_THWIKI_LSTM = [_get_path(_MODEL_NAME_LSTM)[:-4], _get_path(_ITOS_NAME_LSTM)[:-4]]

# Preprocessing rules for Thai text
pre_rules_th = [fix_html, replace_rep_after, normalize_char_order, 
                spec_add_spaces, rm_useless_spaces, rm_useless_newlines, rm_brackets]
post_rules_th = [replace_all_caps, deal_caps]

_tokenizer = ThaiTokenizer()


def document_vector(text, learn, data):
    """
    :meth: `document_vector` get document vector using fastai language model and data bunch
    :param str text: text to extract embeddings
    :param learn: fastai language model learner
    :param data: fastai data bunch 
    :return: `numpy.array` of document vector sized 400 based on the encoder of the model
    """
    
    s = _tokenizer.tokenizer(text)
    t = torch.tensor(data.vocab.numericalize(s), requires_grad=False).to(device)
    m = learn.model[0].encoder.to(device)
    res = m(t).mean(0).cpu().detach().numpy()
    return(res)


def merge_wgts(em_sz, wgts, itos_pre, itos_new):
    """
    :meth: `merge_wgts` insert pretrained weights and vocab into a new set of weights and vocab;
    use average if vocab not in pretrained vocab
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
