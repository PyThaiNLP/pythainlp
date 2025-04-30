# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2025 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
from typing import List, Union


class Translate:
    """
    Machine Translation
    """

    def __init__(
        self,
        src_lang: str,
        target_lang: str,
        engine: str = "default",
        use_gpu: bool = False,
    ) -> None:
        """
        :param str src_lang: source language
        :param str target_lang: target language
        :param str engine: machine translation engine
        :param bool use_gpu: load model using GPU (Default is False)

        **Options for engine*
            * *default* - The default engine for each language.
            * *small100* - A multilingual machine translation model (covering 100 languages)

        **Options for source & target language**
            * *th* - *en* - Thai to English
            * *en* - *th* - English to Thai
            * *th* - *zh* - Thai to Chinese
            * *zh* - *th* - Chinese to Thai
            * *th* - *fr* - Thai to French
            * *th* - *xx* - Thai to xx (xx is language code). It uses small100 model.
            * *xx* - *th* - xx to Thai (xx is language code). It uses small100 model.

        :Example:

        Translate text from Thai to English::

            from pythainlp.translate import Translate

            th2en = Translate("th", "en")

            th2en.translate("ฉันรักแมว")
            # output: I love cat.
        """
        self.model = None
        self.engine = engine
        self.src_lang = src_lang
        self.use_gpu = use_gpu
        self.target_lang = target_lang
        self.load_model()

    def load_model(self):
        src_lang = self.src_lang
        target_lang = self.target_lang
        use_gpu = self.use_gpu
        if self.engine == "small100":
            from .small100 import Small100Translator

            self.model = Small100Translator(use_gpu)
        elif src_lang == "th" and target_lang == "en":
            from pythainlp.translate.en_th import ThEnTranslator

            self.model = ThEnTranslator(use_gpu)
        elif src_lang == "en" and target_lang == "th":
            from pythainlp.translate.en_th import EnThTranslator

            self.model = EnThTranslator(use_gpu)
        elif src_lang == "th" and target_lang == "zh":
            from pythainlp.translate.zh_th import ThZhTranslator

            self.model = ThZhTranslator(use_gpu)
        elif src_lang == "zh" and target_lang == "th":
            from pythainlp.translate.zh_th import ZhThTranslator

            self.model = ZhThTranslator(use_gpu)
        elif src_lang == "th" and target_lang == "fr":
            from pythainlp.translate.th_fr import ThFrTranslator

            self.model = ThFrTranslator(use_gpu)
        else:
            raise ValueError("Not support language!")

    def translate(self, text: str) -> str:
        """
        Translate text

        :param str text: input text in source language
        :return: translated text in target language
        :rtype: str
        """
        if self.engine == "small100":
            return self.model.translate(text, tgt_lang=self.target_lang)
        return self.model.translate(text)


def word_translate(
        word: str,
        src: str,
        target: str,
        engine: str="word2word"
    ) -> Union[List[str], None]:
    """
    Translate word from source language to target language.

    :param str word: text
    :param str src: src language
    :param str target: target language
    :param str engine: Word translate engine (the default engine is word2word)
    :return: return list word translate or None
    :rtype: Union[List[str], None]

    :Example:

    Translate word from Thai to English::

        from pythainlp.translate import word_translate
        print(word_translate("แมว","th","en"))
        # output: ['cat', 'cats', 'kitty', 'kitten', 'Cat']

    Translate word from English to Thai::

        from pythainlp.translate import word_translate
        print(word_translate("cat","en","th"))
        # output: ['แมว', 'แมวป่า', 'ข่วน', 'เลี้ยง', 'อาหาร']

    """
    if engine=="word2word":
        from .word2word_translate import translate
        return translate(word=word, src=src, target=target)
    else:
        raise NotImplementedError(
            f"pythainlp.translate.word_translate isn't support {engine}."
        )
