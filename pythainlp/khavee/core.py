# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Verifier for Thai poetry (khavee) principles."""

from __future__ import annotations

from typing import ClassVar, Optional, Union

from pythainlp import thai_consonants
from pythainlp.tokenize import subword_tokenize
from pythainlp.util import remove_tonemark, sound_syllable
from pythainlp.util.syllable import spelling_class


class KhaveeVerifier:
    """
    Verifier for Thai poetry (ฉันทลักษณ์) principles.

    Provides methods to analyze Thai words and validate poetic structures
    according to traditional Thai prosody rules. This class checks vowel
    sounds (สระ), spelling sections (มาตราตัวสะกด), rhymes (สัมผัส),
    syllable weight (ครุ/ลหุ), and full Thai klon 4/8 poem structure (กลอน).

    This class is designed to be deterministic according to the Royal
    Society of Thailand's orthographic standards. The only exception is
    the use of "ssg" for syllable segmentation in :meth:`check_klon`.

    Key capabilities:

    * :meth:`check_sara` - identify the phonetic vowel sound of a Thai
      word, handling complex vowels (สระประสม), transformed vowels
      (สระเปลี่ยนรูป), and reduced vowels (สระลดรูป)
    * :meth:`check_marttra` - determine the orthographic spelling section
      (relative to the final consonant) per Royal Society standards
    * :meth:`is_sumpus` - evaluate whether two words rhyme by comparing
      both vowel sound and spelling section, with phonetic normalization
      for สระเกิน (e.g., อำ, ไอ)
    * :meth:`check_karu_lahu` - classify a syllable as heavy (ครุ) or
      light (ลหุ) for meter analysis
    * :meth:`check_klon` - validate an entire poem against traditional
      กลอนสี่ (4-syllable) or กลอนแปด (8-syllable) rhyme rules
    * :meth:`check_aek_too` - identify tonal marks (เอก/โท) on Thai words
    * :meth:`handle_karun_sound_silence` - strip characters silenced by
      the การันต์ marker (e.g., "โอห์ม" -> "โอ")
    * :meth:`_has_true_final_yl` and :meth:`_is_true_final` - determine
      whether a word-ending "ย" or "ล" is a genuine final consonant
      rather than part of an initial cluster or vowel digraph

    :Example:
        Basic usage::

            >>> from pythainlp.khavee import KhaveeVerifier
            >>> kv = KhaveeVerifier()
            >>> kv.check_sara("เริง")
            'เออ'
            >>> kv.is_sumpus("สรร", "อัน")
            True
            >>> kv.check_klon(
            ...     'ฉันชื่อหมูกรอบ ฉันชอบกินไก่ แล้ววิ่งตามไป ไล่หมาน้ำทอง',
            ...     k_type=4
            ... )
            'The poem is correct according to the principle.'

    :Note:
        The method :meth:`check_klon` requires the external ``ssg`` library.
    """

    # ฤ and ฦ act as initial consonants but are not in thai_consonants
    VALID_CONSONANTS = frozenset(thai_consonants + "ฤฦ")

    # Pali/Sanskrit loanwords where the final -ิ or -ุ is orthographically
    # present but phonetically silent. Stripping it is harmless in check_sara
    # (the leading vowel is detected first) and necessary in check_marttra
    # (to expose the true final consonant for spelling-section classification).
    _MASKING_TERMINAL_VOWELS: tuple[str, ...] = (
        "เกียรติ",
        "ชาติ",
        "ญาติ",
        "มัติ",
        "วัติ",
        "บัติ",
        "ญัติ",
        "ยัติ",
        "ภูมิ",
        "พฤติ",
        "พรรดิ",
        "วรรดิ",
        "พยาธิ",
        "โพธิ",
        "เกตุ",
        "เมรุ",
        "เหตุ",
        "ธาตุ",
        "วุฒิ",
        "สมมุติ",
        "วิมุติ",
    )

    # Syllables that are always light (ลหุ) regardless of orthography.
    _LAHU_SYLLABLE_OVERRIDES: frozenset[str] = frozenset(
        {
            "บ",
            "บ่",
            "ณ",
            "ธ",
            "ก็",
            "ฤ",
            "ฦ",
        }
    )

    # Pre-computed frozensets for high-frequency set operations
    _SINGLE_CHAR_WORDS: frozenset[str] = frozenset(
        {"บ", "ณ", "ธ", "พณ", "ฤ", "ฦ"}
    )

    # Initial cluster sets for _is_true_final
    _LAM_CLUSTERS: frozenset[str] = frozenset(
        {
            "กล",
            "ขล",
            "คล",
            "ปล",
            "ผล",
            "พล",
            "หล",
            "ถล",
            "ฉล",
            "สล",
            "ศล",
            "ตล",
        }
    )
    _RUA_CLUSTERS: frozenset[str] = frozenset(
        {"กร", "ขร", "คร", "ตร", "ปร", "พร", "ฟร", "บร", "ศร", "สร", "หร"}
    )
    _WA_CLUSTERS: frozenset[str] = frozenset(
        {"กว", "ขว", "คว", "สว", "หว", "ทว", "ชว", "ศว", "ถว"}
    )
    _WA_WHITELIST: frozenset[str] = frozenset(
        {"เขว", "เหว่", "แคว", "แหว", "โคว", "โหว", "โหว่"}
    )

    # Spelling sections (มาตราตัวสะกด)
    _OPEN_SYLLABLE_VOWELS: frozenset[str] = frozenset(
        {"า", "ๅ", "ะ", "ิ", "ี", "ึ", "ุ", "ู", "อ"}
    )

    # Karu / Lahu prosody
    _LONG_VOWELS: frozenset[str] = frozenset(
        {
            "อา",
            "อี",
            "อือ",
            "อู",
            "เอ",
            "แอ",
            "เออ",
            "โอ",
            "ออ",
            "เอีย",
            "เอือ",
            "อัว",
        }
    )
    _SPECIAL_VOWELS: frozenset[str] = frozenset({"อำ", "ไอ", "เอา"})
    _EXPLICIT_SARA_WORDS: frozenset[str] = frozenset(
        {"เออะ", "เออ", "เอ", "เอะ", "เอา", "เอาะ"}
    )

    # check_sara: vowel sound of each vowel sign (สระเดี่ยว).
    # "ั" maps to "อัว" instead when the word ends with "ว".
    _SARA_OF_SIGN: ClassVar[dict[str, str]] = {
        "ะ": "อะ",
        "ั": "อะ",
        "ิ": "อิ",
        "ุ": "อุ",
        "ึ": "อึ",
        "ี": "อี",
        "ู": "อู",
        "ื": "อือ",
        "เ": "เอ",
        "แ": "แอ",
        "า": "อา",
        "โ": "โอ",
        "ำ": "อำ",
        "อ": "ออ",
        "ไ": "ไอ",
        "ใ": "ไอ",
        "็": "็",
    }

    # check_sara: ordered merge rules, first match wins.
    # (first, second, merged, requires the word to end with "อ")
    _SHORT_SARA_MERGES: tuple[tuple[str, str, str, bool], ...] = (
        ("เอ", "อะ", "เอะ", False),
        ("แอ", "อะ", "แอะ", False),
    )
    _COMPOUND_SARA_MERGES: tuple[tuple[str, str, str, bool], ...] = (
        ("เอะ", "ออ", "เออะ", False),
        ("เอ", "อิ", "เออ", False),  # เกิด, เมิน
        ("เอ", "ออ", "เออ", True),  # เหม่อ
        ("โอ", "อะ", "โอะ", False),  # โต๊ะ
        ("เอ", "อี", "เอีย", False),  # เรียน
        ("เอ", "อา", "เอา", False),
    )
    _UEA_SARA_MERGES: tuple[tuple[str, str, str, bool], ...] = (
        ("เออ", "อือ", "เอือ", False),  # มะเขือ, เสือ, เงือก
    )

    # check_sara: ฤ/ฦ sequences
    _RUE_LONG_SEQUENCES: tuple[str, ...] = ("ฤา", "ฤๅ", "ฦา", "ฦๅ")
    # 'อิ' (กฤษณ์, กฤษณะ, ตฤณ, ตฤตีย, ทฤษฎี, ประกฤติ, วิกฤต, ฤทธิ์, อังกฤษ)
    _RUE_I_SEQUENCES: tuple[str, ...] = (
        "กฤช",
        "กฤต",
        "กฤษ",
        "ตฤต",
        "ตฤณ",
        "ทฤษ",
        "ปฤษ",
        "ศฤง",
        "สฤต",
        "ฤทธ",
    )

    # check_marttra: last character -> vowel sign that makes the syllable open
    # (เสีย, เมีย; เรือ, เสือ; ตัว, ชั่ว, กลัว, อัว)
    _SIGN_OF_FINAL: ClassVar[dict[str, str]] = {"ย": "ี", "อ": "ื", "ว": "ั"}
    # check_marttra: spelling section (มาตราตัวสะกด) of each final consonant
    _MARTTRA_OF_FINAL: ClassVar[dict[str, str]] = {
        char: marttra
        for marttra, chars in spelling_class.items()
        for char in chars
    }

    # check_klon
    _WAK_NAMES: tuple[str, ...] = ("Wak 1", "Wak 2", "Wak 3", "Wak 4")

    def __init__(self) -> None:
        """Initialize the KhaveeVerifier class."""

    # Alias of _is_true_final, kept for backward compatibility.
    def _has_true_final_yl(self, word: str) -> bool:
        """
        Check if ย or ล is a true final consonant.

        A true final consonant is not just part of the vowel sound
        with ไ/ใ.

        :param str word: Thai word
        :return: True if ย or ล is a true final consonant
        :rtype: bool
        """
        return self._is_true_final(word)

    def _is_true_final(self, word: str) -> bool:
        """
        Check if the last character is a true final consonant.

        A true final consonant is not part of a vowel sound or an
        initial cluster.

        :param str word: Thai word
        :return: True if the ending character acts as a final consonant
        :rtype: bool
        """
        word = self.handle_karun_sound_silence(word)
        original_word = word  # keeps tone marks for exception lookups
        word = remove_tonemark(word)  # so 'ใกล้' ends in 'ล'

        if len(word) < 2:
            return False

        last_char = word[-1]

        consonants = [c for c in word if c in self.VALID_CONSONANTS]
        if len(consonants) < 2:
            return False

        # ไ/ใ never take a final consonant ย here is silent (ไทย, ไชย)
        # Check for ย inside เ-ีย (เสีย, เมีย) (part of the vowel)
        if last_char == "ย" and (
            ("ไ" in word or "ใ" in word) or ("เ" in word and "ี" in word)
        ):
            return False

        # Skip the cluster checks unless the word ends in ล, ร, or ว,
        # has exactly 2 consonants, and has a pre-posed vowel.
        if last_char not in "ลรว" or len(consonants) != 2:
            return True

        # Initial clusters (คำควบกล้ำ / อักษรนำ) with pre-posed vowels
        # (เปล, เถล, แผล, โหล, ไกล, ใกล้, โปร, แตร, ไกว, เขว)
        if not any(vowel in word for vowel in "เแโไใ"):
            return True

        cluster = consonants[0] + consonants[1]
        return self._is_true_cluster_final(
            word, original_word, last_char, cluster
        )

    def _is_true_cluster_final(
        self, word: str, original_word: str, last_char: str, cluster: str
    ) -> bool:
        """
        Check if a final ล, ร, or ว after a pre-posed vowel is a true final.

        :param str word: Thai word without tone marks
        :param str original_word: Thai word with tone marks
        :param str last_char: last character of ``word``
        :param str cluster: first two consonants of ``word``
        :return: False if the character is part of an initial cluster
        :rtype: bool
        """
        if last_char == "ล" and cluster in self._LAM_CLUSTERS:
            # 'เพล' (ฉันเพล) is the exception: แม่กน
            return word == "เพล"

        if last_char == "ร" and cluster in self._RUA_CLUSTERS:
            return False

        if last_char == "ว":
            # With ไ/ใ, 'ว' is always a cluster (ไกว, ไขว้)
            if ("ไ" in word or "ใ" in word) and (cluster in self._WA_CLUSTERS):
                return False

            # With เ/แ/โ, 'ว' is mostly a true final (เลว, เหว, แก้ว, แห้ว).
            # The whitelist holds the cluster exceptions (เขว, เหว่, แคว).
            # It matches original_word because the tone mark matters.
            if ("เ" in word or "แ" in word or "โ" in word) and (
                original_word in self._WA_WHITELIST
            ):
                return False

        # (จัย, สมัย, ชล, ผล, เหนื่อย)
        return True

    def check_sara(self, word: str) -> str:
        """
        Check the phonetic vowel sound (สระ) of a Thai word.

        Extracts the core vowel representation used for rhyme matching,
        handling complex vowel combinations,
        transformed vowels (สระเปลี่ยนรูป), and reductions (สระลดรูป).

        :param str word: Thai word
        :return: name of the vowel sound of the word
            (e.g., 'เออ', 'อะ', 'เอาะ')
        :rtype: str

        :Example:

            >>> from pythainlp.khavee import KhaveeVerifier  # doctest: +SKIP
            >>> kv = KhaveeVerifier()  # doctest: +SKIP
            >>> print(kv.check_sara("เริง"))  # doctest: +SKIP
            'เออ'
        """
        original_word = word  # keeps ฤทธิ์-like words after การันต์ stripping
        word = self.handle_karun_sound_silence(word)
        word_req = remove_tonemark(word)

        # Catches "", "อ์", "้", etc.
        if not word_req:
            return ""

        # Drop the silent final -ิ or -ุ of Pali/Sanskrit words
        if word_req.endswith(self._MASKING_TERMINAL_VOWELS):
            word = word[:-1]
            word_req = word_req[:-1]

        sara = self._scan_vowel_signs(word, word_req)
        sara = self._merge_vowel_signs(sara, word, word_req)
        sara = self._apply_word_vowel_rules(
            sara, word, word_req, original_word
        )
        sara = self._apply_reduced_vowel_rules(sara, word, word_req)

        if not sara:
            # No explicit vowel: assume the implied short 'a'.
            return "อะ"

        return sara[0]

    def _scan_vowel_signs(self, word: str, word_req: str) -> list[str]:
        """
        List the vowel sound of each vowel sign (สระเดี่ยว) in a word.

        :param str word: Thai word
        :param str word_req: ``word`` without tone marks
        :return: vowel sounds in the order of their signs, plus one for รร
        :rtype: list[str]
        """
        ends_with_wo = word_req.endswith("ว")
        sara = []
        for char in word:
            if char == "ั" and ends_with_wo:
                sara.append("อัว")
            elif char in self._SARA_OF_SIGN:
                sara.append(self._SARA_OF_SIGN[char])

        # In case of รร
        if "รร" in word:
            if self.check_marttra(word) == "กม":
                sara.append("อำ")
            else:
                sara.append("อะ")
        return sara

    @staticmethod
    def _merge_sara_pair(
        sara: list[str],
        rules: tuple[tuple[str, str, str, bool], ...],
        ends_with_o: bool,
    ) -> bool:
        """
        Merge the first matching pair of vowel sounds in place.

        :param list[str] sara: vowel sounds, modified in place
        :param rules: ordered (first, second, merged, requires final อ) rules
        :param bool ends_with_o: whether the word ends with อ
        :return: True if a rule was applied
        :rtype: bool
        """
        for first, second, merged, requires_final_o in rules:
            if requires_final_o and not ends_with_o:
                continue
            if first in sara and second in sara:
                sara.remove(first)
                sara.remove(second)
                sara.append(merged)
                return True
        return False

    @staticmethod
    def _drop_consonant_o(sara: list[str], word: str) -> None:
        """
        Remove 'ออ' in place where อ acts as a consonant.

        :param list[str] sara: vowel sounds, modified in place
        :param str word: Thai word
        """
        countoa = word.count("อ")
        # Clean up 'ออ' if 'อ' is acting purely as an initial consonant (อต, อด, อบ, อวบ)
        if (
            "ออ" in sara
            and len(sara) == 1
            and word.startswith("อ")
            and countoa == 1
        ):
            sara.remove("ออ")

        # In case of ออ (Clean redundant ออ from compound vowels like คือ, มือ)
        if (
            countoa == 1
            and word[-1] == "อ"
            and "เ" not in word
            and "ออ" in sara
            and len(sara) > 1
        ):
            sara.remove("ออ")

    @staticmethod
    def _apply_mai_taikhu(sara: list[str]) -> None:
        """
        Resolve one ไม้ไต่คู้ (-็) into a short vowel in place.

        :param list[str] sara: vowel sounds, modified in place
        """
        if "็" not in sara:
            return
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

    def _merge_vowel_signs(
        self, sara: list[str], word: str, word_req: str
    ) -> list[str]:
        """
        Merge vowel sounds of single signs into compound vowels (สระประสม).

        :param list[str] sara: vowel sounds from :meth:`_scan_vowel_signs`
        :param str word: Thai word
        :param str word_req: ``word`` without tone marks
        :return: merged vowel sounds
        :rtype: list[str]
        """
        # Mixed contract: helpers mutate `sara` in place, but the เอาะ
        # fallback below returns a new list, so callers use the return value.
        self._drop_consonant_o(sara, word)

        # In case of เอ เอ (merging two 'เอ' into 'แอ')
        if sara.count("เอ") >= 2:
            sara.remove("เอ")
            sara.remove("เอ")
            sara.append("แอ")

        # In case of สระประสม
        self._merge_sara_pair(sara, self._SHORT_SARA_MERGES, False)
        # In case of สระประสม Transformed vowels ไม้ไต่คู้ (-็)
        self._apply_mai_taikhu(sara)

        if not self._merge_sara_pair(
            sara, self._COMPOUND_SARA_MERGES, word[-1] == "อ"
        ) and ("เ" in word and "า" in word and "ะ" in word):
            sara = ["เอาะ"]

        if self._merge_sara_pair(sara, self._UEA_SARA_MERGES, False):
            return sara
        if "ออ" in sara and len(sara) > 1:
            sara.remove("ออ")
        elif "ว" in word and len(sara) == 0:
            if word_req in {"บวร", "วร"}:
                sara.append("ออ")
            else:
                sara.append("อัว")  # ควร, บวก, สวม
        return sara

    def _apply_word_vowel_rules(
        self, sara: list[str], word: str, word_req: str, original_word: str
    ) -> list[str]:
        """
        Override vowel sounds by whole-word patterns.

        :param list[str] sara: vowel sounds from :meth:`_merge_vowel_signs`
        :param str word: Thai word after การันต์ and silent vowel removal
        :param str word_req: ``word`` without tone marks
        :param str original_word: Thai word as given
        :return: vowel sounds
        :rtype: list[str]
        """
        if (
            "ั" in word
            and self.check_marttra(word) == "กา"
            and "อัว" not in sara
        ):
            sara = ["ไอ"]

        # In case of อ
        if word in self._EXPLICIT_SARA_WORDS:
            sara = [word]

        # In case of เ-ือ
        if "เ" in word and "ื" in word and "อ" in word:
            sara = ["เอือ"]

        # In case of เ-ย (ลดรูป เ-อ) เลย, เคย, เอย
        # Ensure no competing vowels exist ('เตียง' uses เอีย, not เออ)
        if (
            "เอ" in sara
            and word_req.endswith("ย")
            and self._is_true_final(original_word)
            and all(v in {"เอ", "ออ"} for v in sara)
        ):
            sara = ["เออ"]

        return self._apply_rue_vowel_rules(sara, word, original_word)

    def _apply_rue_vowel_rules(
        self, sara: list[str], word: str, original_word: str
    ) -> list[str]:
        """
        Override vowel sounds for words with ฤ or ฦ.

        :param list[str] sara: vowel sounds
        :param str word: Thai word after การันต์ and silent vowel removal
        :param str original_word: Thai word as given
        :return: vowel sounds
        :rtype: list[str]
        """
        if any(ex in original_word for ex in self._RUE_LONG_SEQUENCES):
            return ["อือ"]
        if "ฤ" not in original_word and "ฦ" not in original_word:
            return sara
        # for 'เออ' (ฤกษ์ - เริก) the only 'เออ' sound exception of ฤ
        if word == "ฤก" or original_word.startswith("ฤกษ"):
            return ["เออ"]
        # Use original_word here to ensure stripped Karun characters (like ธิ์) are evaluated
        if any(ex in original_word for ex in self._RUE_I_SEQUENCES):
            return ["อิ"]
        # Default 'อึ' (รึ) (ฤดู, ฤทัย, พฤษภาคมม)
        return ["อึ"]

    @staticmethod
    def _apply_reduced_vowel_rules(
        sara: list[str], word: str, word_req: str
    ) -> list[str]:
        """
        Override vowel sounds for reduced vowels (สระลดรูป) and symbols.

        :param list[str] sara: vowel sounds
        :param str word: Thai word after การันต์ and silent vowel removal
        :param str word_req: ``word`` without tone marks
        :return: vowel sounds
        :rtype: list[str]
        """
        # In case of สระลดรูป (ออ, โอะ)
        if not sara and len(word) >= 2:
            # Words ending with ร without vowels usually take the 'ออ' sound (พร, นคร).
            # Other consonants without vowels usually take the hidden 'โอะ' sound (นม, กรด).
            sara = ["ออ"] if word[-1] == "ร" else ["โอะ"]

        # In case of นิกหิต (-ํ) + า (miss-typed of สระอำ) or standalone นิกหิต (-ํ) 'อัง'
        if "ํ" in word:
            # The strict decomposed 'อำ' typo, or standalone sounds like
            # 'อัง' (อะ + ง) from pali/sanskrit
            sara = ["อำ"] if "ํา" in word else ["อะ"]

        # In case of บ่ / บ
        if word_req == "บ":
            sara = ["ออ"]

        # In case of isolated symbols as words (ลดรูป อะ)
        if word_req in {"ณ", "ธ", "อ", "พณ"}:
            sara = ["อะ"]

        return sara

    def check_marttra(self, word: str) -> str:
        """
        Check the spelling section (มาตราตัวสะกด) of a Thai word.

        This function strictly adheres to orthographic spelling (รูป)
        based on the Royal Society of Thailand (ราชบัณฑิตยสภา) standards,
        rather than phonetics (เสียง). Therefore, words ending in
        สระเกิน (อำ, ไอ, ใอ, เอา) as well as ฤ, ฤๅ, ฦ, ฦๅ are classified
        as แม่ ก กา ("กา"). Phonetic rhyming for these vowels is handled
        in :meth:`is_sumpus`.

        :param str word: Thai word
        :return: name of the spelling section of the word
            (e.g., กา, กก, กด, กน, กบ, กม, เกย, เกอว)
        :rtype: str

        :Example:

            >>> from pythainlp.khavee import KhaveeVerifier  # doctest: +SKIP
            >>> kv = KhaveeVerifier()  # doctest: +SKIP
            >>> print(kv.check_marttra("สาว"))  # doctest: +SKIP
            'เกอว'
            >>> print(kv.check_marttra("ทำ"))  # doctest: +SKIP
            'กา'
        """
        # Resolve การันต์ first so "ศาสตร์" and "ศุกร์" skip the cluster logic.
        word = self.handle_karun_sound_silence(word)

        # _is_true_final needs the word with tone marks.
        original_word = word
        word = remove_tonemark(word)

        # Catches "", "อ์", "้", etc.
        if not word:
            return ""

        # Drop the silent final -ิ or -ุ of Pali/Sanskrit words
        if word.endswith(self._MASKING_TERMINAL_VOWELS):
            word = word[:-1]

        word = self._strip_silent_final_ro(word)

        marttra = self._marttra_of_open_form(word, original_word)
        if marttra is not None:
            return marttra
        return self._marttra_of_final(word)

    @staticmethod
    def _strip_silent_final_ro(word: str) -> str:
        """
        Remove a silent final ร of a consonant cluster.

        :param str word: Thai word without tone marks
        :return: ``word`` without the silent final ร
        :rtype: str
        """
        if len(word) < 3 or word[-1] != "ร":
            return word
        prev_char = word[-2]

        # Safe to always strip
        # (e.g., บุตร, เนตร, มิตร, เกษตร, บัตร, เพชร, กอปร (อ่านว่า กอบ))
        if prev_char in {"ต", "ช", "ป"}:
            return word[:-1]

        # Ambiguous (e.g., มังกร vs จักร, สุนทร vs สมุทร)
        # Only strip 'ร' if the cluster is preceded by a specific short vowel
        # -ั, -ิ, -ี, -ุ, -ู (e.g., จั-ก-ร, สมุ-ท-ร).
        # Words like นคร, มังกร, สุนทร remain แม่กน.
        if prev_char in {"ก", "ข", "ค", "ฆ", "ท"} and word[-3] in {
            "ั",
            "ิ",
            "ี",
            "ุ",
            "ู",
        }:
            return word[:-1]
        return word

    def _marttra_of_open_form(
        self, word: str, original_word: str
    ) -> Optional[str]:
        """
        Classify words that cannot have a final consonant.

        :param str word: Thai word without tone marks
        :param str original_word: Thai word with tone marks
        :return: "กา" or "กง", or None if not decided here
        :rtype: Optional[str]
        """
        # Single-character words
        if word in self._SINGLE_CHAR_WORDS:
            return "กา"

        # สระเกิน (อำ, ไอ, ใอ, เอา) are แม่ ก กา by spelling.
        # Phonetic rhyming (กรรม with จำ) is normalized in `is_sumpus`.

        # ำ or นิคหิต (-ํ) + า
        if word[-1] == "ำ" or word.endswith("ํา"):
            return "กา"

        # Standalone นิคหิต (-ํ) 'อัง'
        if word.endswith("ํ"):
            return "กง"

        # Any word with exactly 1 consonant (and not ending in ำ/ํ)
        # cannot have a final consonant and therefore must be "กา"
        consonants = sum(1 for c in word if c in self.VALID_CONSONANTS)
        if consonants == 1:
            return "กา"

        # ไ/ใ
        if ("ไ" in word or "ใ" in word) and (
            word[-1] not in "ยลรว" or not self._is_true_final(original_word)
        ):
            return "กา"

        # เ, แ, โ + ย, ร, ล, ว that is not a true final -> แม่ ก กา
        if (
            word[-1] in "ยลรว"
            and ("เ" in word or "แ" in word or "โ" in word)
            and not self._is_true_final(original_word)
        ):
            return "กา"
        return None

    def _marttra_of_final(self, word: str) -> str:
        """
        Classify a word by its last character.

        :param str word: Thai word without tone marks
        :return: name of the spelling section
        :rtype: str
        """
        last_char = word[-1]
        if last_char in self._OPEN_SYLLABLE_VOWELS:
            return "กา"
        sign = self._SIGN_OF_FINAL.get(last_char)
        if sign is not None and sign in word:
            return "กา"
        return self._MARTTRA_OF_FINAL.get(last_char, "กา")

    def is_sumpus(self, word1: str, word2: str) -> bool:
        """
        Check the rhyme (สัมผัส) between two Thai words.

        This function evaluates both the vowel sound (สระ) and the
        spelling section (มาตราตัวสะกด). It applies phonetic normalization
        for สระเกิน (อำ, ไอ, ใอ), so that words with matching sounds but
        different orthographies (e.g., "จำ" and "กรรม") are evaluated as
        rhymes.

        :param str word1: first Thai word
        :param str word2: second Thai word
        :return: ``True`` if the words rhyme, otherwise ``False``
        :rtype: bool

        :Example:

            >>> from pythainlp.khavee import KhaveeVerifier  # doctest: +SKIP
            >>> kv = KhaveeVerifier()  # doctest: +SKIP
            >>> print(kv.is_sumpus("สรร", "อัน"))  # doctest: +SKIP
            True
            >>> print(kv.is_sumpus("จำ", "กรรม"))  # doctest: +SKIP
            True
        """
        if not word1 or not word2:
            return False

        marttra1 = self.check_marttra(word1)
        marttra2 = self.check_marttra(word2)
        sara1 = self.check_sara(word1)
        sara2 = self.check_sara(word2)

        # check_marttra follows spelling ("วัย" is อะ+เกย), but rhyme follows
        # sound, so normalize to the สระเกิน forms. 'เอา' needs none.

        # อัย -> ไอ
        if sara1 == "อะ" and marttra1 == "เกย":
            sara1 = "ไอ"
            marttra1 = "กา"
        if sara2 == "อะ" and marttra2 == "เกย":
            sara2 = "ไอ"
            marttra2 = "กา"
        # อัม -> อำ
        if (sara1 == "อะ" or sara1 == "อำ") and marttra1 == "กม":
            sara1 = "อำ"
            marttra1 = "กา"
        if (sara2 == "อะ" or sara2 == "อำ") and marttra2 == "กม":
            sara2 = "อำ"
            marttra2 = "กา"
        return bool(marttra1 == marttra2 and sara1 == sara2)

    def check_karu_lahu(self, text: str) -> Union[str, bool]:
        """
        Classify a Thai syllable as heavy (ครุ karu) or light (ลหุ lahu).

        Syllable weight is determined by Thai prosody rules for classical
        poetry:

        - A syllable is heavy (ครุ) if it contains a long vowel, ends with any
          final consonant (including sonorant finals / นมยวง), or contains one
          of the special inherently bound vowels (อำ, ไอ, ใอ, เอา).
        - A syllable is light (ลหุ) if it is an open syllable (แม่ ก กา)
          containing a short vowel with no final consonant.

        :param str text: single Thai syllable or word to be classified
        :return: "karu" for a heavy syllable, "lahu" for a light syllable,
            or ``False`` if the text is empty
        :rtype: Union[str, bool]
        """
        if not text:
            return False

        if text in self._LAHU_SYLLABLE_OVERRIDES:
            return "lahu"

        marttra = self.check_marttra(text)
        sara = self.check_sara(text)

        if (
            marttra != "กา"
            or sara in self._LONG_VOWELS
            or sara in self._SPECIAL_VOWELS
        ):
            return "karu"
        return "lahu"

    def check_klon(self, text: str, k_type: int = 8) -> Union[list[str], str]:
        """
        Check the suitability of the poem according to Thai principles.

        :param str text: Thai poem
        :param int k_type: type of Thai poem (4 or 8)
        :return: check results of the poem, a message that the poem is
            correct or a list of error messages
        :rtype: Union[list[str], str]
        :raises ImportError: if the ``ssg`` library is not installed

        ══════════════════════════════════════════════════════════════════════

        กลอนสี่ (Klon 4) Diagram:
        วรรคที่ ๑ (สดับ)    วรรคที่ ๒ (รับ)
        วรรคที่ ๓ (รอง)    วรรคที่ ๔ (ส่ง)

              ┏━━━━━━━━┯━┓    [สัมผัสคำที่ 1 หรือ 2]
        O O O X        X X O O
              ┏━━━━━━━━┯━┳━━━┛
        O O O X        X X O X ━┓
              ┏━━━━━━━━┯━┓      ┃ สัมผัสระหว่างบท
        O O O X        X X O O ━┛
              ┏━━━━━━━━┯━┳━━━┛
        O O O X        X X O X

        ══════════════════════════════════════════════════════════════════════

        กลอนแปด (Klon 8) Diagram:
        วรรคที่ ๑ (สดับ)    วรรคที่ ๒ (รับ)
        วรรคที่ ๓ (รอง)    วรรคที่ ๔ (ส่ง)

                      ┏━━━━━━━━┯━┯━┳━┯━┑  [สัมผัสคำที่ 3 หรือ 5 / อนุโลม 1,2,4]
        O O O O O O O X        O O X O O O O X
                      ┏━━━━━━━━┯━┯━┳━┯━━━━━━━┛
        O O O O O O O X        O O X O O O O X ━┓
                      ┏━━━━━━━━┯━┯━┳━┯━┑        ┃ สัมผัสระหว่างบท
        O O O O O O O X        O O X O O O O X ━┛
                      ┏━━━━━━━━┯━┯━┳━┯━━━━━━━┛
        O O O O O O O X        O O X O O O O X

        ══════════════════════════════════════════════════════════════════════

        :Example:

            >>> from pythainlp.khavee import KhaveeVerifier  # doctest: +SKIP
            >>> kv = KhaveeVerifier()  # doctest: +SKIP
            >>> print(kv.check_klon(  # doctest: +SKIP
            ...     'ฉันชื่อหมูกรอบ ฉันชอบกินไก่ แล้ววิ่งตามไป ไล่หมาน้ำทอง             ...     ฉันมันคนเก่ง เอ๋งเอ๋งคะนอง มีคนจับจอง เป็นของน้องเธียร',             ...     k_type=4
            ... ))
            The poem is correct according to the principle.
        """
        try:
            __import__("ssg")
        except ImportError as exc:
            raise ImportError(
                "The 'ssg' library is required for comprehensive poem analysis (check_klon). "
                "Please install it using: pip install ssg"
            ) from exc

        if k_type not in {4, 8}:
            return "Something went wrong. Make sure you enter it in the correct form (k_type 4 or 8)."

        waks = text.split()
        if len(waks) % 4 != 0 or len(waks) == 0:
            return "The poem does not have complete stanzas (บท). A stanza must contain exactly 4 sentences (วรรค)."

        # Wak 1 สดับ, Wak 2 รับ, Wak 3 รอง, Wak 4 ส่ง
        stanzas = [
            [subword_tokenize(waks[i + j], engine="ssg") for j in range(4)]
            for i in range(0, len(waks), 4)
        ]

        errors: list[str] = []
        for stanza_index in range(len(stanzas)):
            errors.extend(self._check_stanza(stanzas, stanza_index, k_type))

        if not errors:
            return "The poem is correct according to the principle."
        return errors

    @staticmethod
    def _rhyme_targets(
        wak2: list[str], wak4: list[str], k_type: int
    ) -> tuple[list[str], list[str]]:
        """
        Select the words of Wak 2 and Wak 4 that may receive a rhyme.

        :param list[str] wak2: words of Wak 2
        :param list[str] wak4: words of Wak 4
        :param int k_type: type of Thai poem (4 or 8)
        :return: target words of Wak 2 and Wak 4
        :rtype: tuple[list[str], list[str]]
        """
        # Klon 8: first 5 words (อนุโลม 1, 2, 4; บังคับ 3, 5)
        if k_type == 8:
            return wak2[:5], wak4[:5]
        # Klon 4: first 3 words if the wak has 5 words, else first 2
        limit_wak2 = 3 if len(wak2) == 5 else 2
        limit_wak4 = 3 if len(wak4) == 5 else 2
        return wak2[:limit_wak2], wak4[:limit_wak4]

    def _check_stanza(
        self, stanzas: list[list[list[str]]], stanza_index: int, k_type: int
    ) -> list[str]:
        """
        Check word counts and rhymes of one stanza (บท).

        :param list[list[list[str]]] stanzas: tokenized stanzas of the poem
        :param int stanza_index: index of the stanza to check
        :param int k_type: type of Thai poem (4 or 8)
        :return: error messages
        :rtype: list[str]
        """
        stanza = stanzas[stanza_index]
        wak1, wak2, wak3, wak4 = stanza
        number = stanza_index + 1
        wak_names = self._WAK_NAMES

        if not all((wak1, wak2, wak3, wak4)):
            return [f"Stanza (บทที่) {number} contains empty sentences."]

        errors = []
        max_words = 10 if k_type == 8 else 5
        for wak_index, wak in enumerate(stanza):
            if len(wak) > max_words:
                errors.append(
                    f"Stanza (บทที่) {number} {wak_names[wak_index]}: "
                    f"Word count exceeds {max_words}: {wak}"
                )

        wak2_targets, wak4_targets = self._rhyme_targets(wak2, wak4, k_type)

        wak1_last = wak1[-1]
        wak2_last = wak2[-1]
        wak3_last = wak3[-1]

        # Rule 1: วรรคสดับ -> วรรครับ
        if not any(
            self.is_sumpus(wak1_last, target) for target in wak2_targets
        ):
            errors.append(
                f"Rhyme error in Stanza (บทที่) {number}: "
                f"'{wak1_last}' ({wak_names[0]}) does not rhyme with {wak2_targets} ({wak_names[1]})"
            )

        # Rule 2: วรรครับ -> วรรครอง
        if not self.is_sumpus(wak2_last, wak3_last):
            errors.append(
                f"Rhyme error in Stanza (บทที่) {number}: "
                f"'{wak2_last}' ({wak_names[1]}) does not rhyme with '{wak3_last}' ({wak_names[2]})"
            )

        # Rule 3: วรรครอง -> วรรคส่ง
        if not any(
            self.is_sumpus(wak3_last, target) for target in wak4_targets
        ):
            errors.append(
                f"Rhyme error in Stanza (บทที่) {number}: "
                f"'{wak3_last}' ({wak_names[2]}) does not rhyme with {wak4_targets} ({wak_names[3]})"
            )

        # Rule 4: สัมผัสระหว่างบท (Inter-stanza)
        # Skipped when the previous Wak 4 is empty (already reported).
        if stanza_index > 0 and stanzas[stanza_index - 1][3]:
            prev_wak4_last = stanzas[stanza_index - 1][3][-1]
            if not self.is_sumpus(prev_wak4_last, wak2_last):
                errors.append(
                    f"Inter-stanza rhyme error (ผิดสัมผัสระหว่างบท) between Stanza {stanza_index} and {number}: "
                    f"'{prev_wak4_last}' ({wak_names[3]}) does not rhyme with '{wak2_last}' ({wak_names[1]})"
                )
        return errors

    def check_aek_too(
        self, text: Union[list[str], str], dead_syllable_as_aek: bool = False
    ) -> Union[list[Union[bool, str]], bool, str]:
        """
        Check if Thai words carry the tone mark เอก (aek) or โท (too).

        :param Union[list[str], str] text: Thai word or list of Thai words
        :param bool dead_syllable_as_aek: if ``True``, treat a dead
            syllable as aek
        :return: "aek" or "too" if the word has exactly that tone mark,
            otherwise ``False``; a list of results if ``text`` is a list
        :rtype: Union[list[Union[bool, str]], bool, str]
        :raises TypeError: if ``text`` is neither a string nor a list

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
            >>> print(
            ...     kv.check_aek_too(["เอง", "เอ่ง", "เอ้ง"])
            ... )  # doctest: +SKIP
            >>> # -> [False, 'aek', 'too']  ^^^^^^^^^^ # ใช้ List ได้เหมือนกัน
        """
        if isinstance(text, list):
            return [self.check_aek_too(t, dead_syllable_as_aek) for t in text]  # type: ignore[misc]

        if not isinstance(text, str):
            raise TypeError("text must be str or iterable list[str]")

        if "่" in text and "้" not in text:
            return "aek"
        if "้" in text and "่" not in text:
            return "too"
        if dead_syllable_as_aek and sound_syllable(text) == "dead":
            return "aek"
        return False

    def handle_karun_sound_silence(self, word: str) -> str:
        """
        Strip the silent characters of a Thai word marked by Karun (-์).

        Remove the characters before the Karun character that should be
        silenced.

        :param str word: Thai word
        :return: Thai word with silent characters stripped
        :rtype: str
        """
        # Only a final การันต์ is handled (not the middle one in โอห์ม)
        if not word.endswith("์"):
            return word

        # Multi-letter silent suffixes
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

        # Two-consonant suffixes
        # ตร์: ศาสตร์, ภาพยนตร์, กาสาวพัสตร์, เวทมนตร์
        # ทร์: จันทร์, บดินทร์, ภูมินทร์, นราธิเบนทร์
        # ดร์: นิรันดร์
        # ฎร์: ราษฎร์, สุราษฎร์
        if word.endswith(("ตร์", "ทร์", "ดร์", "ฎร์")):
            return word[:-3]

        # One consonant, optional upper/lower vowel, then การันต์:
        # สัตว์ (ว์), แพทย์ (ย์), พันธุ์ (ธุ์), สิทธิ์ (ธิ์)
        if len(word) >= 3 and word[-2] in {"ิ", "ี", "ึ", "ื", "ุ", "ู", "ั"}:
            return word[:-3]
        return word[:-2]
