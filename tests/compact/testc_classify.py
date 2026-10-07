# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

import os
import tempfile
import unittest

from pythainlp.classify import GzipModel


class ClsTestCaseC(unittest.TestCase):
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
        # Edge cases: empty string
        self.assertIsNotNone(model.predict("", k=1))
        # Edge cases: different k values
        self.assertIsNotNone(model.predict("ฉันดีใจ", k=3))
        # Edge cases: k larger than number of classes
        self.assertIsNotNone(model.predict("ฉันดีใจ", k=10))

    def test_GzipModel_save_and_load(self):
        training_data = [
            ("ดีนะครับ", "Positive"),
            ("ลองแล้วรสนี้อร่อย... ชอบๆ", "Positive"),
            ("ขับรถแย่มาก", "Negative"),
            ("บริการแย่มากก เป็นหมอได้ไง😤", "Negative"),
        ]
        model = GzipModel(training_data)
        with tempfile.TemporaryDirectory() as tmp_dir:
            path = os.path.join(tmp_dir, "model.json")
            model.save(path)
            loaded = GzipModel(model_path=path)
        self.assertEqual(loaded.cx2_list, model.cx2_list)
        self.assertEqual(
            loaded.training_data.tolist(), model.training_data.tolist()
        )
        for text in ("ฉันดีใจ", "ขับรถแย่", ""):
            with self.subTest(text=text):
                self.assertEqual(loaded.predict(text), model.predict(text))
