# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Summarization by mT5 model"""

from __future__ import annotations

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
    ) -> None:
        """Initialize mT5 Summarizer.

        :param str model_size: Size of the model ("small", "base", "large",
            "xl", "xxl"). Default is "small".
        :param int num_beams: Number of beams for beam search. Default is 4.
        :param int no_repeat_ngram_size: Size of n-grams to avoid repeating.
            Default is 2.
        :param int min_length: Minimum length of generated summary.
            Default is 30.
        :param int max_length: Maximum length of generated summary.
            Default is 100.
        :param bool skip_special_tokens: Whether to skip special tokens in
            output. Default is True.
        :param str pretrained_mt5_model_name: Name of pretrained model.
            If empty (default), uses google/mt5-{model_size}.
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
            MT5ForConditionalGeneration.from_pretrained(model_name)
        )
        self.tokenizer: T5Tokenizer = T5Tokenizer.from_pretrained(model_name)
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
