# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Characterization tests for pythainlp.benchmarks.metrics.bleu_score.

Golden cases were recorded from the code before the complexity refactor.
Tokenization is replaced with a whitespace split so that the cases depend
only on the scoring code.
"""

from __future__ import annotations

import builtins
import hashlib
import random
import re
import unittest
from typing import Any
from unittest import mock

from pythainlp.benchmarks import bleu_score


def _split(
    text: str, engine: str = "newmm", keep_whitespace: bool = True
) -> list[str]:
    return text.split()


# (references, hypotheses, keyword arguments, expected outcome)
# The outcome is ["ok", score dict] or ["exc", exception name, message].
GOLDEN: list[list[Any]] = [
    [
        ["a b c d e"],
        ["a b c d e"],
        {},
        [
            "ok",
            {
                "bleu": 100.0,
                "precisions": [1.0, 1.0, 1.0, 1.0],
                "bp": 1.0,
                "length_ratio": 1.0,
                "hyp_length": 5,
                "ref_length": 5,
            },
        ],
    ],
    [
        ["a b c d"],
        ["a b c d"],
        {"smooth": False},
        [
            "ok",
            {
                "bleu": 100.0,
                "precisions": [1.0, 1.0, 1.0, 1.0],
                "bp": 1.0,
                "length_ratio": 1.0,
                "hyp_length": 4,
                "ref_length": 4,
            },
        ],
    ],
    [
        ["a b c d e f"],
        ["a b c"],
        {},
        [
            "ok",
            {
                "bleu": 0.0,
                "precisions": [1.0, 1.0, 1.0, 0.0],
                "bp": 0.36787944117144233,
                "length_ratio": 0.5,
                "hyp_length": 3,
                "ref_length": 6,
            },
        ],
    ],
    [
        ["a b c"],
        ["a b c d e f"],
        {},
        [
            "ok",
            {
                "bleu": 30.21375397356768,
                "precisions": [0.5, 0.4, 0.25, 0.16666666666666666],
                "bp": 1.0,
                "length_ratio": 2.0,
                "hyp_length": 6,
                "ref_length": 3,
            },
        ],
    ],
    [
        [["a b c", "a b d"], ["x y z w"]],
        ["a b c", "x y z q"],
        {},
        [
            "ok",
            {
                "bleu": 69.1441569283882,
                "precisions": [
                    0.8571428571428571,
                    0.8,
                    0.6666666666666666,
                    0.5,
                ],
                "bp": 1.0,
                "length_ratio": 1.0,
                "hyp_length": 7,
                "ref_length": 7,
            },
        ],
    ],
    [
        ["a b c d"],
        ["a b x d"],
        {"smooth": False},
        [
            "ok",
            {
                "bleu": 0.0,
                "precisions": [0.75, 0.3333333333333333, 0.0, 0.0],
                "bp": 1.0,
                "length_ratio": 1.0,
                "hyp_length": 4,
                "ref_length": 4,
            },
        ],
    ],
    [
        ["a b c d"],
        ["a b x d"],
        {"smooth": True},
        [
            "ok",
            {
                "bleu": 42.044820762685724,
                "precisions": [0.75, 0.3333333333333333, 0.25, 0.5],
                "bp": 1.0,
                "length_ratio": 1.0,
                "hyp_length": 4,
                "ref_length": 4,
            },
        ],
    ],
    [
        ["a b c d"],
        ["x y z w"],
        {"smooth": False},
        [
            "ok",
            {
                "bleu": 0.0,
                "precisions": [0.0, 0.0, 0.0, 0.0],
                "bp": 1.0,
                "length_ratio": 1.0,
                "hyp_length": 4,
                "ref_length": 4,
            },
        ],
    ],
    [
        ["A B c d"],
        ["a b C D"],
        {"lowercase": True},
        [
            "ok",
            {
                "bleu": 100.0,
                "precisions": [1.0, 1.0, 1.0, 1.0],
                "bp": 1.0,
                "length_ratio": 1.0,
                "hyp_length": 4,
                "ref_length": 4,
            },
        ],
    ],
    [
        ["A B c d"],
        ["a b C D"],
        {"lowercase": False},
        [
            "ok",
            {
                "bleu": 22.59005009024612,
                "precisions": [0.125, 0.16666666666666666, 0.25, 0.5],
                "bp": 1.0,
                "length_ratio": 1.0,
                "hyp_length": 4,
                "ref_length": 4,
            },
        ],
    ],
    [
        ["a b c d"],
        ["a b c d"],
        {"max_ngram": 1},
        [
            "ok",
            {
                "bleu": 100.0,
                "precisions": [1.0],
                "bp": 1.0,
                "length_ratio": 1.0,
                "hyp_length": 4,
                "ref_length": 4,
            },
        ],
    ],
    [
        ["a b c d"],
        ["a b c d"],
        {"max_ngram": 2},
        [
            "ok",
            {
                "bleu": 100.0,
                "precisions": [1.0, 1.0],
                "bp": 1.0,
                "length_ratio": 1.0,
                "hyp_length": 4,
                "ref_length": 4,
            },
        ],
    ],
    [
        ["a b c d"],
        ["a b c d"],
        {"max_ngram": 6},
        [
            "ok",
            {
                "bleu": 0.0,
                "precisions": [1.0, 1.0, 1.0, 1.0, 0.0, 0.0],
                "bp": 1.0,
                "length_ratio": 1.0,
                "hyp_length": 4,
                "ref_length": 4,
            },
        ],
    ],
    [
        ["a b c d"],
        ["a b c d"],
        {"max_ngram": 0},
        ["exc", "ZeroDivisionError", "division by zero"],
    ],
    [
        [],
        [],
        {},
        [
            "ok",
            {
                "bleu": 0.0,
                "precisions": [0.0, 0.0, 0.0, 0.0],
                "bp": 1.0,
                "length_ratio": 0.0,
                "hyp_length": 0,
                "ref_length": 0,
            },
        ],
    ],
    [
        ["a b"],
        [],
        {},
        [
            "exc",
            "ValueError",
            "The number of references (1) and hypotheses (0) must be equal.",
        ],
    ],
    [
        [],
        ["a b"],
        {},
        [
            "exc",
            "ValueError",
            "The number of references (0) and hypotheses (1) must be equal.",
        ],
    ],
    [
        ["a b"],
        [""],
        {},
        [
            "ok",
            {
                "bleu": 0.0,
                "precisions": [0.0, 0.0, 0.0, 0.0],
                "bp": 0.0,
                "length_ratio": 0.0,
                "hyp_length": 0,
                "ref_length": 2,
            },
        ],
    ],
    [
        [""],
        ["a b"],
        {},
        [
            "ok",
            {
                "bleu": 0.0,
                "precisions": [0.25, 0.5, 0.0, 0.0],
                "bp": 1.0,
                "length_ratio": 0.0,
                "hyp_length": 2,
                "ref_length": 0,
            },
        ],
    ],
    [
        [""],
        [""],
        {},
        [
            "ok",
            {
                "bleu": 0.0,
                "precisions": [0.0, 0.0, 0.0, 0.0],
                "bp": 1.0,
                "length_ratio": 0.0,
                "hyp_length": 0,
                "ref_length": 0,
            },
        ],
    ],
    [
        ["a b c", "d e f"],
        ["a b c"],
        {},
        [
            "exc",
            "ValueError",
            "The number of references (2) and hypotheses (1) must be equal.",
        ],
    ],
    [
        ["a b c"],
        ["a b c", "d e f"],
        {},
        [
            "exc",
            "ValueError",
            "The number of references (1) and hypotheses (2) must be equal.",
        ],
    ],
    [
        [[]],
        ["a b"],
        {},
        ["exc", "ValueError", "min() iterable argument is empty"],
    ],
    [
        [["a b", "a b c d e"]],
        ["a b c"],
        {},
        [
            "ok",
            {
                "bleu": 0.0,
                "precisions": [1.0, 1.0, 1.0, 0.0],
                "bp": 1.0,
                "length_ratio": 1.5,
                "hyp_length": 3,
                "ref_length": 2,
            },
        ],
    ],
    [
        ["a a a a a"],
        ["a a a a a a"],
        {},
        [
            "ok",
            {
                "bleu": 75.98356856515926,
                "precisions": [
                    0.8333333333333334,
                    0.8,
                    0.75,
                    0.6666666666666666,
                ],
                "bp": 1.0,
                "length_ratio": 1.2,
                "hyp_length": 6,
                "ref_length": 5,
            },
        ],
    ],
    [
        ["a b c d", "a b"],
        ["a b c d", "a b"],
        {"smooth": False},
        [
            "ok",
            {
                "bleu": 100.0,
                "precisions": [1.0, 1.0, 1.0, 1.0],
                "bp": 1.0,
                "length_ratio": 1.0,
                "hyp_length": 6,
                "ref_length": 6,
            },
        ],
    ],
    [
        ["B a a A a c", ""],
        ["a a d", "a b a A d a"],
        {"max_ngram": 4, "smooth": True, "lowercase": True},
        [
            "ok",
            {
                "bleu": 15.166471346826793,
                "precisions": [
                    0.2222222222222222,
                    0.14285714285714285,
                    0.1,
                    0.16666666666666666,
                ],
                "bp": 1.0,
                "length_ratio": 1.5,
                "hyp_length": 9,
                "ref_length": 6,
            },
        ],
    ],
    [
        [
            ["c b B"],
            ["d d a b d d"],
            ["b d A c", "c B d b b a", "b b"],
            ["a d A", "c c", ""],
        ],
        ["d A", "A A c b B", "", "B A d d d d a"],
        {"max_ngram": 4, "smooth": False, "lowercase": True},
        [
            "ok",
            {
                "bleu": 0.0,
                "precisions": [
                    0.35714285714285715,
                    0.18181818181818182,
                    0.0,
                    0.0,
                ],
                "bp": 1.0,
                "length_ratio": 1.0,
                "hyp_length": 14,
                "ref_length": 14,
            },
        ],
    ],
    [
        ["A a", "A c b", ""],
        ["B a B c", "b c b A A", "B b A b b"],
        {"max_ngram": 4, "smooth": False, "lowercase": True},
        [
            "ok",
            {
                "bleu": 0.0,
                "precisions": [
                    0.2857142857142857,
                    0.09090909090909091,
                    0.0,
                    0.0,
                ],
                "bp": 1.0,
                "length_ratio": 2.8,
                "hyp_length": 14,
                "ref_length": 5,
            },
        ],
    ],
    [
        [],
        [],
        {"max_ngram": 2, "smooth": True, "lowercase": False},
        [
            "ok",
            {
                "bleu": 0.0,
                "precisions": [0.0, 0.0],
                "bp": 1.0,
                "length_ratio": 0.0,
                "hyp_length": 0,
                "ref_length": 0,
            },
        ],
    ],
    [
        [],
        [],
        {"max_ngram": 4, "smooth": False, "lowercase": False},
        [
            "ok",
            {
                "bleu": 0.0,
                "precisions": [0.0, 0.0, 0.0, 0.0],
                "bp": 1.0,
                "length_ratio": 0.0,
                "hyp_length": 0,
                "ref_length": 0,
            },
        ],
    ],
    [
        [["b B a d d b B"], ["B d"]],
        ["c d b c c a", "a c A d d"],
        {"max_ngram": 4, "smooth": True, "lowercase": False},
        [
            "ok",
            {
                "bleu": 13.033894166590244,
                "precisions": [
                    0.36363636363636365,
                    0.1111111111111111,
                    0.07142857142857142,
                    0.1,
                ],
                "bp": 1.0,
                "length_ratio": 1.2222222222222223,
                "hyp_length": 11,
                "ref_length": 9,
            },
        ],
    ],
    [
        [["B", "B d A d A c"], ["b c b", "d c", ""], [""]],
        ["B", "d b a a", "A B c A b B"],
        {"max_ngram": 3, "smooth": True, "lowercase": True},
        [
            "ok",
            {
                "bleu": 11.241107825565228,
                "precisions": [
                    0.2727272727272727,
                    0.0625,
                    0.08333333333333333,
                ],
                "bp": 1.0,
                "length_ratio": 2.75,
                "hyp_length": 11,
                "ref_length": 4,
            },
        ],
    ],
    [
        ["c a d a B A A", "B", "B", "c a c b B b b"],
        ["d d a d B c a", "a A b", "c B B B c", "a d"],
        {"max_ngram": 1, "smooth": True, "lowercase": False},
        [
            "ok",
            {
                "bleu": 41.17647058823529,
                "precisions": [0.4117647058823529],
                "bp": 1.0,
                "length_ratio": 1.0625,
                "hyp_length": 17,
                "ref_length": 16,
            },
        ],
    ],
    [
        [["c", ""], ["d a b B a", "c c a d"], ["c", "c a c a a B"]],
        ["B b b c", "A c b c d a", "A A b B a a"],
        {"max_ngram": 4, "smooth": True, "lowercase": False},
        [
            "ok",
            {
                "bleu": 13.259061490238883,
                "precisions": [
                    0.5625,
                    0.15384615384615385,
                    0.05,
                    0.07142857142857142,
                ],
                "bp": 1.0,
                "length_ratio": 1.3333333333333333,
                "hyp_length": 16,
                "ref_length": 12,
            },
        ],
    ],
    [
        ["d", "d b a b b b A", "B", "a A a a b b A"],
        ["", "b B c A", "B a a a c A", "d c b"],
        {"max_ngram": 4, "smooth": True, "lowercase": False},
        [
            "ok",
            {
                "bleu": 8.594989523443694,
                "precisions": [
                    0.3076923076923077,
                    0.05,
                    0.07142857142857142,
                    0.125,
                ],
                "bp": 0.7939226578179512,
                "length_ratio": 0.8125,
                "hyp_length": 13,
                "ref_length": 16,
            },
        ],
    ],
    [
        [["a", "a d B", "d c d d b d b"], ["B b A b"]],
        ["c d c A a", "d b b"],
        {"max_ngram": 4, "smooth": True, "lowercase": True},
        [
            "ok",
            {
                "bleu": 31.435835742073387,
                "precisions": [0.625, 0.5, 0.125, 0.25],
                "bp": 1.0,
                "length_ratio": 1.1428571428571428,
                "hyp_length": 8,
                "ref_length": 7,
            },
        ],
    ],
    [
        [],
        [],
        {"max_ngram": 4, "smooth": True, "lowercase": True},
        [
            "ok",
            {
                "bleu": 0.0,
                "precisions": [0.0, 0.0, 0.0, 0.0],
                "bp": 1.0,
                "length_ratio": 0.0,
                "hyp_length": 0,
                "ref_length": 0,
            },
        ],
    ],
]


GRID_COUNT = 1276
GRID_DIGEST = (
    "a0be25bcb1e349e0f030a071ca99fd71e9ded0785f99323858efb6751ce04199"
)


def _grid_digest(fn: Any) -> tuple[int, str]:
    """Hash the outcomes of ``fn`` over a seeded grid of equal-length inputs.

    Skips cases where every hypothesis has fewer than 4 tokens: the
    old empty-hypothesis crash was fixed there, and a score of 0.0 for
    short hypotheses is current behavior, not a promise.
    """
    rng = random.Random(0)  # noqa: S311  # seeded test grid, not crypto
    words = ["a", "b", "c", "d", "e"]

    def text() -> str:
        size = rng.choice([0, 0, 1, 2, 3, 5, 8, 12])
        return " ".join(rng.choice(words) for _ in range(size))

    digest = hashlib.sha256()
    count = 0
    with mock.patch("pythainlp.tokenize.word_tokenize", _split):
        for _ in range(2000):
            n = rng.randint(1, 4)
            hyps = [text() for _ in range(n)]
            if rng.random() < 0.4:
                refs: Any = [
                    [text() for _ in range(rng.randint(1, 2))]
                    for _ in range(n)
                ]
            else:
                refs = [text() for _ in range(n)]
            smooth = rng.random() < 0.5
            if all(len(h.split()) < 4 for h in hyps):
                continue
            try:
                got = fn(refs, hyps, smooth=smooth)
                # Round: the last digit of a float differs across Python versions.
                outcome = repr(
                    [
                        (k, [round(x, 9) for x in v])
                        if isinstance(v, list)
                        else (k, round(v, 9))
                        for k, v in sorted(got.items())
                    ]
                )
            except (ValueError, ZeroDivisionError) as err:
                outcome = f"{type(err).__name__}: {err}"
            digest.update(outcome.encode("utf-8"))
            count += 1
    return count, digest.hexdigest()


class BleuScoreCharacterizationTestCase(unittest.TestCase):
    def _run(self, references: Any, hypotheses: Any, **kwargs: Any) -> Any:
        with mock.patch("pythainlp.tokenize.word_tokenize", _split):
            return bleu_score(references, hypotheses, **kwargs)

    def test_golden_cases(self) -> None:
        for refs, hyps, kwargs, expected in GOLDEN:
            with self.subTest(refs=refs, hyps=hyps, kwargs=kwargs):
                if expected[0] == "exc":
                    with self.assertRaises(
                        getattr(builtins, expected[1])
                    ) as ctx:
                        self._run(refs, hyps, **kwargs)
                    # The message of min() on empty input changed in
                    # Python 3.12. Before: "min() arg is an empty sequence".
                    if not str(ctx.exception).startswith("min() "):
                        self.assertEqual(str(ctx.exception), expected[2])
                    continue
                score = self._run(refs, hyps, **kwargs)
                want = expected[1]
                self.assertEqual(set(score), set(want))
                self.assertEqual(score["hyp_length"], want["hyp_length"])
                self.assertEqual(score["ref_length"], want["ref_length"])
                for key in ("bleu", "bp", "length_ratio"):
                    self.assertAlmostEqual(score[key], want[key], places=9)
                self.assertEqual(
                    len(score["precisions"]), len(want["precisions"])
                )
                for got, exp in zip(score["precisions"], want["precisions"]):
                    self.assertAlmostEqual(got, exp, places=9)

    def test_real_tokenizer(self) -> None:
        score = bleu_score(["สวัสดีครับ วันนี้อากาศดีมาก"], ["สวัสดีค่ะ วันนี้อากาศดี"])
        self.assertAlmostEqual(score["bleu"], 28.12, places=2)

    def test_multiple_references_pick_closest_length(self) -> None:
        score = self._run([["a b", "a b c d e"]], ["a b c"])
        self.assertEqual(score["ref_length"], 2)

    def test_changed_behavior(self) -> None:
        """Pin the behavior of empty hypotheses and length mismatch."""
        mismatch = "The number of references ({}) and hypotheses ({}) must be"
        cases = [
            # (references, hypotheses, old behavior, new behavior)
            # old: ZeroDivisionError; new: bp 0.0 and bleu 0.0
            (["a b"], [""], None),
            (["a b", "c"], ["", ""], None),
            # old: silently truncated; new: ValueError
            (["a b c", "d e f"], ["a b c"], mismatch.format(2, 1)),
            (["a b c"], ["a b c", "d e f"], mismatch.format(1, 2)),
            (["a b"], [], mismatch.format(1, 0)),
        ]
        for refs, hyps, err in cases:
            with self.subTest(refs=refs, hyps=hyps):
                if err:
                    with self.assertRaisesRegex(ValueError, re.escape(err)):
                        self._run(refs, hyps)
                    continue
                score = self._run(refs, hyps)
                self.assertEqual(score["bp"], 0.0)
                self.assertEqual(score["bleu"], 0.0)
                self.assertEqual(score["hyp_length"], 0)

    def test_unchanged_behavior_grid(self) -> None:
        """Outcomes for equal-length inputs match the pre-change code."""
        count, digest = _grid_digest(bleu_score)
        self.assertEqual(count, GRID_COUNT)
        self.assertEqual(digest, GRID_DIGEST)

    def test_regression_all_empty_hypotheses(self) -> None:
        """Every hypothesis tokenizes to nothing; this used to crash."""
        for hyps in ([""], ["", ""], ["   "], [" ", ""]):
            with self.subTest(hyps=hyps):
                refs = ["a b"] * len(hyps)
                score = self._run(refs, hyps)
                self.assertEqual(score["bleu"], 0.0)
                self.assertEqual(score["bp"], 0.0)
                self.assertEqual(score["length_ratio"], 0.0)
                self.assertEqual(score["hyp_length"], 0)
                self.assertEqual(score["ref_length"], 2 * len(hyps))

    def test_mismatched_lengths_message(self) -> None:
        cases: list[tuple[Any, Any, str]] = [
            (["a b c", "d e f"], ["a b c"], "(2) and hypotheses (1)"),
            (["a b c"], ["a b c", "d e f"], "(1) and hypotheses (2)"),
            (["a b"], [], "(1) and hypotheses (0)"),
            ([["a"], ["b"]], ["a"], "(2) and hypotheses (1)"),
            # A bare string is a sequence of characters.
            ("a b", ["a b"], "(3) and hypotheses (1)"),
            (["a b"], "a b", "(1) and hypotheses (3)"),
        ]
        for refs, hyps, text in cases:
            with self.subTest(refs=refs, hyps=hyps):
                with self.assertRaisesRegex(ValueError, re.escape(text)):
                    self._run(refs, hyps)

    def test_adversarial_inputs(self) -> None:
        big = " ".join(["a", "b", "c"] * 1700)
        # (references, hypotheses, kwargs, expected); an expected string is
        # an exception name, a tuple is (bleu, bp, hyp_length, ref_length).
        # Exception rows are current behavior, not a promise.
        # Values are hand-derived: identical text gives 100; one mismatch
        # gives the geometric mean of the smoothed precisions
        # (0.8, 0.5, 1/3, 0.25) = 42.73; max_ngram 1 gives 80 (4/5);
        # max_ngram 2 gives sqrt(0.8 * 0.5) = 63.25; a hypothesis 100
        # times shorter has bp = exp(1 - 5100/50), with all precisions 1.
        cases: list[tuple[Any, Any, dict[str, Any], Any]] = [
            (["  "], ["  "], {}, (0.0, 1.0, 0, 0)),
            ([" "], ["a b"], {}, (0.0, 1.0, 2, 0)),
            (None, ["a"], {}, "TypeError"),
            (["a"], None, {}, "TypeError"),
            (5, ["a"], {}, "TypeError"),
            ([None], ["a"], {}, "TypeError"),
            (["a"], [None], {}, "AttributeError"),
            ([1], ["a"], {}, "TypeError"),
            (["a"], [1], {}, "AttributeError"),
            ([["a"], None], ["a", "b"], {}, "TypeError"),
            (
                [["a b"], ["a b", "c d e"]],
                ["a b", "c d"],
                {},
                (0.0, 1.0, 4, 4),
            ),
            ([big], [big], {}, (100.0, 1.0, 5100, 5100)),
            ([big], [big[:100]], {}, (0.0, 1.368539471173853e-44, 50, 5100)),
            (["a a a a a a"], ["a a a a a a"], {}, (100.0, 1.0, 6, 6)),
            (["ก\u200bข ค ง จ"], ["ก\u200bข ค ง จ"], {}, (100.0, 1.0, 4, 4)),
            (
                ["A b c d e"],
                ["a B c d e"],
                {"lowercase": True},
                (100.0, 1.0, 5, 5),
            ),
            (["สวัสดี ครับ ผม วันนี้"], ["สวัสดี ครับ ผม วันนี้"], {}, (100.0, 1.0, 4, 4)),
            (["a b c d e"], ["a b c x e"], {}, (42.728701, 1.0, 5, 5)),
            (
                ["a b c d e"],
                ["a b c x e"],
                {"smooth": False},
                (0.0, 1.0, 5, 5),
            ),
            (
                ["a b c d e"],
                ["a b c x e"],
                {"max_ngram": 1},
                (80.0, 1.0, 5, 5),
            ),
            (
                ["a b c d e"],
                ["a b c x e"],
                {"max_ngram": 2},
                (63.245553, 1.0, 5, 5),
            ),
            (["a b"], ["a b"], {"max_ngram": 2}, (100.0, 1.0, 2, 2)),
            (["a b"], ["a b"], {"max_ngram": 1}, (100.0, 1.0, 2, 2)),
        ]
        for refs, hyps, kwargs, want in cases:
            with self.subTest(
                refs=str(refs)[:20], hyps=str(hyps)[:20], kw=kwargs
            ):
                if isinstance(want, str):
                    with self.assertRaises(getattr(builtins, want)):
                        self._run(refs, hyps, **kwargs)
                    continue
                score = self._run(refs, hyps, **kwargs)
                got = (
                    score["bleu"],
                    score["bp"],
                    score["hyp_length"],
                    score["ref_length"],
                )
                for g, w in zip(got, want):
                    self.assertAlmostEqual(g, w, places=5)

    def test_empty_reference_group_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            self._run([[]], ["a b"])

    def test_zero_max_ngram_raises_zero_division(self) -> None:
        with self.assertRaises(ZeroDivisionError):
            self._run(["a b"], ["a b"], max_ngram=0)


if __name__ == "__main__":
    unittest.main()
