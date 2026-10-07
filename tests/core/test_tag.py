# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

import unittest
from importlib.util import find_spec
from os import path

from pythainlp.corpus import download
from pythainlp.tag import (
    NER,
    EntitySpan,
    PerceptronTagger,
    perceptron,
    pos_tag,
    pos_tag_sents,
    tag_provinces,
    unigram,
)
from pythainlp.tag._utils import _iob_to_markup

TEST_TOKENS = ["ผม", "รัก", "คุณ"]

_PHAYATHAIBERT_DEPENDENCIES = (
    "huggingface_hub",
    "numpy",
    "onnxruntime",
    "tokenizers",
)


class TagTestCase(unittest.TestCase):
    """Test pythainlp.tag.pos_tag."""

    @classmethod
    def setUpClass(cls) -> None:
        """Download required corpora before running tests."""
        download("blackboard_unigram_tagger")

    def test_pos_tag(self):
        self.assertEqual(pos_tag(None), [])  # type: ignore[arg-type]
        self.assertEqual(pos_tag([]), [])
        self.assertEqual(
            pos_tag(["นักเรียน", "ถาม", "ครู"]),
            [("นักเรียน", "NCMN"), ("ถาม", "VACT"), ("ครู", "NCMN")],
        )
        self.assertEqual(
            len(pos_tag(["การ", "เดินทาง", "มี", "ความ", "ท้าทาย"])), 5
        )

        self.assertEqual(unigram.tag(None, corpus="pud"), [])  # type: ignore[arg-type]
        self.assertEqual(unigram.tag([], corpus="pud"), [])
        self.assertEqual(unigram.tag(None, corpus="orchid"), [])  # type: ignore[arg-type]
        self.assertEqual(unigram.tag([], corpus="orchid"), [])
        self.assertEqual(unigram.tag(None, corpus="blackboard"), [])  # type: ignore[arg-type]
        self.assertEqual(unigram.tag([], corpus="blackboard"), [])
        self.assertEqual(unigram.tag(None, corpus="tud"), [])  # type: ignore[arg-type]
        self.assertEqual(unigram.tag([], corpus="tud"), [])
        self.assertIsNotNone(
            pos_tag(TEST_TOKENS, engine="unigram", corpus="orchid")
        )
        self.assertIsNotNone(
            pos_tag(TEST_TOKENS, engine="unigram", corpus="orchid_ud")
        )
        self.assertIsNotNone(
            pos_tag(TEST_TOKENS, engine="unigram", corpus="pud")
        )
        self.assertIsNotNone(pos_tag([""], engine="unigram", corpus="pud"))
        self.assertIsNotNone(
            pos_tag(TEST_TOKENS, engine="unigram", corpus="blackboard")
        )
        self.assertIsNotNone(
            pos_tag([""], engine="unigram", corpus="blackboard")
        )
        self.assertIsNotNone(
            pos_tag([""], engine="unigram", corpus="blackboard_ud")
        )
        self.assertIsNotNone(
            pos_tag(TEST_TOKENS, engine="unigram", corpus="tdtb")
        )
        self.assertIsNotNone(pos_tag([""], engine="unigram", corpus="tdtb"))
        self.assertIsNotNone(
            pos_tag(TEST_TOKENS, engine="unigram", corpus="tud")
        )
        self.assertIsNotNone(pos_tag([""], engine="unigram", corpus="tud"))
        self.assertEqual(
            pos_tag(["คุณ", "กำลัง", "ประชุม"], engine="unigram"),
            [("คุณ", "PPRS"), ("กำลัง", "XVBM"), ("ประชุม", "VACT")],
        )

        self.assertTrue(
            pos_tag(["การ", "รัฐประหาร"], corpus="orchid_ud")[0][1], "NOUN"
        )
        self.assertTrue(
            pos_tag(["ความ", "พอเพียง"], corpus="orchid_ud")[0][1], "NOUN"
        )

        self.assertEqual(pos_tag_sents(None), [])  # type: ignore[arg-type]
        self.assertEqual(pos_tag_sents([]), [])
        self.assertEqual(
            pos_tag_sents([["ผม", "กิน", "ข้าว"], ["แมว", "วิ่ง"]]),
            [
                [("ผม", "PPRS"), ("กิน", "VACT"), ("ข้าว", "NCMN")],
                [("แมว", "NCMN"), ("วิ่ง", "VACT")],
            ],
        )

    def test_pos_tag_error_handling(self):
        with self.assertRaises(ValueError):
            pos_tag(
                ["ทดสอบ"], engine="invalid_engine", corpus="invalid_corpus"
            )
        with self.assertRaises(ValueError):
            pos_tag(["ทดสอบ"], engine="unigram", corpus="invalid_corpus")

    def test_NER_error_handling(self):
        with self.assertRaises(ValueError):
            NER(engine="xx_non_existing", corpus="thainer")
        with self.assertRaises(ValueError):
            NER(engine="xx_non_existing", corpus="thainer-v2")
        with self.assertRaises(ValueError):
            NER(engine="xx_non_existing", corpus="xx_non_existing")


