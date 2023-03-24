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
from transformers import (
    CamembertTokenizer,
    pipeline,
)
import random
from typing import List

model_name = "airesearch/wangchanberta-base-att-spm-uncased"


class Thai2transformersAug:
    def __init__(self):
        self.model_name = "airesearch/wangchanberta-base-att-spm-uncased"
        self.target_tokenizer = CamembertTokenizer
        self.tokenizer = CamembertTokenizer.from_pretrained(
            self.model_name, revision="main"
        )
        self.tokenizer.additional_special_tokens = [
            "<s>NOTUSED",
            "</s>NOTUSED",
            "<_>",
        ]
        self.fill_mask = pipeline(
            task="fill-mask",
            tokenizer=self.tokenizer,
            model=f"{self.model_name}",
            revision="main",
        )
        self.MASK_TOKEN = self.tokenizer.mask_token

    def generate(self, sentence: str, num_replace_tokens: int = 3):
        self.sent2 = []
        self.input_text = sentence
        sent = [
            i for i in self.tokenizer.tokenize(self.input_text) if i != "▁"
        ]
        if len(sent) < num_replace_tokens:
            num_replace_tokens = len(sent)
        masked_text = self.input_text
        for i in range(num_replace_tokens):
            replace_token = [
                sent.pop(random.randrange(len(sent))) for _ in range(1)
            ][0]
            masked_text = masked_text + self.MASK_TOKEN
            self.sent2 += [
                str(j["sequence"]).replace("<s> ", "").replace("</s>", "")
                for j in self.fill_mask(masked_text)
                if j["sequence"] not in self.sent2
            ]
            masked_text = self.input_text
        return self.sent2

    def augment(self, sentence: str, num_replace_tokens: int = 3) -> List[str]:
        """
        Text Augment from wangchanberta

        :param str sentence: thai sentence
        :param int num_replace_tokens: number replace tokens

        :return: list of text augment
        :rtype: List[str]

        :Example:
        ::

            from pythainlp.augment.lm import Thai2transformersAug

            aug=Thai2transformersAug()

            aug.augment("ช้างมีทั้งหมด 50 ตัว บน")
            # output: ['ช้างมีทั้งหมด 50 ตัว บนโลกใบนี้',
             'ช้างมีทั้งหมด 50 ตัว บนสุด',
             'ช้างมีทั้งหมด 50 ตัว บนบก',
             'ช้างมีทั้งหมด 50 ตัว บนนั้น',
             'ช้างมีทั้งหมด 50 ตัว บนหัว']
        """
        self.sent2 = []
        self.sent2 = self.generate(sentence, num_replace_tokens)
        return self.sent2
