# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

# Tests for tag functions that require transformers or torch
# These tests are NOT run in automated CI workflows due to:
# - Large dependencies (transformers, torch)
# - Python 3.13+ compatibility issues

import unittest

from pythainlp.tag import (
    NER,
    NNER,
    pos_tag_transformers,
)


class TagTransformersTestCaseN(unittest.TestCase):
    """Tests for transformers-based engines (requires transformers, torch)"""

    def test_NER_class(self):
        with self.assertRaises(ValueError):
            NER(engine="thainer", corpus="cat")

        ner = NER(engine="thainer")
        self.assertIsNotNone(ner.tag("แมวทำอะไรตอนห้าโมงเช้า"))
        self.assertIsNotNone(ner.tag("แมวทำอะไรตอนห้าโมงเช้า", pos=False))
        self.assertIsNotNone(ner.tag("แมวทำอะไรตอนห้าโมงเช้า", tag=True))

        ner = NER(engine="thainer-v2")
        self.assertIsNotNone(ner.tag("แมวทำอะไรตอนห้าโมงเช้า"))
        self.assertIsNotNone(ner.tag("แมวทำอะไรตอนห้าโมงเช้า", pos=False))
        self.assertIsNotNone(ner.tag("แมวทำอะไรตอนห้าโมงเช้า", tag=True))

        ner = NER(engine="wangchanberta")
        self.assertIsNotNone(ner.tag("แมวทำอะไรตอนห้าโมงเช้า"))
        self.assertIsNotNone(ner.tag("แมวทำอะไรตอนห้าโมงเช้า", pos=False))
        self.assertIsNotNone(ner.tag("แมวทำอะไรตอนห้าโมงเช้า", tag=True))

        ner = NER(engine="tltk")
        self.assertIsNotNone(ner.tag("แมวทำอะไรตอนห้าโมงเช้า"))
        self.assertIsNotNone(ner.tag("แมวทำอะไรตอนห้าโมงเช้า", pos=False))
        self.assertIsNotNone(ner.tag("แมวทำอะไรตอนห้าโมงเช้า", tag=True))

    def test_NNER_class(self):
        nner = NNER()
        self.assertIsNotNone(nner.tag("แมวทำอะไรตอนห้าโมงเช้า"))

    def test_pos_tag_transformers(self):
        self.assertIsNotNone(
            pos_tag_transformers(
                sentence="แมวทำอะไรตอนห้าโมงเช้า",
                engine="bert",
                corpus="blackboard",
            )
        )
        self.assertIsNotNone(
            pos_tag_transformers(
                sentence="แมวทำอะไรตอนห้าโมงเช้า",
                engine="mdeberta",
                corpus="pud",
            )
        )
        self.assertIsNotNone(
            pos_tag_transformers(
                sentence="แมวทำอะไรตอนห้าโมงเช้า",
                engine="wangchanberta",
                corpus="pud",
            )
        )
        with self.assertRaises(ValueError):
            pos_tag_transformers(
                sentence="แมวทำอะไรตอนห้าโมงเช้า", engine="non-existing-engine"
            )
        with self.assertRaises(ValueError):
            pos_tag_transformers(
                sentence="แมวทำอะไรตอนห้าโมงเช้า",
                engine="bert",
                corpus="non-existing corpus",
            )
