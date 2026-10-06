# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Characterization tests for pythainlp.generate.core gen_sentence methods.

Golden cases were recorded from the code before the complexity refactor.
The model is a small in-memory fake, so no corpus is loaded or downloaded.
"""

from __future__ import annotations

import random
import unittest
from typing import Any

from pythainlp.generate.core import Bigram, Trigram

BIGRAMS: dict[tuple[str, str], int] = {
    ("a", "b"): 4,
    ("b", "c"): 3,
    ("b", "d"): 1,
    ("c", "a"): 2,
    ("a", "c"): 2,
    ("d", "a"): 1,
    ("z", "y"): 0,
    ("c", "c"): 1,
}
TRIGRAMS: dict[tuple[str, str, str], int] = {
    ("a", "b", "c"): 2,
    ("a", "b", "d"): 1,
    ("b", "c", "a"): 2,
    ("c", "a", "b"): 1,
    ("b", "d", "a"): 1,
    ("a", "c", "a"): 1,
    ("d", "a", "b"): 1,
    ("c", "a", "c"): 1,
    ("z", "y", "a"): 1,
    ("q", "r", "s"): 1,
    ("c", "c", "c"): 1,
    ("a", "c", "c"): 1,
    ("c", "c", "a"): 1,
}


def make_model() -> Trigram:
    """Build a Trigram without loading corpora."""
    model = Trigram.__new__(Trigram)
    model.uni = {"a": 5, "b": 4, "c": 3, "d": 1}
    model.bi = dict(BIGRAMS)
    model.ti = dict(TRIGRAMS)
    model.uni_keys = list(model.uni)
    model.bi_keys = list(model.bi)
    model.ti_keys = list(model.ti)
    model.words = [i[-1] for i in model.bi_keys]
    return model


# (start_seq, N, prob, output_str, duplicate, random seed, outcome)
# The outcome is ["ok", result] or ["exc", exception name, message].
GOLDEN: list[list[Any]] = [
    ["", 0, 0.001, True, False, 30, ["ok", "ac"]],
    ["", 0, 0.001, False, False, 75, ["ok", ["c"]]],
    ["", 1, 0.001, True, False, 60, ["ok", "ac"]],
    ["", 1, 2.0, True, False, 77, ["ok", "ac"]],
    ["", 3, 2.0, True, False, 24, ["ok", "zy"]],
    ["", 1, 0.001, True, True, 94, ["ok", "bda"]],
    [("a", "b"), 0, 0.001, True, False, 54, ["ok", "ab"]],
    [("q", "r"), 1, 0.001, True, False, 43, ["exc", "KeyError", "('q', 'r')"]],
    ["a", 0, 0.001, True, False, 69, ["ok", "a"]],
    [("c", "a"), 3, 0.001, True, True, 17, ["ok", "cabd"]],
    [None, 6, 0.5, False, False, 48, ["ok", ["d", "a", "b", "c"]]],
    ["", 3, 0.001, False, False, 33, ["ok", ["b", "d", "a", "c"]]],
    [(), 6, 0.5, False, False, 7, ["ok", ["d", "a", "b", "c"]]],
    [None, 6, 0.001, True, True, 84, ["ok", "acbd"]],
    [("a", "b"), 6, 0.001, True, True, 91, ["ok", "abcd"]],
    [("c", "c"), 6, 0.001, False, False, 48, ["ok", ["c", "a", "b", "d"]]],
    [(), 6, 0.001, True, True, 53, ["ok", "cabd"]],
    ["", 6, 0.001, False, True, 60, ["ok", ["a", "c", "b", "d"]]],
    ["", 3, 0.001, True, True, 97, ["ok", "cabd"]],
    [("b", "c"), 6, 0.001, True, False, 77, ["ok", "bcad"]],
    [("c", "a"), 3, 0.001, True, False, 79, ["ok", "cabd"]],
    [(), 3, 0.5, True, True, 76, ["ok", "dabc"]],
    [("b", "c"), 6, 0.001, False, False, 78, ["ok", ["b", "c", "a", "d"]]],
    [("c", "a"), 6, 0.001, True, True, 45, ["ok", "cabd"]],
    [None, 6, 0.001, False, True, 48, ["ok", ["d", "a", "b", "c"]]],
    [("c", "a"), 6, 0.001, False, True, 86, ["ok", ["c", "a", "b", "d"]]],
    [(), 6, 0.001, False, True, 10, ["ok", ["a", "b", "d", "c"]]],
    ["", 3, 0.001, True, False, 60, ["ok", "acbd"]],
    ["", 6, 0.5, True, True, 76, ["ok", "dabc"]],
    [None, 3, 0.001, False, True, 5, ["ok", ["a", "c", "b", "d"]]],
    ["", 6, 0.001, True, True, 34, ["ok", "dabc"]],
    ["", 6, 0.001, True, False, 60, ["ok", "acbd"]],
    [("b", "c"), 6, 0.001, False, True, 19, ["ok", ["b", "c", "a", "d"]]],
    [None, 3, 0.001, False, False, 33, ["ok", ["b", "d", "a", "c"]]],
    [(), 3, 0.001, False, False, 67, ["ok", ["b", "c", "a", "d"]]],
    [("b", "c"), 3, 0.001, False, False, 54, ["ok", ["b", "c", "a", "d"]]],
    [(), 6, 0.001, True, False, 95, ["ok", "bdac"]],
    [
        ("q", "r"),
        1,
        0.001,
        False,
        False,
        94,
        ["exc", "KeyError", "('q', 'r')"],
    ],
    [("q", "r"), 1, 0.5, True, False, 83, ["exc", "KeyError", "('q', 'r')"]],
    [("q", "r"), 1, 0.5, False, False, 27, ["exc", "KeyError", "('q', 'r')"]],
]


def make_bigram_model() -> Bigram:
    """Build a Bigram with two equally likely successors of "x"."""
    model = Bigram.__new__(Bigram)
    model.uni = {"x": 4, "p": 2, "q": 2}
    model.bi = {("x", "p"): 2, ("x", "q"): 2}
    model.uni_keys = list(model.uni)
    model.bi_keys = list(model.bi)
    model.words = [i[-1] for i in model.bi_keys]
    return model


class TrigramGenSentenceTestCase(unittest.TestCase):
    def setUp(self) -> None:
        # The tests seed the global random generator; restore its state.
        state = random.getstate()
        self.addCleanup(random.setstate, state)
        self.model = make_model()

    def test_golden_cases(self) -> None:
        for start, n, prob, output_str, duplicate, seed, expected in GOLDEN:
            with self.subTest(
                start=start, n=n, prob=prob, str=output_str, dup=duplicate
            ):
                random.seed(seed)
                if expected[0] == "exc":
                    with self.assertRaises(KeyError) as ctx:
                        self.model.gen_sentence(
                            start, n, prob, output_str, duplicate
                        )
                    self.assertEqual(str(ctx.exception), expected[2])
                    continue
                got = self.model.gen_sentence(
                    start, n, prob, output_str, duplicate
                )
                self.assertEqual(got, expected[1])

    def test_prob_handles_zero_denominator(self) -> None:
        self.assertEqual(self.model.prob("z", "y", "a"), 0.0)

    def test_stops_when_no_candidate_passes_threshold(self) -> None:
        random.seed(0)
        self.assertEqual(
            self.model.gen_sentence(("a", "b"), 5, 2.0, False), ["a", "b"]
        )

    def test_output_is_a_string_by_default(self) -> None:
        random.seed(0)
        result = self.model.gen_sentence(("a", "b"), 0)
        self.assertEqual(result, "ab")

    # BUG-LEDGER: ngram-gen-tie-bias
    def test_bug_equal_probabilities_always_pick_first_candidate(self) -> None:
        """``probs.index(random.choice(p2))`` ignores ties; expected: random."""
        for seed in range(20):
            with self.subTest(seed=seed):
                random.seed(seed)
                self.assertEqual(
                    self.model.gen_sentence(("a", "c"), 2, 0.0001, False),
                    ["a", "c", "b"],
                )

    # BUG-LEDGER: ngram-gen-flatten-dedup
    def test_bug_repeated_words_are_dropped_from_output(self) -> None:
        """``duplicate=True`` has no effect on output; expected: keep words."""
        for seed in range(5):
            with self.subTest(seed=seed):
                random.seed(seed)
                words = self.model.gen_sentence(
                    ("c", "c"), 4, 0.0001, False, True
                )
                self.assertEqual(words, ["c"])

    def test_start_item_of_other_type_is_skipped(self) -> None:
        self.assertEqual(
            self.model.gen_sentence(["a", "b"], 1, 0.0001, False),  # type: ignore[arg-type]
            [],
        )
        self.assertEqual(
            self.model.gen_sentence((1, 2), 0, 0.0001, False),  # type: ignore[arg-type]
            [1, 2],
        )

    def test_unknown_bigram_raises_key_error(self) -> None:
        with self.assertRaises(KeyError):
            self.model.gen_sentence(("q", "r"), 1)

    def test_string_start_sequence_matches_no_trigram(self) -> None:
        self.assertEqual(self.model.gen_sentence("a", 3, 0.0001, False), ["a"])


class BigramGenSentenceTestCase(unittest.TestCase):
    def setUp(self) -> None:
        state = random.getstate()
        self.addCleanup(random.setstate, state)
        self.model = make_bigram_model()

    # BUG-LEDGER: ngram-gen-tie-bias
    def test_bug_equal_probabilities_always_pick_first_candidate(self) -> None:
        """``probs.index(random.choice(p2))`` ignores ties; expected: random."""
        for seed in range(20):
            with self.subTest(seed=seed):
                random.seed(seed)
                self.assertEqual(
                    self.model.gen_sentence("x", 1, 0.0001, False),
                    ["x", "p"],
                )


if __name__ == "__main__":
    unittest.main()
