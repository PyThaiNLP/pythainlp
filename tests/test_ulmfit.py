# -*- coding: utf-8 -*-

import datetime
import os
import sys
import unittest

from pythainlp.ulmfit import *

class TestUlmfitPackage(unittest.TestCase):

    def test_ThaiTokenizer(self):
        self.thai = ThaiTokenizer()
        self.assertIsNotNone(self.thai.tokenizer("ทดสอบการตัดคำ"))
    def test_rm_useless_newlines(self):
        self.assertIsNotNone(rm_useless_newlines("ผมจะขึ้นบรรทัดใหม่\nคุณโอเคไหม"))
    def test_lowercase_all(self):
        self.assertIsNotNone(lowercase_all(["A","B"]))
