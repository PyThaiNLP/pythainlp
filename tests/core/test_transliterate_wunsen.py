# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""
Tests for pythainlp.transliterate.wunsen.

The optional ``wunsen`` package is replaced by a fake module, so the tests
run in the core tier.
"""

import importlib.util
import sys
import types
import unittest
from pathlib import Path
from typing import Any, ClassVar
from unittest import mock

import pythainlp

MODULE_PATH = Path(pythainlp.__file__).parent / "transliterate" / "wunsen.py"


class FakeThapSap:
    """Replacement for wunsen.ThapSap; records its arguments."""

    created: ClassVar[list[tuple[str, dict[str, Any]]]] = []

    def __init__(self, lang: str, **kwargs: Any) -> None:
        """Record the arguments."""
        FakeThapSap.created.append((lang, kwargs))
        self.lang = lang

    def thap(self, text: str) -> str:
        return f"{self.lang}:{text}"


# (arguments, expected ThapSap constructor call, expected stored options)
# Stored options: (lang, jp_input, zh_sandhi, system)
CASES: tuple[
    tuple[dict[str, Any], tuple[str, dict[str, Any]], tuple[Any, ...]],
    ...,
] = (
    (
        {"lang": "jp"},
        ("ja", {}),
        ("jp", None, None, None),
    ),
    (
        {"lang": "jp", "jp_input": "Hepburn-no diacritic", "system": "RI35"},
        ("ja", {"input": "Hepburn-no diacritic", "system": "RI35"}),
        ("jp", "Hepburn-no diacritic", None, "RI35"),
    ),
    (
        # zh_sandhi is ignored for Japanese
        {"lang": "jp", "zh_sandhi": True},
        ("ja", {}),
        ("jp", None, None, None),
    ),
    (
        {"lang": "zh"},
        ("zh", {}),
        ("zh", None, None, None),
    ),
    (
        {"lang": "zh", "zh_sandhi": False, "system": "RI49"},
        ("zh", {"option": {"sandhi": False}, "system": "RI49"}),
        ("zh", None, False, "RI49"),
    ),
    (
        # jp_input is ignored for Mandarin
        {"lang": "zh", "zh_sandhi": True, "jp_input": "x"},
        ("zh", {"option": {"sandhi": True}}),
        ("zh", None, True, None),
    ),
    (
        {"lang": "ko", "jp_input": "x", "zh_sandhi": True, "system": "y"},
        ("ko", {}),
        ("ko", None, None, None),
    ),
    (
        {"lang": "vi"},
        ("vi", {}),
        ("vi", None, None, None),
    ),
)


class WunsenTestCase(unittest.TestCase):
    def setUp(self) -> None:
        FakeThapSap.created = []
        fake = types.ModuleType("wunsen")
        setattr(fake, "ThapSap", FakeThapSap)
        spec = importlib.util.spec_from_file_location(
            "wunsen_transliterate_under_test", MODULE_PATH
        )
        if spec is None or spec.loader is None:
            raise ImportError(f"Cannot load {MODULE_PATH}")
        self.wunsen = importlib.util.module_from_spec(spec)
        with mock.patch.dict(sys.modules, {"wunsen": fake}):
            spec.loader.exec_module(self.wunsen)

    def test_initial_state(self) -> None:
        wt = self.wunsen.WunsenTransliterate()
        self.assertEqual(
            (wt.lang, wt.jp_input, wt.zh_sandhi, wt.system, wt.thap_value),
            (None, None, None, None, None),
        )

    def test_options(self) -> None:
        for kwargs, created, state in CASES:
            with self.subTest(kwargs=kwargs):
                FakeThapSap.created = []
                wt = self.wunsen.WunsenTransliterate()
                result = wt.transliterate("abc", **kwargs)
                self.assertEqual(result, f"{created[0]}:abc")
                self.assertEqual(FakeThapSap.created, [created])
                self.assertEqual(
                    (wt.lang, wt.jp_input, wt.zh_sandhi, wt.system), state
                )

    def test_reuse_and_rebuild(self) -> None:
        wt = self.wunsen.WunsenTransliterate()
        wt.transliterate("a", lang="zh")
        wt.transliterate("b", lang="zh")
        self.assertEqual(len(FakeThapSap.created), 1)
        wt.transliterate("c", lang="zh", zh_sandhi=True)
        wt.transliterate("d", lang="ko")
        self.assertEqual(
            FakeThapSap.created,
            [
                ("zh", {}),
                ("zh", {"option": {"sandhi": True}}),
                ("ko", {}),
            ],
        )

    def test_unsupported_language(self) -> None:
        wt = self.wunsen.WunsenTransliterate()
        wt.transliterate("a", lang="vi")
        with self.assertRaises(NotImplementedError) as ctx:
            wt.transliterate("a", lang="xx")
        self.assertEqual(
            str(ctx.exception), "The xx language is not implemented."
        )
        # State is unchanged after the error.
        self.assertEqual(wt.lang, "vi")
        self.assertEqual(len(FakeThapSap.created), 1)

    def test_none_language_not_implemented(self) -> None:
        FakeThapSap.created = []
        wt = self.wunsen.WunsenTransliterate()
        with self.assertRaises(NotImplementedError) as ctx:
            wt.transliterate("a", lang=None)
        self.assertEqual(
            str(ctx.exception), "The None language is not implemented."
        )
        self.assertIsNone(wt.lang)
        self.assertIsNone(wt.thap_value)
        self.assertEqual(FakeThapSap.created, [])

    def test_none_language_after_use(self) -> None:
        wt = self.wunsen.WunsenTransliterate()
        wt.transliterate("a", lang="zh", zh_sandhi=True, system="RI49")
        with self.assertRaises(NotImplementedError) as ctx:
            wt.transliterate("a", lang=None)
        self.assertEqual(
            str(ctx.exception), "The None language is not implemented."
        )
        self.assertEqual(
            (wt.lang, wt.zh_sandhi, wt.system), ("zh", True, "RI49")
        )
        self.assertEqual(len(FakeThapSap.created), 1)

    def test_invalid_language_values(self) -> None:
        # (value, message); matching is case-sensitive and exact.
        values: tuple[tuple[Any, str], ...] = (
            (None, "None"),
            ("", ""),
            ("xx", "xx"),
            ("JP", "JP"),
            (" jp", " jp"),
            ("ja", "ja"),
            (123, "123"),
            (["jp"], "['jp']"),
        )
        for value, text in values:
            for used in (False, True):
                with self.subTest(value=value, used=used):
                    FakeThapSap.created = []
                    wt = self.wunsen.WunsenTransliterate()
                    if used:
                        wt.transliterate("a", lang="ko")
                    before = len(FakeThapSap.created)
                    with self.assertRaises(NotImplementedError) as ctx:
                        wt.transliterate("a", lang=value)
                    self.assertEqual(
                        str(ctx.exception),
                        f"The {text} language is not implemented.",
                    )
                    self.assertEqual(wt.lang, "ko" if used else None)
                    self.assertEqual(len(FakeThapSap.created), before)
                    # The object recovers with a valid language.
                    self.assertEqual(wt.transliterate("b", lang="vi"), "vi:b")

    def test_failed_creation_keeps_old_model(self) -> None:
        # BUG-LEDGER: wunsen-stale-model
        # Expected: the repeated call raises again, not reuse the zh model.
        class FailingThapSap(FakeThapSap):
            def __init__(self, lang: str, **kwargs: Any) -> None:
                if kwargs.get("system") == "BAD":
                    raise ValueError("bad system")
                super().__init__(lang, **kwargs)

        wt = self.wunsen.WunsenTransliterate()
        with mock.patch.object(self.wunsen, "ThapSap", FailingThapSap):
            self.assertEqual(wt.transliterate("a", lang="zh"), "zh:a")
            with self.assertRaises(ValueError):
                wt.transliterate("a", lang="jp", system="BAD")
            self.assertEqual(
                wt.transliterate("a", lang="jp", system="BAD"), "zh:a"
            )

    def test_recover_with_options_after_error(self) -> None:
        wt = self.wunsen.WunsenTransliterate()
        with self.assertRaises(NotImplementedError):
            wt.transliterate("a", lang="xx", zh_sandhi=True, system="s")
        self.assertEqual(wt.transliterate("a", lang="vi"), "vi:a")
        wt.transliterate("a", lang="zh", zh_sandhi=False)
        wt.transliterate("a", lang="zh", system="RI49")
        wt.transliterate("a", lang="zh", zh_sandhi=False, system="RI49")
        self.assertEqual(
            FakeThapSap.created,
            [
                ("vi", {}),
                ("zh", {"option": {"sandhi": False}}),
                ("zh", {"system": "RI49"}),
                ("zh", {"option": {"sandhi": False}, "system": "RI49"}),
            ],
        )


if __name__ == "__main__":
    unittest.main()
