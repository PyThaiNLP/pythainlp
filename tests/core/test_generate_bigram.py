# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""
Characterization tests for pythainlp.generate.core.Bigram.gen_sentence.

Golden cases were recorded from the code before the shared-helper refactor.
The model is a small in-memory fake, so no corpus is loaded or downloaded.
"""

# ruff: noqa: S311  # tests seed and compare the global random generator
from __future__ import annotations

import random
import unittest
from typing import Any

from pythainlp.generate.core import Bigram, _pick_next

# (start_seq, N, prob, output_str, duplicate, random seed, outcome)
# The outcome is ["ok", result] or ["exc", exception name, message].
GOLDEN: list[list[Any]] = [
    ["d", 3, 0.4, True, False, 99, ["ok", "d"]],
    ["a", 0, 0.2, True, False, 60, ["ok", "a"]],
    ["a", 6, 0.001, True, True, 93, ["ok", "acddddd"]],
    ["a", 6, 0.4, True, False, 20, ["ok", "abc"]],
    ["", 1, 2.0, True, True, 0, ["ok", "d"]],
    ["", 1, 0.2, True, True, 37, ["ok", "ca"]],
    ["b", 1, 0.2, True, True, 49, ["ok", "ba"]],
    ["b", 0, 0.4, False, True, 18, ["ok", ["b"]]],
    ["b", 0, 0.4, False, True, 76, ["ok", ["b"]]],
    ["b", 0, 0.4, False, False, 61, ["ok", ["b"]]],
    ["b", 1, 2.0, False, True, 7, ["ok", ["b"]]],
    ["b", 0, 0.4, False, True, 70, ["ok", ["b"]]],
    ["c", 3, 2.0, True, False, 5, ["ok", "c"]],
    ["a", 1, 0.001, True, False, 44, ["ok", "ac"]],
    ["d", 3, 0.4, False, True, 75, ["ok", ["d", "d", "d", "d"]]],
    ["b", 3, 0.001, False, True, 26, ["ok", ["b", "a", "d", "d"]]],
    ["b", 3, 0.2, False, False, 89, ["ok", ["b", "a", "c", "d"]]],
    ["d", 0, 0.4, False, False, 22, ["ok", ["d"]]],
    ["", 1, 0.4, False, True, 92, ["ok", ["d", "d"]]],
    ["", 0, 2.0, True, True, 94, ["ok", "y"]],
    ["d", 3, 0.4, False, False, 18, ["ok", ["d"]]],
    ["", 0, 2.0, False, True, 16, ["ok", ["a"]]],
    ["d", 1, 2.0, True, True, 55, ["ok", "d"]],
    ["b", 1, 0.001, False, False, 18, ["ok", ["b", "a"]]],
    ["c", 1, 2.0, False, False, 61, ["ok", ["c"]]],
    ["b", 3, 2.0, False, True, 14, ["ok", ["b"]]],
    ["c", 1, 2.0, False, True, 11, ["ok", ["c"]]],
    ["c", 3, 0.4, True, False, 88, ["ok", "cab"]],
    ["d", 0, 0.4, False, False, 62, ["ok", ["d"]]],
    ["b", 3, 0.4, True, True, 60, ["ok", "bcab"]],
    ["d", 3, 0.4, False, False, 36, ["ok", ["d"]]],
    ["d", 3, 0.4, False, False, 94, ["ok", ["d"]]],
    ["c", 3, 0.2, False, False, 42, ["ok", ["c", "a", "b"]]],
    ["d", 1, 0.2, True, False, 61, ["ok", "d"]],
    ["b", 0, 2.0, True, False, 38, ["ok", "b"]],
    ["d", 3, 0.001, True, True, 75, ["ok", "dddd"]],
    ["c", 1, 0.2, True, True, 60, ["ok", "cd"]],
    ["a", 1, 0.001, True, True, 40, ["ok", "ac"]],
    ["a", 6, 0.2, True, False, 59, ["ok", "abcd"]],
    ["b", 6, 0.001, True, True, 91, ["ok", "baddddd"]],
    ["q", 1, 0.001, True, False, 3, ["ok", "q"]],
]


def make_model() -> Bigram:
    """Build a Bigram without loading corpora."""
    model = Bigram.__new__(Bigram)
    model.uni = {"a": 10, "b": 6, "c": 4, "d": 2}
    model.bi = {
        ("a", "b"): 5,
        ("a", "c"): 3,
        ("a", "d"): 1,
        ("b", "a"): 2,
        ("b", "c"): 3,
        ("c", "a"): 2,
        ("c", "d"): 1,
        ("d", "d"): 2,
        ("z", "y"): 0,
    }
    model.uni_keys = list(model.uni)
    model.bi_keys = list(model.bi)
    model.words = [i[-1] for i in model.bi_keys]
    return model


class BigramGoldenTestCase(unittest.TestCase):
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
                got = self.model.gen_sentence(
                    start, n, prob, output_str, duplicate
                )
                self.assertEqual(got, expected[1])

    def test_prob_handles_zero_denominator(self) -> None:
        self.model.uni["a"] = 0
        self.assertEqual(self.model.prob("a", "b"), 0.0)

    # BUG-LEDGER: ngram-gen-tie-bias
    def test_bug_equal_probabilities_always_pick_first_candidate(self) -> None:
        """probs.index(random.choice(p2)) ignores ties; expected: random."""
        model = make_model()
        model.uni = {"x": 4, "p": 2, "q": 2}
        model.bi = {("x", "p"): 2, ("x", "q"): 2}
        model.bi_keys = list(model.bi)
        for seed in range(20):
            with self.subTest(seed=seed):
                random.seed(seed)
                self.assertEqual(
                    model.gen_sentence("x", 1, 0.0001, False), ["x", "p"]
                )


class PickNextTestCase(unittest.TestCase):
    def setUp(self) -> None:
        state = random.getstate()
        self.addCleanup(random.setstate, state)

    def test_returns_none_when_no_probability_passes(self) -> None:
        self.assertIsNone(_pick_next(["a", "b"], [0.1, 0.2], 0.5))
        self.assertIsNone(_pick_next([], [], 0.0))

    def test_picks_candidate_that_passes_threshold(self) -> None:
        for seed in range(10):
            random.seed(seed)
            self.assertEqual(_pick_next(["a", "b"], [0.1, 0.9], 0.5), "b")

    def test_consumes_one_random_choice(self) -> None:
        random.seed(7)
        _pick_next(["a", "b", "c"], [0.5, 0.6, 0.7], 0.0)
        after = random.random()  # nosec B311
        random.seed(7)
        random.choice([0.5, 0.6, 0.7])  # nosec B311
        self.assertEqual(random.random(), after)  # nosec B311

    def test_no_random_call_when_nothing_passes(self) -> None:
        random.seed(7)
        _pick_next(["a"], [0.1], 0.5)
        after = random.random()  # nosec B311
        random.seed(7)
        self.assertEqual(random.random(), after)


if __name__ == "__main__":
    unittest.main()
