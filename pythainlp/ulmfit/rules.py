# -*- coding: utf-8 -*-
import html
import emoji
import re
from typing import List, Collection

TK_MAJ, TK_UP, TK_REP, TK_WREP = 'xxmaj', 'xxup', 'xxrep', 'xxwrep'
BOS, EOS, FLD, UNK, PAD = 'xxbos', 'xxeos', 'xxfld', 'xxunk', 'xxpad'


def fix_html(x: str) -> str:
    """List of replacements from html strings in `x`. (code from `fastai`)"""
    re1 = re.compile(r'  +')
    x = x.replace('#39;', "'").replace('amp;', '&').replace(
        '#146;', "'").replace('nbsp;', ' ').replace(
        '#36;', '$').replace('\\n', "\n").replace('quot;', "'").replace(
        '<br />', "\n").replace('\\"', '"').replace('<unk>', UNK).replace(
        ' @.@ ', '.').replace(' @-@ ', '-').replace(' @,@ ', ',').replace(
        '\\', ' \\ ')
    return re1.sub(' ', html.unescape(x))


def replace_all_caps(x: Collection[str]) -> Collection[str]:
    """
        Replace tokens in ALL CAPS in `x` by their lower version \
        and add `TK_UP` before." (code from `fastai`)
    """
    res = []
    for t in x:
        if t.isupper() and len(t) > 1:
            res.append(TK_UP)
            res.append(t.lower())
        else:
            res.append(t)
    return res


def rm_useless_spaces(t: str) -> str:
    """Remove multiple spaces in `t`. (code from `fastai`)"""
    return re.sub(' {2,}', ' ', t)


def spec_add_spaces(t: str) -> str:
    """Add spaces around / and # in `t`. \n (code from `fastai`)"""
    return re.sub(r'([/#\n])', r' \1 ', t)


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


def replace_wrep_post(toks: Collection):
    """
    Replace reptitive words post tokenization;
    fastai `replace_wrep` does not work well with Thai.
    """
    previous_word = None
    rep_count = 0
    res = []
    for current_word in toks+['xxend']:
        if current_word == previous_word:
            rep_count += 1
        elif (current_word != previous_word) & (rep_count > 0):
            res += [TK_WREP, str(rep_count), previous_word]
            rep_count = 0
        else:
            res.append(previous_word)
        previous_word = current_word
    return res[1:]


def rm_useless_newlines(text: str) -> str:
    """Remove multiple newlines in `text`."""

    return re.sub(r"[\n]{2,}", " ", text)


def rm_brackets(text: str) -> str:
    """Remove all empty brackets from `t`."""
    new_line = re.sub(r"\(\)", "", text)
    new_line = re.sub(r"\{\}", "", new_line)
    new_line = re.sub(r"\[\]", "", new_line)

    return new_line


def ungroup_emoji(toks: Collection):
    """Ungroup emojis"""

    res = []
    for tok in toks:
        if emoji.emoji_count(tok) == len(tok):
            res.append([char for char in tok])
        else:
            res.append(tok)

    return res


def lowercase_all(toks: Collection):
    """lowercase all English words"""
    return [tok.lower() for tok in toks]


class BaseTokenizer():
    """Basic class for a tokenizer function. (code from `fastai`)"""
    def __init__(self, lang: str): self.lang = lang

    def tokenizer(self, t: str) -> List[str]: return t.split(' ')

    def add_special_cases(self, toks: Collection[str]): pass