class PerceptronTaggerTestCase(unittest.TestCase):
    """
    Test pythainlp.tag.PerceptronTagger.

    :param unittest: _description_
    :type unittest: _type_
    """

    @classmethod
    def setUpClass(cls) -> None:
        """Download required corpora before running tests."""
        download("blackboard_pt_tagger")

    def test_perceptron_tagger(self):
        self.assertEqual(perceptron.tag(None, corpus="orchid"), [])  # type: ignore[arg-type]
        self.assertEqual(perceptron.tag([], corpus="orchid"), [])
        self.assertEqual(perceptron.tag(None, corpus="orchid_ud"), [])  # type: ignore[arg-type]
        self.assertEqual(perceptron.tag([], corpus="orchid_ud"), [])
        self.assertEqual(perceptron.tag(None, corpus="pud"), [])  # type: ignore[arg-type]
        self.assertEqual(perceptron.tag([], corpus="pud"), [])
        self.assertEqual(perceptron.tag(None, corpus="blackboard"), [])  # type: ignore[arg-type]
        self.assertEqual(perceptron.tag([], corpus="blackboard"), [])
        self.assertEqual(perceptron.tag(None, corpus="tud"), [])  # type: ignore[arg-type]
        self.assertEqual(perceptron.tag([], corpus="tud"), [])

        self.assertIsNotNone(
            pos_tag(TEST_TOKENS, engine="perceptron", corpus="orchid")
        )
        self.assertIsNotNone(
            pos_tag(TEST_TOKENS, engine="perceptron", corpus="orchid_ud")
        )
        self.assertIsNotNone(
            pos_tag(TEST_TOKENS, engine="perceptron", corpus="pud")
        )
        self.assertIsNotNone(
            pos_tag(TEST_TOKENS, engine="perceptron", corpus="blackboard")
        )
        self.assertIsNotNone(
            pos_tag(TEST_TOKENS, engine="perceptron", corpus="blackboard_ud")
        )
        self.assertIsNotNone(
            pos_tag(TEST_TOKENS, engine="perceptron", corpus="tdtb")
        )
        self.assertIsNotNone(
            pos_tag(TEST_TOKENS, engine="perceptron", corpus="tdtb")
        )
        self.assertIsNotNone(
            pos_tag(TEST_TOKENS, engine="perceptron", corpus="tud")
        )

    def test_perceptron_tagger_custom(self):
        """Test pythainlp.tag.PerceptronTagger."""
        tagger = PerceptronTagger()
        # train data, with "กิน" > 20 instances to trigger conditions
        # in _make_tagdict()
        data = [
            [("คน", "N"), ("เดิน", "V")],
            [("ฉัน", "N"), ("เดิน", "V")],
            [("แมว", "N"), ("เดิน", "V")],
            [("คน", "N"), ("วิ่ง", "V")],
            [("ปลา", "N"), ("ว่าย", "V")],
            [("นก", "N"), ("บิน", "V")],
            [("คน", "N"), ("พูด", "V")],
            [("C-3PO", "N"), ("พูด", "V")],
            [("คน", "N"), ("กิน", "V")],
            [("แมว", "N"), ("กิน", "V")],
            [("นก", "N"), ("กิน", "V")],
            [("นก", "N"), ("นก", "V")],
            [("คน", "N"), ("นก", "V")],
            [("คน", "N"), ("กิน", "V"), ("นก", "N")],
            [("คน", "N"), ("กิน", "V"), ("ปลา", "N")],
            [("นก", "N"), ("กิน", "V"), ("ปลา", "N")],
            [("คน", "N"), ("กิน", "V"), ("กาแฟ", "N")],
            [("คน", "N"), ("คน", "V"), ("กาแฟ", "N")],
            [("พระ", "N"), ("ฉัน", "V"), ("กาแฟ", "N")],
            [("พระ", "N"), ("คน", "V"), ("กาแฟ", "N")],
            [("พระ", "N"), ("ฉัน", "V"), ("ข้าว", "N")],
            [("ฉัน", "N"), ("กิน", "V"), ("ข้าว", "N")],
            [("เธอ", "N"), ("กิน", "V"), ("ปลา", "N")],
            [("ปลา", "N"), ("กิน", "V"), ("แมลง", "N")],
            [("แมวน้ำ", "N"), ("กิน", "V"), ("ปลา", "N")],
            [("หนู", "N"), ("กิน", "V")],
            [("เสือ", "N"), ("กิน", "V")],
            [("ยีราฟ", "N"), ("กิน", "V")],
            [("แรด", "N"), ("กิน", "V")],
            [("หมู", "N"), ("กิน", "V")],
            [("แมลง", "N"), ("กิน", "V")],
            [("สิงโต", "N"), ("กิน", "V")],
            [("เห็บ", "N"), ("กิน", "V")],
            [("เหา", "N"), ("กิน", "V")],
            [("เต่า", "N"), ("กิน", "V")],
            [("กระต่าย", "N"), ("กิน", "V")],
            [("จิ้งจก", "N"), ("กิน", "V")],
            [("หมี", "N"), ("กิน", "V")],
            [("หมา", "N"), ("กิน", "V")],
            [("ตะพาบ", "N"), ("กิน", "V")],
            [("เม่น", "N"), ("กิน", "V")],
            [("หนอน", "N"), ("กิน", "V")],
            [("ปี", "N"), ("2021", "N")],
        ]
        filename = "ptagger_temp4XcDf.json"
        tagger.train(data, save_loc=filename)
        self.assertTrue(path.exists(filename))

        words = ["นก", "เดิน"]
        word_tags = tagger.tag(words)
        self.assertEqual(len(words), len(word_tags))

        words2, _ = zip(*word_tags)
        self.assertEqual(words, list(words2))

        with self.assertRaises(IOError):
            tagger.load("ptagger_notexistX4AcOcX.pkl")  # file does not exist


