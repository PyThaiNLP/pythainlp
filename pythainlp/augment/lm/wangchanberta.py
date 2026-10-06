# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Augment Thai text using WangchanBERTa."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from transformers import CamembertTokenizer, Pipeline

model_name: str = "airesearch/wangchanberta-base-att-spm-uncased"


class Thai2transformersAug:
    """Augment Thai text using WangchanBERTa."""

    model_name: str
    target_tokenizer: type["CamembertTokenizer"]
    tokenizer: "CamembertTokenizer"
    fill_mask: "Pipeline"
    MASK_TOKEN: str
    input_text: str

    def __init__(self) -> None:
        """Initialize the WangchanBERTa tokenizer and fill-mask pipeline."""
        from transformers import (
            CamembertTokenizer,
            pipeline,
        )

        self.model_name: str = "airesearch/wangchanberta-base-att-spm-uncased"
        self.target_tokenizer: type[CamembertTokenizer] = CamembertTokenizer
        self.tokenizer: CamembertTokenizer = (
            CamembertTokenizer.from_pretrained(
                self.model_name,
                revision="main",  # nosec B615
            )
        )
        self.tokenizer.additional_special_tokens = [
            "<s>NOTUSED",
            "</s>NOTUSED",
            "<_>",
        ]
        self.fill_mask: Pipeline = pipeline(
            task="fill-mask",
            tokenizer=self.tokenizer,
            model=f"{self.model_name}",
            revision="main",
        )
        self.MASK_TOKEN: str = self.tokenizer.mask_token

    def generate(
        self, sentence: str, num_replace_tokens: int = 3
    ) -> list[str]:
        """
        Generate sentences by filling masked tokens.

        :param str sentence: Thai text to augment
        :param int num_replace_tokens: number of tokens to replace
        :return: list of generated sentences
        :rtype: list[str]
        """
        sent2: list[str] = []
        self.input_text: str = sentence
        sent = [
            i for i in self.tokenizer.tokenize(self.input_text) if i != "▁"
        ]
        if len(sent) < num_replace_tokens:
            num_replace_tokens = len(sent)
        masked_text = self.input_text
        for _ in range(num_replace_tokens):
            masked_text = masked_text + self.MASK_TOKEN
            sent2 += [
                str(j["sequence"]).replace("<s> ", "").replace("</s>", "")
                for j in self.fill_mask(masked_text)
                if j["sequence"] not in sent2
            ]
            masked_text = self.input_text
        return sent2

    def augment(self, sentence: str, num_replace_tokens: int = 3) -> list[str]:
        """
        Augment text using WangchanBERTa.

        :param str sentence: Thai text to augment
        :param int num_replace_tokens: number of tokens to replace

        :return: list of augmented sentences
        :rtype: list[str]

        :Example:

            >>> from pythainlp.augment.lm import (
            ...     Thai2transformersAug,
            ... )  # doctest: +SKIP

            >>> aug = Thai2transformersAug()  # doctest: +SKIP

            >>> aug.augment("ช้างมีทั้งหมด 50 ตัว บน")  # doctest: +SKIP
            ['ช้างมีทั้งหมด 50 ตัว บนโลกใบนี้',
             'ช้างมีทั้งหมด 50 ตัว บนสุด',
             'ช้างมีทั้งหมด 50 ตัว บนบก',
             'ช้างมีทั้งหมด 50 ตัว บนนั้น',
             'ช้างมีทั้งหมด 50 ตัว บนหัว']
        """
        sent2 = self.generate(sentence, num_replace_tokens)
        return sent2
