# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

import unittest

from pythainlp.transliterate import transliterate


class TransliterateICUTestCase(unittest.TestCase):
    def test_transliterate(self):
        self.assertEqual(transliterate("แมว", "pyicu"), "mæw")
