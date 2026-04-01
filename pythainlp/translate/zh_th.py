# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Lalita Chinese-Thai Machine Translation

from AI builder

- GitHub: https://github.com/LalitaDeelert/lalita-mt-zhth
- Facebook post https://web.facebook.com/aibuildersx/posts/166736255494822
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    import torch
    from transformers import AutoModelForSeq2SeqLM, AutoTokenizer  # noqa: F401


class ThZhTranslator:
    """Thai-Chinese Machine Translation

    from Lalita @ AI builder

    - GitHub: https://github.com/LalitaDeelert/lalita-mt-zhth
    - Facebook post https://web.facebook.com/aibuildersx/posts/166736255494822

    :param bool use_gpu : load model using GPU (Default is False)
    """

    def __init__(
        self,
        use_gpu: bool = False,
        pretrained: str = "Lalita/marianmt-th-zh_cn",
    ) -> None:
        from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

        self.tokenizer_thzh: AutoTokenizer = AutoTokenizer.from_pretrained(
            pretrained
        )
        self.model_thzh: AutoModelForSeq2SeqLM = (
            AutoModelForSeq2SeqLM.from_pretrained(pretrained)
        )
        if use_gpu:
            self.model_thzh = self.model_thzh.cuda()

    def translate(
        self, text: str, exclude_words: Optional[list[str]] = None
    ) -> str:
        """Translate text from Thai to Chinese

        :param str text: input text in source language
        :param list[str] exclude_words: words to exclude from translation
                                        (optional)
        :return: translated text in target language
        :rtype: str

        :Example:

        Translate text from Thai to Chinese:

            >>> from pythainlp.translate import ThZhTranslator  # doctest: +SKIP

            >>> thzh = ThZhTranslator()  # doctest: +SKIP

            >>> thzh.translate("ผมรักคุณ")  # doctest: +SKIP
            我爱你

        Translate text from Thai to Chinese with excluded words:

            >>> thzh.translate("ผมรักคุณ", exclude_words=["ผม"])  # doctest: +SKIP
            ผม爱你

        """
        from pythainlp.translate.core import (
            _prepare_text_with_exclusions,
            _restore_excluded_words,
        )

        prepared_text, placeholder_map = _prepare_text_with_exclusions(
            text, exclude_words
        )
        self.translated: torch.Tensor = self.model_thzh.generate(
            **self.tokenizer_thzh(
                prepared_text, return_tensors="pt", padding=True
            )
        )
        translated_text = [
            self.tokenizer_thzh.decode(t, skip_special_tokens=True)
            for t in self.translated
        ][0]
        return _restore_excluded_words(translated_text, placeholder_map)


class ZhThTranslator:
    """Chinese-Thai Machine Translation

    from Lalita @ AI builder

    - GitHub: https://github.com/LalitaDeelert/lalita-mt-zhth
    - Facebook post https://web.facebook.com/aibuildersx/posts/166736255494822

    :param bool use_gpu : load model using GPU (Default is False)
    """

    def __init__(
        self,
        use_gpu: bool = False,
        pretrained: str = "Lalita/marianmt-zh_cn-th",
    ) -> None:
        from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

        self.tokenizer_zhth: AutoTokenizer = AutoTokenizer.from_pretrained(
            pretrained
        )
        self.model_zhth: AutoModelForSeq2SeqLM = (
            AutoModelForSeq2SeqLM.from_pretrained(pretrained)
        )
        if use_gpu:
            self.model_zhth = self.model_zhth.cuda()

    def translate(
        self, text: str, exclude_words: Optional[list[str]] = None
    ) -> str:
        """Translate text from Chinese to Thai

        :param str text: input text in source language
        :param list[str] exclude_words: words to exclude from translation
                                        (optional)
        :return: translated text in target language
        :rtype: str

        :Example:

        Translate text from Chinese to Thai:

            >>> from pythainlp.translate import ZhThTranslator  # doctest: +SKIP

            >>> zhth = ZhThTranslator()  # doctest: +SKIP

            >>> zhth.translate("我爱你")  # doctest: +SKIP
            ผมรักคุณนะ

        Translate text from Chinese to Thai with excluded words:

            >>> zhth.translate("我爱你", exclude_words=["我"])  # doctest: +SKIP
            我รักคุณนะ

        """
        from pythainlp.translate.core import (
            _prepare_text_with_exclusions,
            _restore_excluded_words,
        )

        prepared_text, placeholder_map = _prepare_text_with_exclusions(
            text, exclude_words
        )
        self.translated: torch.Tensor = self.model_zhth.generate(
            **self.tokenizer_zhth(
                prepared_text, return_tensors="pt", padding=True
            )
        )
        translated_text = [
            self.tokenizer_zhth.decode(t, skip_special_tokens=True)
            for t in self.translated
        ][0]
        return _restore_excluded_words(translated_text, placeholder_map)
