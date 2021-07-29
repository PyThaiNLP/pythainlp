# -*- coding: utf-8 -*-
from tltk.nlp import pos_tag_wordlist
from typing import List, Tuple


def pos_tag(words: List[str], corpus: str = "tnc") -> List[Tuple[str, str]]:
    if corpus != "tnc":
        raise NotImplemented("tltk not support {0} corpus.".format(0))
    return pos_tag_wordlist(words)
