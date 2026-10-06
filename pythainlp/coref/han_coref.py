# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Han-Coref: Thai coreference resolution model."""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from spacy.language import Language

from pythainlp.coref._fastcoref import FastCoref


class HanCoref(FastCoref):
    """Coreference resolver using the Han-Coref model."""

    def __init__(
        self, device: str = "cpu", nlp: Optional[Language] = None
    ) -> None:
        """
        Initialize the Han-Coref resolver.

        :param str device: device to run the model on
            ("cpu", "cuda", and others)
        :param Optional[spacy.language.Language] nlp: spaCy pipeline to use;
            a blank Thai pipeline is created if ``None``
        """
        super().__init__(
            model_name="pythainlp/han-coref-v1.0", device=device, nlp=nlp
        )
