# -*- coding: utf-8 -*-

"""
Code by https://github.com/cstorm125/thai2fit/
"""
import re

import torch
from typing import List, Collection
from fastai import TK_REP, BaseTokenizer
from fastai.text.transform import (
    deal_caps,
    fix_html,
    rm_useless_spaces,
    spec_add_spaces,
)
from pythainlp.corpus import download, get_file
from pythainlp.tokenize import word_tokenize
from pythainlp.util import normalize as normalize_char_order

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


MODEL_NAME = "thai2fit_lm"
ITOS_NAME = "thai2fit_itos"


# custom fastai tokenizer
class ThaiTokenizer(BaseTokenizer):
    """
    Wrapper around a frozen newmm tokenizer to make it a fastai `BaseTokenizer`.
    """

    def __init__(self, lang: str = "th"):
        self.lang = lang

    def tokenizer(self, t: str) -> List[str]:
        """
        :meth: tokenize text with a frozen newmm engine
        :param str t: text to tokenize
        :return: tokenized text
        """
        return word_tokenize(t, engine="ulmfit")

    def add_special_cases(self, toks: Collection[str]):
        pass


# special rules for Thai
def replace_rep_after(t: str) -> str:
    "Replace repetitions at the character level in `t` after the repetition"

    def _replace_rep(m: Collection[str]) -> str:
        c, cc = m.groups()
        return f" {c} {TK_REP} {len(cc)+1} "

    re_rep = re.compile(r"(\S)(\1{3,})")
    return re_rep.sub(_replace_rep, t)


def rm_useless_newlines(t: str) -> str:
    "Remove multiple newlines in `t`."
    return re.sub(r"[\n]{2,}", " ", t)


def rm_brackets(t: str) -> str:
    "Remove all empty brackets from `t`."
    new_line = re.sub(r"\(\)", "", t)
    new_line = re.sub(r"\{\}", "", new_line)
    new_line = re.sub(r"\[\]", "", new_line)
    return new_line


# in case we want to add more specific rules for Thai
thai_rules = [
    fix_html,
    deal_caps,
    replace_rep_after,
    normalize_char_order,
    spec_add_spaces,
    rm_useless_spaces,
    rm_useless_newlines,
    rm_brackets,
]


# Download pretrained models
def get_path(fname):
    """
    :meth: download get path of file from pythainlp-corpus
    :param str fname: file name
    :return: path to downloaded file
    """
    path = get_file(fname)
    if not path:
        download(fname)
        path = get_file(fname)
    return path


# pretrained paths
THWIKI = [get_path(MODEL_NAME)[:-4], get_path(ITOS_NAME)[:-4]]
tt = ThaiTokenizer()


def document_vector(ss, learn, data):
    """
    :meth: `document_vector` get document vector using pretrained ULMFiT model
    :param str ss: sentence to extract embeddings
    :param learn: fastai language model learner
    :param data: fastai data bunch
    :return: `numpy.array` of document vector sized 400
    """
    s = tt.tokenizer(ss)
    t = torch.tensor(data.vocab.numericalize(s), requires_grad=False)[:, None].to(
        device
    )
    m = learn.model[0]
    m.reset()
    pred, _ = m(t)
    res = pred[-1][-1, :, :].squeeze().detach().numpy()
    return res
