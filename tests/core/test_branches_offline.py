# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Offline tests for branches in spelling, profanity, and POS tagging.

These cover code that is otherwise tested only with a downloaded corpus
or model. ``transformers`` and the profanity corpus are replaced with fakes.
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

# (word, expected spelling): short vowel mark, tone marks, no change
_SPELLING = [
    ("กา", ["กอ", "อา", "กา"]),
    ("เด็ก", ["ดอ", "เอะ", "กอ", "เด็ก"]),
    ("น้ำ", ["นอ", "อำ", "นำ", "ไม้โท", "น้ำ"]),
    ("เรื่อง", ["รอ", "เอือ", "งอ", "เรือง", "ไม้เอก", "เรื่อง"]),
]


class SpellingBranchesTestCase(unittest.TestCase):
    def test_spelling(self) -> None:
        for word, expected in _SPELLING:
            with self.subTest(word=word):
                self.assertEqual(spelling(word), expected)


class ContainsProfanityTestCase(unittest.TestCase):
    def check(self, tokens: list[str], expected: bool, **kwargs: Any) -> None:
        patches = {
            "thai_profanity_words": frozenset({"คำหยาบ"}),
            "thai_words": frozenset({"สวัสดี"}),
            "word_tokenize": tokens,
        }
        with ExitStack() as stack:
            for name, value in patches.items():
                stack.enter_context(
                    mock.patch(
                        f"pythainlp.util.profanity.{name}", return_value=value
                    )
                )
            self.assertIs(contains_profanity("x", **kwargs), expected)

    def test_found(self) -> None:
        self.check(["สวัสดี", "คำหยาบ"], True)

    def test_not_found(self) -> None:
        self.check(["สวัสดี"], False)

    def test_custom_words(self) -> None:
        self.check(["คำใหม่"], True, custom_words={"คำใหม่"})

    def test_empty_text(self) -> None:
        self.assertIs(contains_profanity(""), False)


def _fake_transformers() -> tuple[types.ModuleType, mock.Mock]:
    """Return a fake ``transformers`` module and its model loader."""
    module = types.ModuleType("transformers")
    model_loader = mock.Mock()
    auto_model = mock.Mock()
    auto_model.from_pretrained = model_loader
    auto_tokenizer = mock.Mock()
    pipeline = mock.Mock(
        return_value=mock.Mock(
            return_value=[{"word": "แมว", "entity_group": "NOUN"}]
        )
    )
    module.AutoModelForTokenClassification = auto_model  # type: ignore[attr-defined]
    module.AutoTokenizer = auto_tokenizer  # type: ignore[attr-defined]
    module.TokenClassificationPipeline = pipeline  # type: ignore[attr-defined]
    return module, model_loader


class PosTagTransformersTestCase(unittest.TestCase):
    def run_tag(self, **kwargs: Any) -> tuple[Any, mock.Mock]:
        module, model_loader = _fake_transformers()
        with mock.patch.dict(sys.modules, {"transformers": module}):
            result = pos_tag_transformers("แมว", **kwargs)
        return result, model_loader

    def test_blackboard_corpus(self) -> None:
        result, loader = self.run_tag(engine="bert", corpus="blackboard")
        self.assertEqual(result, [[("แมว", "NOUN")]])
        loader.assert_called_once_with("lunarlist/pos_thai", revision=None)

    def test_pud_corpus(self) -> None:
        result, loader = self.run_tag(engine="mdeberta", corpus="pud")
        self.assertEqual(result, [[("แมว", "NOUN")]])
        loader.assert_called_once_with(
            "Pavarissy/mdeberta-v3-ud-thai-pud-upos", revision=None
        )

    def test_unsupported_engine_or_corpus(self) -> None:
        for kwargs in (
            {"engine": "mdeberta", "corpus": "blackboard"},
            {"engine": "bert", "corpus": "pud"},
            {"engine": "bert", "corpus": "other"},
        ):
            with self.subTest(**kwargs), self.assertRaises(ValueError):
                self.run_tag(**kwargs)

    def test_empty_sentence(self) -> None:
        module, _ = _fake_transformers()
        with mock.patch.dict(sys.modules, {"transformers": module}):
            self.assertEqual(pos_tag_transformers(""), [])


if __name__ == "__main__":
    unittest.main()
