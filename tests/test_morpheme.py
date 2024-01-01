# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: Copyright 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0

import unittest
from pythainlp.morpheme import nighit


class TestMorphemePackage(unittest.TestCase):
    def test_nighit(self):
        self.assertEqual(nighit("สํ","คีต"), "สังคีต")
        self.assertEqual(nighit("สํ","จร"), "สัญจร")
        self.assertEqual(nighit("สํ","ฐาน"), "สัณฐาน")
        self.assertEqual(nighit("สํ","นิษฐาน"), "สันนิษฐาน")
        self.assertEqual(nighit("สํ","ปทา"), "สัมปทา")
        self.assertEqual(nighit("สํ","โยค"), "สังโยค")