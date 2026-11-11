# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Thai NLP functions using TLTK models re-implemented in pure Python."""

from __future__ import annotations

import re
from typing import Optional, Union

from pythainlp.corpus import corpus_path
from pythainlp.tag._tag_perceptron import PerceptronTagger
from pythainlp.tag._utils import _iob_to_markup
from pythainlp.tag.crf import CRFTagger
from pythainlp.tokenize import word_tokenize
from pythainlp.tools.path import safe_path_join

_POS_MODEL_PATH: str = safe_path_join(corpus_path(), "tltk_pos_tnc.json.gz")
_NER_MODEL_PATH: str = safe_path_join(corpus_path(), "tltk_ner.json.gz")

_TAGGER: Optional[PerceptronTagger] = None
_NER_TAGGER: Optional[CRFTagger] = None


def _get_pos_tagger() -> PerceptronTagger:
    global _TAGGER
    if _TAGGER is None:
        _TAGGER = PerceptronTagger(path=_POS_MODEL_PATH)
    return _TAGGER


def _get_ner_tagger() -> CRFTagger:
    global _NER_TAGGER
    if _NER_TAGGER is None:
        _NER_TAGGER = CRFTagger()
        _NER_TAGGER.open(_NER_MODEL_PATH)
    return _NER_TAGGER


def _change_tag(w: str, pos: str) -> str:
    if re.match(r"[\#\+\-\_\=\*\&\^\%\$\@\}\{\]\[\<\>\/]$", w):
        return "SYM"
    if re.match(r"[\,\;\:\.\(\)\'\"\!\?]$", w):
        return "PUNCT"
    if re.match(r"[0-9][0-9.,\+\-\*\/]*$", w):
        return "NUM"
    if re.match(r"<s/>$", w):
        return "PUNCT"
    if re.match(r"[\<\>a-zA-Z\/]+$", w):
        return "SYM"
    if re.match(r"[a-zA-Z0-9_]+$", w):
        return "X"
    return pos


def _wrd_len(word: str) -> str:
    if len(word) > 20:
        return "l"
    if len(word) > 10:
        return "m"
    return "s"


def _word2features(
    sent: list[tuple[str, str]], i: int
) -> dict[str, Union[float, str, bool]]:
    word, postag = sent[i][0], sent[i][1]
    features: dict[str, Union[float, str, bool]] = {
        "bias": 1.0,
        "word": word,
        "postag": postag,
        "len": _wrd_len(word),
    }
    if i > 0:
        features["-1:word"] = sent[i - 1][0]
        features["-1:postag"] = sent[i - 1][1]
    else:
        features["BOS"] = True
    if i > 2:
        features["-2:word"] = sent[i - 2][0]
        features["-2:postag"] = sent[i - 2][1]
    if i < len(sent) - 1:
        features["+1:word"] = sent[i + 1][0]
        features["+1:postag"] = sent[i + 1][1]
    else:
        features["EOS"] = True
    return features


def pos_tag(words: list[str], corpus: str = "tnc") -> list[tuple[str, str]]:
    """
    Tag part-of-speech (POS) in a list of words using **TLTK**.

    :param list[str] words: list of words
    :param str corpus: corpus used to train the tagger; only
        ``"tnc"`` is supported
    :return: list of tuples (word, POS tag)
    :rtype: list[tuple[str, str]]
    :raises ValueError: if the corpus is not supported
    """
    if corpus != "tnc":
        raise ValueError(f"tltk not support {corpus!r} corpus.")
    tagger = _get_pos_tagger()
    return [(w, _change_tag(w, pos)) for w, pos in tagger.tag(words)]


def _post_process(text: str) -> str:
    return text.replace("<s/>", " ")


def get_ner(
    text: str, pos: bool = True, tag: bool = False
) -> Union[list[tuple[str, str]], list[tuple[str, str, str]], str]:
    """
    Tag named entities in text using **TLTK**.

    This function tags named entities in text in IOB format.

    :param str text: Thai text to be tagged
    :param bool pos: include POS tags in the results (``True``, default)
        or exclude them (``False``)
    :param bool tag: return the text with HTML-like tags
        instead of a list of tuples
    :return: list of tuples of word, POS tag (if ``pos`` is ``True``),
        and named entity tag; or the text with HTML-like tags
        (if ``tag`` is ``True``)
    :rtype: Union[list[tuple[str, str]], list[tuple[str, str, str]], str]
    :Example:

        >>> from pythainlp.tag.tltk import get_ner
        >>> get_ner("เขาเรียนที่โรงเรียนนางรอง")
        [('เขา', 'PRON', 'O'), ('เรียน', 'VERB', 'O'), ('ที่', 'SCONJ', 'O'), ('โรงเรียน', 'NOUN', 'B-L'), ('นางรอง', 'VERB', 'I-L')]
        >>> get_ner("เขาเรียนที่โรงเรียนนางรอง", pos=False)
        [('เขา', 'O'), ('เรียน', 'O'), ('ที่', 'O'), ('โรงเรียน', 'B-L'), ('นางรอง', 'I-L')]
        >>> get_ner("เขาเรียนที่โรงเรียนนางรอง", tag=True)
        'เขาเรียนที่<L>โรงเรียนนางรอง</L>'
    """
    if not text:
        return []
    list_word = ["<s/>" if i == " " else i for i in word_tokenize(text, engine="newmm")]
    tagged_pos = pos_tag(list_word)
    features = [_word2features(tagged_pos, i) for i in range(len(tagged_pos))]
    ner_labels = _get_ner_tagger().tag(features)
    sent_ner = [
        (_post_process(word), p, n) for (word, p), n in zip(tagged_pos, ner_labels)
    ]
    if tag:
        return _iob_to_markup([(word, ner) for word, _, ner in sent_ner])
    if pos is False:
        return [(word, ner) for word, pos, ner in sent_ner]
    return sent_ner
