# -*- coding: utf-8 -*-
"""
Linguistic tagger.

Tagging each token in a sentence with supplementary information,
such as its Part-of-Speech (POS) tag, and Named Entity Recognition (NER) tag.
"""

__all__ = ["pos_tag", "pos_tag_sents", "tag_provinces"]

from pythainlp.tag.locations import tag_provinces
from pythainlp.tag.pos_tag import pos_tag
from pythainlp.tag.pos_tag import pos_tag_sents
