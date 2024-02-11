# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
# ruff: noqa: C901

from typing import List, Union

from pythainlp.tokenize import subword_tokenize
from pythainlp.util import remove_tonemark, sound_syllable


class KhaveeVerifier:
    def __init__(self):
        """
        KhaveeVerifier: Thai Poetry verifier
        """

    def check_sara(self, word: str) -> str:
        """
        Check the vowels in the Thai word.

        :param str word: Thai word
        :return: vowel name of the word
        :rtype: str

        :Example:
        ::

            from pythainlp.khavee import KhaveeVerifier

            kv = KhaveeVerifier()

            print(kv.check_sara("เริง"))
            # output: 'เออ'
        """
        sara = []
        countoa = 0

        # In case of การันย์
        if "์" in word[-1]:
            word = word[:-2]

        # In case of สระเดี่ยว
        for i in word:
            if i in ("ะ", "ั"):
                sara.append("อะ")
            elif i == "ิ":
                sara.append("อิ")
            elif i == "ุ":
                sara.append("อุ")
            elif i == "ึ":
                sara.append("อึ")
            elif i == "ี":
                sara.append("อี")
            elif i == "ู":
                sara.append("อู")
            elif i == "ื":
                sara.append("อือ")
            elif i == "เ":
                sara.append("เอ")
            elif i == "แ":
                sara.append("แอ")
            elif i == "า":
                sara.append("อา")
            elif i == "โ":
                sara.append("โอ")
            elif i == "ำ":
                sara.append("อำ")
            elif i == "อ":
                countoa += 1
                sara.append("ออ")
            elif i == "ั" and "ว" in word:
                sara.append("อัว")
            elif i in ("ไ", "ใ"):
                sara.append("ไอ")
            elif i == "็":
                sara.append("ออ")
            elif "รร" in word:
                if self.check_marttra(word) == "กม":
                    sara.append("อำ")
                else:
                    sara.append("อะ")

        # In case of ออ
        if countoa == 1 and "อ" in word[-1] and "เ" not in word:
            sara.remove("ออ")

        # In case of เอ เอ
        countA = 0
        for i in sara:
            if i == "เอ":
                countA = countA + 1
            if countA > 1:
                sara.remove("เอ")
                sara.remove("เอ")
                sara.append("แ")

        # In case of สระประสม
        if "เอ" in sara and "อะ" in sara:
            sara.remove("เอ")
            sara.remove("อะ")
            sara.append("เอะ")
        elif "แอ" in sara and "อะ" in sara:
            sara.remove("แอ")
            sara.remove("อะ")
            sara.append("แอะ")

        if "เอะ" in sara and "ออ" in sara:
            sara.remove("เอะ")
            sara.remove("ออ")
            sara.append("เออะ")
        elif "เอ" in sara and "อิ" in sara:
            sara.remove("เอ")
            sara.remove("อิ")
            sara.append("เออ")
        elif "เอ" in sara and "ออ" in sara and "อ" in word[-1]:
            sara.remove("เอ")
            sara.remove("ออ")
            sara.append("เออ")
        elif "โอ" in sara and "อะ" in sara:
            sara.remove("โอ")
            sara.remove("อะ")
            sara.append("โอะ")
        elif "เอ" in sara and "อี" in sara:
            sara.remove("เอ")
            sara.remove("อี")
            sara.append("เอีย")
        elif "เอ" in sara and "อือ" in sara:
            sara.remove("เอ")
            sara.remove("อือ")
            sara.append("อัว")
        elif "เอ" in sara and "อา" in sara:
            sara.remove("เอ")
            sara.remove("อา")
            sara.append("เอา")
        elif "เ" in word and "า" in word and "ะ" in word:
            sara = []
            sara.append("เอาะ")

        if "อือ" in sara and "เออ" in sara:
            sara.remove("เออ")
            sara.remove("อือ")
            sara.append("เอือ")
        elif "ออ" in sara and len(sara) > 1:
            sara.remove("ออ")
        elif "ว" in word and len(sara) == 0:
            sara.append("อัว")

        if "ั" in word and self.check_marttra(word) == "กา":
            sara = []
            sara.append("ไอ")

        # In case of อ
        if word == "เออะ":
            sara = []
            sara.append("เออะ")
        elif word == "เออ":
            sara = []
            sara.append("เออ")
        elif word == "เอ":
            sara = []
            sara.append("เอ")
        elif word == "เอะ":
            sara = []
            sara.append("เอะ")
        elif word == "เอา":
            sara = []
            sara.append("เอา")
        elif word == "เอาะ":
            sara = []
            sara.append("เอาะ")

        if "ฤา" in word or "ฦา" in word:
            sara = []
            sara.append("อือ")
        elif "ฤ" in word or "ฦ" in word:
            sara = []
            sara.append("อึ")

        # In case of กน
        if not sara and len(word) == 2:
            if word[-1] != "ร":
                sara.append("โอะ")
            else:
                sara.append("ออ")
        elif not sara and len(word) == 3:
            sara.append("ออ")

        # In case of บ่
        if word == "บ่":
            sara = []
            sara.append("ออ")

        if "ํ" in word:
            sara = []
            sara.append("อำ")

        if "เ" in word and "ื" in word and "อ" in word:
            sara = []
            sara.append("เอือ")

        if not sara:
            return "Can't find Sara in this word"

        return sara[0]

    def check_marttra(self, word: str) -> str:
        """
        Check the Thai spelling Section in the Thai word.

        :param str word: Thai word
        :return: name of spelling Section of the word.
        :rtype: str

        :Example:
        ::

            from pythainlp.khavee import KhaveeVerifier

            kv = KhaveeVerifier()

            print(kv.check_marttra('สาว'))
            # output: 'เกอว'
        """
        if word[-1] == "ร" and word[-2] in ["ต", "ท"]:
            word = word[:-1]
        word = self.handle_karun_sound_silence(word)
        word = remove_tonemark(word)
        if (
            "ำ" in word
            or ("ํ" in word and "า" in word)
            or "ไ" in word
            or "ใ" in word
        ):
            return "กา"
        elif (
            word[-1] in ["า", "ะ", "ิ", "ี", "ุ", "ู", "อ"]
            or ("ี" in word and "ย" in word[-1])
            or ("ื" in word and "อ" in word[-1])
        ):
            return "กา"
        elif word[-1] in ["ง"]:
            return "กง"
        elif word[-1] in ["ม"]:
            return "กม"
        elif word[-1] in ["ย"]:
            if "ั" in word:
                return "กา"
            else:
                return "เกย"
        elif word[-1] in ["ว"]:
            return "เกอว"
        elif word[-1] in ["ก", "ข", "ค", "ฆ"]:
            return "กก"
        elif word[-1] in [
            "จ",
            "ช",
            "ซ",
            "ฎ",
            "ฏ",
            "ฐ",
            "ฑ",
            "ฒ",
            "ด",
            "ต",
            "ถ",
            "ท",
            "ธ",
            "ศ",
            "ษ",
            "ส",
        ]:
            return "กด"
        elif word[-1] in ["ญ", ", ณ", "น", "ร", "ล", "ฬ"]:
            return "กน"
        elif word[-1] in ["บ", "ป", "พ", "ฟ", "ภ"]:
            return "กบ"
        else:
            if "็" in word:
                return "กา"
            else:
                return "Cant find Marttra in this word"

    def is_sumpus(self, word1: str, word2: str) -> bool:
        """
        Check the rhyme between two words.

        :param str word1: Thai word
        :param str word2: Thai word
        :return: boolean
        :rtype: bool

        :Example:
        ::

            from pythainlp.khavee import KhaveeVerifier

            kv = KhaveeVerifier()

            print(kv.is_sumpus('สรร', 'อัน'))
            # output: True

            print(kv.is_sumpus('สรร', 'แมว'))
            # output: False
        """
        marttra1 = self.check_marttra(word1)
        marttra2 = self.check_marttra(word2)
        sara1 = self.check_sara(word1)
        sara2 = self.check_sara(word2)
        if sara1 == "อะ" and marttra1 == "เกย":
            sara1 = "ไอ"
            marttra1 = "กา"
        elif sara2 == "อะ" and marttra2 == "เกย":
            sara2 = "ไอ"
            marttra2 = "กา"
        if sara1 == "อำ" and marttra1 == "กม":
            sara1 = "อำ"
            marttra1 = "กา"
        elif sara2 == "อำ" and marttra2 == "กม":
            sara2 = "อำ"
            marttra2 = "กา"
        return bool(marttra1 == marttra2 and sara1 == sara2)

    def check_karu_lahu(self, text):
        if (
            self.check_marttra(text) != "กา"
            or (
                self.check_marttra(text) == "กา"
                and self.check_sara(text)
                in [
                    "อา",
                    "อี",
                    "อือ",
                    "อู",
                    "เอ",
                    "แอ",
                    "โอ",
                    "ออ",
                    "เออ",
                    "เอีย",
                    "เอือ",
                    "อัว",
                ]
            )
            or self.check_sara(text) in ["อำ", "ไอ", "เอา"]
        ) and text not in ["บ่", "ณ", "ธ", "ก็"]:
            return "karu"
        else:
            return "lahu"

    def check_klon(self, text: str, k_type: int = 8) -> Union[List[str], str]:
        """
        Check the suitability of the poem according to Thai principles.

        :param str text: Thai poem
        :param int k_type: type of Thai poem
        :return: the check results of the suitability of the poem according to Thai principles.
        :rtype: Union[List[str], str]

        :Example:
        ::

            from pythainlp.khavee import KhaveeVerifier

            kv = KhaveeVerifier()

            print(kv.check_klon(
                'ฉันชื่อหมูกรอบ ฉันชอบกินไก่ แล้วก็วิ่งไล่ หมาชื่อนํ้าทอง ลคคนเก่ง เอ๋งเอ๋งคะนอง \
                มีคนจับจอง เขาชื่อน้องเธียร',
                k_type=4
            ))
            # output: The poem is correct according to the principle.

            print(kv.check_klon(
                'ฉันชื่อหมูกรอบ ฉันชอบกินไก่ แล้วก็วิ่งไล่ หมาชื่อนํ้าทอง ลคคนเก่ง \
                เอ๋งเอ๋งเสียงหมา มีคนจับจอง เขาชื่อน้องเธียร',
                k_type=4
            ))
            # output: [
                "Can't find rhyme between paragraphs ('หมา', 'จอง') in paragraph 2",
                "Can't find rhyme between paragraphs ('หมา', 'ทอง') in paragraph 2"
            ]
        """
        if k_type == 8:
            try:
                error = []
                list_sumpus_sent1 = []
                list_sumpus_sent2h = []
                list_sumpus_sent2l = []
                list_sumpus_sent3 = []
                list_sumpus_sent4 = []
                for i, sent in enumerate(text.split()):
                    sub_sent = subword_tokenize(sent, engine="dict")
                    if len(sub_sent) > 10:
                        error.append(
                            "In sentence "
                            + str(i + 2)
                            + ", there are more than 10 words. "
                            + str(sub_sent)
                        )
                    if (i + 1) % 4 == 1:
                        list_sumpus_sent1.append(sub_sent[-1])
                    elif (i + 1) % 4 == 2:
                        list_sumpus_sent2h.append(
                            [
                                sub_sent[1],
                                sub_sent[2],
                                sub_sent[3],
                                sub_sent[4],
                            ]
                        )
                        list_sumpus_sent2l.append(sub_sent[-1])
                    elif (i + 1) % 4 == 3:
                        list_sumpus_sent3.append(sub_sent[-1])
                    elif (i + 1) % 4 == 0:
                        list_sumpus_sent4.append(sub_sent[-1])
                if (
                    len(list_sumpus_sent1) != len(list_sumpus_sent2h)
                    or len(list_sumpus_sent2h) != len(list_sumpus_sent2l)
                    or len(list_sumpus_sent2l) != len(list_sumpus_sent3)
                    or len(list_sumpus_sent3) != len(list_sumpus_sent4)
                    or len(list_sumpus_sent4) != len(list_sumpus_sent1)
                ):
                    return "The poem does not have 4 complete sentences."
                else:
                    for i in range(len(list_sumpus_sent1)):
                        countwrong = 0
                        for j in list_sumpus_sent2h[i]:
                            if (
                                self.is_sumpus(list_sumpus_sent1[i], j)
                                is False
                            ):
                                countwrong += 1
                        if countwrong > 3:
                            error.append(
                                "Can't find rhyme between paragraphs "
                                + str(
                                    (
                                        list_sumpus_sent1[i],
                                        list_sumpus_sent2h[i],
                                    )
                                )
                                + " in paragraph "
                                + str(i + 1)
                            )
                        if (
                            self.is_sumpus(
                                list_sumpus_sent2l[i], list_sumpus_sent3[i]
                            )
                            is False
                        ):
                            error.append(
                                "Can't find rhyme between paragraphs "
                                + str(
                                    (
                                        list_sumpus_sent2l[i],
                                        list_sumpus_sent3[i],
                                    )
                                )
                                + " in paragraph "
                                + str(i + 1)
                            )
                        if i > 0:
                            if (
                                self.is_sumpus(
                                    list_sumpus_sent2l[i],
                                    list_sumpus_sent4[i - 1],
                                )
                                is False
                            ):
                                error.append(
                                    "Can't find rhyme between paragraphs "
                                    + str(
                                        (
                                            list_sumpus_sent2l[i],
                                            list_sumpus_sent4[i - 1],
                                        )
                                    )
                                    + " in paragraph "
                                    + str(i + 1)
                                )
                    if not error:
                        return (
                            "The poem is correct according to the principle."
                        )
                    else:
                        return error
            except:
                return "Something went wrong. Make sure you enter it in the correct form of klon 8."
        elif k_type == 4:
            try:
                error = []
                list_sumpus_sent1 = []
                list_sumpus_sent2h = []
                list_sumpus_sent2l = []
                list_sumpus_sent3 = []
                list_sumpus_sent4 = []
                for i, sent in enumerate(text.split()):
                    sub_sent = subword_tokenize(sent, engine="dict")
                    if len(sub_sent) > 5:
                        error.append(
                            "In sentence "
                            + str(i + 2)
                            + ", there are more than 4 words. "
                            + str(sub_sent)
                        )
                    if (i + 1) % 4 == 1:
                        list_sumpus_sent1.append(sub_sent[-1])
                    elif (i + 1) % 4 == 2:
                        list_sumpus_sent2h.append([sub_sent[1], sub_sent[2]])
                        list_sumpus_sent2l.append(sub_sent[-1])
                    elif (i + 1) % 4 == 3:
                        list_sumpus_sent3.append(sub_sent[-1])
                    elif (i + 1) % 4 == 0:
                        list_sumpus_sent4.append(sub_sent[-1])
                if (
                    len(list_sumpus_sent1) != len(list_sumpus_sent2h)
                    or len(list_sumpus_sent2h) != len(list_sumpus_sent2l)
                    or len(list_sumpus_sent2l) != len(list_sumpus_sent3)
                    or len(list_sumpus_sent3) != len(list_sumpus_sent4)
                    or len(list_sumpus_sent4) != len(list_sumpus_sent1)
                ):
                    return "The poem does not have 4 complete sentences."
                else:
                    for i in range(len(list_sumpus_sent1)):
                        countwrong = 0
                        for j in list_sumpus_sent2h[i]:
                            if (
                                self.is_sumpus(list_sumpus_sent1[i], j)
                                is False
                            ):
                                countwrong += 1
                        if countwrong > 1:
                            error.append(
                                "Can't find rhyme between paragraphs "
                                + str(
                                    (
                                        list_sumpus_sent1[i],
                                        list_sumpus_sent2h[i],
                                    )
                                )
                                + " in paragraph "
                                + str(i + 1)
                            )
                        if (
                            self.is_sumpus(
                                list_sumpus_sent2l[i], list_sumpus_sent3[i]
                            )
                            is False
                        ):
                            error.append(
                                "Can't find rhyme between paragraphs "
                                + str(
                                    (
                                        list_sumpus_sent2l[i],
                                        list_sumpus_sent3[i],
                                    )
                                )
                                + " in paragraph "
                                + str(i + 1)
                            )
                        if i > 0:
                            if (
                                self.is_sumpus(
                                    list_sumpus_sent2l[i],
                                    list_sumpus_sent4[i - 1],
                                )
                                is False
                            ):
                                error.append(
                                    "Can't find rhyme between paragraphs "
                                    + str(
                                        (
                                            list_sumpus_sent2l[i],
                                            list_sumpus_sent4[i - 1],
                                        )
                                    )
                                    + " in paragraph "
                                    + str(i + 1)
                                )
                    if not error:
                        return (
                            "The poem is correct according to the principle."
                        )
                    else:
                        return error
            except:
                return "Something went wrong. Make sure you enter it in the correct form."

        else:
            return "Something went wrong. Make sure you enter it in the correct form."

    def check_aek_too(
        self, text: Union[List[str], str], dead_syllable_as_aek: bool = False
    ) -> Union[List[bool], List[str], bool, str]:
        """
        Checker of Thai tonal words

        :param Union[List[str], str] text: Thai word or list of Thai words
        :param bool dead_syllable_as_aek: if True, dead syllable will be considered as aek
        :return: the check result if the word is aek or too or False (not both) or list of check results if input is list
        :rtype: Union[List[bool], List[str], bool, str]

        :Example:
        ::

            from pythainlp.khavee import KhaveeVerifier

            kv = KhaveeVerifier()

            # การเช็คคำเอกโท
            print(kv.check_aek_too('เอง'), kv.check_aek_too('เอ่ง'), kv.check_aek_too('เอ้ง'))
            # -> False, aek, too
            print(kv.check_aek_too(['เอง', 'เอ่ง', 'เอ้ง'])) # ใช้ List ได้เหมือนกัน
            # -> [False, 'aek', 'too']


        """
        if isinstance(text, list):
            return [self.check_aek_too(t, dead_syllable_as_aek) for t in text]

        if not isinstance(text, str):
            raise TypeError("text must be str or iterable list[str]")

        word_characters = [*text]
        if "่" in word_characters and "้" not in word_characters:
            return "aek"
        elif "้" in word_characters and "่" not in word_characters:
            return "too"
        if dead_syllable_as_aek and sound_syllable(text) == "dead":
            return "aek"
        else:
            return False

    def handle_karun_sound_silence(self, word: str) -> str:
        """
        Handle silent sounds in Thai words using '์' character (Karun)
        by stripping all characters before the 'Karun' character that should be silenced

        :param str text: Thai word
        :return: Thai word with silent words stripped
        :rtype: str
        """
        sound_silenced = word.endswith("์")
        if not sound_silenced:
            return word
        thai_consonants = "กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธนบปผฝพฟภมยรลวศษสหฬอฮ"
        locate_silenced = word.rfind("์") - 1
        can_silence_two = word[locate_silenced - 2] in thai_consonants
        cut_off = 2 if can_silence_two else 1
        word = word[: locate_silenced + 1 - cut_off]
        return word
