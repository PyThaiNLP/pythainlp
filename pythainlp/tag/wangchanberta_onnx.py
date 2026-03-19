# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any, Union

if TYPE_CHECKING:
    import numpy as np
    import sentencepiece as spm
    from onnxruntime import InferenceSession, SessionOptions

from pythainlp.corpus import get_corpus_path
from pythainlp.tools import safe_path_join


class WngchanBerta_ONNX:
    """WangchanBERTa NER engine with ONNX Runtime backend"""

    model_name: str
    model_version: str
    options: "SessionOptions"
    session: "InferenceSession"
    outputs_name: str
    sp: "spm.SentencePieceProcessor"
    _json: dict[str, Any]
    id2tag: dict[str, str]
    _s: dict[str, "np.ndarray"]

    def __init__(
        self,
        model_name: str,
        model_version: str,
        file_onnx: str,
        providers: list[str] = ["CPUExecutionProvider"],
    ) -> None:
        import sentencepiece as spm
        from onnxruntime import (
            GraphOptimizationLevel,
            InferenceSession,
            SessionOptions,
        )

        self.model_name = model_name
        self.model_version = model_version
        self.options = SessionOptions()
        self.options.graph_optimization_level = (
            GraphOptimizationLevel.ORT_ENABLE_ALL
        )
        _corpus_base = get_corpus_path(self.model_name, self.model_version)
        if not _corpus_base:
            raise FileNotFoundError(self.model_name)
        self.session = InferenceSession(
            safe_path_join(_corpus_base, file_onnx),
            sess_options=self.options,
            providers=providers,
        )
        self.session.disable_fallback()
        self.outputs_name = self.session.get_outputs()[0].name
        self.sp = spm.SentencePieceProcessor(
            model_file=safe_path_join(_corpus_base, "sentencepiece.bpe.model")
        )
        with open(
            safe_path_join(_corpus_base, "config.json"),
            encoding="utf-8-sig",
        ) as fh:
            self._json = json.load(fh)
            self.id2tag = self._json["id2label"]

    def build_tokenizer(self, sent: str) -> dict[str, "np.ndarray"]:
        import numpy as np

        _t = [5] + [i + 4 for i in self.sp.encode(sent)] + [6]
        model_inputs = {}
        model_inputs["input_ids"] = np.array([_t], dtype=np.int64)
        model_inputs["attention_mask"] = np.array(
            [[1] * len(_t)], dtype=np.int64
        )
        return model_inputs

    def postprocess(self, logits_data: "np.ndarray") -> "np.ndarray":
        import numpy as np

        logits_t = logits_data[0]
        maxes = np.max(logits_t, axis=-1, keepdims=True)
        shifted_exp = np.exp(logits_t - maxes)
        scores = shifted_exp / shifted_exp.sum(axis=-1, keepdims=True)
        return scores

    def clean_output(self, list_text: list[tuple[str, str]]) -> list[tuple[str, str]]:
        return list_text

    def totag(self, post: np.ndarray, sent: str) -> list[tuple[str, str]]:
        tag = []
        _s = self.sp.EncodeAsPieces(sent)
        for i in range(len(_s)):
            tag.append(
                (
                    _s[i],
                    self.id2tag[str(list(post[i + 1]).index(max(list(post[i + 1]))))],
                )
            )
        return tag

    def _config(self, list_ner: list[tuple[str, str]]) -> list[tuple[str, str]]:
        return list_ner

    def get_ner(
        self, text: str, tag: bool = False
    ) -> Union[str, list[tuple[str, str]]]:
        self._s: dict[str, "np.ndarray"] = self.build_tokenizer(text)
        logits = self.session.run(output_names=[self.outputs_name], input_feed=self._s)[
            0
        ]
        _tag = self.clean_output(self.totag(self.postprocess(logits), text))
        if tag:
            _tag = self._config(_tag)
            temp = ""
            sent = ""
            for idx, (word, ner) in enumerate(_tag):
                if ner.startswith("B-") and temp != "":
                    sent += "</" + temp + ">"
                    temp = ner[2:]
                    sent += "<" + temp + ">"
                elif ner.startswith("B-"):
                    temp = ner[2:]
                    sent += "<" + temp + ">"
                elif ner == "O" and temp != "":
                    sent += "</" + temp + ">"
                    temp = ""
                sent += word

                if idx == len(_tag) - 1 and temp != "":
                    sent += "</" + temp + ">"

            return sent
        else:
            return _tag
