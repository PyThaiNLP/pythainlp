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
from typing import List
import re
import random
from pythainlp.phayathaibert.core import ThaiTextProcessor


_model_name = "clicknext/phayathaibert"

class ThaiTextAugmenter:
    def __init__(self,)->None:
        from transformers import (AutoTokenizer, 
                                  AutoModelForMaskedLM, 
                                  pipeline,)
        self.tokenizer = AutoTokenizer.from_pretrained(_model_name)
        self.model_for_masked_lm = AutoModelForMaskedLM.from_pretrained(_model_name)
        self.model = pipeline("fill-mask", tokenizer=self.tokenizer, model=self.model_for_masked_lm)
        self.processor = ThaiTextProcessor()

    def generate(self,
                 sample_text: str, 
                 word_rank: int, 
                 max_length: int=3,
                 sample: bool=False
                 )->str:
        sample_txt = sample_text
        final_text = ""
        for j in range(max_length):
            input = self.processor.preprocess(sample_txt)
            if sample:
                random_word_idx = random.randint(0, 4)
                output = self.model(input)[random_word_idx]['sequence']
            else:
                output = self.model(input)[word_rank]['sequence']
            sample_txt = output+"<mask>"
            final_text = sample_txt

        gen_txt = re.sub("<mask>","",final_text)
        return gen_txt
    

    def augment(self,
                text: str, 
                num_augs: int=3, 
                sample: bool=False)->List[str]:
        augment_list = []
        if "<mask>" not in text:
            text = text+"<mask>" 
        if num_augs <= 5:
            for rank in range(num_augs):
                gen_text = self.generate(text, rank, sample=sample)
                processed_text = re.sub("<_>", " ", self.processor.preprocess(gen_text))
                augment_list.append(processed_text)

            return augment_list
        else:
            raise ValueError(
                f"augmentation of more than {num_augs} is exceeded the default limit"
            )

