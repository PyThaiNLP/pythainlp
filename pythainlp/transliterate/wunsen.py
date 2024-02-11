# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
"""
Transliterating Japanese/Korean/Mandarin/Vietnamese romanization text
to Thai text
By Wunsen

:See Also:
    * `GitHub \
        <https://github.com/cakimpei/wunsen>`_
"""
from wunsen import ThapSap


class WunsenTransliterate:
    """
    Transliterating Japanese/Korean/Mandarin/Vietnamese romanization text
    to Thai text
    by Wunsen

    :See Also:
        * `GitHub \
            <https://github.com/cakimpei/wunsen>`_
    """

    def __init__(self) -> None:
        self.thap_value = None
        self.lang = None
        self.jp_input = None
        self.zh_sandhi = None
        self.system = None

    def transliterate(
        self,
        text: str,
        lang: str,
        jp_input: str = None,
        zh_sandhi: bool = None,
        system: str = None,
    ):
        """
        Use Wunsen for transliteration

        :param str text: text to be transliterated to Thai text.
        :param str lang: source language
        :param str jp_input: Japanese input method (for Japanese only)
        :param bool zh_sandhi: Mandarin third tone sandhi option
            (for Mandarin only)
        :param str system: transliteration system (for Japanese and
            Mandarin only)

        :return: Thai text
        :rtype: str

        :Options for lang:
            * *jp* - Japanese (from Hepburn romanization)
            * *ko* - Korean (from Revised Romanization)
            * *vi* - Vietnamese (Latin script)
            * *zh* - Mandarin (from Hanyu Pinyin)
        :Options for jp_input:
            * *Hepburn-no diacritic* - Hepburn-no diacritic (without macron)
        :Options for zh_sandhi:
            * *True* - apply third tone sandhi rule
            * *False* - do not apply third tone sandhi rule
        :Options for system:
            * *ORS61* - for Japanese หลักเกณฑ์การทับศัพท์ภาษาญี่ปุ่น
                (สำนักงานราชบัณฑิตยสภา พ.ศ. 2561)
            * *RI35* - for Japanese หลักเกณฑ์การทับศัพท์ภาษาญี่ปุ่น
                (ราชบัณฑิตยสถาน พ.ศ. 2535)
            * *RI49* - for Mandarin หลักเกณฑ์การทับศัพท์ภาษาจีน
                (ราชบัณฑิตยสถาน พ.ศ. 2549)
            * *THC43* - for Mandarin เกณฑ์การถ่ายทอดเสียงภาษาจีนแมนดาริน
                ด้วยอักขรวิธีไทย (คณะกรรมการสืบค้นประวัติศาสตร์ไทยในเอกสาร
                ภาษาจีน พ.ศ. 2543)

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

            wt.transliterate("ohayō", lang="jp", system="RI35")
            # output: 'โอะฮะโย'

            wt.transliterate("annyeonghaseyo", lang="ko")
            # output: 'อันนย็องฮาเซโย'

            wt.transliterate("xin chào", lang="vi")
            # output: 'ซีน จ่าว'

            wt.transliterate("ni3 hao3", lang="zh")
            # output: 'หนี เห่า'

            wt.transliterate("ni3 hao3", lang="zh", zh_sandhi=False)
            # output: 'หนี่ เห่า'

            wt.transliterate("ni3 hao3", lang="zh", system="RI49")
            # output: 'หนี ห่าว'
        """
        if (
            self.lang != lang
            or self.jp_input != jp_input
            or self.zh_sandhi != zh_sandhi
            or self.system != system
        ):
            if lang == "jp":
                self.jp_input = jp_input
                self.zh_sandhi = None
                self.system = system
            elif lang == "zh":
                self.jp_input = None
                self.zh_sandhi = zh_sandhi
                self.system = system
            elif lang in ("ko", "vi"):
                self.jp_input = None
                self.zh_sandhi = None
                self.system = None
            else:
                raise NotImplementedError(
                    "The %s language is not implemented." % lang
                )
            self.lang = lang
            input_lang = lang
            if input_lang == "jp":
                input_lang = "ja"
            setting = {}
            if self.jp_input is not None:
                setting.update({"input": self.jp_input})
            if self.zh_sandhi is not None:
                setting.update({"option": {"sandhi": self.zh_sandhi}})
            if self.system is not None:
                setting.update({"system": self.system})
            self.thap_value = ThapSap(input_lang, **setting)
        return self.thap_value.thap(text)
