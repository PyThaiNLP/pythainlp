# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

import unittest

from pythainlp.classify import GzipModel


class ClsTestCaseX(unittest.TestCase):
    def test_GzipModel(self):
        training_data = [
            ("รายละเอียดตามนี้เลยค่าา ^^", "Neutral"),
            ("กลัวพวกมึงหาย อดกินบาบิก้อน", "Neutral"),
            ("บริการแย่มากก เป็นหมอได้ไง😤", "Negative"),
            ("ขับรถแย่มาก", "Negative"),
            ("ดีนะครับ", "Positive"),
            ("ลองแล้วรสนี้อร่อย... ชอบๆ", "Positive"),
            ("ฉันรู้สึกโกรธ เวลามือถือแบตหมด", "Negative"),
            ("เธอภูมิใจที่ได้ทำสิ่งดี ๆ และดีใจกับเด็ก ๆ", "Positive"),
            ("นี่เป็นบทความหนึ่ง", "Neutral"),
        ]
        model = GzipModel(training_data)
        self.assertEqual(model.predict("ฉันดีใจ", k=1), "Positive")
