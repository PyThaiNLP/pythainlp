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


class ThFrTranslator:
    """Thai-French Machine Translation

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
        from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

        self.tokenizer_thzh = AutoTokenizer.from_pretrained(pretrained)
        self.model_thzh = AutoModelForSeq2SeqLM.from_pretrained(pretrained)
        if use_gpu:
            self.model_thzh = self.model_thzh.cuda()

    def translate(
        self, text: str, exclude_words: list[str] | None = None
    ) -> str:
        """Translate text from Thai to French

        :param str text: input text in source language
        :param list[str] exclude_words: words to exclude from translation
                                        (optional)
        :return: translated text in target language
        :rtype: str

        :Example:

        Translate text from Thai to French::

            from pythainlp.translate.th_fr import ThFrTranslator

            thfr = ThFrTranslator()

            thfr.translate("ทดสอบระบบ")
            # output: "Test du système."

        Translate text from Thai to French with excluded words::

            thfr.translate("ทดสอบระบบ", exclude_words=["ระบบ"])
            # output: "Test du ระบบ."

        """
        from pythainlp.translate.core import (
            _prepare_text_with_exclusions,
            _restore_excluded_words,
        )

        prepared_text, placeholder_map = _prepare_text_with_exclusions(
            text, exclude_words
        )
        self.translated = self.model_thzh.generate(
            **self.tokenizer_thzh(
                prepared_text, return_tensors="pt", padding=True
            )
        )
        translated_text = [
            self.tokenizer_thzh.decode(t, skip_special_tokens=True)
            for t in self.translated
        ][0]
        return _restore_excluded_words(translated_text, placeholder_map)
