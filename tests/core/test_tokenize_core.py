# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Characterization tests for engine dispatch in pythainlp.tokenize.core.

Optional engines are replaced by fake modules in :data:`sys.modules`,
so every dispatch branch runs with core dependencies only.
"""

from __future__ import annotations

import sys
import types
import unittest
from contextlib import contextmanager
from typing import TYPE_CHECKING, Any, Optional

from pythainlp.tokenize import (
    paragraph_tokenize,
    sent_tokenize,
    subword_tokenize,
    syllable_tokenize,
    word_detokenize,
    word_tokenize,
)
from pythainlp.util.trie import Trie

if TYPE_CHECKING:
    from collections.abc import Iterator

TEXT = "ก ข1.5"
FAKE_RESULT = ["ก", " ", "ข", "1", ".", "5"]

WORD_NO_CUSTOM_DICT = (
    "attacut",
    "icu",
    "nercut",
    "sefr_cut",
    "tltk",
    "oskut",
    "budoux",
)

# engine: (module, function, passes custom_dict, extra keyword arguments)
WORD_ENGINES: dict[str, tuple[str, str, bool, dict[str, Any]]] = {
    "newmm": ("pythainlp.tokenize.newmm", "segment", True, {}),
    "onecut": ("pythainlp.tokenize.newmm", "segment", True, {}),
    "newmm-safe": (
        "pythainlp.tokenize.newmm",
        "segment",
        True,
        {"safe_mode": True},
    ),
    "attacut": ("pythainlp.tokenize.attacut", "segment", False, {}),
    "longest": ("pythainlp.tokenize.longest", "segment", True, {}),
    "mm": ("pythainlp.tokenize.multi_cut", "segment", True, {}),
    "multi_cut": ("pythainlp.tokenize.multi_cut", "segment", True, {}),
    "deepcut": ("pythainlp.tokenize.deepcut", "segment", False, {}),
    "icu": ("pythainlp.tokenize.pyicu", "segment", False, {}),
    "budoux": ("pythainlp.tokenize.budoux", "segment", False, {}),
    "nercut": ("pythainlp.tokenize.nercut", "segment", False, {}),
    "sefr_cut": ("pythainlp.tokenize.sefr_cut", "segment", False, {}),
    "tltk": ("pythainlp.tokenize.tltk", "segment", False, {}),
    "oskut": ("pythainlp.tokenize.oskut", "segment", False, {}),
    "nlpo3": ("pythainlp.tokenize.nlpo3", "segment", False, {}),
}

# engine: (module, function)
SENT_ENGINES: dict[str, tuple[str, str]] = {
    "crfcut": ("pythainlp.tokenize.crfcut", "segment"),
    "tltk": ("pythainlp.tokenize.tltk", "sent_tokenize"),
}

# engine: (module, function)
SUBWORD_ENGINES: dict[str, tuple[str, str]] = {
    "tcc": ("pythainlp.tokenize.tcc", "segment"),
    "tcc_p": ("pythainlp.tokenize.tcc_p", "segment"),
    "etcc": ("pythainlp.tokenize.etcc", "segment"),
    "wangchanberta": ("pythainlp.wangchanberta", "segment"),
    "ssg": ("pythainlp.tokenize.ssg", "segment"),
    "tltk": ("pythainlp.tokenize.tltk", "syllable_tokenize"),
    "han_solo": ("pythainlp.tokenize.han_solo", "segment"),
    "phayathai": ("pythainlp.phayathaibert", "segment"),
}

# engine: model size passed to pythainlp.tokenize.wtsplit.tokenize
WTP_SIZES: dict[str, str] = {
    "wtp": "mini",
    "wtp-tiny": "tiny",
    "wtp-mini": "mini",
    "wtp-base": "base",
    "wtp-large": "large",
    "wtp-a-b": "b",
    "wtpx": "mini",
    "wtp-": "",
}


def not_found(engine: object) -> str:
    return (
        f'Tokenizer "{engine}" not found.\n'
        "            It might be a typo; if not, please consult our document."
    )


class Recorder:
    """Callable that records its calls and returns a copy of a result."""

    def __init__(self, result: list[str]) -> None:
        """Set the result to return."""
        self.result: list[str] = result
        self.calls: list[tuple[tuple[Any, ...], dict[str, Any]]] = []

    def __call__(self, *args: Any, **kwargs: Any) -> list[str]:
        self.calls.append((args, kwargs))
        return list(self.result)


_MISSING = object()


@contextmanager
def fake_module(name: str, **attrs: Any) -> Iterator[None]:
    """Replace one module in sys.modules for the duration of the block."""
    module = types.ModuleType(name)
    module.__dict__.update(attrs)
    saved: Any = sys.modules.get(name, _MISSING)
    sys.modules[name] = module
    try:
        yield
    finally:
        if saved is _MISSING:
            del sys.modules[name]
        else:
            sys.modules[name] = saved


@contextmanager
def fake_engine(
    module: str, func: str, result: Optional[list[str]] = None
) -> Iterator[Recorder]:
    recorder = Recorder(FAKE_RESULT if result is None else result)
    with fake_module(module, **{func: recorder}):
        yield recorder


@contextmanager
def fake_thaisum(result: Optional[list[str]] = None) -> Iterator[Recorder]:
    recorder = Recorder(FAKE_RESULT if result is None else result)

    class FakeSegmentor:
        def split_into_sentences(self, text: str) -> list[str]:
            return recorder(text)

    with fake_module(
        "pythainlp.tokenize.thaisumcut", ThaiSentenceSegmentor=FakeSegmentor
    ):
        yield recorder


class WordTokenizeDispatchTestCase(unittest.TestCase):
    def test_engines_without_custom_dict(self) -> None:
        for engine, (module, func, with_dict, kwargs) in WORD_ENGINES.items():
            with self.subTest(engine=engine):
                with fake_engine(module, func) as rec:
                    self.assertEqual(
                        word_tokenize(TEXT, engine=engine),
                        ["ก", " ", "ข", "1.5"],
                    )
                self.assertEqual(len(rec.calls), 1)
                args, kw = rec.calls[0]
                self.assertEqual(kw, kwargs)
                self.assertEqual(args[0], TEXT)
                if with_dict:
                    self.assertEqual(len(args), 2)
                    self.assertIsInstance(args[1], Trie)
                    self.assertEqual(len(args[1]), 0)
                else:
                    self.assertEqual(len(args), 1)

    def test_engines_with_custom_dict(self) -> None:
        trie = Trie(["ก"])
        for engine, (module, func, with_dict, kwargs) in WORD_ENGINES.items():
            with self.subTest(engine=engine):
                with fake_engine(module, func) as rec:
                    if engine in WORD_NO_CUSTOM_DICT:
                        with self.assertRaises(NotImplementedError) as cm:
                            word_tokenize(
                                TEXT, custom_dict=trie, engine=engine
                            )
                        self.assertEqual(
                            str(cm.exception),
                            f"The {engine} engine does not support"
                            " custom dictionaries.",
                        )
                        self.assertEqual(rec.calls, [])
                        continue
                    word_tokenize(TEXT, custom_dict=trie, engine=engine)
                args, kw = rec.calls[0]
                self.assertEqual(kw, kwargs)
                expected = (TEXT, trie) if with_dict else (TEXT,)
                self.assertEqual(args, expected)
                if with_dict:
                    self.assertIs(args[1], trie)

    def test_empty_custom_dict_is_allowed(self) -> None:
        for engine in WORD_NO_CUSTOM_DICT:
            module, func, _, _ = WORD_ENGINES[engine]
            with self.subTest(engine=engine):
                with fake_engine(module, func) as rec:
                    word_tokenize(TEXT, custom_dict=Trie([]), engine=engine)
                self.assertEqual(rec.calls, [((TEXT,), {})])

    def test_postprocessors(self) -> None:
        cases = (
            (True, True, ["ก", " ", "ข", "1.5"]),
            (True, False, ["ก", " ", "ข", "1", ".", "5"]),
            (False, True, ["ก", "ข", "1.5"]),
            (False, False, ["ก", "ข", "1", ".", "5"]),
        )
        for keep_whitespace, join_broken_num, expected in cases:
            with self.subTest(
                keep_whitespace=keep_whitespace,
                join_broken_num=join_broken_num,
            ):
                with fake_engine("pythainlp.tokenize.newmm", "segment"):
                    self.assertEqual(
                        word_tokenize(
                            TEXT,
                            keep_whitespace=keep_whitespace,
                            join_broken_num=join_broken_num,
                        ),
                        expected,
                    )

    def test_unknown_engine(self) -> None:
        for engine in ("XX", "", "NEWMM", "newmm ", None, 1, ["newmm"]):
            for custom_dict in (None, Trie(["ก"])):
                with self.subTest(engine=engine, custom_dict=custom_dict):
                    with self.assertRaises(ValueError) as cm:
                        word_tokenize(
                            TEXT,
                            custom_dict=custom_dict,
                            engine=engine,  # type: ignore[arg-type]
                        )
                    self.assertEqual(str(cm.exception), not_found(engine))

    def test_empty_or_wrong_text(self) -> None:
        for text in ("", None, 0, 1, ["ก"], b"ab"):
            with self.subTest(text=text):
                # Even an unknown engine returns [] for these inputs.
                self.assertEqual(
                    word_tokenize(text, engine="XX"),  # type: ignore[arg-type]
                    [],
                )

    def test_real_engines(self) -> None:
        text = "ฉันรักภาษาไทย  เพราะ 12:30 น."
        for engine in ("newmm", "onecut", "newmm-safe", "longest", "mm"):
            with self.subTest(engine=engine):
                tokens = word_tokenize(text, engine=engine)
                self.assertEqual("".join(tokens), text)
                self.assertIn("12:30", tokens)
                self.assertEqual(
                    word_tokenize(text, engine=engine, keep_whitespace=False),
                    [t for t in tokens if not t.isspace()],
                )

    def test_whitespace_only_and_long_text(self) -> None:
        self.assertEqual(word_tokenize(" \n\t "), [" ", "\n", "\t "])
        # Only the space character is stripped.
        self.assertEqual(
            word_tokenize(" \n\t ", keep_whitespace=False), ["\n", "\t"]
        )
        text = "ฉันรักภาษาไทย " * 2000
        tokens = word_tokenize(text, engine="newmm-safe")
        self.assertEqual("".join(tokens), text)


class SentTokenizeDispatchTestCase(unittest.TestCase):
    def test_string_engines(self) -> None:
        for engine, (module, func) in SENT_ENGINES.items():
            with self.subTest(engine=engine):
                with fake_engine(module, func) as rec:
                    self.assertEqual(
                        sent_tokenize(TEXT, engine=engine), FAKE_RESULT
                    )
                    self.assertEqual(
                        sent_tokenize(
                            TEXT, engine=engine, keep_whitespace=False
                        ),
                        ["ก", "ข", "1", ".", "5"],
                    )
                self.assertEqual(rec.calls, [((TEXT,), {})] * 2)

    def test_thaisum(self) -> None:
        with fake_thaisum() as rec:
            self.assertEqual(
                sent_tokenize(TEXT, engine="thaisum"), FAKE_RESULT
            )
        self.assertEqual(rec.calls, [((TEXT,), {})])

    def test_wtp(self) -> None:
        for engine, size in WTP_SIZES.items():
            with self.subTest(engine=engine):
                with fake_engine(
                    "pythainlp.tokenize.wtsplit", "tokenize"
                ) as rec:
                    self.assertEqual(
                        sent_tokenize(TEXT, engine=engine), FAKE_RESULT
                    )
                self.assertEqual(
                    rec.calls,
                    [
                        (
                            (),
                            {
                                "text": TEXT,
                                "size": size,
                                "tokenize": "sentence",
                            },
                        )
                    ],
                )

    def test_word_list_input(self) -> None:
        words = ["ก", " ", "ขค", "ง"]
        result = ["ก ", "ขคง"]
        for engine, (module, func) in SENT_ENGINES.items():
            if engine == "crfcut":
                continue
            with self.subTest(engine=engine):
                with fake_engine(module, func, result) as rec:
                    self.assertEqual(
                        sent_tokenize(words, engine=engine),
                        [["ก", " "], ["ขค", "ง"]],
                    )
                    self.assertEqual(
                        sent_tokenize(
                            words, engine=engine, keep_whitespace=False
                        ),
                        # BUG-LEDGER: sent-tokenize-strip-misaligns-words
                        [["ก"], ["ข", "คง"]],
                    )
                self.assertEqual(rec.calls, [(("ก ขคง",), {})] * 2)

    def test_word_list_input_crfcut_ignores_segments(self) -> None:
        # BUG-LEDGER: sent-tokenize-crfcut-segments
        words = ["ก", " ", "ขค", "ง"]
        for keep_whitespace in (True, False):
            with self.subTest(keep_whitespace=keep_whitespace):
                with fake_engine(
                    "pythainlp.tokenize.crfcut", "segment", ["ก ", "ขคง"]
                ) as rec:
                    self.assertEqual(
                        sent_tokenize(
                            words,
                            engine="crfcut",
                            keep_whitespace=keep_whitespace,
                        ),
                        [words],
                    )
                self.assertEqual(rec.calls, [(("ก ขคง",), {})])

    def test_whitespace_engines(self) -> None:
        text = " ก ข  ค\nง "
        cases = (
            ("whitespace", True, ["", "ก", "ข", "ค\nง", ""]),
            ("whitespace", False, ["ก", "ข", "ค\nง"]),
            ("whitespace+newline", True, ["ก", "ข", "ค", "ง"]),
            ("whitespace+newline", False, ["ก", "ข", "ค", "ง"]),
        )
        for engine, keep_whitespace, expected in cases:
            with self.subTest(engine=engine, keep_whitespace=keep_whitespace):
                self.assertEqual(
                    sent_tokenize(
                        text, engine=engine, keep_whitespace=keep_whitespace
                    ),
                    expected,
                )

    def test_whitespace_engines_word_list(self) -> None:
        cases: tuple[tuple[str, list[str], list[list[str]]], ...] = (
            ("whitespace", ["ก", " ", "ข"], [["ก"], ["ข"]]),
            ("whitespace", [" ", "ก", "\n", "ข"], [["ก", "\n", "ข"]]),
            ("whitespace", ["ก", "  ", " ", "ข"], [["ก"], ["ข"]]),
            ("whitespace", ["ก", " a", "ข"], [["ก", " a", "ข"]]),
            ("whitespace", [" "], []),
            ("whitespace", ["ก"], [["ก"]]),
            ("whitespace+newline", [" ", "ก", "\n", "ข"], [["ก"], ["ข"]]),
            ("whitespace+newline", ["ก", "\t", "ข"], [["ก"], ["ข"]]),
            ("whitespace+newline", ["ก", " a", "ข"], [["ก", " a", "ข"]]),
            ("whitespace+newline", ["\n"], []),
        )
        for engine, words, expected in cases:
            for keep_whitespace in (True, False):
                with self.subTest(engine=engine, words=words):
                    self.assertEqual(
                        sent_tokenize(
                            words,
                            engine=engine,
                            keep_whitespace=keep_whitespace,
                        ),
                        expected,
                    )

    def test_whitespace_engines_word_list_trailing_separator(self) -> None:
        # BUG-LEDGER: whitespace-trailing-append
        for engine in ("whitespace", "whitespace+newline"):
            with self.subTest(engine=engine):
                self.assertEqual(
                    sent_tokenize(["ก", " ", "ข", " "], engine=engine),
                    [["ก"], ["ข"], []],
                )

    def test_unknown_engine(self) -> None:
        for text in (TEXT, ["ก", "ข"]):
            for engine in ("XX", "", "CRFCUT", "wt", "Wtp"):
                with self.subTest(text=text, engine=engine):
                    with self.assertRaises(ValueError) as cm:
                        sent_tokenize(text, engine=engine)
                    self.assertEqual(str(cm.exception), not_found(engine))

    def test_wrong_engine_type(self) -> None:
        for engine in (None, 1):
            with self.subTest(engine=engine):
                with self.assertRaises(AttributeError):
                    sent_tokenize(TEXT, engine=engine)  # type: ignore[arg-type]

    def test_empty_or_wrong_text(self) -> None:
        cases: tuple[Any, ...] = (
            "",
            None,
            [],
            0,
            1,
            ("ก",),
            b"ab",
            ["ก", 1],
            ["ก", None],
        )
        for text in cases:
            with self.subTest(text=text):
                self.assertEqual(sent_tokenize(text, engine="XX"), [])

    def test_string_subclass(self) -> None:
        class Text(str):
            pass

        result = sent_tokenize(Text("ก ข"), engine="whitespace")
        self.assertEqual(result, ["ก", "ข"])
        self.assertIs(type(result[0]), str)


class SubwordTokenizeDispatchTestCase(unittest.TestCase):
    def test_engines(self) -> None:
        for engine, (module, func) in SUBWORD_ENGINES.items():
            with self.subTest(engine=engine):
                with fake_engine(module, func) as rec:
                    self.assertEqual(
                        subword_tokenize(TEXT, engine=engine), FAKE_RESULT
                    )
                    self.assertEqual(
                        subword_tokenize(
                            TEXT, engine=engine, keep_whitespace=False
                        ),
                        ["ก", "ข", "1", ".", "5"],
                    )
                self.assertEqual(rec.calls, [((TEXT,), {})] * 2)

    def test_dict_engine(self) -> None:
        cases: tuple[tuple[str, bool, list[str]], ...] = (
            ("สวัสดีชาวโลก ครับ", True, ["สวัส", "ดี", "ชาว", "โลก", " ", "ครับ"]),
            ("สวัสดีชาวโลก ครับ", False, ["สวัส", "ดี", "ชาว", "โลก", "ครับ"]),
            (" ", True, [" "]),
            (" ", False, []),
        )
        for text, keep_whitespace, expected in cases:
            with self.subTest(text=text, keep_whitespace=keep_whitespace):
                self.assertEqual(
                    subword_tokenize(
                        text, engine="dict", keep_whitespace=keep_whitespace
                    ),
                    expected,
                )

    def test_dict_engine_uses_newmm(self) -> None:
        with fake_engine(
            "pythainlp.tokenize.newmm", "segment", ["ab", "c"]
        ) as rec:
            self.assertEqual(
                subword_tokenize("xyz", engine="dict"),
                ["ab", "c", "ab", "c"],
            )
        self.assertEqual(
            [call[0][0] for call in rec.calls], ["xyz", "ab", "c"]
        )
        self.assertEqual(len(rec.calls[0][0][1]), 0)
        self.assertGreater(len(rec.calls[1][0][1]), 0)
        self.assertIs(rec.calls[1][0][1], rec.calls[2][0][1])

    def test_unknown_engine(self) -> None:
        for engine in ("XX", "", "TCC", "newmm", "crfcut", None):
            with self.subTest(engine=engine):
                with self.assertRaises(ValueError) as cm:
                    subword_tokenize(TEXT, engine=engine)  # type: ignore[arg-type]
                self.assertEqual(str(cm.exception), not_found(engine))

    def test_empty_or_wrong_text(self) -> None:
        for text in ("", None, 0, ["ก"]):
            with self.subTest(text=text):
                self.assertEqual(
                    subword_tokenize(text, engine="XX"),  # type: ignore[arg-type]
                    [],
                )

    def test_syllable_tokenize(self) -> None:
        for engine in ("han_solo", "ssg", "tltk"):
            module, func = SUBWORD_ENGINES[engine]
            with self.subTest(engine=engine):
                with fake_engine(module, func) as rec:
                    self.assertEqual(
                        syllable_tokenize(
                            TEXT, engine=engine, keep_whitespace=False
                        ),
                        ["ก", "ข", "1", ".", "5"],
                    )
                self.assertEqual(rec.calls, [((TEXT,), {})])
        self.assertEqual(syllable_tokenize("", engine="dict"), [])
        for engine in ("tcc", "etcc", "XX"):
            with self.subTest(engine=engine):
                with self.assertRaises(ValueError) as cm:
                    syllable_tokenize(TEXT, engine=engine)
                self.assertEqual(str(cm.exception), not_found(engine))

    def test_paragraph_tokenize(self) -> None:
        for engine, size in WTP_SIZES.items():
            with self.subTest(engine=engine):
                with fake_engine(
                    "pythainlp.tokenize.wtsplit", "tokenize"
                ) as rec:
                    self.assertEqual(
                        paragraph_tokenize(
                            TEXT,
                            engine=engine,
                            paragraph_threshold=0.2,
                            style="opening",
                        ),
                        FAKE_RESULT,
                    )
                self.assertEqual(
                    rec.calls,
                    [
                        (
                            (TEXT,),
                            {
                                "size": size,
                                "tokenize": "paragraph",
                                "paragraph_threshold": 0.2,
                                "style": "opening",
                            },
                        )
                    ],
                )
        with fake_engine("pythainlp.tokenize.wtsplit", "tokenize") as rec:
            paragraph_tokenize(TEXT)
        self.assertEqual(rec.calls[0][1]["size"], "mini")
        for engine in ("XX", "", "WTP"):
            with self.subTest(engine=engine):
                with self.assertRaises(ValueError) as cm:
                    paragraph_tokenize(TEXT, engine=engine)
                self.assertEqual(str(cm.exception), not_found(engine))


class WordDetokenizeTestCase(unittest.TestCase):
    def test_golden(self) -> None:
        cases: tuple[tuple[Any, list[list[str]]], ...] = (
            (["ผม", "เลี้ยง", "5", "ตัว"], [["ผม", "เลี้ยง", " ", "5", " ", "ตัว"]]),
            (["a", "b"], [["a", " ", "b"]]),
            (["ก", "ๆ", "ข"], [["ก", " ", "ๆ", " ", "ข"]]),
            (["ก", " ", "ๆ", "ข"], [["ก", " ", "ๆ", " ", "ข"]]),
            (["ก", "ๆ", " ", "ข"], [["ก", " ", "ๆ", " ", "ข"]]),
            (["ก", "ๆ", " ", " ", "ข"], [["ก", " ", "ๆ", " ", " ", "ข"]]),
            ([" ", " ", "ก"], [[" ", " ", "ก"]]),
            (["ก", " ", " ", " ", "ข"], [["ก", " ", " ", " ", "ข"]]),
            (["", "", " ", "a"], [[" ", "a"]]),
            (["a", "", "b"], [["a", " ", "b"]]),
            (["ก", "", "ข"], [["ก", "ข"]]),
            (["ก", "ๆ", "", "ข"], [["ก", " ", "ๆ", "ข"]]),
            (["ก", " ", "", " ", "ข"], [["ก", " ", " ", "ข"]]),
            (["ๆ", "ๆ", "ก"], [["ๆ", " ", "ๆ", " ", "ก"]]),
            (["1", "ๆ", "ก"], [["1", " ", "ๆ", "ก"]]),
            (["ก", "1", " ", "ข"], [["ก", " ", "1", " ", " ", "ข"]]),
            (["ก", "\n", "ข"], [["ก", "\n", "ข"]]),
            (["ก", "ข", "ค"], [["ก", "ข", "ค"]]),
            ([""], [[]]),
            ([["ก", "1"], ["x", "y"]], [["ก", " ", "1"], ["x", " ", "y"]]),
            ([["ก"], []], [["ก"], []]),
        )
        for segments, expected in cases:
            with self.subTest(segments=segments):
                self.assertEqual(word_detokenize(segments, "list"), expected)
                text = " ".join("".join(s) for s in expected)
                self.assertEqual(word_detokenize(segments), text)
                self.assertEqual(word_detokenize(segments, "other"), text)

    def test_empty(self) -> None:
        self.assertEqual(word_detokenize([]), "")
        self.assertEqual(word_detokenize([], "list"), [])
        self.assertEqual(word_detokenize([], "other"), [])
        self.assertEqual(word_detokenize(None), "")  # type: ignore[arg-type]

    def test_wrong_word_type(self) -> None:
        self.assertEqual(word_detokenize([["ก", 0, "ข"]]), "กข")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            word_detokenize([["ก", 5]])  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
