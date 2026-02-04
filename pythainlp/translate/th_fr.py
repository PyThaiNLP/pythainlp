# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Thai-French Machine Translation

Trained by OPUS Corpus

Model is from Language Technology Research Group at the University of Helsinki

BLEU 20.4

- Huggingface https://huggingface.co/Helsinki-NLP/opus-mt-th-fr
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import torch
    from transformers import AutoModelForSeq2SeqLM, AutoTokenizer


class ThFrTranslator:
    """Thai-French Machine Translation

    Trained by OPUS Corpus

    Model is from Language Technology Research Group at the University of Helsinki

    BLEU 20.4

    - Huggingface https://huggingface.co/Helsinki-NLP/opus-mt-th-fr

    :param bool use_gpu : load model using GPU (Default is False)
    """

    tokenizer_thfr: AutoTokenizer
    model_thfr: AutoModelForSeq2SeqLM
    translated: torch.Tensor

    def __init__(
        self,
        use_gpu: bool = False,
        pretrained: str = "Helsinki-NLP/opus-mt-th-fr",
    ) -> None:
        from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

        self.tokenizer_thfr: AutoTokenizer = AutoTokenizer.from_pretrained(
            pretrained
        )
        self.model_thfr: AutoModelForSeq2SeqLM = (
            AutoModelForSeq2SeqLM.from_pretrained(pretrained)
        )
        if use_gpu:
            self.model_thfr = self.model_thfr.cuda()

    def translate(self, text: str) -> str:
        """Translate text from Thai to French

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
        self.translated: torch.Tensor = self.model_thfr.generate(
            **self.tokenizer_thfr(text, return_tensors="pt", padding=True)
        )
        decoded_list: list[str] = [
            self.tokenizer_thfr.decode(t, skip_special_tokens=True)
            for t in self.translated
        ]
        return decoded_list[0]
