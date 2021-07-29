# -*- coding: utf-8 -*-
from tltk import nlp
from typing import List, Tuple

nlp.pos_load()


def pos_tag(words: List[str], corpus: str = "tnc") -> List[Tuple[str, str]]:
    if corpus != "tnc":
        raise NotImplemented("tltk not support {0} corpus.".format(0))
    return nlp.pos_tag_wordlist(words)
