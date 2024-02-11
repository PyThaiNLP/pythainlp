# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
import spacy
from pythainlp.coref._fastcoref import FastCoref


class HanCoref(FastCoref):
    def __init__(self, device: str = "cpu", nlp=spacy.blank("th")) -> None:
        super().__init__(
            model_name="pythainlp/han-coref-v1.0", device=device, nlp=nlp
        )
