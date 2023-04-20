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
Summarization by mT5 model
"""
from transformers import T5Tokenizer, MT5ForConditionalGeneration
from typing import List

from pythainlp.summarize import CPE_KMUTT_THAI_SENTENCE_SUM


class mT5Summarizer:
    def __init__(
        self,
        model_size: str = "small",
        num_beams: int = 4,
        no_repeat_ngram_size: int = 2,
        min_length: int = 30,
        max_length: int = 100,
        skip_special_tokens: bool = True,
        pretrained_mt5_model_name: str = None,
    ):
        model_name = ""
        if pretrained_mt5_model_name is None:
            if model_size not in ["small", "base", "large", "xl", "xxl"]:
                raise ValueError(
                    f"""model_size \"{model_size}\" not found.
                    It might be a typo; if not, please consult our document."""
                )
            model_name = f"google/mt5-{model_size}"
        else:
            if pretrained_mt5_model_name == CPE_KMUTT_THAI_SENTENCE_SUM:
                model_name = f"thanathorn/{CPE_KMUTT_THAI_SENTENCE_SUM}"
            else:
                model_name = pretrained_mt5_model_name
        self.model_name = model_name
        self.model = MT5ForConditionalGeneration.from_pretrained(model_name)
        self.tokenizer = T5Tokenizer.from_pretrained(model_name)
        self.num_beams = num_beams
        self.no_repeat_ngram_size = no_repeat_ngram_size
        self.min_length = min_length
        self.max_length = max_length
        self.skip_special_tokens = skip_special_tokens

    def summarize(self, text: str) -> List[str]:
        preprocess_text = text.strip().replace("\n", "")
        if self.model_name == f"thanathorn/{CPE_KMUTT_THAI_SENTENCE_SUM}":
            t5_prepared_Text = "simplify: " + preprocess_text
        else:
            t5_prepared_Text = "summarize: " + preprocess_text
        tokenized_text = self.tokenizer.encode(
            t5_prepared_Text, return_tensors="pt"
        )
        summary_ids = self.model.generate(
            tokenized_text,
            num_beams=self.num_beams,
            no_repeat_ngram_size=self.no_repeat_ngram_size,
            min_length=self.min_length,
            max_length=self.max_length,
            early_stopping=True,
        )
        output = self.tokenizer.decode(
            summary_ids[0], skip_special_tokens=self.skip_special_tokens
        )
        return [output]
