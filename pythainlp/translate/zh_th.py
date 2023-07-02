# -*- coding: utf-8 -*-
# Copyright (C) 2016-2023 PyThaiNLP Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Lalita Chinese-Thai Machine Translation

from AI builder

- GitHub: https://github.com/LalitaDeelert/lalita-mt-zhth
- Facebook post https://web.facebook.com/aibuildersx/posts/166736255494822
"""
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


class ThZhTranslator:
    """
    Thai-Chinese Machine Translation

    from Lalita @ AI builder

    - GitHub: https://github.com/LalitaDeelert/lalita-mt-zhth
    - Facebook post https://web.facebook.com/aibuildersx/posts/166736255494822

    :param bool use_gpu : load model to gpu (Default is False)
    """

    def __init__(
        self,
        use_gpu: bool = False,
        pretrained: str = "Lalita/marianmt-th-zh_cn",
    ) -> None:
        self.tokenizer_thzh = AutoTokenizer.from_pretrained(pretrained)
        self.model_thzh = AutoModelForSeq2SeqLM.from_pretrained(pretrained)
        if use_gpu:
            self.model_thzh = self.model_thzh.cuda()

    def translate(self, text: str) -> str:
        """
        Translate text from Thai to Chinese

        :param str text: input text in source language
        :return: translated text in target language
        :rtype: str

        :Example:

        Translate text from Thai to Chinese::

            from pythainlp.translate import ThZhTranslator

            thzh = ThZhTranslator()

            thzh.translate("ผมรักคุณ")
            # output: 我爱你

        """
        self.translated = self.model_thzh.generate(
            **self.tokenizer_thzh(text, return_tensors="pt", padding=True)
        )
        return [
            self.tokenizer_thzh.decode(t, skip_special_tokens=True)
            for t in self.translated
        ][0]


class ZhThTranslator:
    """
    Chinese-Thai Machine Translation

    from Lalita @ AI builder

    - GitHub: https://github.com/LalitaDeelert/lalita-mt-zhth
    - Facebook post https://web.facebook.com/aibuildersx/posts/166736255494822

    :param bool use_gpu : load model to gpu (Default is False)
    """

    def __init__(
        self,
        use_gpu: bool = False,
        pretrained: str = "Lalita/marianmt-zh_cn-th",
    ) -> None:
        self.tokenizer_zhth = AutoTokenizer.from_pretrained(pretrained)
        self.model_zhth = AutoModelForSeq2SeqLM.from_pretrained(pretrained)
        if use_gpu:
            self.model_zhth.cuda()

    def translate(self, text: str) -> str:
        """
        Translate text from Chinese to Thai

        :param str text: input text in source language
        :return: translated text in target language
        :rtype: str

        :Example:

        Translate text from Chinese to Thai::

            from pythainlp.translate import ZhThTranslator

            zhth = ZhThTranslator()

            zhth.translate("我爱你")
            # output: ผมรักคุณนะ

        """
        self.translated = self.model_zhth.generate(
            **self.tokenizer_zhth(text, return_tensors="pt", padding=True)
        )
        return [
            self.tokenizer_zhth.decode(t, skip_special_tokens=True)
            for t in self.translated
        ][0]
