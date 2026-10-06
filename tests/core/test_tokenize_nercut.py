# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Characterization tests for pythainlp.tokenize.nercut.

Golden data were recorded from the implementation before its refactor.
A fake tagger replaces the NER engine. The module is imported with a fake
``NER`` class, because importing it builds the real ThaiNER model.
"""

import importlib
import importlib.util
import unittest
from pathlib import Path
from typing import Any
from unittest import mock

import pythainlp


def _import_nercut() -> Any:
    """Load nercut.py under a private name with a fake NER.

    Neither ``sys.modules`` nor the ``pythainlp.tokenize`` package
    attribute is changed.
    """
    named_entity = importlib.import_module("pythainlp.tag.named_entity")
    path = Path(pythainlp.__file__).parent / "tokenize" / "nercut.py"
    spec = importlib.util.spec_from_file_location("nercut_under_test", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    with mock.patch.object(named_entity, "NER", mock.MagicMock()):
        spec.loader.exec_module(module)
    return module


nercut = _import_nercut()

# Each case: [(word, tag), ...], taglist, expected outcome.
_GOLDEN: list[list[Any]] = [
    [
        [
            ["c", "I-DATE"],
            ["a", "B-PERSON"],
            ["b", "B-DATE"],
            ["a", "I-PERSON"],
            ["b", "I-LOCATION"],
            ["c", "I-X"],
            ["c", "B-DATE"],
            ["d", "O"],
        ],
        ["PERSON", "DATE"],
        ["ok", ["c", "b", "c", "c", "d"]],
    ],
    [
        [
            ["a", "B-LOCATION"],
            ["a", "I-LOCATION"],
            ["d", "B-PERSON"],
            ["a", "B-PERSON"],
            ["c", "B-PERSON"],
            ["d", "B-DATE"],
            ["d", "I-X"],
            ["a", "B-PERSON"],
        ],
        ["PERSON"],
        ["ok", ["a", "a", "d", "d", "a"]],
    ],
    [
        [
            ["c", "I-LOCATION"],
            ["b", "I-DATE"],
            ["b", "B-LOCATION"],
            ["c", "I-LOCATION"],
        ],
        ["DATE", "LOCATION"],
        ["ok", ["c", "b", "bc"]],
    ],
    [
        [
            ["c", "I-DATE"],
            ["c", "I-DATE"],
            ["b", "I-LOCATION"],
            ["b", "B-PERSON"],
        ],
        ["PERSON"],
        ["ok", ["c", "c", "b", "b"]],
    ],
    [
        [
            ["d", "I-DATE"],
            ["c", "O"],
            ["c", "B-PERSON"],
            ["c", "B-PERSON"],
            ["c", "I-PERSON"],
            ["d", "I-DATE"],
        ],
        ["PERSON", "DATE"],
        ["ok", ["d", "c", "ccd"]],
    ],
    [[], [], ["ok", []]],
    [
        [["d", "I-PERSON"], ["d", "B-X"], ["d", "B-LOCATION"]],
        ["DATE", "LOCATION"],
        ["ok", ["d", "d", "d"]],
    ],
    [[], [], ["ok", []]],
    [
        [
            ["b", "B-X"],
            ["d", "I-PERSON"],
            ["d", "I-PERSON"],
            ["c", "I-LOCATION"],
            ["a", "B-LOCATION"],
            ["a", "B-LOCATION"],
        ],
        ["PERSON"],
        ["ok", ["b", "d", "d", "c", "a", "a"]],
    ],
    [
        [["a", "B-LOCATION"], ["d", "B-DATE"], ["b", "B-X"], ["b", "I-DATE"]],
        ["DATE", "LOCATION"],
        ["ok", ["b", "b"]],
    ],
    [[["d", "B-X"]], ["PERSON", "DATE"], ["ok", ["d"]]],
    [[["c", "O"]], ["DATE", "LOCATION"], ["ok", ["c"]]],
    [[["b", "I-LOCATION"]], ["DATE", "LOCATION"], ["ok", ["b"]]],
    [[["b", "I-PERSON"], ["c", "I-LOCATION"]], ["PERSON"], ["ok", ["b", "c"]]],
    [
        [
            ["a", "B-LOCATION"],
            ["b", "O"],
            ["d", "I-DATE"],
            ["c", "I-LOCATION"],
            ["a", "B-X"],
            ["a", "B-DATE"],
            ["b", "I-LOCATION"],
            ["c", "I-DATE"],
        ],
        ["PERSON"],
        ["ok", ["a", "b", "d", "c", "a", "a", "b", "c"]],
    ],
    [[["b", "B-X"]], [], ["ok", ["b"]]],
    [
        [
            ["b", "I-LOCATION"],
            ["a", "O"],
            ["a", "B-LOCATION"],
            ["d", "B-DATE"],
            ["d", "B-LOCATION"],
            ["d", "I-PERSON"],
        ],
        [],
        ["ok", ["b", "a", "a", "d", "d", "d"]],
    ],
    [
        [
            ["a", "O"],
            ["c", "I-DATE"],
            ["b", "B-LOCATION"],
            ["c", "O"],
            ["a", "I-DATE"],
            ["d", "I-X"],
            ["b", "I-LOCATION"],
        ],
        ["PERSON"],
        ["ok", ["a", "c", "b", "c", "a", "d", "b"]],
    ],
    [[["c", "I-DATE"]], ["PERSON", "DATE"], ["ok", ["c"]]],
    [[["d", "B-DATE"]], ["DATE", "LOCATION"], ["ok", ["d"]]],
    [
        [
            ["d", "I-DATE"],
            ["b", "I-X"],
            ["c", "I-X"],
            ["b", "I-X"],
            ["a", "O"],
            ["d", "B-PERSON"],
            ["a", "O"],
        ],
        ["DATE", "LOCATION"],
        ["ok", ["d", "b", "c", "b", "a", "d", "a"]],
    ],
    [[["b", "B-PERSON"]], ["PERSON", "DATE"], ["ok", ["b"]]],
    [
        [
            ["a", "B-LOCATION"],
            ["a", "O"],
            ["d", "I-PERSON"],
            ["a", "I-DATE"],
            ["b", "I-DATE"],
        ],
        ["DATE", "LOCATION"],
        ["ok", ["a", "a", "d", "a", "b"]],
    ],
    [[["b", "O"], ["a", "O"]], ["DATE", "LOCATION"], ["ok", ["b", "a"]]],
    [
        [
            ["c", "I-LOCATION"],
            ["a", "I-DATE"],
            ["b", "I-LOCATION"],
            ["b", "O"],
            ["d", "B-PERSON"],
            ["a", "I-DATE"],
        ],
        ["PERSON", "DATE"],
        ["ok", ["c", "a", "b", "b", "da"]],
    ],
    [
        [["c", "I-X"], ["b", "B-DATE"], ["b", "B-PERSON"], ["d", "B-DATE"]],
        ["DATE", "LOCATION"],
        ["ok", ["c", "b", "d"]],
    ],
    [
        [["d", "I-DATE"], ["a", "B-LOCATION"], ["c", "B-DATE"]],
        ["PERSON"],
        ["ok", ["d", "a", "c"]],
    ],
    [
        [
            ["c", "I-DATE"],
            ["a", "B-LOCATION"],
            ["b", "B-PERSON"],
            ["c", "B-PERSON"],
        ],
        [],
        ["ok", ["c", "a", "b", "c"]],
    ],
]


class _FakeTagger:
    def __init__(self, tagged: list[Any]) -> None:
        self.tagged = tagged

    def tag(self, text: str, pos: bool = False) -> list[Any]:
        return self.tagged


def _segment(tagged: list[Any], taglist: list[str]) -> list[str]:
    tagger: Any = _FakeTagger([tuple(item) for item in tagged])
    result: list[str] = nercut.segment("x", taglist=taglist, tagger=tagger)
    return result


class NercutGoldenTestCase(unittest.TestCase):
    def test_segment_golden(self):
        for tagged, taglist, expected in _GOLDEN:
            with self.subTest(tagged=tagged, taglist=taglist):
                self.assertEqual(expected[0], "ok")
                self.assertEqual(_segment(tagged, taglist), expected[1])

    def test_empty_text(self):
        self.assertEqual(nercut.segment(""), [])

    def test_taglist_is_iterable(self):
        tagged = [("a", "B-PERSON"), ("b", "I-PERSON"), ("c", "O")]
        for taglist in (["PERSON"], ("PERSON",), {"PERSON"}):
            with self.subTest(taglist=taglist):
                tagger: Any = _FakeTagger(tagged)
                self.assertEqual(
                    nercut.segment("x", taglist=taglist, tagger=tagger),
                    ["ab", "c"],
                )

    def test_combined_word_dropped(self):
        # BUG-LEDGER: nercut-combined-word-dropped
        # A pending entity is lost when the next token starts a new entity
        # or has a tag outside taglist. Expected: "a" and "b" are kept.
        self.assertEqual(
            _segment([("a", "B-PERSON"), ("b", "B-PERSON")], ["PERSON"]),
            ["b"],
        )
        self.assertEqual(
            _segment([("a", "B-PERSON"), ("b", "B-X")], ["PERSON"]),
            ["b"],
        )


if __name__ == "__main__":
    unittest.main()
