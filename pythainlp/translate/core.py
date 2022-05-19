# -*- coding: utf-8 -*-


class Translate:
    """
    Machine Translation

    :param str src_lang: source language
    :param str target_lang: target language
    :param bool use_gpu: load model to gpu (Default is False)

    **Options for source & target language**
        * *th* - *en* - Thai to English
        * *en* - *th* - English to Thai
        * *th* - *zh* - Thai to Chinese
        * *zh* - *th* - Chinese to Thai
        * *th* - *fr* - Thai to French

    :Example:

    Translate text from Thai to English::

        from pythainlp.translate import Translate
        th2en = Translate('th', 'en')

        th2en.translate("ฉันรักแมว")
        # output: I love cat.
    """
    def __init__(self,
                 src_lang: str,
                 target_lang: str,
                 use_gpu: bool = False) -> None:
        """
        :param str src_lang: source language
        :param str target_lang: target language
        :param bool use_gpu: load model to gpu (Default is False)

        **Options for source & target language**
            * *th* - *en* - Thai to English
            * *en* - *th* - English to Thai
            * *th* - *zh* - Thai to Chinese
            * *zh* - *th* - Chinese to Thai
            * *th* - *fr* - Thai to French

        :Example:

        Translate text from Thai to English::

            from pythainlp.translate import Translate
            th2en = Translate('th', 'en')

            th2en.translate("ฉันรักแมว")
            # output: I love cat.
        """
        self.model = None
        self.load_model(src_lang, target_lang, use_gpu)

    def load_model(self, src_lang: str, target_lang: str, use_gpu: bool):
        if src_lang == "th" and target_lang == "en":
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
        return self.model.translate(text)
