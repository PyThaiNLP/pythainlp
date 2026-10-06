# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""
Transliterate Japanese, Korean, Mandarin, and Vietnamese romanization
text to Thai text, using Wunsen.

:See Also:
    * `GitHub <https://github.com/cakimpei/wunsen>`_
"""

from __future__ import annotations

from typing import Optional, Union, cast

from wunsen import ThapSap


class WunsenTransliterate:
    """
    Transliterate Japanese, Korean, Mandarin, and Vietnamese romanization
    text to Thai text, using Wunsen.

    :See Also:
        * `GitHub <https://github.com/cakimpei/wunsen>`_
    """

    thap_value: Optional["ThapSap"]
    lang: Optional[str]
    jp_input: Optional[str]
    zh_sandhi: Optional[bool]
    system: Optional[str]

    def __init__(self) -> None:
        self.thap_value: Optional[ThapSap] = None
        self.lang: Optional[str] = None
        self.jp_input: Optional[str] = None
        self.zh_sandhi: Optional[bool] = None
        self.system: Optional[str] = None

    def _set_options(
        self,
        lang: str,
        jp_input: Optional[str],
        zh_sandhi: Optional[bool],
        system: Optional[str],
    ) -> None:
        """Store the options that apply to the language."""
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

    def _create_thap_sap(self) -> ThapSap:
        """Create a ThapSap object from the stored options."""
        input_lang = "ja" if self.lang == "jp" else self.lang
        setting: dict[str, Union[str, dict[str, bool]]] = {}
        if self.jp_input is not None:
            setting.update({"input": self.jp_input})
        if self.zh_sandhi is not None:
            setting.update({"option": {"sandhi": self.zh_sandhi}})
        if self.system is not None:
            setting.update({"system": self.system})
        return ThapSap(input_lang, **setting)

    def transliterate(
        self,
        text: str,
        lang: str,
        jp_input: Optional[str] = None,
        zh_sandhi: Optional[bool] = None,
        system: Optional[str] = None,
    ) -> str:
        """
        Transliterate romanization text to Thai text using Wunsen.

        :param str text: romanization text to be transliterated
        :param str lang: source language (see the options below)
        :param Optional[str] jp_input: Japanese input method, for Japanese
            only (default is ``None``)
        :param Optional[bool] zh_sandhi: Mandarin third tone sandhi option,
            for Mandarin only (default is ``None``)
        :param Optional[str] system: transliteration system, for Japanese
            and Mandarin only (default is ``None``)
        :return: Thai text
        :rtype: str
        :raises NotImplementedError: if the language is not supported

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

            >>> from pythainlp.transliterate.wunsen import (
            ...     WunsenTransliterate,
            ... )  # doctest: +SKIP
            >>> wt = WunsenTransliterate()  # doctest: +SKIP
            >>> wt.transliterate("ohayō", lang="jp")  # doctest: +SKIP
            'โอฮาโย'
            >>> wt.transliterate(
            ...     "ohayou", lang="jp", jp_input="Hepburn-no diacritic"
            ... )  # doctest: +SKIP
            'โอฮาโย'
            >>> wt.transliterate(
            ...     "ohayō", lang="jp", system="RI35"
            ... )  # doctest: +SKIP
            'โอะฮะโย'
            >>> wt.transliterate("annyeonghaseyo", lang="ko")  # doctest: +SKIP
            'อันนย็องฮาเซโย'
            >>> wt.transliterate("xin chào", lang="vi")  # doctest: +SKIP
            'ซีน จ่าว'
            >>> wt.transliterate("ni3 hao3", lang="zh")  # doctest: +SKIP
            'หนี เห่า'
            >>> wt.transliterate(
            ...     "ni3 hao3", lang="zh", zh_sandhi=False
            ... )  # doctest: +SKIP
            'หนี่ เห่า'
            >>> wt.transliterate(
            ...     "ni3 hao3", lang="zh", system="RI49"
            ... )  # doctest: +SKIP
            'หนี ห่าว'
        """
        if (
            self.thap_value is None
            or self.lang != lang
            or self.jp_input != jp_input
            or self.zh_sandhi != zh_sandhi
            or self.system != system
        ):
            self._set_options(lang, jp_input, zh_sandhi, system)
            self.thap_value = self._create_thap_sap()

        return cast("str", self.thap_value.thap(text))