class TagLocationsTestCase(unittest.TestCase):
    """Test pythainlp.tag.locations."""

    def test_ner_locations(self):
        self.assertEqual(
            tag_provinces(["หนองคาย", "น่าอยู่"]),
            [("หนองคาย", "B-LOCATION"), ("น่าอยู่", "O")],
        )


class BlackboardPreProcessTestCase(unittest.TestCase):
    """Tests for pythainlp.tag.blackboard.pre_process."""

    def setUp(self):
        from pythainlp.tag.blackboard import pre_process

        self.pre_process = pre_process

    def test_space_is_escaped(self):
        self.assertEqual(self.pre_process([" "]), ["_"])

    def test_regular_words_unchanged(self):
        self.assertEqual(
            self.pre_process(["ผม", "รัก", "คุณ"]), ["ผม", "รัก", "คุณ"]
        )

    def test_mixed_space_and_words(self):
        self.assertEqual(
            self.pre_process(["ผม", " ", "คุณ"]), ["ผม", "_", "คุณ"]
        )

    def test_multiple_spaces(self):
        self.assertEqual(self.pre_process([" ", " "]), ["_", "_"])

    def test_empty_list(self):
        self.assertEqual(self.pre_process([]), [])

    def test_non_space_special_chars_unchanged(self):
        self.assertEqual(
            self.pre_process(["_"]), ["_"]
        )  # already escaped form

    def test_single_thai_word(self):
        self.assertEqual(self.pre_process(["สวัสดี"]), ["สวัสดี"])


