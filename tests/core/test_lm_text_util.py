# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Characterization tests for pythainlp.lm.text_util.remove_repeated_ngrams.

Golden cases were recorded from the code before the complexity refactor.
"""

from __future__ import annotations

import unittest
from typing import Any

from pythainlp.lm import calculate_ngram_counts, remove_repeated_ngrams

# (word list, n, outcome)
# The outcome is ["ok", result] or ["exc", exception name, message].
GOLDEN: list[list[Any]] = [
    [["เอา", "เอา", "แบบ", "ไหน"], 1, ["ok", ["เอา", "แบบ", "ไหน"]]],
    [[], 2, ["ok", []]],
    [["a"], 2, ["ok", ["a"]]],
    [["a", "b", "a", "b"], 2, ["ok", ["a", "b", "a", "b"]]],
    [["a", "a", "a"], 2, ["ok", ["a", "a"]]],
    [
        ["a", "b", "c", "a", "b", "c"],
        3,
        ["ok", ["a", "b", "c", "a", "b", "c"]],
    ],
    [["a", "b"], 0, ["ok", ["a", "b"]]],
    [["a", "b"], -1, ["ok", ["a", "b"]]],
    [["a", "b", "a"], 1, ["ok", ["a", "b"]]],
    [["a", "b", "c"], 5, ["ok", ["a", "b", "c", "b", "c"]]],
    [["a", "a", "b", "b"], 2, ["ok", ["a", "a", "b", "b"]]],
    [None, 2, ["ok", None]],
    ["abc", 2, ["ok", ["a", "b", "c"]]],
    [
        ["a", "b"],
        None,
        [
            "exc",
            "TypeError",
            "'<=' not supported between instances of 'NoneType' and 'int'",
        ],
    ],
    [
        ["a", "b"],
        "2",
        [
            "exc",
            "TypeError",
            "'<=' not supported between instances of 'str' and 'int'",
        ],
    ],
    [
        ["a", "b", "c", "d"],
        4,
        ["ok", ["a", "b", "c", "d", "b", "c", "d", "c", "d"]],
    ],
    [["a", "b", "a", "c"], 2, ["ok", ["a", "b", "a", "c"]]],
    [["x", "x", "x", "x", "x", "x", "x", "x"], 3, ["ok", ["x", "x", "x"]]],
    [
        ["c", "b", "b", "c", "c", "a", "a"],
        3,
        ["ok", ["c", "b", "b", "c", "c", "a", "a"]],
    ],
    [
        ["c", "c", "a", "a", "b", "b", "a"],
        -1,
        ["ok", ["c", "c", "a", "a", "b", "b", "a"]],
    ],
    [
        ["c", "c", "a", "c", "b", "b", "c", "c"],
        3,
        ["ok", ["c", "c", "a", "c", "b", "b", "c", "c"]],
    ],
    [["c", "a"], 3, ["ok", ["c", "a"]]],
    [["a"], -1, ["ok", ["a"]]],
    [["a", "c", "a"], 2, ["ok", ["a", "c", "a"]]],
    [
        ["b", "c", "a", "c", "a"],
        4,
        ["ok", ["b", "c", "a", "c", "a", "c", "a", "c", "a"]],
    ],
    [["b", "a", "c", "a"], 2, ["ok", ["b", "a", "c", "a"]]],
    [["b", "c", "a", "c"], 1, ["ok", ["b", "c", "a"]]],
    [["a", "c", "b", "a", "a"], 3, ["ok", ["a", "c", "b", "a", "a"]]],
    [["b"], -1, ["ok", ["b"]]],
    [["b", "a", "a", "c"], -1, ["ok", ["b", "a", "a", "c"]]],
    [["a", "a", "b"], 2, ["ok", ["a", "a", "b"]]],
    [["b", "a", "c", "c", "a", "c"], 1, ["ok", ["b", "a", "c"]]],
    [["a", "b", "b", "a", "b"], -1, ["ok", ["a", "b", "b", "a", "b"]]],
    [["a", "c"], -1, ["ok", ["a", "c"]]],
    [[], -1, ["ok", []]],
    [
        ["b", "a", "c", "c", "a", "b", "c"],
        0,
        ["ok", ["b", "a", "c", "c", "a", "b", "c"]],
    ],
    [["b", "c"], 2, ["ok", ["b", "c"]]],
    [["b"], 2, ["ok", ["b"]]],
    [["a", "b", "c"], 1, ["ok", ["a", "b", "c"]]],
    [[], 0, ["ok", []]],
    [["b", "c"], 4, ["ok", ["b", "c"]]],
    [
        ["a", "a", "a", "a", "b", "b", "a", "c", "b"],
        1,
        ["ok", ["a", "b", "c"]],
    ],
    [
        ["a", "a", "a", "a", "c", "c"],
        0,
        ["ok", ["a", "a", "a", "a", "c", "c"]],
    ],
]


class RemoveRepeatedNgramsTestCase(unittest.TestCase):
    def test_golden_cases(self) -> None:
        for words, n, expected in GOLDEN:
            with self.subTest(words=words, n=n):
                arg = list(words) if isinstance(words, list) else words
                if expected[0] == "exc":
                    with self.assertRaises(TypeError) as ctx:
                        remove_repeated_ngrams(arg, n)
                    self.assertEqual(str(ctx.exception), expected[2])
                    continue
                self.assertEqual(remove_repeated_ngrams(arg, n), expected[1])

    def test_calculate_ngram_counts(self) -> None:
        self.assertEqual(calculate_ngram_counts([]), {})
        self.assertEqual(
            calculate_ngram_counts(["a", "b", "a", "b"], 2, 3),
            {
                ("a", "b"): 2,
                ("b", "a"): 1,
                ("a", "b", "a"): 1,
                ("b", "a", "b"): 1,
            },
        )

    def test_docstring_example(self) -> None:
        self.assertEqual(
            remove_repeated_ngrams(["เอา", "เอา", "แบบ", "ไหน"], n=1),
            ["เอา", "แบบ", "ไหน"],
        )

    def test_empty_and_non_positive_n_return_input(self) -> None:
        words = ["a", "b"]
        self.assertIs(remove_repeated_ngrams(words, 0), words)
        self.assertIs(remove_repeated_ngrams(words, -1), words)
        empty: list[str] = []
        self.assertIs(remove_repeated_ngrams(empty), empty)

    # BUG-LEDGER: remove-repeated-ngrams-zero
    def test_bug_unigram_slice_zero_returns_whole_list(self) -> None:
        """For n=1 the slice is ``[-0:]``, the whole list, not ``[]``.

        The output is the same as the intended one, because for a unigram
        both branches add the same word. Expected: slice ``[len - (n - 1):]``.
        """
        self.assertEqual(
            remove_repeated_ngrams(["a", "b", "a", "c"], 1), ["a", "b", "c"]
        )

    # BUG-LEDGER: remove-repeated-ngrams-tail
    def test_bug_n_longer_than_list_repeats_words(self) -> None:
        """Tail words are re-added after the last n-gram; expected: no repeat."""
        self.assertEqual(
            remove_repeated_ngrams(["a", "b", "c"], 5),
            ["a", "b", "c", "b", "c"],
        )


if __name__ == "__main__":
    unittest.main()
