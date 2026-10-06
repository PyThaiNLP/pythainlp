# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Offline tests for pythainlp.summarize and the benchmark text helpers.

They use only the standard library and the bundled corpora. The mT5 and
KeyBERT engines are replaced with fakes.
"""

import sys
import types
import unittest
from typing import Any, Union
from unittest import mock

from pythainlp.benchmarks import word_tokenization as wt
from pythainlp.summarize import extract_keywords, summarize
from pythainlp.summarize.freq import FrequencySummarizer

_TEXT = "แมวกินปลาแมว\nแมวนอนหลับ\nสุนัขเห่า"  # "แมว" is the top word
_WORDS = "แมวกินปลา แมวนอนหลับ แมวกินปลา ปลาว่ายน้ำ"


def _fake(name: str, **attrs: Any) -> dict[str, types.ModuleType]:
    """Return a ``sys.modules`` patch with a fake module."""
    module = types.ModuleType(name)
    module.__dict__.update(attrs)
    return {name: module}


class SummarizeOfflineTestCase(unittest.TestCase):
    def test_frequency_summarizer(self) -> None:
        wide = FrequencySummarizer(min_cut=0.0, max_cut=1.1)
        top2 = wide.summarize(_TEXT, 2)
        self.assertEqual(wide.summarize(_TEXT, 1), ["แมวกินปลาแมว"])
        self.assertEqual((len(top2), top2[0]), (2, "แมวกินปลาแมว"))
        self.assertEqual(len(wide.summarize(_TEXT, 10)), 3)
        self.assertEqual(FrequencySummarizer().summarize("", 3), [])
        self.assertEqual(FrequencySummarizer().summarize("! ? ,", 1), ["!"])
        # One-word sentences with frequencies a=1.0, b=0.5, c=0.25.
        # With max_cut=0.6, "a" is dropped and "b" ranks first.
        text = "a a a a b b c"
        self.assertEqual(wide.summarize(text, 1), ["a"])
        self.assertEqual(
            FrequencySummarizer(0.0, 0.6).summarize(text, 1), ["b"]
        )

    def test_summarize(self) -> None:
        for text in ("", None, 123):
            with self.subTest(text=text):
                self.assertEqual(summarize(text), [])  # type: ignore[arg-type]
        self.assertEqual(summarize(_TEXT, n=1)[0], "แมวกินปลาแมว")
        # An unknown engine returns the first n sentences
        self.assertEqual(
            summarize(_TEXT, n=2, engine="unknown"),
            ["แมวกินปลาแมว", "แมวนอนหลับ"],
        )

    def test_summarize_mt5(self) -> None:
        mt5 = mock.Mock()
        mt5.return_value.summarize.return_value = ["สรุป"]
        cases: list[tuple[str, dict[str, Any]]] = [
            (
                "mt5-cpe-kmutt-thai-sentence-sum",
                {
                    "pretrained_mt5_model_name": "mt5-cpe-kmutt-thai-sentence-sum",
                    "min_length": 5,
                },
            ),
            ("mt5-small", {"model_size": "small"}),
            ("mt5", {"model_size": "mt5"}),
        ]
        with mock.patch.dict(
            sys.modules, _fake("pythainlp.summarize.mt5", mT5Summarizer=mt5)
        ):
            for engine, kwargs in cases:
                with self.subTest(engine=engine):
                    mt5.reset_mock()
                    self.assertEqual(summarize(_TEXT, engine=engine), ["สรุป"])
                    mt5.assert_called_once_with(**kwargs)

    def test_extract_keywords(self) -> None:
        kw = "frequency"
        self.assertEqual(
            extract_keywords(_WORDS, max_keywords=3, engine=kw),
            ["แมว", "ปลา", "กิน"],
        )
        self.assertEqual(extract_keywords("แมวกินปลา", min_df=5, engine=kw), [])
        self.assertNotIn(
            "แมว", extract_keywords(_WORDS, stop_words=["แมว"], engine=kw)
        )
        for text in ("", "   "):
            self.assertEqual(extract_keywords(text, engine=kw), [])
        with self.assertRaisesRegex(ValueError, "'unknown'"):
            extract_keywords("แมว", engine="unknown")

    def test_extract_keywords_keybert(self) -> None:
        extractor = mock.Mock()
        extractor.extract_keywords.return_value = ["คำ"]
        patch = _fake("pythainlp.summarize.keybert", KeyBERT=lambda: extractor)
        with mock.patch.dict(sys.modules, patch):
            self.assertEqual(
                extract_keywords("แมว", max_keywords=2, min_df=3), ["คำ"]
            )
        kwargs = extractor.extract_keywords.call_args.kwargs
        self.assertEqual(
            (
                kwargs["max_keywords"],
                kwargs["min_df"],
                kwargs["return_similarity"],
            ),
            (2, 3, False),
        )

    def test_benchmark_text_helpers(self) -> None:
        for text, expected in (
            ("ก|ข | |ค||<NE>ง</NE>|", "ก|ข|ค|ง"),
            ("ก ข|ค", "กข|ค"),
            ("", ""),
            ("||", ""),
        ):
            with self.subTest(text=text):
                self.assertEqual(wt.preprocessing(text), expected)
        self.assertEqual(wt.preprocessing("ก ข", remove_space=False), "ก ข")
        self.assertEqual((wt._f1(0, 0), wt._f1(0.5, 0.5)), (0, 0.5))
        self.assertAlmostEqual(wt._f1(1.0, 0.5), 2 / 3)
        nested: dict[str, dict[str, Union[int, str]]] = {
            "a": {"b": 1, "c": "x"},
            "d": {"e": 2},
        }
        self.assertEqual(
            wt._flatten_result(nested), {"a:b": 1, "a:c": "x", "d:e": 2}
        )
        self.assertEqual(
            wt._flatten_result({"a": {"b": 1}}, sep="."), {"a.b": 1}
        )
        self.assertEqual(wt._flatten_result({}), {})


if __name__ == "__main__":
    unittest.main()
