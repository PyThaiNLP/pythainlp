# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

import unittest

from pythainlp.transliterate.th_pron import get_word_dict, transliterate


class TransliterateThPronTestCase(unittest.TestCase):
    def test_transliterate_supported_modes(self):
        self.assertEqual(transliterate("แมว", mode="royin"), "maeo")
        self.assertEqual(transliterate("คน", mode="paiboon"), "kon")
        self.assertEqual(transliterate("คน", mode="ipa"), "kʰon˧")

    def test_transliterate_preserves_unknown_mode(self):
        self.assertEqual(transliterate("แมว", mode="unknown"), "แมว")

    def test_thai_digits_conversion(self):
        self.assertEqual(transliterate("๑๒๓", mode="royin"), "123")

    def test_get_word_dict(self):
        self.assertEqual(
            get_word_dict("ปฺระ-ชา"),
            {
                "word": "ปฺระ-ชา",
                "paiboon": "bprà-chaa",
                "royin": "pra-cha",
                "ipa": "pra˨˩.t͡ɕʰaː˧",
            },
        )
