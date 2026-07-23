# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
# ruff: noqa: C901
from __future__ import annotations

import re
from typing import Union

from pythainlp import thai_consonants
from pythainlp.tokenize import subword_tokenize
from pythainlp.util import remove_tonemark, sound_syllable


class KhaveeVerifier:
    # explicitly include ฤ and ฦ as they act as initial consonants but aren't in thai_consonants
    VALID_CONSONANTS = frozenset(thai_consonants + "ฤฦ")

    def __init__(self) -> None:
        """
        KhaveeVerifier: Thai Poetry verifier
        """

    # For backward compatibility, this method is kept as a private method.
    def _has_true_final_yl(self, word: str) -> bool:
        """
        Check if ย or ล is a true final consonant
        (not just part of the vowel sound with ไ/ใ)

        :param str word: Thai word
        :return: True if ย or ล is a true final consonant
        :rtype: bool
        """
        return self._is_true_final(word)

    def _is_true_final(self, word: str) -> bool:
        """
        Check if the last character is a true final consonant
        (not part of a vowel sound or an initial cluster).

        :param str word: Thai word
        :return: True if the ending character acts as a final consonant
        :rtype: bool
        """
        # Handle การันย์
        word = self.handle_karun_sound_silence(word)
        # Store original word to distinguish tone-dependent structures
        original_word = word
        # Strip tone marks first so words like 'ใกล้' properly evaluate as ending in 'ล'
        word = remove_tonemark(word)

        if len(word) < 2:
            return False

        last_char = word[-1]

        consonants = [c for c in word if c in self.VALID_CONSONANTS]
        if len(consonants) < 2:
            return False

        # คำควบกล้ำ / อักษรนำ (initial clusters)
        cluster = consonants[0] + consonants[1]

        # ไ/ใ never take a final consonant ย here is silent (ไทย, ไชย)
        # Check for ย inside เ-ีย (เสีย, เมีย) (part of the vowel)
        if last_char == "ย":
            if ("ไ" in word or "ใ" in word) or ("เ" in word and "ี" in word):
                return False

        # ---------------------------------------------------------------------
        # Guard Clauses: If it's not ending in ล, ร, ว, or doesn't have exactly 2
        # consonants, or lacks pre-posed vowels, it bypasses the cluster checks.
        # ---------------------------------------------------------------------
        if last_char not in {"ล", "ร", "ว"} or len(consonants) != 2:
            return True

        # Check for ล, ร, ว in initial clusters (คำควบกล้ำ / อักษรนำ) with pre-posed vowels เ-, แ-, โ-, ไ-, ใ- (เปล, เถล, แผล, โหล, ไกล, ใกล้, โปร, แตร, ไกว, เขว)
        if not any(v in word for v in {"เ", "แ", "โ", "ไ", "ใ"}):
            return True

        # Check for ล
        if last_char == "ล" and cluster in {"กล", "ขล", "คล", "ปล", "ผล", "พล", "หล", "ถล", "ฉล", "สล", "ศล", "ตล"}:
            # Exception 'เพล' - แม่กน (monk food ฉันเพล) Returns True, otherwise False
            return word == "เพล"

        # Check for ร
        if last_char == "ร" and cluster in {"กร", "ขร", "คร", "ตร", "ปร", "พร", "ฟร", "บร", "ศร", "สร", "หร"}:
            return False

        # Check for ว (ควบแท้ and อักษรนำ)
        if last_char == "ว":
            # With ไ/ใ, 'ว' is ALWAYS a cluster (ไกว, ไขว้)
            if ("ไ" in word or "ใ" in word) and cluster in {"กว", "ขว", "คว", "สว", "หว", "ทว", "ชว", "ศว", "ถว"}:
                return False

            # With เ/แ/โ, 'ว' is mostly is a true final (เลว, เหว, แก้ว, แห้ว). Whitelist อักษรนำ/คำควบกล้ำ as exceptions
            elif any(v in word for v in {"เ", "แ", "โ"}):
                # USE ORIGINAL_WORD to safely catch open syllables แม่ ก กา
                # เดินเขว, ว้าเหว่, แม่น้ำแคว, ตวาดแหว, โควตา, ช่องโหว่
                if original_word in {"เขว", "เหว่", "แคว", "แหว", "โคว", "โหว", "โหว่"}:
                    return False

        # If it passed all the filters above, it is a true final (จัย, สมัย, ชล, ผล, เหนื่อย)
        return True

    def check_sara(self, word: str) -> str:
        """
        Check the phonetic vowel sound (สระ) of a Thai word.

        Extracts the core vowel representation used for rhyme matching, handling complex vowel combinations,
        transformed vowels (สระเปลี่ยนรูป), and reductions (สระลดรูป).

        :param str word: Thai word
        :return: The name of the vowel sound of the word (e.g., 'เออ', 'อะ', 'เอาะ')
        :rtype: str

        :Example:

            >>> from pythainlp.khavee import KhaveeVerifier  # doctest: +SKIP
            >>> kv = KhaveeVerifier()  # doctest: +SKIP
            >>> print(kv.check_sara("เริง"))  # doctest: +SKIP
            'เออ'
        """
        sara = []
        countoa = 0  # Count occurrences of 'อ'

        # Store original word to safely evaluate exceptions (like ฤทธิ์) after Karun stripping
        original_word = word

        # In case of การันย์ (word stripped of Karun characters)
        word = self.handle_karun_sound_silence(word)
        # Remove tonemarks for checking endings safely
        word_req = remove_tonemark(word)

        # Intercept Pali/Sanskrit words with silent terminal vowels (สระที่ไม่ออกเสียงท้ายคำ) Removing the final character -ิ or -ุ
        silent_vowel_exceptions = {"เกียรติ", "ชาติ", "ญาติ", "มัติ", "วัติ", "บัติ", "ญัติ", "ยัติ",
                                   "ภูมิ", "พฤติ", "พรรดิ", "วรรดิ", "พยาธิ", "โพธิ", "เกตุ", "เมรุ", "เหตุ", "ธาตุ", "วุฒิ"}
        if any(word_req.endswith(ex) for ex in silent_vowel_exceptions):
            word = word[:-1]
            word_req = word_req[:-1]

        # In case of สระเดี่ยว
        for i in word:
            if i == "ั" and word_req.endswith("ว"):
                sara.append("อัว")
            elif i in ("ะ", "ั"):
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
            elif i in ("ไ", "ใ"):
                sara.append("ไอ")
            elif i == "็":
                sara.append("็")

        # In case of รร
        if "รร" in word:
            if self.check_marttra(word) == "กม":
                sara.append("อำ")
            else:
                sara.append("อะ")

        # Clean up 'ออ' if 'อ' is acting purely as an initial consonant (อต, อด, อบ, อวบ)
        if "ออ" in sara and len(sara) == 1 and word.startswith("อ") and countoa == 1:
            sara.remove("ออ")

        # In case of ออ (Clean redundant ออ from compound vowels like คือ, มือ)
        if countoa == 1 and "อ" in word[-1] and "เ" not in word and "ออ" in sara and len(sara) > 1:
            sara.remove("ออ")

        # In case of เอ เอ (merging two 'เอ' into 'แอ')
        if sara.count("เอ") >= 2:
            sara.remove("เอ")
            sara.remove("เอ")
            sara.append("แอ")

        # In case of สระประสม
        if "เอ" in sara and "อะ" in sara:
            sara.remove("เอ")
            sara.remove("อะ")
            sara.append("เอะ")
        elif "แอ" in sara and "อะ" in sara:
            sara.remove("แอ")
            sara.remove("อะ")
            sara.append("แอะ")

        # In case of สระประสม Transformed vowels ไม้ไต่คู้ (-็)
        if "็" in sara:
            sara.remove("็")
            if "เอ" in sara:
                sara.remove("เอ")
                sara.append("เอะ")  # เจ็ด, เป็น, เด็ก
            elif "แอ" in sara:
                sara.remove("แอ")
                sara.append("แอะ")  # แข็ง, แท็กซี่, แย็บ
            else:
                if "ออ" in sara:
                    sara.remove("ออ")
                sara.append("เอาะ")  # ก็, ล็อก, ผล็อย

        if "เอะ" in sara and "ออ" in sara:
            sara.remove("เอะ")
            sara.remove("ออ")
            sara.append("เออะ")
        elif "เอ" in sara and "อิ" in sara:
            sara.remove("เอ")
            sara.remove("อิ")
            sara.append("เออ")  # เกิด, เมิน
        elif "เอ" in sara and "ออ" in sara and "อ" in word[-1]:
            sara.remove("เอ")
            sara.remove("ออ")
            sara.append("เออ")  # เหม่อ
        elif "โอ" in sara and "อะ" in sara:
            sara.remove("โอ")
            sara.remove("อะ")
            sara.append("โอะ")  # โต๊ะ
        elif "เอ" in sara and "อี" in sara:
            sara.remove("เอ")
            sara.remove("อี")
            sara.append("เอีย")  # เรียน
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
            sara.append("เอือ")  # มะเขือ, เสือ, เงือก
        elif "ออ" in sara and len(sara) > 1:
            sara.remove("ออ")
        elif "ว" in word and len(sara) == 0:
            if word_req in {"บวร", "วร"}:
                sara.append("ออ")
            else:
                sara.append("อัว")  # ควร, บวก, สวม

        if "ั" in word and self.check_marttra(word) == "กา":
            if "อัว" not in sara:
                sara = ["ไอ"]

        # In case of อ
        if word == "เออะ":
            sara = ["เออะ"]
        elif word == "เออ":
            sara = ["เออ"]
        elif word == "เอ":
            sara = ["เอ"]
        elif word == "เอะ":
            sara = ["เอะ"]
        elif word == "เอา":
            sara = ["เอา"]
        elif word == "เอาะ":
            sara = ["เอาะ"]

        # In case of เ-ือ
        if "เ" in word and "ื" in word and "อ" in word:
            sara = ["เอือ"]

        # In case of เ-ย (ลดรูป เ-อ) เลย, เคย, เอย
        if "เอ" in sara and word_req.endswith("ย") and self._is_true_final(original_word):
            # Ensure no competing vowels exist ('เตียง' uses เอีย, not เออ)
            other_vowels = [v for v in sara if v not in {"เอ", "ออ"}]
            if not other_vowels:
                sara = ["เออ"]

        # In case of ฤ ฦ
        if any(ex in original_word for ex in ("ฤา", "ฤๅ", "ฦา", "ฦๅ")):
            sara = ["อือ"]
        elif "ฤ" in original_word or "ฦ" in original_word:
            sara = []
            # for 'เออ' (ฤกษ์ - เริก) the only 'เออ' sound exception of ฤ
            if word == "ฤก" or original_word.startswith("ฤกษ"):
                sara.append("เออ")
            # for 'อิ' (กฤษณ์, กฤษณะ, ตฤณ, ตฤตีย, ทฤษฎี, ประกฤติ, วิกฤต, ฤทธิ์, อังกฤษ)
            # Use original_word here to ensure stripped Karun characters (like ธิ์) are evaluated
            elif any(ex in original_word for ex in {"กฤช", "กฤต", "กฤษ", "ตฤต", "ตฤณ", "ทฤษ", "ปฤษ", "ศฤง", "สฤต", "ฤทธ"}):
                sara.append("อิ")
            # Default 'อึ' (รึ) (ฤดู, ฤทัย, พฤษภาคมม)
            else:
                sara.append("อึ")

        # In case of สระลดรูป (ออ, โอะ)
        if not sara and len(word) >= 2:
            if word[-1] == "ร":
                # Words ending with ร without vowels usually take the 'ออ' sound (พร, นคร)
                sara.append("ออ")
            else:
                # Other consonants without vowels usually take the hidden 'โอะ' sound (นม, กรด)
                sara.append("โอะ")

        # In case of นิกหิต (-ํ) + า (miss-typed of สระอำ) or standalone นิกหิต (-ํ) 'อัง'
        if "ํ" in word:
            if "ํา" in word:
                sara = ["อำ"]  # The strict decomposed 'อำ' typo
            else:
                # Standalone sounds like 'อัง' (อะ + ง) from pali/sanskrit
                sara = ["อะ"]

        # In case of บ่ / บ
        if word_req == "บ":
            sara = ["ออ"]

        # In case of isolated symbols as words (ลดรูป อะ)
        if word_req in {"ณ", "ธ", "อ", "พณ"}:
            sara = ["อะ"]

        if not sara:
            return "Can't find Sara in this word"

        return sara[0]

    def check_marttra(self, word: str) -> str:
        """
        Check the spelling section (มาตราตัวสะกด) of a Thai word.

        Note: This function strictly adheres to orthographic spelling (รูป) based on
        the Royal Society of Thailand (ราชบัณฑิตยสภา) standards, rather than phonetics (เสียง).
        Therefore, words ending in สระเกิน (อำ, ไอ, ใอ, เอา) as well as ฤ, ฤๅ, ฦ, ฦๅ
        are correctly classified grammatically as แม่ ก กา ("กา"). Phonetic rhyming
        for these vowels is handled dynamically in the `is_sumpus` function.

        :param str word: Thai word
        :return: name of the spelling section of the word (e.g., กา, กก, กด, กน, กบ, กม, เกย, เกอว)
        :rtype: str

        :Example:

            >>> from pythainlp.khavee import KhaveeVerifier  # doctest: +SKIP
            >>> kv = KhaveeVerifier()  # doctest: +SKIP
            >>> print(kv.check_marttra("สาว"))  # doctest: +SKIP
            'เกอว'
            >>> print(kv.check_marttra("ทำ"))  # doctest: +SKIP
            'กา'
        """
        # Handle consonant clusters ending with ร
        # ตร, ทร → remove ร (treat as final ต/ท sound)
        # กร, ขร, คร, ฆร in compound words → remove ร (treat as final ก/ข/ค sound)
        # But single syllable words like "กร" should keep ร
        if len(word) >= 3 and word[-1] == "ร":
            if word[-2] in {"ต", "ท"}:
                word = word[:-1]
            elif word[-2] in {"ก", "ข", "ค", "ฆ"}:
                word = word[:-1]

        word = self.handle_karun_sound_silence(word)

        # is_true_final process requires the original word to check for exceptions in อักษรนำ/คำควบกล้ำ
        original_word = word

        word = remove_tonemark(word)

        # Intercept Pali/Sanskrit words with silent terminal vowels (สระที่ไม่ออกเสียงท้ายคำ) Removing the final character -ิ or -ุ
        silent_vowel_exceptions = {"เกียรติ", "ชาติ", "ญาติ", "มัติ", "วัติ", "บัติ", "ญัติ", "ยัติ", "ภูมิ",
                                   "พฤติ", "พรรดิ", "วรรดิ", "พยาธิ", "โพธิ", "เกตุ", "เมรุ", "เหตุ", "ธาตุ", "วุฒิ", "สมมุติ"}
        if any(word.endswith(ex) for ex in silent_vowel_exceptions):
            word = word[:-1]

        # Check for อักษรตัวเดียวแทนคำ Standalone words
        if word in {"บ", "ณ", "ธ", "พณ", "ฤ", "ฦ"}:
            return "กา"

        # -------------------------------------------------------------------------
        # สระเกิน (อำ, ไอ, ใอ, เอา) Orthographic Handlers
        # According to the Royal Society, these are classified structurally as แม่ ก กา.
        # Phonetic rhyming (e.g. กรรม rhyming with จำ) is normalized in `is_sumpus`.
        # -------------------------------------------------------------------------

        # Check for ำ or นิคหิต (-ํ) + า
        if word[-1] == "ำ" or word.endswith("ํา"):
            return "กา"

        # Check for standalone นิคหิต (-ํ) 'อัง'
        if word.endswith("ํ"):
            return "กง"

        # Any word with exactly 1 consonant (and not ending in ำ/ํ) cannot have a final consonant and therefore must be "กา"

        consonants = [c for c in word if c in self.VALID_CONSONANTS]
        if len(consonants) == 1:
            return "กา"

        # Check for ไ/ใ
        if "ไ" in word or "ใ" in word:
            if word[-1] not in {"ย", "ล", "ร", "ว"}:
                return "กา"
            elif not self._is_true_final(original_word):
                return "กา"

        # Check for เ, แ, โ + ย, ร, ล, ว (คำควบกล้ำ / อักษรนำ)
        if word[-1] in {"ย", "ล", "ร", "ว"} and any(v in word for v in {"เ", "แ", "โ"}):
            # ไม่ใช่ตัวสะกดแท้ -> แม่ก กา
            if not self._is_true_final(original_word):
                return "กา"

        # Check for ตัวสะกด final consonants
        # Add รากยาว "ๅ" (not สระอา) for word like ฤๅ(ษี)
        if (
            word[-1] in {"า", "ๅ", "ะ", "ิ", "ี", "ึ", "ุ", "ู", "อ"}
            or ("ี" in word and "ย" in word[-1])  # Catch สระเอีย (เสีย, เมีย)
            or ("ื" in word and "อ" in word[-1])  # Catch สระอือ (เรือ, เสือ)
            or ("ั" in word and "ว" in word[-1])  # Catch สระอัว (ตัว, ชั่ว, กลัว, อัว)
        ):
            return "กา"
        elif word[-1] in {"ง"}:
            return "กง"
        elif word[-1] in {"ม"}:
            return "กม"
        elif word[-1] in {"ย"}:
            return "เกย"
        elif word[-1] in {"ว"}:
            return "เกอว"
        elif word[-1] in {"ก", "ข", "ค", "ฆ"}:
            return "กก"
        elif word[-1] in {
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
        }:
            return "กด"
        elif word[-1] in {"ญ", "ณ", "น", "ร", "ล", "ฬ"}:
            return "กน"
        elif word[-1] in {"บ", "ป", "พ", "ฟ", "ภ"}:
            return "กบ"
        else:
            if "็" in word:
                return "กา"
            else:
                return "Can't find Marttra in this word"

    def is_sumpus(self, word1: str, word2: str) -> bool:
        """
        Check the rhyme (สัมผัส) between two Thai words.

        This function evaluates both the vowel sound (สระ) and the spelling section (มาตราตัวสะกด).
        It incorporates phonetic normalization for สระเกิน (อำ, ไอ, ใอ) to ensure that
        words with matching sounds but differing orthographies (e.g., "จำ" and "กรรม")
        are correctly evaluated as rhymes.

        :param str word1: First Thai word
        :param str word2: Second Thai word
        :return: True if the words rhyme, False otherwise.
        :rtype: bool

        :Example:

            >>> from pythainlp.khavee import KhaveeVerifier  # doctest: +SKIP
            >>> kv = KhaveeVerifier()  # doctest: +SKIP
            >>> print(kv.is_sumpus("สรร", "อัน"))  # doctest: +SKIP
            True
            >>> print(kv.is_sumpus("จำ", "กรรม"))  # doctest: +SKIP
            True
        """
        marttra1 = self.check_marttra(word1)
        marttra2 = self.check_marttra(word2)
        sara1 = self.check_sara(word1)
        sara2 = self.check_sara(word2)

        # -------------------------------------------------------------------------
        # Phonetic Normalization for สระเกิน (อำ, ไอ, ใอ)
        #
        # While check_marttra classifies words like "วัย" as อะ+เกย and "ใจ" as ไอ+กา,
        # poetry cares about the sound (เสียง).
        # We normalize the phonetic CVC structures into their สระเกิน counterparts.
        # ('เอา' requires no normalizer as native Thai spelling forces the /aw/ sound
        # to use 'เ-า', bypassing the need for an อะ+เกอว collision).
        # -------------------------------------------------------------------------

        # อัย -> ไอ (Normalize 'อะ' + 'เกย' to 'ไอ' + 'กา')
        if sara1 == "อะ" and marttra1 == "เกย":
            sara1 = "ไอ"
            marttra1 = "กา"
        if sara2 == "อะ" and marttra2 == "เกย":
            sara2 = "ไอ"
            marttra2 = "กา"
        # อัม -> อำ (Normalize both 'อำ' and 'อะ' + 'กม' to 'อำ' + 'กา')
        if (sara1 == "อะ" or sara1 == "อำ") and marttra1 == "กม":
            sara1 = "อำ"
            marttra1 = "กา"
        if (sara2 == "อะ" or sara2 == "อำ") and marttra2 == "กม":
            sara2 = "อำ"
            marttra2 = "กา"
        return bool(marttra1 == marttra2 and sara1 == sara2)

    def check_karu_lahu(self, text: str) -> str:
        if text in {"บ", "บ่", "ณ", "ธ", "ก็", "ฤ", "ฦ"}:
            return "lahu"

        marttra = self.check_marttra(text)
        sara = self.check_sara(text)

        if (marttra != "กา"
            or (marttra == "กา" and sara in
                {"อา", "อี", "อือ", "อู", "เอ", "แอ",
                 "เออ", "โอ", "ออ", "เอีย", "เอือ", "อัว"})
                or sara in {"อำ", "ไอ", "เอา"}):
            return "karu"
        else:
            return "lahu"

    def check_klon(self, text: str, k_type: int = 8) -> Union[list[str], str]:
        """
        Check the suitability of the poem according to Thai principles.

        :param str text: Thai poem
        :param int k_type: type of Thai poem (4 or 8)
        :return: the check results of the suitability of the poem according to Thai principles.
        :rtype: Union[list[str], str]

        ════════════════════════════════════════════════════════════════════════

        กลอนสี่ (Klon 4) Diagram:
        วรรคที่ ๑ (สดับ)    วรรคที่ ๒ (รับ)
        วรรคที่ ๓ (รอง)    วรรคที่ ๔ (ส่ง)

              ┏━━━━━━━━┯━┓    [สัมผัสคำที่ 1 หรือ 2]
        O O O X        X X O O
              ┏━━━━━━━━┯━┳━━━┛
        O O O X        X X O X ━┓
              ┏━━━━━━━━┯━┓      ┃ สัมผัสระหว่างบท (Inter-stanza rhyme)
        O O O X        X X O O ━┛
              ┏━━━━━━━━┯━┳━━━┛
        O O O X        X X O X

        ════════════════════════════════════════════════════════════════════════

        กลอนแปด (Klon 8) Diagram:
        วรรคที่ ๑ (สดับ)    วรรคที่ ๒ (รับ)
        วรรคที่ ๓ (รอง)    วรรคที่ ๔ (ส่ง)

                      ┏━━━━━━━━┯━┯━┳━┯━┑    [สัมผัสคำที่ 3 หรือ 5 / อนุโลม 1,2,4]
        O O O O O O O X        O O X O O O O X
                      ┏━━━━━━━━┯━┯━┳━┯━━━━━━━┛
        O O O O O O O X        O O X O O O O X ━┓
                      ┏━━━━━━━━┯━┯━┳━┯━┑        ┃ สัมผัสระหว่างบท (Inter-stanza rhyme)
        O O O O O O O X        O O X O O O O X ━┛
                      ┏━━━━━━━━┯━┯━┳━┯━━━━━━━┛
        O O O O O O O X        O O X O O O O X

        ════════════════════════════════════════════════════════════════════════

        :Example:

            >>> from pythainlp.khavee import KhaveeVerifier  # doctest: +SKIP
            >>> kv = KhaveeVerifier()  # doctest: +SKIP
            >>> print(kv.check_klon(  # doctest: +SKIP
            ...     'ฉันชื่อหมูกรอบ ฉันชอบกินไก่ แล้ววิ่งตามไป ไล่หมาน้ำทอง \
            ...     ฉันมันคนเก่ง เอ๋งเอ๋งคะนอง มีคนจับจอง เป็นของน้องเธียร', \
            ...     k_type=4
            ... ))
            The poem is correct according to the principle.
        """

        try:
            import ssg  # type: ignore[import-unresolved]
        except ImportError:
            raise ImportError(
            "The 'ssg' package is required for check_klon. "
            "Please install it using: pip install pythainlp[extra] or pip install ssg"
        )

        if k_type not in {4, 8}:
            return "Something went wrong. Make sure you enter it in the correct form (k_type 4 or 8)."

        try:
            # Normalize spacing with regex Splits by spaces, newlines, or transitions between phrases
            waks = [w for w in re.split(r'\s+|\n+|\t+', text.strip()) if w]
            # Ensure the poem has complete stanzas (4 waks per stanza)
            if len(waks) % 4 != 0 or len(waks) == 0:
                return "The poem does not have complete stanzas (บท). A stanza must contain exactly 4 sentences (วรรค)."

            errors = []
            stanzas = []
            wak_names = ["วรรคสดับ (Wak 1)", "วรรครับ (Wak 2)", "วรรครอง (Wak 3)", "วรรคส่ง (Wak 4)"]

            # 1. Tokenize and group sentences into stanzas (4 Waks per stanza)
            for i in range(0, len(waks), 4):
                stanza = [
                    subword_tokenize(waks[i], engine="ssg"),
                    subword_tokenize(waks[i + 1], engine="ssg"),
                    subword_tokenize(waks[i + 2], engine="ssg"),
                    subword_tokenize(waks[i + 3], engine="ssg"),
                ]
                stanzas.append(stanza)

            # 2. Evaluate rules for each stanza
            for stanza_index, stanza in enumerate(stanzas):
                wak1, wak2, wak3, wak4 = stanza

                # Safety check against empty sentences
                if not all((wak1, wak2, wak3, wak4)):
                    errors.append(f"Stanza (บทที่) {stanza_index + 1} contains empty sentences.")
                    continue

                # Check word counts
                max_words = 10 if k_type == 8 else 5
                for wak_index, wak in enumerate(stanza):
                    if len(wak) > max_words:
                        errors.append(
                            f"Stanza (บทที่) {stanza_index + 1} {wak_names[wak_index]}: "
                            f"Word count exceeds {max_words}: {wak}"
                        )

                # Define rhyme target lengths based on Klon type
                # Klon 8: Targets first 5 words (อนุโลม 1, 2, 4 บังคับ 3, 5)
                # Klon 4: Targets first 2 words
                if k_type == 8:
                    wak2_targets = wak2[:5]
                    wak4_targets = wak4[:5]
                else:
                    # Klon 4: If the target sentence has 5 words, check the first 3 words.
                    # Otherwise, check the standard first 2 words.
                    limit_wak2 = 3 if len(wak2) == 5 else 2
                    limit_wak4 = 3 if len(wak4) == 5 else 2

                    wak2_targets = wak2[:limit_wak2]
                    wak4_targets = wak4[:limit_wak4]

                # Extract the last word of each Wak
                wak1_last = wak1[-1]
                wak2_last = wak2[-1]
                wak3_last = wak3[-1]

                # Rule 1: วรรคสดับ -> วรรครับ
                if not any(self.is_sumpus(wak1_last, target) for target in wak2_targets):
                    errors.append(
                        f"Rhyme error in Stanza (บทที่) {stanza_index + 1}: "
                        f"'{wak1_last}' ({wak_names[0]}) does not rhyme with {wak2_targets} ({wak_names[1]})"
                    )

                # Rule 2: วรรครับ -> วรรครอง
                if not self.is_sumpus(wak2_last, wak3_last):
                    errors.append(
                        f"Rhyme error in Stanza (บทที่) {stanza_index + 1}: "
                        f"'{wak2_last}' ({wak_names[1]}) does not rhyme with '{wak3_last}' ({wak_names[2]})"
                    )

                # Rule 3: วรรครอง -> วรรคส่ง
                if not any(self.is_sumpus(wak3_last, target) for target in wak4_targets):
                    errors.append(
                        f"Rhyme error in Stanza (บทที่) {stanza_index + 1}: "
                        f"'{wak3_last}' ({wak_names[2]}) does not rhyme with {wak4_targets} ({wak_names[3]})"
                    )

                # Rule 4: สัมผัสระหว่างบท (Inter-stanza)
                if stanza_index > 0:
                    # Target Wak 4 of the previous stanza
                    prev_wak4_last = stanzas[stanza_index - 1][3][-1]
                    if not self.is_sumpus(prev_wak4_last, wak2_last):
                        errors.append(
                            f"Inter-stanza rhyme error (ผิดสัมผัสระหว่างบท) between Stanza {stanza_index} and {stanza_index + 1}: "
                            f"'{prev_wak4_last}' ({wak_names[3]}) does not rhyme with '{wak2_last}' ({wak_names[1]})"
                        )

            if not errors:
                return "The poem is correct according to the principle."
            return errors

        except Exception as e:
            return f"Something went wrong during evaluation: {e}"

    def check_aek_too(
        self, text: Union[list[str], str], dead_syllable_as_aek: bool = False
    ) -> Union[list[Union[bool, str]], bool, str]:
        """
        Checker of Thai tonal words

        :param Union[list[str], str] text: Thai word or list of Thai words
        :param bool dead_syllable_as_aek: if True, dead syllable will
            be considered as aek
        :return: the check result if the word is aek or too
            or False (not both) or list of check results if input is list
        :rtype: Union[list[bool], List[str], bool, str]

        :Example:

            >>> from pythainlp.khavee import KhaveeVerifier  # doctest: +SKIP

            >>> kv = KhaveeVerifier()  # doctest: +SKIP

            >>> # การเช็คคำเอกโท
            >>> print(  # doctest: +SKIP
            ...     kv.check_aek_too("เอง"),
            ...     kv.check_aek_too("เอ่ง"),
            ...     kv.check_aek_too("เอ้ง"),
            ... )
            >>> # -> False, aek, too
            >>> print(kv.check_aek_too(["เอง", "เอ่ง", "เอ้ง"]))  # ใช้ List ได้เหมือนกัน  # doctest: +SKIP
            >>> # -> [False, 'aek', 'too']
        """
        if isinstance(text, list):
            return [self.check_aek_too(t, dead_syllable_as_aek) for t in text] # type: ignore[misc]

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
        Handle silent sounds in Thai words using '-์' character (Karun)
        by stripping all characters before the 'Karun' character
        that should be silenced

        :param str word: Thai word
        :return: Thai word with silent consonant stripped
        :rtype: str
        """
        # Only process if the word ends with Karun (-์) [word like โอห์ม which has Karun in the middle will not be processed]
        if not word.endswith("์"):
            return word

        # For specific multi-letter Karun silent suffixes
        # 'พระลักษมณ์' -> strip 'ษมณ์' (leaving 'ก' for แม่กก)
        if word.endswith("กษมณ์"):
            return word[:-4]
        # 'ลักษณ์', 'ทรลักษณ์' -> strip 'ษณ์' avoid breaking 'สัมภาษณ์'
        if word.endswith("กษณ์"):
            return word[:-3]
        # 'กษัตริย์' -> strip 'ริย์'
        if word.endswith("ตริย์"):
            return word[:-4]
        # 'กาญจน์' -> strip 'จน์' avoid breaking 'โรจน์'
        if word.endswith("ญจน์"):
            return word[:-3]

        # For 2-Consonant Karun silent suffixes
        # ตร์: ศาสตร์, ภาพยนตร์, กาสาวพัสตร์, เวทมนตร์
        # ทร์: จันทร์, บดินทร์, ภูมินทร์, นราธิเบนทร์
        # ดร์: นิรันดร์
        # ฎร์: ราษฎร์, สุราษฎร์
        if word.endswith(("ตร์", "ทร์", "ดร์", "ฎร์")):
            return word[:-3]

        # For Standard Karun silent suffixes (1 Consonant + Optional Vowel + Karun)
        # สัตว์ (ว์), แพทย์ (ย์), พันธุ์ (ธุ์), สิทธิ์ (ธิ์)
        # Check if there is an upper/lower vowel right before the Karun (ธุ์, ธิ์)
        if len(word) >= 3 and word[-2] in {"ิ", "ี", "ึ", "ื", "ุ", "ู", "ั"}:
            return word[:-3]
        else:
            return word[:-2]
