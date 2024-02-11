# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
from typing import List
import json

import numpy as np
from pythainlp.corpus import get_path_folder_corpus


class WngchanBerta_ONNX:
    def __init__(
        self,
        model_name: str,
        model_version: str,
        file_onnx: str,
        providers: List[str] = ["CPUExecutionProvider"],
    ) -> None:
        import sentencepiece as spm
        from onnxruntime import (
            InferenceSession,
            SessionOptions,
            GraphOptimizationLevel,
        )

        self.model_name = model_name
        self.model_version = model_version
        self.options = SessionOptions()
        self.options.graph_optimization_level = (
            GraphOptimizationLevel.ORT_ENABLE_ALL
        )
        self.session = InferenceSession(
            get_path_folder_corpus(
                self.model_name, self.model_version, file_onnx
            ),
            sess_options=self.options,
            providers=providers,
        )
        self.session.disable_fallback()
        self.outputs_name = self.session.get_outputs()[0].name
        self.sp = spm.SentencePieceProcessor(
            model_file=get_path_folder_corpus(
                self.model_name, self.model_version, "sentencepiece.bpe.model"
            )
        )
        with open(
            get_path_folder_corpus(
                self.model_name, self.model_version, "config.json"
            ),
            encoding="utf-8-sig",
        ) as fh:
            self._json = json.load(fh)
            self.id2tag = self._json["id2label"]

    def build_tokenizer(self, sent):
        _t = [5] + [i + 4 for i in self.sp.encode(sent)] + [6]
        model_inputs = {}
        model_inputs["input_ids"] = np.array([_t], dtype=np.int64)
        model_inputs["attention_mask"] = np.array(
            [[1] * len(_t)], dtype=np.int64
        )
        return model_inputs

    def postprocess(self, logits_data):
        logits_t = logits_data[0]
        maxes = np.max(logits_t, axis=-1, keepdims=True)
        shifted_exp = np.exp(logits_t - maxes)
        scores = shifted_exp / shifted_exp.sum(axis=-1, keepdims=True)
        return scores

    def clean_output(self, list_text):
        return list_text

    def totag(self, post, sent):
        tag = []
        _s = self.sp.EncodeAsPieces(sent)
        for i in range(len(_s)):
            tag.append(
                (
                    _s[i],
                    self.id2tag[
                        str(list(post[i + 1]).index(max(list(post[i + 1]))))
                    ],
                )
            )
        return tag

    def _config(self, list_ner):
        return list_ner

    def get_ner(self, text: str, tag: bool = False):
        self._s = self.build_tokenizer(text)
        logits = self.session.run(
            output_names=[self.outputs_name], input_feed=self._s
        )[0]
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
