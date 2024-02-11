# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0

from typing import List

from transformers import (
    CamembertTokenizer,
    pipeline,
)

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
        Text augmentation from WangchanBERTa

        :param str sentence: Thai sentence
        :param int num_replace_tokens: number replace tokens

        :return: list of text augment
        :rtype: List[str]

        :Example:
        ::

            from pythainlp.augment.lm import Thai2transformersAug

            aug = Thai2transformersAug()

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
