# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0


class Translate:
    """
    Machine Translation
    """

    def __init__(
        self, src_lang: str, target_lang: str, engine: str="default", use_gpu: bool = False
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
            th2en = Translate('th', 'en')

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

    def translate(self, text) -> str:
        """
        Translate text

        :param str text: input text in source language
        :return: translated text in target language
        :rtype: str
        """
        if self.engine == "small100":
            return self.model.translate(text, tgt_lang=self.target_lang)
        return self.model.translate(text)
