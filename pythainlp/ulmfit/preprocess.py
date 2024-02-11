# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
"""
Preprocessing for ULMFiT
"""
import html
import re
from typing import Collection, List

import emoji

_TK_UNK = "xxunk"
_TK_REP = "xxrep"
_TK_WREP = "xxwrep"
_TK_END = "xxend"
_TK_URL = "xxurl"


def replace_url(text: str) -> str:
    """
    Replace URL in `text` with TK_URL

    :param str text: text to replace URL in

    :return: text with URLs replaced
    :rtype: str

    :Example:

        >>> from pythainlp.ulmfit import replace_url
        >>> replace_url("go to github.com")
        go to xxurl
    """
    URL_PATTERN = r"""(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))"""
    return re.sub(URL_PATTERN, _TK_URL, text)


def fix_html(text: str) -> str:
    """
    Replace HTML strings in `test`. (codes from `fastai`)

    :param str text: text to replace HTML strings in

    :return: text with HTML strings replaced
    :rtype: str

    :Example:

        >>> from pythainlp.ulmfit import fix_html
        >>> fix_html("Anbsp;amp;nbsp;B @.@ ")
        A & B.
    """
    re1 = re.compile(r"  +")
    text = (
        text.replace("#39;", "'")
        .replace("amp;", "&")
        .replace("#146;", "'")
        .replace("nbsp;", " ")
        .replace("#36;", "$")
        .replace("\\n", "\n")
        .replace("quot;", "'")
        .replace("<br />", "\n")
        .replace('\\"', '"')
        .replace("<unk>", _TK_UNK)
        .replace(" @.@ ", ".")
        .replace(" @-@ ", "-")
        .replace(" @,@ ", ",")
        .replace("\\", " \\ ")
    )
    return re1.sub(" ", html.unescape(text))


def rm_useless_spaces(text: str) -> str:
    """Remove multiple spaces in `text`. (codes from `fastai`)"""
    return re.sub(" {2,}", " ", text)


def spec_add_spaces(text: str) -> str:
    """Add spaces around / and # in `text`. \n (codes from `fastai`)"""
    return re.sub(r"([/#\n])", r" \1 ", text)


def replace_rep_after(text: str) -> str:
    """
    Replace repetitions at the character level in `text` after the repeated character.
    This is to prevent cases such as 'น้อยยยยยยยย' becomes 'น้อ xxrep 8 ย'
    ; instead it will retain the word as 'น้อย xxrep 8'

    :param str text: input text to replace character repetitions in

    :return: text with repetitive token **xxrep** and the counter
             after the repeated character

    :rtype: str
    :Example:

        >>> from pythainlp.ulmfit import replace_rep_after
        >>>
        >>> text = "กาาาาาาา"
        >>> replace_rep_after(text)
        'กาxxrep7 '
    """

    def _replace_rep(m):
        c, cc = m.groups()
        return f"{c}{_TK_REP}{len(cc)+1} "

    re_rep = re.compile(r"(\S)(\1{3,})")

    return re_rep.sub(_replace_rep, text)


def replace_wrep_post(toks: Collection[str]) -> List[str]:
    """
    Replace repetitive words after tokenization;
    fastai `replace_wrep` does not work well with Thai.

    :param list[str] toks: list of tokens

    :return: list of tokens where **xxwrep** token and the counter
             is added before repetitive words.
    :rtype: list[str]

    :Example:

        >>> from pythainlp.ulmfit import replace_wrep_post_nonum
        >>>
        >>> toks = ["กา", "น้ำ", "น้ำ", "น้ำ", "น้ำ"]
        >>> replace_wrep_post(toks)
        ['กา', 'xxwrep', '3', 'น้ำ']

    """
    previous_word = None
    rep_count = 0
    res = []
    for current_word in toks + [_TK_END]:
        if current_word == previous_word:
            rep_count += 1
        elif (current_word != previous_word) & (rep_count > 0):
            res += [_TK_WREP, str(rep_count), previous_word]
            rep_count = 0
        else:
            res.append(previous_word)
        previous_word = current_word
    return res[1:]


def rm_useless_newlines(text: str) -> str:
    "Remove multiple newlines in `text`."

    return re.sub(r"[\n]{2,}", " ", text)


