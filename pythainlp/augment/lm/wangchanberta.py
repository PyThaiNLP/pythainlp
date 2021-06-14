# -*- coding: utf-8 -*-

# transformers
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
                                    self.model_name,
                                    revision='main')
        self.tokenizer.additional_special_tokens = [
            '<s>NOTUSED',
            '</s>NOTUSED',
            '<_>'
        ]
        self.fill_mask = pipeline(
            task='fill-mask',
            tokenizer=self.tokenizer,
            model=f'{self.model_name}',
            revision='main'
        )

    def generate(self, sentence: str, num_replace_tokens: int = 3):
        self.sent2 = []
        self.input_text = sentence
        sent = [
            i for i in self.tokenizer.tokenize(self.input_text) if i != '▁'
        ]
        if len(sent) < num_replace_tokens:
            num_replace_tokens = len(sent)
        masked_text = self.input_text
        for i in range(num_replace_tokens):
            replace_token = [
                sent.pop(random.randrange(len(sent))) for _ in range(1)
            ][0]
            masked_text = masked_text.replace(
                replace_token, f"{self.fill_mask.tokenizer.mask_token}", 1
            )
            self.sent2 += [
                str(j['sequence']).replace('<s> ', '').replace('</s>', '')
                for j in self.fill_mask(masked_text+'<pad>')
                if j['sequence'] not in self.sent2
            ]
            masked_text = self.input_text
        return self.sent2

    def augment(
        self, sentence: str, num_replace_tokens: int = 3
    ) -> List[str]:
        """
        Text Augment from wangchanberta

        :param str sentence: thai sentence
        :param int num_replace_tokens: number replace tokens

        :return: list of text augment
        :rtype: List[str]
        """
        self.sent2 = []
        try:
            self.sent2 = self.generate(sentence, num_replace_tokens)
            if self.sent2 == []:
                self.sent2 = self.generate(sentence, num_replace_tokens)
            return self.sent2
        except:
            if len(self.sent2) > 0:
                return self.sent2
            else:
                return self.sent2
