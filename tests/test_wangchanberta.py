# -*- coding: utf-8 -*-

import unittest

from pythainlp.wangchanberta import ThaiNameTagger, pos_tag, segment


class TestWangchanberta(unittest.TestCase):
    def test_thainer_wangchanberta(self):
        ner = ThaiNameTagger()
        self.assertIsNotNone(
            ner.get_ner("I คิด therefore I am ผ็ฎ์")
        )
        ner = ThaiNameTagger()
        self.assertIsNotNone(
            ner.get_ner("I คิด therefore I am ผ็ฎ์", tag = True)
        )

    def test_lst20_ner_wangchanberta(self):
        ner = ThaiNameTagger(dataset_name="lst20")
        self.assertIsNotNone(
            ner.get_ner("I คิด therefore I am ผ็ฎ์")
        )
        self.assertIsNotNone(
            ner.get_ner("I คิด therefore I am ผ็ฎ์", tag = True)
        )

    def test_segment_wangchanberta(self):
        self.assertIsNotNone(
            segment("I คิด therefore I am ผ็ฎ์")
        )
        self.assertIsNotNone(
            segment([])
        )
