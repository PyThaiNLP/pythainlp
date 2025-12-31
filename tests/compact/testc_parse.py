# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

import unittest

from pythainlp.tag import chunk_parse, pos_tag


class ChunkParseTestCase(unittest.TestCase):
    def test_chunk_parse(self):
        tokens = ["ผม", "รัก", "คุณ"]

        w_p = pos_tag(tokens, engine="perceptron", corpus="orchid")
        self.assertIsNotNone(chunk_parse(w_p))
