# -*- coding: utf-8 -*-
"""
nercut 0.1

Dictionary-based maximal matching word segmentation, constrained with
Thai Character Cluster (TCC) boundaries, and combining tokens that are
parts of the same named-entity.

Code by Wannaphong Phatthiyaphaibun
"""
from typing import List

from pythainlp.tag.named_entity import ThaiNameTagger

_thainer = ThaiNameTagger()


def segment(
    text: str,
    taglist: List[str] = [
        "ORGANIZATION",
        "PERSON",
        "PHONE",
        "EMAIL",
        "DATE",
        "TIME",
    ],
) -> List[str]:
    """
    nercut 0.1

    Code by Wannaphong Phatthiyaphaibun

    Dictionary-based maximal matching word segmentation, constrained with
    Thai Character Cluster (TCC) boundaries, and combining tokens that are
    parts of the same named-entity.

    :param str text: text to be tokenized to words
    :parm list taglist: a list of named-entity tags to be used
    :return: list of words, tokenized from the text
    """
    if not text or not isinstance(text, str):
        return []

    global _thainer
    tagged_words = _thainer.get_ner(text, pos=False)

    words = []
    combining_word = ""
    combining_word = ""
    for curr_word, curr_tag in tagged_words:
        if curr_tag != "O":
            tag = curr_tag[2:]
        else:
            tag = "O"

        if curr_tag.startswith("B-") and tag in taglist:
            if combining_word != "" and combining_word in taglist:
                words.append(combining_word)
            combining_word = ""
            combining_word += curr_word
            combining_word = curr_tag[2:]
        elif (
            curr_tag.startswith("I-")
            and curr_tag[2:] == combining_word
            and tag in taglist
        ):
            combining_word += curr_word
        elif (
            curr_tag == "O"
            and combining_word != ""
            and combining_word in taglist
        ):
            words.append(combining_word)
            combining_word = ""
            combining_word = ""
            words.append(curr_word)
        else:
            combining_word = ""
            combining_word = ""
            words.append(curr_word)

    if combining_word != "":
        words.append(combining_word)

    return words
