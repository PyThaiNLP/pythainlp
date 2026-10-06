# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""
Translate Thai to French using a Helsinki-NLP model.

The model is trained on the OPUS corpus. It is from the Language
Technology Research Group at the University of Helsinki.

BLEU 20.4

- Hugging Face: https://huggingface.co/Helsinki-NLP/opus-mt-th-fr
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    import torch
    from transformers import AutoModelForSeq2SeqLM, AutoTokenizer


class ThFrTranslator:
    """
    Translate Thai to French.

    The model is trained on the OPUS corpus. It is from the Language
    Technology Research Group at the University of Helsinki.

    BLEU 20.4

    - Hugging Face: https://huggingface.co/Helsinki-NLP/opus-mt-th-fr

    :param bool use_gpu: load the model on a GPU (default: False)
    """

    tokenizer_thfr: AutoTokenizer
    model_thfr: AutoModelForSeq2SeqLM
    translated: torch.Tensor

    def __init__(
        self,
        use_gpu: bool = False,
        pretrained: str = "Helsinki-NLP/opus-mt-th-fr",
        revision: Optional[str] = None,
    ) -> None:
        """
        Initialize the Thai-to-French translator.

        :param bool use_gpu: load the model on a GPU
        :param str pretrained: name of the pretrained model
        :param Optional[str] revision: revision of the pretrained model
        """
        from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

        self.tokenizer_thfr: AutoTokenizer = AutoTokenizer.from_pretrained(
            pretrained, revision=revision
        )
        self.model_thfr: AutoModelForSeq2SeqLM = (
            AutoModelForSeq2SeqLM.from_pretrained(
                pretrained, revision=revision
            )
        )
        if use_gpu:
            self.model_thfr = self.model_thfr.cuda()

    def translate(
        self, text: str, exclude_words: Optional[list[str]] = None
    ) -> str:
        """
        Translate text from Thai to French.

        :param str text: text to translate
        :param Optional[list[str]] exclude_words: words to exclude from
            translation
        :return: translated text
        :rtype: str

        :Example:

        Translate text from Thai to French:

            >>> from pythainlp.translate.th_fr import (
            ...     ThFrTranslator,
            ... )  # doctest: +SKIP

            >>> thfr = ThFrTranslator()  # doctest: +SKIP

            >>> thfr.translate("ทดสอบระบบ")  # doctest: +SKIP
            "Test du système."

        Translate text from Thai to French with excluded words:

            >>> thfr.translate(
            ...     "ทดสอบระบบ", exclude_words=["ระบบ"]
            ... )  # doctest: +SKIP
            "Test du ระบบ."

        """
        from pythainlp.translate.core import (
            _prepare_text_with_exclusions,
            _restore_excluded_words,
        )

        prepared_text, placeholder_map = _prepare_text_with_exclusions(
            text, exclude_words
        )
        self.translated: torch.Tensor = self.model_thfr.generate(
            **self.tokenizer_thfr(
                prepared_text, return_tensors="pt", padding=True
            )
        )
        translated_text = [
            self.tokenizer_thfr.decode(t, skip_special_tokens=True)
            for t in self.translated
        ][0]
        return _restore_excluded_words(translated_text, placeholder_map)