class BlackboardPostProcessTestCase(unittest.TestCase):
    """Tests for pythainlp.tag.blackboard.post_process."""

    def setUp(self):
        from pythainlp.tag.blackboard import TO_UD, post_process

        self.post_process = post_process
        self.TO_UD = TO_UD

    def test_unescape_underscore_to_space(self):
        result = self.post_process([("_", "NN"), ("คน", "NN")])
        self.assertEqual(result, [(" ", "NN"), ("คน", "NN")])

    def test_regular_words_pass_through(self):
        result = self.post_process([("ผม", "PPRS"), ("รัก", "VACT")])
        self.assertEqual(result, [("ผม", "PPRS"), ("รัก", "VACT")])

    def test_unescape_to_space_with_ud(self):
        result = self.post_process([("_", "NN")], to_ud=True)
        self.assertEqual(result, [(" ", "NOUN")])

    def test_regular_word_to_ud(self):
        result = self.post_process([("คน", "NN")], to_ud=True)
        self.assertEqual(result, [("คน", "NOUN")])

    def test_all_to_ud_mappings(self):
        for bb_tag, ud_tag in self.TO_UD.items():
            if bb_tag == "":
                continue  # skip empty-string sentinel
            result = self.post_process([("word", bb_tag)], to_ud=True)
            self.assertEqual(
                result[0][1],
                ud_tag,
                f"TO_UD mapping failed for tag '{bb_tag}': "
                f"expected '{ud_tag}', got '{result[0][1]}'",
            )

    def test_empty_list(self):
        self.assertEqual(self.post_process([]), [])
        self.assertEqual(self.post_process([], to_ud=True), [])

    def test_no_ud_default_preserves_tag(self):
        result = self.post_process([("คน", "VV")])
        self.assertEqual(result[0][1], "VV")


class TagNNERTestCase(unittest.TestCase):
    """Test pythainlp.tag.thai_nner."""

    def test_get_top_level_entities(self):
        from pythainlp.tag.thai_nner import get_top_level_entities

        # Test with nested entities
        entities = [
            EntitySpan(text=["ห้า"], span=[7, 9], entity_type="cardinal"),
            EntitySpan(text=["ห้า", "โมง"], span=[7, 11], entity_type="time"),
            EntitySpan(text=["โมง"], span=[9, 11], entity_type="unit"),
        ]
        top_entities = get_top_level_entities(entities)
        # Should only return 'time' as it contains the others
        self.assertEqual(len(top_entities), 1)
        self.assertEqual(top_entities[0]["entity_type"], "time")
        self.assertEqual(top_entities[0]["span"], [7, 11])

        # Test with non-overlapping entities
        entities = [
            EntitySpan(text=["วัน"], span=[0, 1], entity_type="time"),
            EntitySpan(text=["เดือน"], span=[2, 3], entity_type="time"),
        ]
        top_entities = get_top_level_entities(entities)
        # Both should be returned as neither contains the other
        self.assertEqual(len(top_entities), 2)

        # Test with empty list
        self.assertEqual(get_top_level_entities([]), [])

        # Test with single entity
        entities = [{"text": ["test"], "span": [0, 1], "entity_type": "test"}]
        top_entities = get_top_level_entities(entities)
        self.assertEqual(len(top_entities), 1)
        self.assertEqual(top_entities[0], entities[0])

    def test_entities_to_iob(self):
        from pythainlp.tag.thai_nner import _entities_to_iob

        # Test basic IOB conversion
        tokens = ["วัน", "ที่", " ", "5", " ", "เมษายน"]
        entities = [
            EntitySpan(
                text=["5", " ", "เมษายน"], span=[3, 6], entity_type="date"
            )
        ]
        result = _entities_to_iob(tokens, entities)

        # Check format
        self.assertEqual(len(result), len(tokens))
        self.assertEqual(result[0], ("วัน", "O"))
        self.assertEqual(result[1], ("ที่", "O"))
        self.assertEqual(result[2], (" ", "O"))
        self.assertEqual(result[3], ("5", "B-DATE"))
        self.assertEqual(result[4], (" ", "I-DATE"))
        self.assertEqual(result[5], ("เมษายน", "I-DATE"))

    def test_entities_to_html(self):
        from pythainlp.tag.thai_nner import _entities_to_html

        # Test basic HTML conversion
        tokens = ["วัน", "ที่", " ", "5", " ", "เมษายน"]
        entities = [
            EntitySpan(
                text=["5", " ", "เมษายน"], span=[3, 6], entity_type="date"
            )
        ]
        result = _entities_to_html(tokens, entities)

        # Check format
        expected = "วันที่ <DATE>5 เมษายน</DATE>"
        self.assertEqual(result, expected)

        # Test with multiple entities
        tokens = ["นาย", "สมชาย", " ", "อยู่", "ที่", "กรุงเทพ"]
        entities = [
            EntitySpan(
                text=["นาย", "สมชาย"], span=[0, 2], entity_type="person"
            ),
            EntitySpan(text=["กรุงเทพ"], span=[5, 6], entity_type="location"),
        ]
        result = _entities_to_html(tokens, entities)
        expected = "<PERSON>นายสมชาย</PERSON> อยู่ที่<LOCATION>กรุงเทพ</LOCATION>"
        self.assertEqual(result, expected)


