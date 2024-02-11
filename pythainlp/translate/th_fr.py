# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
"""
Thai-French Machine Translation

Trained by OPUS Corpus

Model is from Language Technology Research Group at the University of Helsinki

BLEU 20.4

- Huggingface https://huggingface.co/Helsinki-NLP/opus-mt-th-fr
"""
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


class ThFrTranslator:
    """
    Thai-French Machine Translation

    Trained by OPUS Corpus

    Model is from Language Technology Research Group at the University of Helsinki

    BLEU 20.4

    - Huggingface https://huggingface.co/Helsinki-NLP/opus-mt-th-fr

    :param bool use_gpu : load model using GPU (Default is False)
    """

    def __init__(
        self,
        use_gpu: bool = False,
        pretrained: str = "Helsinki-NLP/opus-mt-th-fr",
    ) -> None:
        self.tokenizer_thzh = AutoTokenizer.from_pretrained(pretrained)
        self.model_thzh = AutoModelForSeq2SeqLM.from_pretrained(pretrained)
        if use_gpu:
            self.model_thzh = self.model_thzh.cuda()

    def translate(self, text: str) -> str:
        """
        Translate text from Thai to French

        :param str text: input text in source language
        :return: translated text in target language
        :rtype: str

        :Example:

        Translate text from Thai to French::

            from pythainlp.translate.th_fr import ThFrTranslator

            thfr = ThFrTranslator()

            thfr.translate("ทดสอบระบบ")
            # output: "Test du système."

        """
        self.translated = self.model_thzh.generate(
            **self.tokenizer_thzh(text, return_tensors="pt", padding=True)
        )
        return [
            self.tokenizer_thzh.decode(t, skip_special_tokens=True)
            for t in self.translated
        ][0]
