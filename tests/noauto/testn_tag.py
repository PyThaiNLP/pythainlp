# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

# DEPRECATED: This file is kept for backward compatibility only.
# New tests should be added to tests.noauto-torch for transformers-based tests.

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
    """Tests for transformers-based engines (requires transformers, torch)

    DEPRECATED: Moved to tests.noauto-torch.testn_tag_torch
    """

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
