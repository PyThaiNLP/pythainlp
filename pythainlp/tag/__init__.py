# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Linguistic and other taggers.

Tagging each token in a sentence with supplementary information,
such as its part-of-speech (POS) tag, and named entity (NE) tag.

.. note::
    :func:`chunk_parse` has moved to :mod:`pythainlp.chunk`.
    Importing it from :mod:`pythainlp.tag` still works but emits a
    :class:`DeprecationWarning` and will be removed in 6.0.
"""

__all__: list[str] = [
    "EntitySpan",
    "NER",
    "NNER",
    "PerceptronTagger",
    "chunk_parse",
    "pos_tag",
    "pos_tag_sents",
    "pos_tag_transformers",
    "tag_provinces",
]

from pythainlp.tag._tag_perceptron import PerceptronTagger
from pythainlp.tag.chunk import chunk_parse
from pythainlp.tag.locations import tag_provinces
from pythainlp.tag.named_entity import NER, NNER, EntitySpan
from pythainlp.tag.pos_tag import pos_tag, pos_tag_sents, pos_tag_transformers
