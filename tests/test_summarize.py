# -*- coding: utf-8 -*-

import datetime
import os
import sys
import unittest

from pythainlp.summarize import summarize


class TestSummarizePackage(unittest.TestCase):

    def test_summarize(self):
        text = "อาหาร หมายถึง ของแข็งหรือของเหลว "
        text += "ที่กินหรือดื่มเข้าสู่ร่างกายแล้ว "
        text += "จะทำให้เกิดพลังงานและความร้อนแก่ร่างกาย "
        text += "ทำให้ร่างกายเจริญเติบโต "
        text += "ซ่อมแซมส่วนที่สึกหรอ ควบคุมการเปลี่ยนแปลงต่างๆ ในร่างกาย "
        text += "ช่วยทำให้อวัยวะต่างๆ ทำงานได้อย่างปกติ "
        text += "อาหารจะต้องไม่มีพิษและไม่เกิดโทษต่อร่างกาย"
        self.assertEqual(
            summarize(text=text, n=1, engine="frequency"),
            ["อาหารจะต้องไม่มีพิษและไม่เกิดโทษต่อร่างกาย"],
        )
        self.assertIsNotNone(summarize(text, 1, engine="XX"))
