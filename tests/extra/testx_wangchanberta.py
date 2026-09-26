# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

import unittest
import warnings

from pythainlp.lm.wangchanberta import ThaiNameTagger, segment


class WangchanbertaTestCaseX(unittest.TestCase):
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

    def test_segment_wangchanberta(self):
        self.assertIsNotNone(
            segment("I คิด therefore I am ผ็ฎ์")
        )
        self.assertIsNotNone(
            segment([])  # type: ignore[arg-type]
        )

    def test_deprecated_wangchanberta(self):
        import importlib
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            import pythainlp.wangchanberta
            importlib.reload(pythainlp.wangchanberta)
        self.assertTrue(
            any(issubclass(warning.category, DeprecationWarning) for warning in w)
        )
