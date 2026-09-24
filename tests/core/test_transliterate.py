# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

import unittest
from unittest.mock import patch

from pythainlp.transliterate import pronunciate_pali, romanize, transliterate
from pythainlp.transliterate._repetition import find_trailing_repeat_period

BASIC_TESTS = {
    None: "",
    "": "",
    "abc": "abc",
    "หมอก": "mok",
    "หาย": "hai",
    "แมว": "maeo",
    "เดือน": "duean",
    "ดำ": "dam",
    "ดู": "du",
    "บัว": "bua",
    "กก": "kok",
    "พร": "phon",
    "กร": "kon",
    "กรร": "kan",
    "กรรม": "kam",
    "กรม": "krom",
    "ฝ้าย": "fai",
    "นพพร": "nopphon",
    "อัก": "ak",
    "ทีปกร": "thipakon",
    "ธรรพ์": "than",
    "ธรรม": "tham",
    "มหา": "maha",
    "หยาก": "yak",
    "อยาก": "yak",
    "ยมก": "yamok",
    "กลัว": "klua",
    "บ้านไร่": "banrai",
    "ชารินทร์": "charin",
}

# words containing ฤ (U+0E24 THAI CHARACTER RU), see issue #1444
RU_TESTS = {
    "ฤก": "rueok",
    "ฤดู": "rueadu",
    "ฤทธิ์": "rueot",
}

# these are set of two-syllable words,
# to test if the transliteration/romanization is consistent, say
# romanize(1+2) = romanize(1) + romanize(2)
CONSISTENCY_TESTS = [
    # ("กระจก", "กระ", "จก"),  # failed - tokenization issue
    ("ระเบิด", "ระ", "เบิด"),
    ("หยากไย่", "หยาก", "ไย่"),
    ("ตากใบ", "ตาก", "ใบ"),
    # ("จัดสรร", "จัด", "สรร"),  # failed - tokenization issue
]


