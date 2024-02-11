# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0

from typing import List
import random
import re

from pythainlp.phayathaibert.core import ThaiTextProcessor


_MODEL_NAME = "clicknext/phayathaibert"


class ThaiTextAugmenter:
    def __init__(self) -> None:
        from transformers import (
            AutoTokenizer,
            AutoModelForMaskedLM,
            pipeline,
        )

        self.tokenizer = AutoTokenizer.from_pretrained(_MODEL_NAME)
        self.model_for_masked_lm = AutoModelForMaskedLM.from_pretrained(
            _MODEL_NAME
        )
        self.model = pipeline(
            "fill-mask",
            tokenizer=self.tokenizer,
            model=self.model_for_masked_lm,
        )
        self.processor = ThaiTextProcessor()

    def generate(
        self,
        sample_text: str,
        word_rank: int,
        max_length: int = 3,
        sample: bool = False,
    ) -> str:
        sample_txt = sample_text
        final_text = ""

        for j in range(max_length):
            input = self.processor.preprocess(sample_txt)
            if sample:
                random_word_idx = random.randint(0, 4)
                output = self.model(input)[random_word_idx]["sequence"]
            else:
                output = self.model(input)[word_rank]["sequence"]
            sample_txt = output + "<mask>"
            final_text = sample_txt

        gen_txt = re.sub("<mask>", "", final_text)

        return gen_txt

    def augment(
        self, text: str, num_augs: int = 3, sample: bool = False
    ) -> List[str]:
        """
        Text augmentation from PhayaThaiBERT

        :param str text: Thai text
        :param int num_augs: an amount of augmentation text needed as an output
        :param bool sample: whether to sample the text as an output or not, \
                            true if more word diversity is needed

        :return: list of text augment
        :rtype: List[str]

        :Example:
        ::

            from pythainlp.augment.lm import ThaiTextAugmenter

            aug = ThaiTextAugmenter()
            aug.augment("ช้างมีทั้งหมด 50 ตัว บน", num_args=5)

            # output = ['ช้างมีทั้งหมด 50 ตัว บนโลกใบนี้ครับ.',
                'ช้างมีทั้งหมด 50 ตัว บนพื้นดินครับ...',
                'ช้างมีทั้งหมด 50 ตัว บนท้องฟ้าครับ...',
                'ช้างมีทั้งหมด 50 ตัว บนดวงจันทร์.‼',
                'ช้างมีทั้งหมด 50 ตัว บนเขาค่ะ😁']
        """
        MAX_NUM_AUGS = 5
        augment_list = []

        if "<mask>" not in text:
            text = text + "<mask>"

        if num_augs <= MAX_NUM_AUGS:
            for rank in range(num_augs):
                gen_text = self.generate(text, rank, sample=sample)
                processed_text = re.sub(
                    "<_>", " ", self.processor.preprocess(gen_text)
                )
                augment_list.append(processed_text)
        else:
            raise ValueError(
                f"augmentation of more than {num_augs} is exceeded \
                    the default limit: {MAX_NUM_AUGS}"
            )

        return augment_list
