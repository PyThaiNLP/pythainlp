# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

from typing import Optional

from transformers import M2M100ForConditionalGeneration

from .tokenization_small100 import SMALL100Tokenizer


class Small100Translator:
    """Machine Translation using small100 model

    - Huggingface https://huggingface.co/alirezamsh/small100

    :param bool use_gpu : load model using GPU (Default is False)
    """

    def __init__(
        self,
        use_gpu: bool = False,
        pretrained: str = "alirezamsh/small100",
    ) -> None:
        self.pretrained = pretrained
        self.model = M2M100ForConditionalGeneration.from_pretrained(
            self.pretrained
        )
        self.tgt_lang = None
        if use_gpu:
            self.model = self.model.cuda()

    def translate(
        self,
        text: str,
        tgt_lang: str = "en",
        exclude_words: Optional[list[str]] = None,
    ) -> str:
        """Translate text from X to X

        :param str text: input text in source language
        :param str tgt_lang: target language
        :param list[str] exclude_words: words to exclude from translation
                                        (optional)
        :return: translated text in target language
        :rtype: str

        :Example:

        ::

            from pythainlp.translate.small100 import Small100Translator

            mt = Small100Translator()

            # Translate text from Thai to English
            mt.translate("ทดสอบระบบ", tgt_lang="en")
            # output: 'Testing system'

            # Translate text from Thai to Chinese
            mt.translate("ทดสอบระบบ", tgt_lang="zh")
            # output: '系统测试'

            # Translate text from Thai to French
            mt.translate("ทดสอบระบบ", tgt_lang="fr")
            # output: 'Test du système'

            # Translate text from Thai to English with excluded words
            mt.translate("ทดสอบระบบ", tgt_lang="en", exclude_words=["ระบบ"])
            # output: 'Testing ระบบ'

        """
        from pythainlp.translate.core import (
            _prepare_text_with_exclusions,
            _restore_excluded_words,
        )

        if tgt_lang != self.tgt_lang:
            self.tokenizer = SMALL100Tokenizer.from_pretrained(
                self.pretrained, tgt_lang=tgt_lang
            )
            self.tgt_lang = tgt_lang

        prepared_text, placeholder_map = _prepare_text_with_exclusions(
            text, exclude_words
        )
        self.translated = self.model.generate(
            **self.tokenizer(prepared_text, return_tensors="pt")
        )
        translated_text = self.tokenizer.batch_decode(
            self.translated, skip_special_tokens=True
        )[0]
        return _restore_excluded_words(translated_text, placeholder_map)
