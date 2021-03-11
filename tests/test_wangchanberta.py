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
            ner.get_ner("I คิด therefore I am ผ็ฎ์", tag=True)
        )
        self.assertIsNotNone(
            ner.get_ner(
                "โรงเรียนสวนกุหลาบเป็นโรงเรียนที่ดี แต่ไม่มีสวนกุหลาบ",
                tag=True
            )
        )

        ner = ThaiNameTagger(grouped_entities=False)
        self.assertIsNotNone(
            ner.get_ner("I คิด therefore I am ผ็ฎ์", tag=True)
        )

    def test_lst20_ner_wangchanberta(self):
        ner = ThaiNameTagger(dataset_name="lst20")
        self.assertIsNotNone(
            ner.get_ner("I คิด therefore I am ผ็ฎ์")
        )
        self.assertIsNotNone(
            ner.get_ner("I คิด therefore I am ผ็ฎ์", tag=True)
        )
        self.assertIsNotNone(
            ner.get_ner(
                "โรงเรียนสวนกุหลาบเป็นโรงเรียนที่ดี แต่ไม่มีสวนกุหลาบ",
                tag=True
            )
        )

        ner = ThaiNameTagger(
            dataset_name="lst20",
            grouped_entities=False
        )
        self.assertIsNotNone(
            ner.get_ner("I คิด therefore I am ผ็ฎ์", tag=True)
        )

    def test_segment_wangchanberta(self):
        self.assertIsNotNone(
            segment("I คิด therefore I am ผ็ฎ์")
        )
        self.assertIsNotNone(
            segment([])
        )

    def test_pos_tag_wangchanberta(self):
        self.assertIsNotNone(
            pos_tag("I คิด therefore I am ผ็ฎ์")
        )
        self.assertIsNotNone(
            pos_tag(
                [
                    'I',
                    ' ',
                    'คิด',
                    ' ',
                    'therefore',
                    ' ',
                    'I',
                    ' ',
                    'am',
                    ' ',
                    'ผ็ฎ์'
                ]
            )
        )
        self.assertIsNotNone(
            pos_tag(None)
        )
        self.assertIsNotNone(
            pos_tag("I คิด therefore I am ผ็ฎ์", grouped_word=True)
        )
        self.assertIsNotNone(
            pos_tag("ทดสอบระบบ", grouped_word=False)
        )
