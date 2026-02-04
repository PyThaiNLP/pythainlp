# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from spacy.language import Language

from pythainlp.coref._fastcoref import FastCoref


class HanCoref(FastCoref):
    def __init__(
        self, device: str = "cpu", nlp: Optional[Language] = None
    ) -> None:
        super().__init__(
            model_name="pythainlp/han-coref-v1.0", device=device, nlp=nlp
        )
