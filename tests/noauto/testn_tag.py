# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

# Tests for tag functions that require transformers or tltk
# These tests are NOT run in automated CI workflows due to:
# - Large dependencies (transformers, torch)
# - Compilation issues (tltk)
# - Python 3.13+ compatibility issues

import unittest

from pythainlp.tag import (
    NER,
    NNER,
    pos_tag,
    pos_tag_transformers,
    tltk,
)


class TagTLTKTestCaseN(unittest.TestCase):
    """Tests for tltk engine (requires tltk with compilation issues)"""

    def test_pos_tag_tltk(self):
        tokens = ["ผม", "รัก", "คุณ"]
        self.assertIsNotNone(pos_tag(tokens, engine="tltk"))
        with self.assertRaises(ValueError):
            tltk.pos_tag(tokens, corpus="blackboard")

    def test_tltk_ner(self):
        self.assertEqual(tltk.get_ner(""), [])
        self.assertIsNotNone(tltk.get_ner("แมวทำอะไรตอนห้าโมงเช้า"))
        self.assertIsNotNone(tltk.get_ner("แมวทำอะไรตอนห้าโมงเช้า", pos=False))
        self.assertIsNotNone(
            tltk.get_ner("พลเอกประยุกธ์ จันทร์โอชา ประกาศในฐานะหัวหน้า")
        )
        self.assertIsNotNone(
            tltk.get_ner(
                "พลเอกประยุกธ์ จันทร์โอชา ประกาศในฐานะหัวหน้า",
                tag=True,
            )
        )
        self.assertIsNotNone(
            tltk.get_ner(
                """คณะวิทยาศาสตร์ประยุกต์และวิศวกรรมศาสตร์ มหาวิทยาลัยขอนแก่น
                จังหวัดหนองคาย 43000"""
            )
        )
        self.assertIsNotNone(
            tltk.get_ner(
                """คณะวิทยาศาสตร์ประยุกต์และวิศวกรรมศาสตร์ มหาวิทยาลัยขอนแก่น
                จังหวัดหนองคาย 43000""",
                tag=True,
            )
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

        # Test thai-nner engine
        ner = NER(engine="thai-nner")
        self.assertIsNotNone(ner.tag("แมวทำอะไรตอนห้าโมงเช้า"))
        self.assertIsNotNone(ner.tag("แมวทำอะไรตอนห้าโมงเช้า", pos=False))
        self.assertIsNotNone(ner.tag("แมวทำอะไรตอนห้าโมงเช้า", tag=True))

    def test_NNER_class(self):
        nner = NNER()
        # Test basic tagging
        self.assertIsNotNone(nner.tag("แมวทำอะไรตอนห้าโมงเช้า"))

        # Test with top_level_only parameter
        tokens, entities = nner.tag("แมวทำอะไรตอนห้าโมงเช้า")
        self.assertIsInstance(tokens, list)
        self.assertIsInstance(entities, list)

        tokens_top, entities_top = nner.tag("แมวทำอะไรตอนห้าโมงเช้า", top_level_only=True)
        self.assertIsInstance(tokens_top, list)
        self.assertIsInstance(entities_top, list)
        # Top-level entities should be less than or equal to all entities
        self.assertLessEqual(len(entities_top), len(entities))

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
