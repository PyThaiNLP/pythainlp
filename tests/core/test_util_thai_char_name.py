# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Tests for pythainlp.util.thai_char_name."""

import unicodedata
import unittest

from pythainlp.util import thai_char_to_name, thai_name_to_char
from pythainlp.util.thai_char_name import _alias_to_char, _char_to_name


class ThaiCharNameTestCase(unittest.TestCase):
    def test_name_to_char(self):
        cases = [
            ("ยามักการ", "๎"),
            ("ไม้ยามักการ", "๎"),
            ("ทัณฑฆาต", "์"),
            ("การันต์", "์"),
            ("โคมูตร", "๛"),
            ("ฟองมัน", "๏"),
            ("อังคั่นคู่", "๚"),
            ("ไม้ผัด", "\u0e31"),
            ("  ไม้เอก ", "่"),
        ]
        for name, expected in cases:
            with self.subTest(name=name):
                self.assertEqual(thai_name_to_char(name), expected)

    def test_char_to_name(self):
        cases = [
            ("๎", "ยามักการ"),
            ("๛", "โคมูตร"),
            ("่", "ไม้เอก"),
            ("ะ", "สระอะ"),
        ]
        for ch, expected in cases:
            with self.subTest(ch=ch):
                self.assertEqual(thai_char_to_name(ch), expected)

    def test_round_trip(self):
        for ch, name in _char_to_name.items():
            with self.subTest(ch=ch):
                self.assertEqual(thai_name_to_char(name), ch)

    def test_dictionary_data(self):
        for ch in _char_to_name:
            with self.subTest(ch=ch):
                self.assertEqual(len(ch), 1)
                self.assertTrue(unicodedata.name(ch).startswith("THAI "))
        for alias, ch in _alias_to_char.items():
            with self.subTest(alias=alias):
                self.assertNotIn(alias, _char_to_name.values())
                self.assertIn(ch, _char_to_name)

    def test_invalid(self):
        for bad in ["", " ", "ก", "abc", "ยามักการ์", "ไปยาลใหญ่", None, 1]:
            with self.subTest(name=bad):
                with self.assertRaises(ValueError):
                    thai_name_to_char(bad)  # type: ignore[arg-type]
        for bad in [
            "",
            "ก",
            "\u0e51",
            "a",
            "\u0e48\u0e48",
            "\u25cc\u0e4e",
            " \u0e48",
            None,
            1,
        ]:
            with self.subTest(ch=bad):
                with self.assertRaises(ValueError):
                    thai_char_to_name(bad)  # type: ignore[arg-type]
