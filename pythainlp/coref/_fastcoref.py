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
import spacy


class FastCoref:
    def __init__(self, model_name, nlp=spacy.blank("th"), device="cpu", type="FCoref") -> None:
        if type == "FCoref":
            from fastcoref import FCoref as _model
        else:
            from fastcoref import LingMessCoref as _model
        self.model_name = model_name
        self.nlp = nlp
        self.model = _model(self.model_name,device=device,nlp=self.nlp)
    
    def predict(self, texts:list):
        return self.model.predict(texts=texts)
