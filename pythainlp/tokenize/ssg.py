# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileCopyrightText: Copyright 2019 Ponrawee Prasertsom
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""
Syllable segmentation using bundled SSG CRF weights.

GitHub: https://github.com/ponrawee/ssg
License: Apache-2.0
"""

from __future__ import annotations

import threading
from importlib.resources import as_file, files
from typing import Any, Optional

from pythainlp.tag.crf import CRFTagger
from pythainlp.tokenize.han_solo import Featurizer

__all__: list[str] = ["segment", "syllable_tokenize"]

_tagger: Optional[CRFTagger] = None
_model_file_ctx: Optional[Any] = None
_load_lock: threading.Lock = threading.Lock()
_featurizer: Featurizer = Featurizer(N=3)
_DELIMITER: str = "<SSG_SPECIAL>"


def _get_tagger() -> CRFTagger:
    """Lazy load the SSG tagger model."""
    global _tagger, _model_file_ctx
    if _tagger is None:
        with _load_lock:
            if _tagger is None:
                _tagger = CRFTagger()
                corpus_files = files("pythainlp.corpus")
                model_file = corpus_files.joinpath("ssg.json.gz")
                _model_file_ctx = as_file(model_file)
                model_path = _model_file_ctx.__enter__()
                _tagger.open(str(model_path))
    return _tagger


def _decode(text: str, tags: list[str]) -> list[str]:
    res: list[str] = []
    for char, tag in zip(list(text), tags):
        if tag == "1":
            res.append(_DELIMITER)
        res.append(char)
    return "".join(res).split(_DELIMITER)


def segment(text: str) -> list[str]:
    """
    Tokenize text into syllables using bundled SSG weights.

    :param str text: Thai text to be tokenized into syllables.
    :return: list of syllables
    :rtype: list[str]
    """
    if not text or not isinstance(text, str):
        return []

    tagger = _get_tagger()
    features = _featurizer.featurize(
        text, return_type="list", padding=True, indiv_char=True
    )
    tags = tagger.tag(features["X"])
    return _decode(text, tags)


def syllable_tokenize(text: str) -> list[str]:
    """
    Alias for segment to match the upstream ssg API.

    :param str text: Thai text to be tokenized into syllables.
    :return: List of syllables.
    :rtype: list[str]
    """
    return segment(text)
