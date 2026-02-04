# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    import torch
    from transformers import M2M100ForConditionalGeneration

from .tokenization_small100 import SMALL100Tokenizer


class Small100Translator:
    """Machine Translation using small100 model

    - Huggingface https://huggingface.co/alirezamsh/small100

    :param bool use_gpu : load model using GPU (Default is False)
    """

    pretrained: str
    model: "M2M100ForConditionalGeneration"
    tgt_lang: Optional[str]
    tokenizer: "SMALL100Tokenizer"
    translated: "torch.Tensor"

    def __init__(
        self,
        use_gpu: bool = False,
        pretrained: str = "alirezamsh/small100",
    ) -> None:
        from transformers import M2M100ForConditionalGeneration

        self.pretrained: str = pretrained
        self.model: "M2M100ForConditionalGeneration" = M2M100ForConditionalGeneration.from_pretrained(
            self.pretrained
        )
        self.tgt_lang: Optional[str] = None
        if use_gpu:
            self.model: "M2M100ForConditionalGeneration" = self.model.cuda()

    def translate(self, text: str, tgt_lang: str = "en") -> str:
        """Translate text from X to X

        :param str text: input text in source language
        :param str tgt_lang: target language
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

        """
        if tgt_lang != self.tgt_lang:
            self.tokenizer: SMALL100Tokenizer = SMALL100Tokenizer.from_pretrained(
                self.pretrained, tgt_lang=tgt_lang
            )
            self.tgt_lang: str = tgt_lang
        self.translated: torch.Tensor = self.model.generate(
            **self.tokenizer(text, return_tensors="pt")
        )
        decoded_list: list[str] = self.tokenizer.batch_decode(
            self.translated, skip_special_tokens=True
        )
        return decoded_list[0]
