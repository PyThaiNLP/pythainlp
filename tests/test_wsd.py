# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0

import unittest
from pythainlp.wsd import get_sense


class TestWsdPackage(unittest.TestCase):
    def test_get_sense(self):
        self.assertTrue(get_sense("เขากำลังอบขนมคุกกี้", "คุกกี้"))
        self.assertTrue(get_sense("เว็บนี้ต้องการคุกกี้ในการทำงาน", "คุกกี้"))
        self.assertFalse(get_sense("เว็บนี้ต้องการคุกกี้ในการทำงาน", "คน"))
