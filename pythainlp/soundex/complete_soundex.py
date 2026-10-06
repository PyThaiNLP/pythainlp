# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""
Complete Soundex for Thai word similarity analysis.

Original paper:
Chalermpol Tapsai, Phayung Meesad, and Choochart Haruechaiyasak. 2020.
Complete Soundex for Thai Words Similarity Analysis.
Information Technology Journal KMUTNB. 2020 June 30;16(1):46-59.

https://ph01.tci-thaijo.org/index.php/IT_Journal/article/view/241562
https://ph01.tci-thaijo.org/index.php/IT_Journal/article/view/241562/164358

Note:
    This soundex algorithm handles both single and multi-syllable Thai words.
    Multi-syllable words are automatically tokenized internally when the
    syllable_tokenize dependency is available (python-crfsuite).

    Example:
        from pythainlp.soundex import complete_soundex

        # Single syllable
        complete_soundex("ก้าน")  # 'กก1Bน2-'

        # Multi-syllable (automatically handled)
        complete_soundex("ปุญญา")  # 'ปป1B0น-*'
        complete_soundex("สวรรค์")  # 'ซศ1A-0-วว1Aน0-'
"""

from __future__ import annotations

import re
from typing import Optional

# Vowel codes shortened by 'ะ'
_SHORT_VOWEL: dict[str, str] = {
    "5J": "5I",
    "6L": "6K",
    "7N": "7M",
    "1B": "1A",
}


class CompleteSoundex:
    """
    Complete Soundex implementation for Thai words similarity analysis.

    This class implements the Complete Soundex algorithm as described in
    the paper by Chalermpol Tapsai, Phayung Meesad, and
    Choochart Haruechaiyasak (2020).
    """

    def __init__(self) -> None:
        """Initialize the Complete Soundex lookup tables."""
        self.thai_consonants: str = (
            "กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธนบปผฝพฟภมยรลวศษสหฬฮอ"
        )

        # Tables 5.1 - 5.4 of the paper
        self.initial_map: dict[str, str] = {
            "ก": "กก",
            "ข": "คข",
            "ฃ": "คข",
            "ค": "คค",
            "ฅ": "คค",
            "ฆ": "คค",
            "ง": "งง",
            "จ": "จจ",
            "ฉ": "ชช",
            "ช": "ชช",
            "ฌ": "ชช",
            "ซ": "ซซ",
            "ศ": "ซศ",
            "ษ": "ซศ",
            "ส": "ซศ",
            "ญ": "ยย",
            "ย": "ยย",
            "ด": "ดด",
            "ฎ": "ดด",
            "ต": "ตต",
            "ฏ": "ตต",
            "ถ": "ทธ",
            "ฐ": "ทธ",
            "ท": "ทท",
            "ธ": "ทท",
            "ฑ": "ทท",
            "ฒ": "ทท",
            "น": "นน",
            "ณ": "นน",
            "บ": "บบ",
            "ป": "ปป",
            "ผ": "พผ",
            "ฝ": "ฟฝ",
            "พ": "พพ",
            "ภ": "พพ",
            "ฟ": "ฟฟ",
            "ม": "มม",
            "ร": "รร",
            "ล": "รร",
            "ฬ": "รร",
            "ฤ": "รร",
            "ว": "วว",
            "ห": "ฮห",
            "ฮ": "ฮห",
            "อ": "ออ",
        }

        self.vowel_map: dict[str, str] = {
            "ะ": "1A",
            "ั": "1A",
            "รร": "1A",
            "ำ": "1A",
            "ไ": "1A",
            "ใ": "1A",
            "เา": "1A",
            "า": "1B",
            "ิ": "2C",
            "ี": "2D",
            "ึ": "3E",
            "ื": "3F",
            "ุ": "4G",
            "ู": "4H",
            "เะ": "5I",
            "เ็": "5I",
            "เ": "5J",
            "แะ": "6K",
            "แ็": "6K",
            "แ": "6L",
            "โะ": "7M",
            "โ": "7N",
            "เาะ": "8O",
            "อ": "8P",
            "เอะ": "9Q",
            "เอ": "9R",
            "เอียะ": "AS",
            "เอีย": "AT",
            "เอือะ": "BU",
            "เอือ": "BV",
            "อัวะ": "CW",
            "อัว": "CX",
            "ว": "CX",
        }

        self.final_map: dict[str, str] = {
            "ก": "ก",
            "ข": "ก",
            "ค": "ก",
            "ฆ": "ก",
            "ง": "ง",
            "จ": "ด",
            "ช": "ด",
            "ซ": "ด",
            "ด": "ด",
            "ต": "ด",
            "ถ": "ด",
            "ท": "ด",
            "ธ": "ด",
            "ศ": "ด",
            "ษ": "ด",
            "ส": "ด",
            "ฎ": "ด",
            "ฏ": "ด",
            "ฐ": "ด",
            "ฑ": "ด",
            "ฒ": "ด",
            "น": "น",
            "ณ": "น",
            "ญ": "น",
            "ร": "น",
            "ล": "น",
            "ฬ": "น",
            "บ": "บ",
            "ป": "บ",
            "พ": "บ",
            "ฟ": "บ",
            "ภ": "บ",
            "ม": "ม",
            "ย": "ย",
            "ว": "ว",
        }

        self.tone_map: dict[str, str] = {"่": "1", "้": "2", "๊": "3", "๋": "4"}

    def clean_text(self, text: str) -> str:
        """Remove silent characters (karan/thanthakhat) from text."""
        return re.sub(r"[ก-ฮ][ะ-ู]?์", "", text)

    def heuristic_split(self, text: str) -> list[tuple[str, Optional[str]]]:
        """
        Apply heuristic rules to split syllables.

        Return a list of tuples (syllable, implicit_rule) where
        implicit_rule can be 'a', 'o', or None.
        """
        # อัต pattern: split as อัต-ตX..., ต stays with the second syllable
        if text.startswith("อัต") and len(text) > 3:
            return [("อัต", None), ("ต" + text[3:], None)]

        # Aksorn Nam with Ro Han (e.g. สวรรค์ -> ส-วรรค์)
        if re.match(r"[ขฃฉฐถผฝศษสฮกจดตฎฏบปอ]วรร.*", text):
            return [(text[0], "a"), (text[1:], None)]

        # Two consonants without vowel (e.g. กม -> ก-a ม-a)
        if re.fullmatch(r"[ก-ฮ]{2}", text):
            return [(text[0], "a"), (text[1], "a")]

        # 3 consonants -> C1-a C2C3-o (e.g. กมล)
        if re.fullmatch(r"[ก-ฮ]{3}", text):
            return [(text[0], "a"), (text[1:], "o")]

        # 3 consonants + vowel -> C1-a C2-a C3-V (e.g. กมลา)
        if re.fullmatch(r"[ก-ฮ]{3}[า-ู]", text):
            return [(text[0], "a"), (text[1], "a"), (text[2:], None)]

        return [(text, None)]

    def _process_leading_vowel(
        self, chars: list[str], idx: int
    ) -> tuple[str, int]:
        """Extract and process leading vowel."""
        leading_vowel = ""
        if idx < len(chars) and chars[idx] in ["เ", "แ", "โ", "ไ", "ใ"]:
            leading_vowel = chars[idx]
            idx += 1
        return leading_vowel, idx

    def _process_initial_consonant(
        self, chars: list[str], idx: int, leading_vowel: str
    ) -> tuple[str, str, str, int]:
        """Process initial consonant and cluster."""
        init_char = ""
        init_code = ""
        cluster_char = "-"

        if idx >= len(chars):
            return init_char, init_code, cluster_char, idx

        init_char = chars[idx]

        # ทร- maps to the ซ initial
        if init_char == "ท" and idx + 1 < len(chars) and chars[idx + 1] == "ร":
            init_code = "ซซ"
            idx += 2
            cluster_char = "-"  # no cluster output for ทร
        else:
            init_code = self.initial_map.get(init_char, "xx")
            idx += 1

            if idx < len(chars) and chars[idx] in ["ร", "ล", "ว"]:
                is_cluster = self._detect_cluster(chars, idx, leading_vowel)
                if is_cluster:
                    cluster_char = chars[idx]
                    idx += 1

        return init_char, init_code, cluster_char, idx

    def _detect_cluster(
        self, chars: list[str], idx: int, leading_vowel: str
    ) -> bool:
        """Detect if ร/ล/ว is a cluster."""
        if idx + 1 < len(chars):
            nc = chars[idx + 1]
            # Cluster only if followed by a vowel mark or tone
            if nc in "ะัิีึืุู" or nc in self.tone_map:
                return True
            # With a leading vowel, a following non-consonant also counts
            if (
                leading_vowel
                and nc not in ["ร", "ล", "ว"]
                and nc not in self.thai_consonants
                and nc != "า"
            ):
                return True
        # End of word with a leading vowel (e.g. เกล)
        elif leading_vowel:
            return True
        return False

    def _map_leading_vowel_code(self, leading_vowel: str) -> tuple[str, str]:
        """Map leading vowel to initial vowel and final code."""
        vowel_code = ""
        final_code = "-"

        if leading_vowel:
            if leading_vowel == "โ":
                vowel_code = "7N"
            elif leading_vowel == "ไ" or leading_vowel == "ใ":
                vowel_code = "1A"
                final_code = "ย"
            elif leading_vowel == "แ":
                vowel_code = "6L"
            elif leading_vowel == "เ":
                vowel_code = "5J"

        return vowel_code, final_code

    def _scan_vowels_tones_finals(
        self,
        chars: list[str],
        idx: int,
        leading_vowel: str,
        vowel_code: str,
        final_code: str,
    ) -> tuple[str, str, str, list[str]]:
        """Scan remaining characters for vowels, tones, and finals."""
        remaining = chars[idx:]
        final_candidates = []
        tone_code = "0"

        for c in remaining:
            if c in self.tone_map:
                tone_code = self.tone_map[c]
            elif c in "ะัาิีึืุู" or (c == "อ" and leading_vowel == "เ") or c == "ำ":
                vowel_code, final_code = self._process_vowel_char(
                    c, leading_vowel, vowel_code, final_code
                )
            else:
                final_candidates.append(c)

        return vowel_code, final_code, tone_code, final_candidates

    def _process_vowel_char(
        self, c: str, leading_vowel: str, vowel_code: str, final_code: str
    ) -> tuple[str, str]:
        """Process a single vowel character."""
        if leading_vowel == "เ" and c == "ื":
            vowel_code = "BV"  # Part of uea
        elif leading_vowel == "เ" and c == "อ":
            if vowel_code != "BV":
                vowel_code = "9R"  # E + O -> Oe
        elif c == "ำ":
            vowel_code = "1A"
            final_code = "ม"
        elif c == "อ" and not leading_vowel and vowel_code == "":
            vowel_code = "8P"  # 'อ' as vowel 8P (Saw)
        else:
            vowel_code = self.vowel_map.get(c) or vowel_code

        # 'ะ' shortens the vowel
        if c == "ะ":
            vowel_code = _SHORT_VOWEL.get(vowel_code, vowel_code)

        return vowel_code, final_code

    def _process_final_consonant(
        self,
        syl: str,
        final_code: str,
        vowel_code: str,
        final_candidates: list[str],
    ) -> tuple[str, str, bool]:
        """Process final consonant and detect dropped ร."""
        dropped_r = False

        if final_code == "-":
            if "รร" in syl:
                vowel_code = "1A"
                if final_candidates:
                    f = final_candidates[-1]
                    final_code = self.final_map.get(f, "-")
                else:
                    final_code = "น"
            elif final_candidates:
                # Rule: Drop 'r' in final cluster
                raw_final = "".join(final_candidates)
                if (
                    len(raw_final) >= 2
                    and raw_final[-2] == "ร"
                    and raw_final[-1] in self.final_map
                ):
                    f = raw_final[-1]
                    dropped_r = True
                elif raw_final.endswith("ตร"):
                    f = "ต"
                    dropped_r = True
                else:
                    f = final_candidates[-1]

                final_code = self.final_map.get(f, "-")

        return vowel_code, final_code, dropped_r

    def _check_special_format(
        self,
        init_char: str,
        final_candidates: list[str],
        vowel_code: str,
    ) -> bool:
        """Check if special format (tone before final) should be used."""
        # Tone goes before the final when the initial is ญ, ย, or น;
        # or a final is ญ or ณ; or a final is น with the short vowel 1A.
        if init_char in ["ญ", "ย", "น"]:
            return True
        if final_candidates and any(c in ["ญ", "ณ"] for c in final_candidates):
            return True
        return bool(
            final_candidates
            and any(c == "น" for c in final_candidates)
            and vowel_code == "1A"
        )

    def _apply_implicit_vowel(
        self, vowel_code: str, implicit_rule: Optional[str]
    ) -> str:
        """Apply implicit vowel defaults."""
        if vowel_code == "":
            if implicit_rule == "a":
                vowel_code = "1A"
            elif implicit_rule == "o":
                vowel_code = "7M"
            else:
                vowel_code = "7M"
        return vowel_code

    def _adjust_so_sua_mapping(
        self,
        init_char: str,
        init_code: str,
        syl: str,
        implicit_rule: Optional[str],
    ) -> str:
        """Special adjustments for ส (so sua) mapping."""
        # Not for implicit splits
        if (
            init_char == "ส"
            and init_code == "ซศ"
            and implicit_rule is None
            and len(syl) >= 2
        ):
            # Simple syllable: ส + vowel, no other consonants except ร ล ว
            consonants_after_init = [c for c in syl[1:] if "ก" <= c <= "ฮ"]
            if not consonants_after_init or all(
                c in "รลว" for c in consonants_after_init
            ):
                init_code = "ซซ"
        return init_code

    def _format_output(
        self,
        init_code: str,
        vowel_code: str,
        final_code: str,
        tone_code: str,
        cluster_char: str,
        special_format: bool,
        dropped_r: bool,
    ) -> str:
        """Format the final output."""
        if special_format:
            # Init Vowel Tone Final Cluster
            result = (
                f"{init_code}{vowel_code}{tone_code}{final_code}{cluster_char}"
            )
        else:
            # Init Vowel Final Tone Cluster; a dropped ร adds a dash
            # after the vowel when the final is ก or absent
            if dropped_r and (final_code == "ก" or final_code == "-"):
                result = f"{init_code}{vowel_code}-{final_code}{tone_code}{cluster_char}"
            else:
                result = f"{init_code}{vowel_code}{final_code}{tone_code}{cluster_char}"
        return result

    def process_syllable(
        self, syl: str, implicit_rule: Optional[str] = None
    ) -> str:
        """
        Process a single syllable and return its soundex code.

        :param str syl: syllable to be processed
        :param str implicit_rule: implicit vowel rule, 'a' or 'o'
            (optional)
        :return: soundex code of the syllable
        :rtype: str
        """
        chars = list(syl)
        idx = 0

        leading_vowel, idx = self._process_leading_vowel(chars, idx)

        init_char, init_code, cluster_char, idx = (
            self._process_initial_consonant(chars, idx, leading_vowel)
        )

        vowel_code, final_code = self._map_leading_vowel_code(leading_vowel)

        vowel_code, final_code, tone_code, final_candidates = (
            self._scan_vowels_tones_finals(
                chars, idx, leading_vowel, vowel_code, final_code
            )
        )

        vowel_code, final_code, dropped_r = self._process_final_consonant(
            syl, final_code, vowel_code, final_candidates
        )

        special_format = self._check_special_format(
            init_char, final_candidates, vowel_code
        )

        vowel_code = self._apply_implicit_vowel(vowel_code, implicit_rule)

        # Leading โ and แ override the vowel code
        if leading_vowel == "โ":
            vowel_code = "7N"
        if leading_vowel == "แ":
            vowel_code = "6L"

        init_code = self._adjust_so_sua_mapping(
            init_char, init_code, syl, implicit_rule
        )

        result = self._format_output(
            init_code,
            vowel_code,
            final_code,
            tone_code,
            cluster_char,
            special_format,
            dropped_r,
        )

        return result

    @staticmethod
    def _needs_asterisk(text: str, syllables: list[str]) -> bool:
        """
        Check if the code needs a trailing asterisk.

        The asterisk marks these patterns:

        1. Contains ญญ (double ญ)
        2. Contains ญ and ย together
        3. Contains ณ and ย together
        4. Starts with ญ (ญ as initial)
        """
        return (
            "ญญ" in text
            or ("ญ" in text and "ย" in text)
            or ("ณ" in text and "ย" in text)
            or any(s.startswith("ญ") for s in syllables)
        )

    def _encode_syllables(self, text: str, syllables: list[str]) -> str:
        """Encode syllables with heuristic splits and add the asterisk."""
        parts = []
        for syl in syllables:
            for sub_syl, rule in self.heuristic_split(syl):
                parts.append(self.process_syllable(sub_syl, rule))
        result = "".join(parts)
        if self._needs_asterisk(text, syllables):
            result += "*"
        return result

    def encode(self, text: str) -> str:
        """
        Encode a Thai word into Complete Soundex code.

        This method handles both single and multi-syllable words by
        internally tokenizing multi-syllable words using syllable_tokenize.

        :param str text: Thai word to be encoded
        :return: Complete Soundex code
        :rtype: str

        :Example:

            >>> from pythainlp.soundex import complete_soundex
            >>> complete_soundex("ก้าน")
            'กก1Bน2-'
            >>> complete_soundex("ปุญญา")  # doctest: +SKIP
            'ปป1B0น-*'
        """
        text = self.clean_text(text)

        if not text:
            return ""

        try:
            from pythainlp.tokenize import syllable_tokenize

            syllables = syllable_tokenize(text)
            if len(syllables) > 1:
                return self._encode_syllables(text, syllables)
        except (ImportError, ModuleNotFoundError):
            # Without syllable_tokenize, encode as one syllable
            pass

        return self._encode_syllables(text, [text])


# Shared instance for the module-level function
_complete_soundex_instance: "Optional[CompleteSoundex]" = None


def complete_soundex(text: str) -> str:
    """
    Convert a Thai word into phonetic code using Complete Soundex.

    This function handles both single and multi-syllable words by
    internally tokenizing multi-syllable words when the syllable_tokenize
    dependency is available.

    :param str text: Thai word to be encoded
    :return: Complete Soundex code
    :rtype: str

    :Example:

        >>> from pythainlp.soundex import complete_soundex  # doctest: +SKIP

        >>> # Single syllable encoding
        >>> complete_soundex("ก้าน")  # doctest: +SKIP
        'กก1Bน2-'

        >>> complete_soundex("กลับ")  # doctest: +SKIP
        'กก1Aบ0ล'

        >>> # Multi-syllable words (automatically tokenized)
        >>> complete_soundex("ปุญญา")  # doctest: +SKIP
        'ปป1B0น-*'

        >>> complete_soundex("สวรรค์")  # doctest: +SKIP
        'ซศ1A-0-วว1Aน0-'

        >>> complete_soundex("ปันนา")  # doctest: +SKIP
        'ปป1Bน0-'
    """
    global _complete_soundex_instance

    if not text or not isinstance(text, str):
        return ""

    if _complete_soundex_instance is None:
        _complete_soundex_instance = CompleteSoundex()

    return _complete_soundex_instance.encode(text)


def complete_soundex_similarity(code1: str, code2: str) -> float:
    """
    Calculate the similarity between two Complete Soundex codes.

    The calculation follows the character-wise comparison formula
    defined in Tapsai et al. (2020), character by character:
    S(X,Y) = Sum(sim(c_xi, c_yi)) / max(len(X), len(Y))

    Where sim(c_xi, c_yi) = 1 if characters match, else 0.

    This implements Equation (1) from the paper (Section 3.3, page 55),
    which compares codes position by position rather than by syllable
    blocks.

    :param str code1: full concatenated soundex code of the first word
    :param str code2: full concatenated soundex code of the second word
    :return: similarity score between 0.0 and 1.0
    :rtype: float

    :Example:

        >>> from pythainlp.soundex import (  # doctest: +SKIP
        ...     complete_soundex,
        ...     complete_soundex_similarity,
        ... )

        >>> # Encode two words
        >>> code1 = complete_soundex(
        ...     "ข้มขืน"
        ... )  # Bitter/Forced (with tone)  # doctest: +SKIP
        >>> code2 = complete_soundex(
        ...     "ขมขืน"
        ... )  # Bitter (no tone)  # doctest: +SKIP

        >>> # Calculate similarity
        >>> similarity = complete_soundex_similarity(
        ...     code1, code2
        ... )  # doctest: +SKIP
        ~0.93 (13 matches out of 14 characters)

        >>> # Perfect match
        >>> code_a = complete_soundex("ก้าน")  # doctest: +SKIP
        >>> code_b = complete_soundex("ก้าน")  # doctest: +SKIP
        >>> complete_soundex_similarity(code_a, code_b)  # doctest: +SKIP
        1.0

        >>> # No match
        >>> code_x = complete_soundex("ทราย")  # doctest: +SKIP
        >>> code_y = complete_soundex("น้ำ")  # doctest: +SKIP
        >>> complete_soundex_similarity(code_x, code_y)  # doctest: +SKIP
        0.0 (completely different)
    """
    if not code1 and not code2:
        return 1.0
    if not code1 or not code2:
        return 0.0

    max_len = max(len(code1), len(code2))

    match_count = 0
    min_len = min(len(code1), len(code2))

    for i in range(min_len):
        if code1[i] == code2[i]:
            match_count += 1

    similarity = match_count / max_len

    return similarity
