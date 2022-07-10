# -*- coding: utf-8 -*-
"""
Transliterating Japanese/Korean/Vietnamese romanization text to Thai text
By Wunsen

:See Also:
    * `GitHub \
        <https://github.com/cakimpei/wunsen>`_
"""
from wunsen import ThapSap


class WunsenTransliterate:
    """
    Transliterating Japanese/Korean/Vietnamese romanization text to Thai text
    by Wunsen

    :See Also:
        * `GitHub \
            <https://github.com/cakimpei/wunsen>`_
    """
    def __init__(self) -> None:
        self.thap_value = None
        self.lang = None
        self.jp_input = None

    def transliterate(self, text: str, lang: str, jp_input: str = None):
        """
        Use Wunsen for transliteration

        :param str text: text wants transliterated to Thai text.
        :param str lang: source language
        :param str jp_input: japanese input method (for japanese only)

        :return: Thai text
        :rtype: str

        :Options for lang:
            * *jp* - Japanese (from Hepburn romanization)
            * *ko* - Korean (from Revised Romanization)
            * *vi* - Vietnamese (Latin script)
        :Options for jp_input:
            * *Hepburn-no diacritic* - Hepburn-no diacritic (without macron)

        :Example:
        ::
            from pythainlp.transliterate.wunsen import WunsenTransliterate

            wt = WunsenTransliterate()

            wt.transliterate("ohayō", lang="jp")
            # output: 'โอฮาโย'

            wt.transliterate(
                "ohayou",
                lang="jp",
                jp_input="Hepburn-no diacritic"
            )
            # output: 'โอฮาโย'

            wt.transliterate("annyeonghaseyo", lang="ko")
            # output: 'อันนย็องฮาเซโย'

            wt.transliterate("xin chào", lang="vi")
            # output: 'ซีน จ่าว'
        """
        if self.lang != lang or self.jp_input != jp_input:
            if lang == "jp":
                if jp_input is None:
                    self.thap_value = ThapSap("ja")
                else:
                    self.thap_value = ThapSap("ja", input=jp_input)
                self.jp_input = jp_input
            elif lang == "ko" or lang == "vi":
                self.jp_input = None
                self.thap_value = ThapSap(lang)
            else:
                raise NotImplementedError(
                    "The %s language is not implemented." % lang
                )
        return self.thap_value.thap(text)