class IobToMarkupTestCase(unittest.TestCase):
    """Test pythainlp.tag._utils._iob_to_markup."""

    def test_iob_to_markup(self):
        cases = [
            ("empty", [], ""),
            ("no entity", [("ก", "O"), ("ข", "O")], "กข"),
            ("single", [("ก", "B-A")], "<A>ก</A>"),
            ("entity then O", [("ก", "B-A"), ("ข", "O")], "<A>ก</A>ข"),
            ("inside", [("ก", "B-A"), ("ข", "I-A")], "<A>กข</A>"),
            (
                "adjacent entities",
                [("ก", "B-A"), ("ข", "B-B")],
                "<A>ก</A><B>ข</B>",
            ),
            (
                "leading O",
                [("ก", "O"), ("ข", "B-A"), ("ค", "I-A"), ("ง", "O")],
                "ก<A>ขค</A>ง",
            ),
            # Quirks kept from the original loops
            ("I without B", [("ก", "I-A"), ("ข", "O")], "กข"),
            (
                "I with other type",
                [("ก", "B-A"), ("ข", "I-B")],
                "<A>กข</A>",
            ),
            ("unknown tag", [("ก", "B-A"), ("ข", "X")], "<A>กข</A>"),
            ("empty type", [("ก", "B-")], "<>ก"),
            (
                "empty type reopened",
                [("ก", "B-"), ("ข", "B-A")],
                "<>ก<A>ข</A>",
            ),
            (
                "spaces and empty words",
                [(" ", "B-A"), ("", "I-A"), (" ", "O")],
                "<A> </A> ",
            ),
            (
                "O with trailing space",
                [("ก", "B-A"), ("ข", "O ")],
                "<A>กข</A>",
            ),
        ]
        for name, tagged, expected in cases:
            with self.subTest(name):
                self.assertEqual(_iob_to_markup(tagged), expected)

    def test_iob_to_markup_long_input(self):
        tagged = [("ก", "B-A")] + [("ก", "I-A")] * 10000
        self.assertEqual(_iob_to_markup(tagged), "<A>" + "ก" * 10001 + "</A>")


