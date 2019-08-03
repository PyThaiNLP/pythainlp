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
    def test_load_pretrained(self):
        self.assertIsNotNone(_THWIKI_LSTM)
    def test_pre_rules_th(self):
        self.assertIsNotNone(pre_rules_th)
    def test_post_rules_th(self):
        self.assertIsNotNone(post_rules_th)
