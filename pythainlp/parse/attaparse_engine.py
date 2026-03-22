# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Attaparse: Thai dependency parser based on Stanza and PhayaThaiBERT.

GitHub: https://github.com/nlp-chula/attaparse
"""

from __future__ import annotations

from typing import TYPE_CHECKING, List, Union

try:
    from attaparse import depparse, load_model
except ImportError as e:
    raise ImportError(
        "attaparse is not installed. Install it with: pip install attaparse"
    ) from e

if TYPE_CHECKING:
    from stanza import Pipeline


class Parse:
    def __init__(self) -> None:
        self.nlp: Pipeline = load_model()

    def __call__(
        self, text: str, tag: str = "str"
    ) -> Union[List[List[str]], str]:
        doc = depparse(text, self.nlp)
        rows = []
        for sent in doc.sentences:
            for word in sent.words:
                row = [
                    str(word.id),
                    word.text,
                    word.lemma if word.lemma else "_",
                    word.upos if word.upos else "_",
                    word.xpos if word.xpos else "_",
                    word.feats if word.feats else "_",
                    str(word.head),
                    word.deprel if word.deprel else "_",
                    "_",  # DEPS (enhanced dependencies, not provided)
                    "SpaceAfter=No",  # MISC: Thai text has no inter-word spaces
                ]
                rows.append(row)
        if tag == "list":
            return rows
        return "\n".join("\t".join(row) for row in rows)