class PhayaThaiBERTHelperTestCase(unittest.TestCase):
    """Test the pure-Python helpers of pythainlp.tag.phayathaibert_onnx"""

    def test_first_subword_labels(self):
        from pythainlp.tag.phayathaibert_onnx import _first_subword_labels

        id2label = {0: "NOUN", 1: "VERB", 2: "PRON"}
        # <s> word0-a word0-b word1 </s>
        word_ids = [None, 0, 0, 1, None]
        label_ids = [1, 2, 1, 0, 1]
        self.assertEqual(
            _first_subword_labels(word_ids, label_ids, 2, id2label),
            ["PRON", "NOUN"],
        )

    def test_first_subword_labels_word_without_subword(self):
        from pythainlp.tag.phayathaibert_onnx import _first_subword_labels

        id2label = {0: "NOUN", 1: "VERB"}
        # word 1 produced no subword at all
        word_ids = [None, 0, 2, None]
        label_ids = [0, 0, 1, 0]
        self.assertEqual(
            _first_subword_labels(word_ids, label_ids, 3, id2label),
            ["NOUN", "X", "VERB"],
        )

    def test_chunk_spans(self):
        from pythainlp.tag.phayathaibert_onnx import _chunk_spans

        cases = [
            ("empty", [], 5, []),
            ("fits in one", [3, 4, 5], 20, [(0, 3)]),
            ("exact fit", [3, 4], 7, [(0, 2)]),
            ("split at word boundaries", [3, 4, 5], 7, [(0, 2), (2, 3)]),
            (
                "oversized word gets own span",
                [3, 10, 2],
                5,
                [(0, 1), (1, 2), (2, 3)],
            ),
            ("oversized first word", [10, 1], 5, [(0, 1), (1, 2)]),
            ("word with no subword", [3, 0, 4], 7, [(0, 3)]),
        ]
        for name, counts, limit, expected in cases:
            with self.subTest(name):
                self.assertEqual(_chunk_spans(counts, limit), expected)

    def test_chunk_spans_exact_fit(self):
        from pythainlp.tag.phayathaibert_onnx import _chunk_spans

        self.assertEqual(_chunk_spans([3, 4], 7), [(0, 2)])

    def test_chunk_spans_zero_count_words(self):
        from pythainlp.tag.phayathaibert_onnx import _chunk_spans

        self.assertEqual(_chunk_spans([0, 3, 0, 4], 7), [(0, 4)])

    def test_is_blank(self):
        from pythainlp.tag.phayathaibert_onnx import _is_blank

        for word in ("", " ", "\n", " ", "　", "​", "﻿"):
            self.assertTrue(_is_blank(word), repr(word))
        for word in ("แมว", " แมว ", "a", "1", "​แมว"):
            self.assertFalse(_is_blank(word), repr(word))

    def test_tag_empty_list(self):
        from pythainlp.tag.phayathaibert_onnx import tag

        self.assertEqual(tag([]), [])

    def test_missing_dependency_error_before_download(self):
        import sys
        from unittest import mock

        from pythainlp.tag import phayathaibert_onnx

        for module in _PHAYATHAIBERT_DEPENDENCIES:
            with self.subTest(module):
                # Fake every dependency, so none is really imported (and
                # then unloaded) inside patch.dict.
                modules = {
                    m: mock.MagicMock() for m in _PHAYATHAIBERT_DEPENDENCIES
                }
                modules[module] = None
                with mock.patch.dict(sys.modules, modules):
                    with mock.patch(
                        "pythainlp.tag.phayathaibert_onnx.get_hf_hub"
                    ) as get_hf_hub:
                        with self.assertRaises(ImportError) as ctx:
                            phayathaibert_onnx.PhayaThaiBERTTagger()
                self.assertIn(
                    "pythainlp[phayathaibert_onnx]", str(ctx.exception)
                )
                get_hf_hub.assert_not_called()

    def _first_download_revision(self, **kwargs: str) -> object:
        """Return the revision PhayaThaiBERTTagger passes to get_hf_hub."""
        import sys
        from unittest import mock

        from pythainlp.tag import phayathaibert_onnx

        fake_modules = {
            m: mock.MagicMock() for m in _PHAYATHAIBERT_DEPENDENCIES
        }
        with mock.patch.dict(sys.modules, fake_modules):
            with mock.patch(
                "pythainlp.tag.phayathaibert_onnx.get_hf_hub",
                side_effect=RuntimeError("stop"),
            ) as get_hf_hub:
                with self.assertRaises(RuntimeError):
                    phayathaibert_onnx.PhayaThaiBERTTagger(**kwargs)
        return get_hf_hub.call_args.kwargs["revision"]

    def test_default_repo_is_pinned(self):
        from pythainlp.tag import phayathaibert_onnx

        self.assertEqual(
            self._first_download_revision(), phayathaibert_onnx._REVISION
        )

    def test_custom_repo_is_not_pinned_to_default_revision(self):
        self.assertIsNone(
            self._first_download_revision(repo_id="someone/other-model")
        )
        self.assertEqual(
            self._first_download_revision(
                repo_id="someone/other-model", revision="abc123"
            ),
            "abc123",
        )


