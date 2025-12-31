# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

import unittest

from pythainlp.generate.thai2fit import gen_sentence


class GenerateTestCaseX(unittest.TestCase):
    def test_thai2fit(self):
        self.assertIsNotNone(gen_sentence("กาลครั้งหนึ่งนานมาแล้ว"))
        self.assertIsNotNone(
            gen_sentence("กาลครั้งหนึ่งนานมาแล้ว", output_str=False)
        )
        self.assertIsNotNone(gen_sentence())
