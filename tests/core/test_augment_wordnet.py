# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""
Characterization tests for pythainlp.augment.wordnet.WordNetAug.augment.

Golden cases were recorded from the code before the complexity refactor.
The NLTK WordNet reader, the Thai WordNet wrapper, and the POS tagger are
replaced by fakes, so no corpus is needed or downloaded.
"""

from __future__ import annotations

import importlib.util
import sys
import types
import unittest
from contextlib import ExitStack
from pathlib import Path
from typing import Any
from unittest import mock

import pythainlp.corpus

# word -> synsets, each synset is a list of Thai lemma names
SYNSETS: dict[str, list[list[str]]] = {
    "a": [["x", "y"], ["x"]],
    "c": [["z"]],
    "d": [["p", "q", "r"]],
    "e": [["m", "n"]],
}
# word -> Orchid POS tag; other words get "NCMN"
TAGS: dict[str, str] = {
    "a": "NCMN",
    "b": "VACT",
    "c": "PROPN",
    "d": "ADJ",
    "e": "XXX",
}


class FakeSynset:
    """Synset with a fixed list of lemma names."""

    def __init__(self, names: list[str]) -> None:
        """Set the lemma names."""
        self.names = names

    def lemma_names(self, lang: str = "eng") -> list[str]:
        return list(self.names)


class FakeWordNet:
    """Replacement for pythainlp.corpus.wordnet; records its calls."""

    def __init__(self) -> None:
        """Start with no recorded calls."""
        self.calls: list[tuple[str, Any]] = []

    def synsets(self, word: str, pos: Any = None) -> list[FakeSynset]:
        self.calls.append((word, pos))
        return [FakeSynset(names) for names in SYNSETS.get(word, [])]


def fake_pos_tag(
    words: list[str], corpus: str = "orchid"
) -> list[tuple[str, str]]:
    return [(word, TAGS.get(word, "NCMN")) for word in words]


def load_module(fake: FakeWordNet) -> Any:
    """Import pythainlp/augment/wordnet.py with fake NLTK and WordNet."""
    nltk = types.ModuleType("nltk")
    nltk_corpus = types.ModuleType("nltk.corpus")
    setattr(
        nltk_corpus,
        "wordnet",
        types.SimpleNamespace(NOUN="n", VERB="v", ADJ="a", ADV="r"),
    )
    setattr(nltk, "corpus", nltk_corpus)
    corpus_wordnet = types.ModuleType("pythainlp.corpus.wordnet")
    setattr(corpus_wordnet, "synsets", fake.synsets)
    path = Path(pythainlp.__file__).parent / "augment" / "wordnet.py"
    fakes = {
        "nltk": nltk,
        "nltk.corpus": nltk_corpus,
        "pythainlp.corpus.wordnet": corpus_wordnet,
    }
    with ExitStack() as stack:
        stack.enter_context(mock.patch.dict(sys.modules, fakes))
        stack.enter_context(
            mock.patch.object(
                pythainlp.corpus, "wordnet", corpus_wordnet, create=True
            )
        )
        spec = importlib.util.spec_from_file_location(
            "wordnet_augment_under_test", path
        )
        if spec is None or spec.loader is None:
            raise ImportError(f"Cannot load {path}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    setattr(module, "pos_tag", fake_pos_tag)
    return module


# (sentence, max_syn_sent, postag, postag_corpus, outcome, WordNet calls)
# The outcome is ["ok", sentences] or ["exc", exception name, message].
GOLDEN: list[list[Any]] = [
    [
        "a b c d",
        6,
        True,
        "orchid",
        [
            "ok",
            [
                ["x", "b", "z", "p"],
                ["x", "b", "z", "q"],
                ["x", "b", "z", "r"],
                ["y", "b", "z", "p"],
                ["y", "b", "z", "q"],
                ["y", "b", "z", "r"],
            ],
        ],
        [
            ["a", "n"],
            ["a", None],
            ["b", "v"],
            ["b", None],
            ["c", None],
            ["c", None],
            ["d", "a"],
            ["d", None],
        ],
    ],
    [
        "a b c d",
        6,
        True,
        "other",
        [
            "ok",
            [
                ["x", "b", "z", "p"],
                ["x", "b", "z", "q"],
                ["x", "b", "z", "r"],
                ["y", "b", "z", "p"],
                ["y", "b", "z", "q"],
                ["y", "b", "z", "r"],
            ],
        ],
        [
            ["a", None],
            ["a", None],
            ["b", None],
            ["b", None],
            ["c", None],
            ["c", None],
            ["d", None],
            ["d", None],
        ],
    ],
    [
        "a b c d",
        100,
        True,
        "orchid",
        [
            "ok",
            [
                ["x", "b", "z", "p"],
                ["x", "b", "z", "q"],
                ["x", "b", "z", "r"],
                ["y", "b", "z", "p"],
                ["y", "b", "z", "q"],
                ["y", "b", "z", "r"],
            ],
        ],
        [
            ["a", "n"],
            ["a", None],
            ["b", "v"],
            ["b", None],
            ["c", None],
            ["c", None],
            ["d", "a"],
            ["d", None],
        ],
    ],
    [
        "a b c d",
        6,
        False,
        "orchid",
        [
            "ok",
            [
                ["x", "b", "z", "p"],
                ["x", "b", "z", "q"],
                ["x", "b", "z", "r"],
                ["y", "b", "z", "p"],
                ["y", "b", "z", "q"],
                ["y", "b", "z", "r"],
            ],
        ],
        [
            ["a", None],
            ["a", None],
            ["b", None],
            ["b", None],
            ["c", None],
            ["c", None],
            ["d", None],
            ["d", None],
        ],
    ],
    ["e", 6, True, "orchid", ["exc", "KeyError", "'XXX'"], []],
    [
        "e",
        6,
        True,
        "other",
        ["ok", [["m"], ["n"]]],
        [["e", None], ["e", None]],
    ],
    ["", 6, False, "orchid", ["ok", [[]]], []],
    [
        "c d",
        1,
        False,
        "other",
        ["ok", [["z", "p"]]],
        [["c", None], ["c", None], ["d", None], ["d", None]],
    ],
    ["a", 0, False, "orchid", ["ok", []], [["a", None], ["a", None]]],
    [
        "c d",
        100,
        True,
        "other",
        ["ok", [["z", "p"], ["z", "q"], ["z", "r"]]],
        [["c", None], ["c", None], ["d", None], ["d", None]],
    ],
    [
        "d d d",
        -1,
        True,
        "other",
        [
            "ok",
            [
                ["p", "p", "p"],
                ["p", "p", "q"],
                ["p", "p", "r"],
                ["p", "q", "p"],
                ["p", "q", "q"],
                ["p", "q", "r"],
                ["p", "r", "p"],
                ["p", "r", "q"],
                ["p", "r", "r"],
                ["q", "p", "p"],
                ["q", "p", "q"],
                ["q", "p", "r"],
                ["q", "q", "p"],
                ["q", "q", "q"],
                ["q", "q", "r"],
                ["q", "r", "p"],
                ["q", "r", "q"],
                ["q", "r", "r"],
                ["r", "p", "p"],
                ["r", "p", "q"],
                ["r", "p", "r"],
                ["r", "q", "p"],
                ["r", "q", "q"],
                ["r", "q", "r"],
                ["r", "r", "p"],
                ["r", "r", "q"],
            ],
        ],
        [
            ["d", None],
            ["d", None],
            ["d", None],
            ["d", None],
            ["d", None],
            ["d", None],
        ],
    ],
    [
        "c d",
        6,
        True,
        "orchid",
        ["ok", [["z", "p"], ["z", "q"], ["z", "r"]]],
        [["c", None], ["c", None], ["d", "a"], ["d", None]],
    ],
    [
        "c d",
        0,
        True,
        "other",
        ["ok", []],
        [["c", None], ["c", None], ["d", None], ["d", None]],
    ],
    [
        "a a",
        1,
        True,
        "other",
        ["ok", [["x", "x"]]],
        [["a", None], ["a", None], ["a", None], ["a", None]],
    ],
    ["b", -1, True, "orchid", ["ok", []], [["b", "v"], ["b", None]]],
    [
        "d d d",
        1,
        False,
        "orchid",
        ["ok", [["p", "p", "p"]]],
        [
            ["d", None],
            ["d", None],
            ["d", None],
            ["d", None],
            ["d", None],
            ["d", None],
        ],
    ],
    [
        "a",
        2,
        True,
        "other",
        ["ok", [["x"], ["y"]]],
        [["a", None], ["a", None]],
    ],
    ["", 0, True, "orchid", ["ok", []], []],
    [
        "c d",
        2,
        True,
        "other",
        ["ok", [["z", "p"], ["z", "q"]]],
        [["c", None], ["c", None], ["d", None], ["d", None]],
    ],
    [
        "a b c d",
        2,
        True,
        "other",
        ["ok", [["x", "b", "z", "p"], ["x", "b", "z", "q"]]],
        [
            ["a", None],
            ["a", None],
            ["b", None],
            ["b", None],
            ["c", None],
            ["c", None],
            ["d", None],
            ["d", None],
        ],
    ],
    [
        "a c d b",
        0,
        False,
        "other",
        ["ok", []],
        [
            ["a", None],
            ["a", None],
            ["c", None],
            ["c", None],
            ["d", None],
            ["d", None],
            ["b", None],
            ["b", None],
        ],
    ],
    [
        "a c d b",
        1,
        True,
        "orchid",
        ["ok", [["x", "z", "p", "b"]]],
        [
            ["a", "n"],
            ["a", None],
            ["c", None],
            ["c", None],
            ["d", "a"],
            ["d", None],
            ["b", "v"],
            ["b", None],
        ],
    ],
    ["b", 2, True, "orchid", ["ok", [["b"]]], [["b", "v"], ["b", None]]],
    ["b", -1, False, "other", ["ok", []], [["b", None], ["b", None]]],
    [
        "x y",
        0,
        False,
        "orchid",
        ["ok", []],
        [["x", None], ["x", None], ["y", None], ["y", None]],
    ],
    [
        "d d d",
        2,
        True,
        "orchid",
        ["ok", [["p", "p", "p"], ["p", "p", "q"]]],
        [
            ["d", "a"],
            ["d", None],
            ["d", "a"],
            ["d", None],
            ["d", "a"],
            ["d", None],
        ],
    ],
    [
        "d d d",
        2,
        True,
        "other",
        ["ok", [["p", "p", "p"], ["p", "p", "q"]]],
        [
            ["d", None],
            ["d", None],
            ["d", None],
            ["d", None],
            ["d", None],
            ["d", None],
        ],
    ],
]


class WordNetAugCharacterizationTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.fake = FakeWordNet()
        self.module = load_module(self.fake)
        self.aug = self.module.WordNetAug()

    def test_golden_cases(self) -> None:
        for sentence, max_syn, postag, corpus, expected, calls in GOLDEN:
            with self.subTest(
                sentence=sentence,
                max_syn=max_syn,
                postag=postag,
                corpus=corpus,
            ):
                self.fake.calls.clear()
                if expected[0] == "exc":
                    with self.assertRaises(KeyError) as ctx:
                        self.aug.augment(
                            sentence, str.split, max_syn, postag, corpus
                        )
                    self.assertEqual(str(ctx.exception), expected[2])
                else:
                    got = self.aug.augment(
                        sentence, str.split, max_syn, postag, corpus
                    )
                    self.assertEqual(got, expected[1])
                self.assertEqual(
                    [list(call) for call in self.fake.calls], calls
                )

    def test_default_postag_and_corpus(self) -> None:
        result = self.aug.augment("c d", str.split)
        self.assertEqual(result, [["z", "p"], ["z", "q"], ["z", "r"]])

    def test_state_attributes_are_set(self) -> None:
        self.aug.augment("a b", str.split, 6, True)
        self.assertEqual(self.aug.list_words, ["a", "b"])
        self.assertEqual(self.aug.list_pos, [("a", "NCMN"), ("b", "VACT")])
        self.assertEqual(self.aug.list_synonym, [["x", "y"], ["b"]])
        self.assertEqual(self.aug.p_all, 2)
        self.assertEqual(self.aug.temp, [])
        self.aug.augment("a b", str.split, 6, False)
        self.assertEqual(self.aug.list_synonym, [["x", "y"], ["b"]])

    # BUG-LEDGER: wordnetaug-pos-ignored
    def test_bug_pos_filter_is_ignored(self) -> None:
        """
        The synonyms ignore ``pos``; only an unused lookup uses it.

        Expected: synsets are filtered by the WordNet POS.
        """
        with_pos = self.aug.find_synonyms("a", "NCMN")
        without_pos = self.aug.find_synonyms("a")
        self.assertEqual(with_pos, without_pos)
        self.assertEqual(
            self.fake.calls,
            [("a", "n"), ("a", None), ("a", None), ("a", None)],
        )

    # BUG-LEDGER: wordnetaug-pos-ignored
    def test_bug_negative_max_syn_sent_drops_last_sentence(self) -> None:
        """A negative limit slices ``[0:-1]``; expected: no clamp below 0."""
        self.assertEqual(
            self.aug.augment("c d", str.split, -1, False),
            [["z", "p"], ["z", "q"]],
        )

    def test_postype2wordnet(self) -> None:
        self.assertEqual(self.module.postype2wordnet("NCMN", "orchid"), "n")
        self.assertEqual(self.module.postype2wordnet("VACT", "orchid"), "v")
        self.assertEqual(self.module.postype2wordnet("PROPN", "orchid"), "")
        self.assertIsNone(self.module.postype2wordnet("NCMN", "other"))
        with self.assertRaises(KeyError):
            self.module.postype2wordnet("XXX", "orchid")


if __name__ == "__main__":
    unittest.main()
