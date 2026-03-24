# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

from typing import TYPE_CHECKING, Optional, TypedDict

if TYPE_CHECKING:
    from fastcoref.modeling import CorefModel
    from fastcoref.modeling import CorefResult as FastCorefResult
    from spacy.language import Language


class CorefResult(TypedDict):
    """Coreference resolution result for a single text."""

    text: str
    clusters_string: list[list[str]]
    clusters: list[list[tuple[int, int]]]


class FastCoref:
    def __init__(
        self,
        model_name: str,
        nlp: Optional[Language] = None,
        device: str = "cpu",
        type: str = "FCoref",
    ) -> None:
        if type == "FCoref":
            from fastcoref import FCoref as _model
        else:
            from fastcoref import LingMessCoref as _model

        if nlp is None:
            import spacy

            nlp = spacy.blank("th")

        self.model_name: str = model_name
        self.nlp: Language = nlp
        self.model: CorefModel = _model(
            self.model_name, device=device, nlp=self.nlp
        )

    def _to_json(self, _predict: "FastCorefResult") -> CorefResult:
        return {
            "text": _predict.text,
            "clusters_string": _predict.get_clusters(as_strings=True),
            "clusters": _predict.get_clusters(as_strings=False),
        }

    def predict(self, texts: list[str]) -> list[CorefResult]:
        return [
            self._to_json(pred) for pred in self.model.predict(texts=texts)
        ]
