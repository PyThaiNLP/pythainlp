# -*- coding: utf-8 -*-
# Copyright (C) 2016-2023 PyThaiNLP Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Where's the Point? Self-Supervised Multilingual Punctuation-Agnostic Sentence Segmentation

GitHub: https://github.com/bminixhofer/wtpsplit
"""
from typing import List
from wtpsplit import WtP

_MODEL = None
_MODEL_NAME = None


def _tokenize(
        text:str,
        lang_code:str="th",
        model:str="wtp-bert-mini",
        tokenize:str="sentence",
        paragraph_threshold:float=0.5,
    )-> List[str]:
    global _MODEL_NAME,_MODEL
    if _MODEL_NAME != model:
        _MODEL = WtP(model_name_or_model=model)
        _MODEL_NAME = model
    if tokenize=="sentence":
        return _MODEL.split(text,lang_code=lang_code)
    else: # Paragraph
        return _MODEL.split(
            text,
            lang_code=lang_code,
            do_paragraph_segmentation=True,
            paragraph_threshold=paragraph_threshold
        )


def tokenize(text:str, size:str="mini", tokenize:str="sentence", paragraph_threshold:float=0.5)-> List[str]:
    _model_load=""
    if size=="tiny":
        _model_load="wtp-bert-tiny"
    elif size=="base":
        _model_load="wtp-canine-s-1l"
    elif size=="large":
        _model_load="wtp-canine-s-12l"
    else:  # mini
        _model_load="wtp-bert-mini"
    return _tokenize(text, model=_model_load,tokenize=tokenize,paragraph_threshold=paragraph_threshold)