class TransliterateTestCase(unittest.TestCase):
    def test_romanize(self):
        self.assertEqual(romanize(None), "")  # type: ignore[arg-type]
        self.assertEqual(romanize(""), "")
        self.assertEqual(romanize("แมว"), "maeo")

    def test_romanize_royin_basic(self):
        for word, expect in BASIC_TESTS.items():
            self.assertEqual(romanize(word, engine="royin"), expect)  # type: ignore[arg-type]

    def test_romanize_royin_ru(self):
        # ฤ (U+0E24) is a key of _CONSONANTS but is not in thai_consonants,
        # so it used to desynchronize the consonant list and raise IndexError.
        for word, expect in RU_TESTS.items():
            self.assertEqual(romanize(word, engine="royin"), expect)  # type: ignore[arg-type]

    def test_romanize_royin_consistency(self):
        for word, part1, part2 in CONSISTENCY_TESTS:
            self.assertEqual(
                romanize(word, engine="royin"),
                (
                    romanize(part1, engine="royin")
                    + romanize(part2, engine="royin")
                ),
            )

    def test_romanize_lookup(self):
        # found in v1.4
        self.assertEqual(romanize("บอล", engine="lookup"), "ball")
        self.assertEqual(romanize("บอยแบนด์", engine="lookup"), "boyband")
        self.assertEqual(romanize("กาแล็กซี", engine="lookup"), "galaxy")
        self.assertEqual(romanize("กีย์เซอไรต์", engine="lookup"), "geyserite")
        self.assertEqual(romanize("พลีโอนาสต์", engine="lookup"), "pleonaste")
        self.assertEqual(
            romanize("คาราเมล คาปูชิโน่", engine="lookup"),
            "caramel cappuccino",
        )
        ## found individually, but needs tokenization
        # Updated expectation after royin improvements for syllable boundary detection
        self.assertEqual(
            romanize("คาราเมลคาปูชิโน่", engine="lookup"), "kharamenkhapuchino"
        )
        # not found in v1.4
        self.assertEqual(romanize("ภาพยนตร์", engine="lookup"), "phapn")
        self.assertEqual(romanize("แมว", engine="lookup"), "maeo")

    def test_transliterate(self):
        self.assertEqual(transliterate(""), "")
        self.assertEqual(transliterate("", engine="thaig2p_v4"), "")
        self.assertIsNotNone(transliterate("คน", engine="iso_11940"))
        self.assertIsNotNone(transliterate("แมว", engine="iso_11940"))

    @patch("pythainlp.transliterate.thaig2p_v4.transliterate")
    def test_transliterate_thaig2p_v4_dispatch(self, mock_g2p):
        mock_g2p.return_value = "/kʰon˧/"
        self.assertEqual(transliterate("คน", engine="thaig2p_v4"), "/kʰon˧/")
        mock_g2p.assert_called_once_with("คน")

    def test_transliterate_iso11940(self):
        self.assertEqual(
            transliterate("เชียงใหม่", engine="iso_11940"), "echīyngıh̄m̀"
        )
        self.assertEqual(
            transliterate("ภาษาไทย", engine="iso_11940"), "p̣hās̛̄āịthy"
        )

    def test_pronunciate_pali(self):
        # rule 1
        self.assertEqual(
            pronunciate_pali("ติสรเณนสห"), "ติสะระเณนะสะหะ"
        )
        self.assertEqual(
            pronunciate_pali("สีลานิ ยาจาม"), "สีลานิ ยาจามะ"
        )
        self.assertEqual(
            pronunciate_pali("ภควา"), "ภะคะวา"
        )
        self.assertEqual(
            pronunciate_pali("อรหโต"), "อะระหะโต"
        )
        self.assertEqual(
            pronunciate_pali("โลกวิทู"), "โลกะวิทู"
        )
        self.assertEqual(
            pronunciate_pali("นมามิ"), "นะมามิ"
        )
        # rule 2
        self.assertEqual(
            pronunciate_pali("สมฺมา"), "สัมมา"
        )
        self.assertEqual(
            pronunciate_pali("สงฺโฆ"), "สังโฆ"
        )
        self.assertEqual(
            pronunciate_pali("พุทฺโธ"), "พุทโธ"
        )
        self.assertEqual(
            pronunciate_pali("พุทฺธสฺส"), "พุทธัสสะ"
        )
        self.assertEqual(
            pronunciate_pali("สนฺทิฏฺฐิโก"), "สันทิฏฐิโก"
        )
        self.assertEqual(
            pronunciate_pali("ปาหุเนยฺโย"), "ปาหุเนยโย"
        )
        # rule 3
        self.assertEqual(
            pronunciate_pali("มยํ"), "มะยัง"
        )
        self.assertEqual(
            pronunciate_pali("วิสุ ํ"), "วิสุง"
        )
        self.assertEqual(
            pronunciate_pali("อรหํ"), "อะระหัง"
        )
        self.assertEqual(
            pronunciate_pali("สงฺฆํ"), "สังฆัง"
        )
        self.assertEqual(
            pronunciate_pali("ธมฺมํ"), "ธัมมัง"
        )
        self.assertEqual(
            pronunciate_pali("สรณํ"), "สะระณัง"
        )
        self.assertEqual(
            pronunciate_pali("สีล ํ"), "สีลัง"
        )
        self.assertEqual(
            pronunciate_pali("พาหุ ํ"), "พาหุง"
        )
        # rule 4,5
        self.assertEqual(
            pronunciate_pali("สฺวากฺขาโต"), "สวากขาโต"
        )
        self.assertEqual(
            pronunciate_pali("พฺยาธิ"), "พยาธิ"
        )
        self.assertEqual(
            pronunciate_pali("พฺราหฺมณ"), "พราหมะณะ"
        )

class RepetitionCycleTestCase(unittest.TestCase):
    """Tests for the greedy-decoding cycle detector.

    See: https://github.com/PyThaiNLP/pythainlp/issues/1403
    """

    def test_no_cycle(self):
        self.assertIsNone(find_trailing_repeat_period([]))
        self.assertIsNone(find_trailing_repeat_period([1, 2, 3, 4, 5]))
        self.assertIsNone(find_trailing_repeat_period([1, 1, 2, 2]))

    def test_single_char_cycle(self):
        # e.g. the "aaaa..." tail seen for "กรุงเทพฯ"
        self.assertEqual(find_trailing_repeat_period([9, 1, 1, 1]), 1)
        self.assertIsNone(find_trailing_repeat_period([1, 1]))

    def test_multi_char_cycle(self):
        # e.g. the "botbotbot..." tail seen for "ราษฎรบำรุง"
        tokens = [9, 8, 7, 1, 2, 3, 1, 2, 3, 1, 2, 3]
        self.assertEqual(find_trailing_repeat_period(tokens), 3)

    def test_longer_period_requires_larger_max_period(self):
        period = list(range(8))
        tokens = period * 3
        self.assertIsNone(find_trailing_repeat_period(tokens, max_period=5))
        self.assertEqual(find_trailing_repeat_period(tokens, max_period=8), 8)

    def test_min_repeats_threshold(self):
        tokens = [1, 2, 1, 2]  # only repeats twice
        self.assertIsNone(find_trailing_repeat_period(tokens, min_repeats=3))
        self.assertEqual(find_trailing_repeat_period(tokens, min_repeats=2), 2)
