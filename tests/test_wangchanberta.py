# -*- coding: utf-8 -*-

import unittest

from pythainlp.wangchanberta import ThaiNameTagger, pos_tag


class TestWangchanberta(unittest.TestCase):
    def test_thainer_wangchanberta(self):
        ner = ThaiNameTagger()
        self.assertIsNotNone(
            ner.get_ner("I คิด therefore I am ผ็ฎ์")
        )
    def test_lst20_ner_wangchanberta(self):
        ner = ThaiNameTagger(dataset_name="lst20")
        self.assertIsNotNone(
            ner.get_ner("I คิด therefore I am ผ็ฎ์")
        )
