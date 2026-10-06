# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Summarize text using the mT5 model."""

from __future__ import annotations

from typing import Optional

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
        pretrained_mt5_model_name: str = "",
        revision: Optional[str] = None,
    ) -> None:
        """
        Initialize the mT5 summarizer.

        :param str model_size: model size, one of ``"small"``, ``"base"``,
            ``"large"``, ``"xl"``, or ``"xxl"`` (default is ``"small"``)
        :param int num_beams: number of beams for beam search (default is 4)
        :param int no_repeat_ngram_size: size of n-grams that must not
            repeat (default is 2)
        :param int min_length: minimum length of the generated summary
            (default is 30)
        :param int max_length: maximum length of the generated summary
            (default is 100)
        :param bool skip_special_tokens: skip special tokens in the output
            (default is True)
        :param str pretrained_mt5_model_name: name of the pretrained model.
            If empty (default), use ``google/mt5-{model_size}``.
        :param Optional[str] revision: git revision id (branch, tag, or
            commit hash). Pin to a full commit hash for secure downloads.
        """
        from transformers import MT5ForConditionalGeneration, T5Tokenizer

        model_name = ""
        if not pretrained_mt5_model_name:
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
        self.model_name: str = model_name
        self.model: MT5ForConditionalGeneration = (
            MT5ForConditionalGeneration.from_pretrained(
                model_name, revision=revision
            )
        )
        self.tokenizer: T5Tokenizer = T5Tokenizer.from_pretrained(
            model_name, revision=revision
        )
        self.num_beams: int = num_beams
        self.no_repeat_ngram_size: int = no_repeat_ngram_size
        self.min_length: int = min_length
        self.max_length: int = max_length
        self.skip_special_tokens: bool = skip_special_tokens

    def summarize(self, text: str) -> list[str]:
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
