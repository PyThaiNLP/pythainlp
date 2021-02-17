# -*- coding: utf-8 -*-

import unittest

from pythainlp.summarize import summarize


class TestSummarizePackage(unittest.TestCase):
    def test_summarize(self):
        text = (
            "อาหาร หมายถึง ของแข็งหรือของเหลว "
            "ที่กินหรือดื่มเข้าสู่ร่างกายแล้ว "
            "จะทำให้เกิดพลังงานและความร้อนแก่ร่างกาย "
            "ทำให้ร่างกายเจริญเติบโต "
            "ซ่อมแซมส่วนที่สึกหรอ ควบคุมการเปลี่ยนแปลงต่างๆ ในร่างกาย "
            "ช่วยทำให้อวัยวะต่างๆ ทำงานได้อย่างปกติ "
            "อาหารจะต้องไม่มีพิษและไม่เกิดโทษต่อร่างกาย"
        )
        self.assertEqual(
            summarize(text=text, n=1),
            ["อาหารจะต้องไม่มีพิษและไม่เกิดโทษต่อร่างกาย"],
        )
        self.assertIsNotNone(summarize(text, engine="mt5-small"))
        self.assertIsNotNone(summarize([]))
        self.assertIsNotNone(summarize(text, 1, engine="mt5-small"))
        self.assertIsNotNone(summarize(text, 1, engine="XX"))
