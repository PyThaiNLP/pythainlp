# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

"""Unit tests for pythainlp.util module.
"""

import unittest

from pythainlp.util import rhyme, thai_word_tone_detector


class UtilTestCaseX(unittest.TestCase):
    def test_rhyme(self):
        self.assertIsInstance(rhyme("แมว"), list)
        self.assertGreater(len(rhyme("แมว")), 2)

    def test_thai_word_tone_detector(self):
        self.assertIsNotNone(thai_word_tone_detector("คนดี"))
        self.assertEqual(
            thai_word_tone_detector("ราคา"), [("รา", "m"), ("คา", "m")]
        )
        # Edge cases: None and empty string
        self.assertEqual(thai_word_tone_detector(None), [("", "")])
        self.assertEqual(thai_word_tone_detector(""), [("", "")])
