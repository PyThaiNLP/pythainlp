# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Offline tests for branches in spelling, profanity, and POS tagging.

``transformers`` and the profanity corpus are replaced with fakes.
"""

import sys
import types
import unittest
from contextlib import ExitStack
from typing import Any
from unittest import mock

from pythainlp.tag import pos_tag_transformers
from pythainlp.util import contains_profanity
from pythainlp.util.pronounce import spelling

_SPELLING = [
    ("กา", ["กอ", "อา", "กา"]),
    ("เด็ก", ["ดอ", "เอะ", "กอ", "เด็ก"]),
    ("น้ำ", ["นอ", "อำ", "นำ", "ไม้โท", "น้ำ"]),
    ("เรื่อง", ["รอ", "เอือ", "งอ", "เรือง", "ไม้เอก", "เรื่อง"]),
]


class BranchesOfflineTestCase(unittest.TestCase):
    def test_spelling(self) -> None:
        for word, expected in _SPELLING:
            with self.subTest(word=word):
                self.assertEqual(spelling(word), expected)

    def test_contains_profanity(self) -> None:
        cases: list[tuple[list[str], dict[str, Any], bool]] = [
            (["สวัสดี", "คำหยาบ"], {}, True),
            (["สวัสดี"], {}, False),
            (["คำใหม่"], {"custom_words": {"คำใหม่"}}, True),
        ]
        patches = {
            "thai_profanity_words": frozenset({"คำหยาบ"}),
            "thai_words": frozenset({"สวัสดี"}),
        }
        for tokens, kwargs, expected in cases:
            with self.subTest(tokens=tokens), ExitStack() as stack:
                patches["word_tokenize"] = tokens  # type: ignore[assignment]
                for name, value in patches.items():
                    stack.enter_context(
                        mock.patch(
                            f"pythainlp.util.profanity.{name}",
                            return_value=value,
                        )
                    )
                self.assertIs(contains_profanity("x", **kwargs), expected)
        self.assertIs(contains_profanity(""), False)

    def test_pos_tag_transformers(self) -> None:
        loader = mock.Mock()
        fake = types.ModuleType("transformers")
        fake.__dict__.update(
            AutoModelForTokenClassification=mock.Mock(from_pretrained=loader),
            AutoTokenizer=mock.Mock(),
            TokenClassificationPipeline=mock.Mock(
                return_value=lambda _: [
                    {"word": "แมว", "entity_group": "NOUN"}
                ]
            ),
        )
        ok = [
            ({"engine": "bert", "corpus": "blackboard"}, "lunarlist/pos_thai"),
            (
                {"engine": "mdeberta", "corpus": "pud"},
                "Pavarissy/mdeberta-v3-ud-thai-pud-upos",
            ),
        ]
        bad = [
            {"engine": "mdeberta", "corpus": "blackboard"},
            {"engine": "bert", "corpus": "pud"},
            {"engine": "bert", "corpus": "other"},
        ]
        with mock.patch.dict(sys.modules, {"transformers": fake}):
            for kwargs, model in ok:
                with self.subTest(**kwargs):
                    loader.reset_mock()
                    self.assertEqual(
                        pos_tag_transformers("แมว", **kwargs),
                        [[("แมว", "NOUN")]],
                    )
                    loader.assert_called_once_with(model, revision=None)
            for kwargs in bad:
                with self.subTest(**kwargs), self.assertRaises(ValueError):
                    pos_tag_transformers("แมว", **kwargs)
            self.assertEqual(pos_tag_transformers(""), [])


if __name__ == "__main__":
    unittest.main()
