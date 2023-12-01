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
from typing import List, Tuple, Union
import re
import warnings
from transformers import (
    CamembertTokenizer,
)


_model_name = "clicknext/phayathaibert"
_tokenizer = CamembertTokenizer.from_pretrained(_model_name)


class PartOfSpeechTagger:
    def __init__(self, model: str="lunarlist/pos_thai_phayathai") -> None:
        # Load model directly
        from transformers import (
            AutoTokenizer, 
            AutoModelForTokenClassification,
        )
        self.tokenizer = AutoTokenizer.from_pretrained(model)
        self.model = AutoModelForTokenClassification.from_pretrained(model)

    def get_tag(self, sentence: str, strategy: str='simple')->List[List[Tuple[str, str]]]:
        from transformers import TokenClassificationPipeline
        pipeline = TokenClassificationPipeline(
            model=self.model, 
            tokenizer=self.tokenizer, 
            aggregation_strategy=strategy,
        )
        outputs = pipeline(sentence)
        word_tags = [[(tag['word'], tag['entity_group']) for tag in outputs]]
        return word_tags
    
def segment(sentence: str)->List[str]:
    if not sentence or not isinstance(sentence, str):
        return []

    return _tokenizer.tokenize(sentence)