def rm_brackets(text: str) -> str:
    "Remove all empty brackets and artifacts within brackets from `text`."
    # remove empty brackets
    new_line = re.sub(r"\(\)", "", text)
    new_line = re.sub(r"\{\}", "", new_line)
    new_line = re.sub(r"\[\]", "", new_line)
    # brackets with only punctuation marks
    new_line = re.sub(r"\([^a-zA-Z0-9ก-๙]+\)", "", new_line)
    new_line = re.sub(r"\{[^a-zA-Z0-9ก-๙]+\}", "", new_line)
    new_line = re.sub(r"\[[^a-zA-Z0-9ก-๙]+\]", "", new_line)
    # artifacts after (
    new_line = re.sub(
        r"(?<=\()[^a-zA-Z0-9ก-๙]+(?=[a-zA-Z0-9ก-๙])", "", new_line
    )
    new_line = re.sub(
        r"(?<=\{)[^a-zA-Z0-9ก-๙]+(?=[a-zA-Z0-9ก-๙])", "", new_line
    )
    new_line = re.sub(
        r"(?<=\[)[^a-zA-Z0-9ก-๙]+(?=[a-zA-Z0-9ก-๙])", "", new_line
    )
    # artifacts before )
    new_line = re.sub(
        r"(?<=[a-zA-Z0-9ก-๙])[^a-zA-Z0-9ก-๙]+(?=\))", "", new_line
    )
    new_line = re.sub(
        r"(?<=[a-zA-Z0-9ก-๙])[^a-zA-Z0-9ก-๙]+(?=\})", "", new_line
    )
    new_line = re.sub(
        r"(?<=[a-zA-Z0-9ก-๙])[^a-zA-Z0-9ก-๙]+(?=\])", "", new_line
    )
    return new_line


def ungroup_emoji(toks: Collection[str]) -> List[str]:
    """
    Ungroup Zero Width Joiner (ZVJ) Emojis

    See https://emojipedia.org/emoji-zwj-sequence/
    """
    res = []
    for tok in toks:
        if emoji.emoji_count(tok) == len(tok):
            res.extend(list(tok))
        else:
            res.append(tok)
    return res


def lowercase_all(toks: Collection[str]) -> List[str]:
    """
    Lowercase all English words;
    English words in Thai texts don't usually have nuances of capitalization.
    """
    return [tok.lower() for tok in toks]


def replace_rep_nonum(text: str) -> str:
    """
    Replace repetitions at the character level in `text` after the repetition.
    This is done to prevent such case as 'น้อยยยยยยยย' becoming 'น้อ xxrep ย';
    instead it will retain the word as 'น้อย xxrep '

    :param str text: input text to replace character repetition

    :return: text with repetitive token **xxrep** after
             character repetition
    :rtype: str

    :Example:

        >>> from pythainlp.ulmfit import replace_rep_nonum
        >>>
        >>> text = "กาาาาาาา"
        >>> replace_rep_nonum(text)
        'กา xxrep '

    """

    def _replace_rep(m):
        c, _ = m.groups()
        return f"{c} {_TK_REP} "

    re_rep = re.compile(r"(\S)(\1{3,})")
    return re_rep.sub(_replace_rep, text)


def replace_wrep_post_nonum(toks: Collection[str]) -> List[str]:
    """
    Replace reptitive words post tokenization;
    fastai `replace_wrep` does not work well with Thai.

    :param list[str] toks: list of tokens

    :return: list of tokens where **xxwrep** token is added in front of
             repetitive words.
    :rtype: list[str]

    :Example:

        >>> from pythainlp.ulmfit import replace_wrep_post_nonum
        >>>
        >>> toks = ["กา", "น้ำ", "น้ำ", "น้ำ", "น้ำ"]
        >>> replace_wrep_post_nonum(toks)
        ['กา', 'xxwrep', 'น้ำ']

    """
    previous_word = None
    rep_count = 0
    res = []
    for current_word in toks + [_TK_END]:
        if current_word == previous_word:
            rep_count += 1
        elif (current_word != previous_word) & (rep_count > 0):
            res += [_TK_WREP, previous_word]
            rep_count = 0
        else:
            res.append(previous_word)
        previous_word = current_word
    return res[1:]


def remove_space(toks: Collection[str]) -> List[str]:
    """
    Do not include space for bag-of-word models.

    :param list[str] toks: list of tokens

    :return: list of tokens where space tokens (" ") are filtered out
    :rtype: list[str]
    """
    res = []
    for t in toks:
        t = t.strip()
        if t:
            res.append(t)
    return res
