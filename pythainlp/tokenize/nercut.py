# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""nercut 0.2

Word segmentation from a named entity tagger,
combining tokens that are parts of the same named entity.

Code by Wannaphong Phatthiyaphaibun
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterable

from pythainlp.tag.named_entity import NER

_thainer: NER = NER(engine="thainer")


def _combine_step(
    curr_word: str,
    curr_tag: str,
    combining_word: str,
    taglist: Iterable[str],
) -> tuple[str, list[str]]:
    """Process one tagged token.

    :return: the updated combining word, and the words to emit
    """
    tag = curr_tag[2:] if curr_tag != "O" else "O"

    if curr_tag.startswith("B-") and tag in taglist:
        return curr_word, []
    if curr_tag.startswith("I-") and combining_word != "" and tag in taglist:
        return combining_word + curr_word, []
    if curr_tag == "O" and combining_word != "":
        return "", [combining_word, curr_word]
    return "", [curr_word]


def segment(
    text: str,
    taglist: Iterable[str] = [
        "ORGANIZATION",
        "PERSON",
        "PHONE",
        "EMAIL",
        "DATE",
        "TIME",
    ],
    tagger: NER = _thainer,
) -> list[str]:
    """Word segmentation that merges tokens of the same named entity.

    :param str text: text to be tokenized into words
    :param Iterable[str] taglist: named entity tags to merge
    :param pythainlp.tag.NER tagger: named entity tagger
    :return: list of words, tokenized from the text
    """
    if not text:
        return []

    tagged_words = tagger.tag(text, pos=False)

    words: list[str] = []
    combining_word = ""
    for idx, (curr_word, curr_tag) in enumerate(tagged_words):
        combining_word, emitted = _combine_step(
            curr_word, curr_tag, combining_word, taglist
        )
        words.extend(emitted)
        # flush the pending entity at the end of the text
        if (
            idx + 1 == len(tagged_words)
            and curr_tag.startswith(("B-", "I-"))
            and combining_word != ""
        ):
            words.append(combining_word)

    return words
