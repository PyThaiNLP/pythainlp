# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations


class FastCoref:
    def __init__(
        self,
        model_name,
        nlp=None,
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

        self.model_name = model_name
        self.nlp = nlp
        self.model = _model(self.model_name, device=device, nlp=self.nlp)

    def _to_json(self, _predict):
        return {
            "text": _predict.text,
            "clusters_string": _predict.get_clusters(as_strings=True),
            "clusters": _predict.get_clusters(as_strings=False),
        }

    def predict(self, texts: list[str]) -> list[dict]:
        return [
            self._to_json(pred) for pred in self.model.predict(texts=texts)
        ]