class _FakeEncoding:
    """
    Encode each word as one subword per character.

    Only the first subword carries the word's label id (1 for words that
    start with "ก", 2 otherwise); the others carry 0, so tagging with any
    subword but the first gives the wrong tag.
    """

    def __init__(self, words):
        self.ids = [0]
        self.word_ids = [None]
        for i, word in enumerate(words):
            label_id = 1 if word.startswith("ก") else 2
            self.ids += [label_id] + [0] * (len(word) - 1)
            self.word_ids += [i] * len(word)
        self.ids.append(0)
        self.word_ids.append(None)
        self.attention_mask = [1] * len(self.ids)


class _FakeTokenizer:
    def encode(self, words, is_pretokenized=False):
        return _FakeEncoding(words)


class _FakeSession:
    """Predict the label id equal to each input id (one-hot logits)."""

    def __init__(self):
        self.lengths = []

    def run(self, output_names, feeds):
        import numpy as np

        ids = feeds["input_ids"]
        self.lengths.append(ids.shape[1])
        return [np.eye(3)[ids]]


class PhayaThaiBERTTaggerTestCase(unittest.TestCase):
    """Test pythainlp.tag.phayathaibert_onnx with a fake model."""

    def _tagger(self):
        from pythainlp.tag.phayathaibert_onnx import PhayaThaiBERTTagger

        tagger = PhayaThaiBERTTagger.__new__(PhayaThaiBERTTagger)
        tagger.session = _FakeSession()
        tagger.tokenizer = _FakeTokenizer()
        tagger.id2label = {0: "SCONJ", 1: "NOUN", 2: "VERB"}
        return tagger

    @unittest.skipUnless(find_spec("numpy"), "numpy is not installed")
    def test_tag(self):
        from unittest import mock

        from pythainlp.tag import phayathaibert_onnx

        cases = [
            ("short", ["กา", "ขาว"], 20, ["NOUN", "VERB"]),
            (
                "blank words skipped",
                ["กา", " ", "ขา", "", "​"],
                20,
                ["NOUN", "PUNCT", "VERB", "PUNCT", "PUNCT"],
            ),
            ("all blank", [" ", "﻿"], 20, ["PUNCT", "PUNCT"]),
            (
                "chunked",
                ["กา", "ขา", "ก", "ขาว", "กก", "ขข"],
                6,
                ["NOUN", "VERB", "NOUN", "VERB", "NOUN", "VERB"],
            ),
            ("overlong word", ["ก" * 20, "ขา"], 6, ["NOUN", "VERB"]),
            ("overlong last word", ["ขา", "ก" * 20], 6, ["VERB", "NOUN"]),
        ]
        for name, words, limit, expected in cases:
            with self.subTest(name):
                tagger = self._tagger()
                with mock.patch.object(
                    phayathaibert_onnx, "_MAX_SEQUENCE_LENGTH", limit
                ):
                    result = tagger.tag(words)
                self.assertEqual(result, list(zip(words, expected)))
                self.assertTrue(
                    all(n <= limit for n in tagger.session.lengths)
                )

    def test_init(self):
        import json
        import sys
        import tempfile
        from unittest import mock

        from pythainlp.tag import phayathaibert_onnx

        fake_modules = {
            m: mock.MagicMock() for m in _PHAYATHAIBERT_DEPENDENCIES
        }
        with tempfile.TemporaryDirectory() as tmp:
            config_path = path.join(tmp, "config.json")
            with open(config_path, "w", encoding="utf-8") as f:
                json.dump({"id2label": {"0": "NOUN", "1": "VERB"}}, f)

            def fake_get_hf_hub(repo_id, filename, revision=None):
                return config_path if filename == "config.json" else filename

            with mock.patch.dict(sys.modules, fake_modules):
                with mock.patch.object(
                    phayathaibert_onnx,
                    "get_hf_hub",
                    side_effect=fake_get_hf_hub,
                ) as get_hf_hub:
                    tagger = phayathaibert_onnx.PhayaThaiBERTTagger()
        self.assertEqual(
            [c.args[1] for c in get_hf_hub.call_args_list],
            ["model.onnx", "tokenizer.json", "config.json"],
        )
        self.assertEqual(tagger.id2label, {0: "NOUN", 1: "VERB"})
        # tokenizer.json truncates at 510 tokens; the tagger must undo it.
        tagger.tokenizer.no_truncation.assert_called_once_with()
        tagger.tokenizer.no_padding.assert_called_once_with()

    def test_tag_function_loads_tagger_once(self):
        from unittest import mock

        from pythainlp.tag import phayathaibert_onnx

        with mock.patch.object(phayathaibert_onnx, "_TAGGER", None):
            with mock.patch.object(
                phayathaibert_onnx, "PhayaThaiBERTTagger"
            ) as tagger_class:
                tagger_class.return_value.tag.return_value = [("ก", "NOUN")]
                for _ in range(2):
                    self.assertEqual(
                        phayathaibert_onnx.tag(["ก"], corpus="orchid"),
                        [("ก", "NOUN")],
                    )
                tagger_class.assert_called_once_with()

    def test_pos_tag_phayathaibert_uses_tud(self):
        from unittest import mock

        with mock.patch(
            "pythainlp.tag.phayathaibert_onnx.tag",
            return_value=[("ก", "NOUN")],
        ) as tag:
            self.assertEqual(
                pos_tag(["ก"], engine="phayathaibert", corpus="orchid"),
                [("ก", "NOUN")],
            )
        tag.assert_called_once_with(["ก"], corpus="tud")

    def test_pos_tag_transformers_engine_lookup(self):
        import sys
        from unittest import mock

        from pythainlp.tag import pos_tag_transformers

        transformers = mock.MagicMock()
        pipeline = transformers.TokenClassificationPipeline.return_value
        pipeline.return_value = [{"word": "กิน", "entity_group": "VERB"}]
        supported = [
            ("bert", "blackboard", "lunarlist/pos_thai"),
            ("phayathai", "blackboard", "lunarlist/pos_thai_phayathai"),
            (
                "wangchanberta",
                "pud",
                "Pavarissy/wangchanberta-ud-thai-pud-upos",
            ),
            ("mdeberta", "pud", "Pavarissy/mdeberta-v3-ud-thai-pud-upos"),
            (
                "phayathaibert",
                "tud",
                "nlp-chula/phayathaibert-thai-pos-tagger",
            ),
        ]
        unsupported = [
            ("phayathaibert", "pud"),
            ("bert", "tud"),
            ("bert", "non-existing corpus"),
        ]
        auto_tokenizer = transformers.AutoTokenizer.from_pretrained
        with mock.patch.dict(sys.modules, {"transformers": transformers}):
            for engine, corpus, model_name in supported:
                with self.subTest(engine=engine, corpus=corpus):
                    self.assertEqual(
                        pos_tag_transformers(
                            "กิน", engine=engine, corpus=corpus
                        ),
                        [[("กิน", "VERB")]],
                    )
                    auto_tokenizer.assert_called_with(
                        model_name, revision=None
                    )
            for engine, corpus in unsupported:
                with self.subTest(engine=engine, corpus=corpus):
                    with self.assertRaises(ValueError):
                        pos_tag_transformers(
                            "กิน", engine=engine, corpus=corpus
                        )
