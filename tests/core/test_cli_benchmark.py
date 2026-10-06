# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Offline tests for pythainlp.cli.benchmark.

``yaml`` and the benchmark function are replaced with fakes, so the tests
need neither pandas nor PyYAML.
"""

import io
import json
import sys
import tempfile
import types
import unittest
from argparse import ArgumentError
from contextlib import ExitStack, redirect_stderr, redirect_stdout
from pathlib import Path
from typing import Any
from unittest import mock

from pythainlp.benchmarks import word_tokenization
from pythainlp.cli import benchmark
from pythainlp.cli.benchmark import App, WordTokenizationBenchmark, _read_file

_RECORD: dict[str, Any] = {
    "char_level:tp": 8,
    "char_level:fp": 2,
    "char_level:tn": 4,
    "char_level:fn": 2,
    "word_level:correctly_tokenized_words": 3,
    "word_level:total_words_in_sample": 4,
    "word_level:total_words_in_ref_sample": 6,
    "expected": "ก|ข",
    "actual": "ก|ข",
}


class _FakeFrame:
    """The part of pandas.DataFrame that the command uses."""

    def __init__(self, records: list[dict[str, Any]]) -> None:
        self.records = records

    def __getitem__(self, column: str) -> Any:
        return mock.Mock(sum=lambda: sum(r[column] for r in self.records))

    def to_dict(self, orient: str) -> list[dict[str, Any]]:
        return [dict(r) for r in self.records]


class CliBenchmarkTestCase(unittest.TestCase):
    def setUp(self) -> None:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)

    def write(self, name: str, text: str) -> str:
        (self.root / name).write_text(text, encoding="utf-8")
        return str(self.root / name)

    def command(self, actual: str, expected: str, *extra: str) -> None:
        WordTokenizationBenchmark(
            "word-tokenization",
            [
                "--input-file",
                self.write("sub.txt", actual),
                "--test-file",
                self.write("ref.txt", expected),
                *extra,
            ],
        )

    def test_read_file(self) -> None:
        # Regression: a lazy generator read the file after it was closed.
        path = self.write("a.txt", " ก|ข \nค\n\n  \n")
        self.assertEqual(_read_file(path), ["ก|ข", "ค", "", ""])
        with self.assertRaises(FileNotFoundError):
            _read_file(str(self.root / "missing.txt"))

    def test_app(self) -> None:
        cases = [
            (
                ["Word-Tokenization", "--x", "1"],
                ("word-tokenization", ["--x", "1"]),
            ),
            (["unknown"], None),
        ]
        for argv, call in cases:
            with self.subTest(argv=argv):
                with mock.patch.object(
                    benchmark, "WordTokenizationBenchmark"
                ) as command:
                    App(["thainlp", "benchmark", *argv])
                if call is None:
                    command.assert_not_called()
                else:
                    command.assert_called_once_with(*call)

    def test_app_without_task(self) -> None:
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            for argv in (
                ["thainlp", "benchmark", ""],
                ["thainlp", "benchmark"],
            ):
                with self.subTest(argv=argv):
                    with self.assertRaises((ArgumentError, SystemExit)):
                        App(argv)

    def test_run(self) -> None:
        fake_yaml = types.ModuleType("yaml")
        fake_yaml.dump = lambda data, f, **kw: f.write(json.dumps(data))  # type: ignore[attr-defined]
        frame = _FakeFrame([dict(_RECORD), dict(_RECORD)])
        out = io.StringIO()
        with ExitStack() as stack:
            stack.enter_context(
                mock.patch.dict(sys.modules, {"yaml": fake_yaml})
            )
            bench = stack.enter_context(
                mock.patch.object(
                    word_tokenization, "benchmark", return_value=frame
                )
            )
            stack.enter_context(redirect_stdout(out))
            self.command("ก|ข\nค\n", "ก|ข\nค\n")
            self.assertEqual(
                sorted(p.name for p in self.root.iterdir()),
                ["ref.txt", "sub.txt"],
            )
            self.command("ก|ข\nค\n", "ก|ข\nค\n", "--save-details")
        bench.assert_called_with(["ก|ข", "ค"], ["ก|ข", "ค"])
        output = out.getvalue()
        # tp=16 fp=4 fn=4: char precision = recall = 0.8; words 6/8 and 6/12
        for text in (
            "with 2 samples in total",
            "char_level:precision 0.8000",
            "char_level:recall 0.8000",
            "word_level:precision 0.7500",
            "word_level:recall 0.5000",
            "eval-sub.yml",
            "eval-details-sub.json",
        ):
            self.assertIn(text, output)
        details = json.loads(
            (self.root / "eval-details-sub.json").read_text(encoding="utf-8")
        )
        self.assertEqual([s["id"] for s in details["samples"]], [0, 1])
        self.assertEqual(details["samples"][0]["expected"], "ก|ข")
        self.assertNotIn("expected", details["samples"][0]["metrics"])
        self.assertEqual(details["metrics"]["char_level:tp"], 16.0)
        self.assertTrue((self.root / "eval-sub.yml").exists())

    def test_errors(self) -> None:
        with redirect_stdout(io.StringIO()):
            with self.assertRaisesRegex(ValueError, "same number of samples"):
                self.command("ก\n", "ก\nข\n")
            # None in sys.modules makes "import yaml" raise ImportError
            with mock.patch.dict(sys.modules, {"yaml": None}):
                with self.assertRaisesRegex(
                    ImportError, r"pythainlp\[benchmarks\]"
                ):
                    self.command("ก\n", "ก\n")
            with self.assertRaises(TypeError):  # no file arguments
                WordTokenizationBenchmark("word-tokenization", [])


if __name__ == "__main__":
    unittest.main()
