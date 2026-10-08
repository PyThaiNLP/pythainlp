# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Test CRF model weight loading edge cases."""

import gzip
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from pythainlp.tag.crf import CRFTagger, _extract_item_features
from pythainlp.tag.thainer import ThaiNameTagger
from pythainlp.tokenize import ssg

MODEL_DATA = {
    "labels": ["O"],
    "transitions": {},
    "state_features": {},
}


class CRFWeightsTestCase(unittest.TestCase):
    def test_extract_numeric_features(self) -> None:
        self.assertEqual(
            _extract_item_features(
                {
                    "int": 2,
                    "float": 0.5,
                    "zero": 0,
                    "true": True,
                    "false": False,
                    "text": "value",
                    "unsupported": None,
                }
            ),
            [
                ("int", 2.0),
                ("float", 0.5),
                ("true", 1.0),
                ("text:value", 1.0),
            ],
        )

    def test_resolves_legacy_model_path_to_gzipped_json(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            model_path = Path(temp_dir) / "model.crfsuite"
            weights_path = model_path.with_suffix(".json.gz")
            with gzip.open(weights_path, "wt", encoding="utf-8") as file_obj:
                json.dump(MODEL_DATA, file_obj)

            tagger = CRFTagger(str(model_path))

        self.assertEqual(tagger.labels, ["O"])

    def test_resolves_legacy_model_path_to_json(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            model_path = Path(temp_dir) / "model.model"
            weights_path = model_path.with_suffix(".json")
            weights_path.write_text(json.dumps(MODEL_DATA), encoding="utf-8")

            tagger = CRFTagger(str(model_path))

        self.assertEqual(tagger.labels, ["O"])

    def test_loads_crfsuite_sidecar_appended_to_model_path(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            model_path = Path(temp_dir) / "model.crfsuite"
            model_path.write_bytes(b"lCRF binary model")
            weights_path = Path(f"{model_path}.json.gz")
            with gzip.open(weights_path, "wt", encoding="utf-8") as file_obj:
                json.dump(MODEL_DATA, file_obj)

            tagger = CRFTagger()
            tagger.open(str(model_path))

        self.assertEqual(tagger.labels, ["O"])

    def test_loads_crfsuite_sidecar_with_replaced_suffix(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            model_path = Path(temp_dir) / "model.model"
            model_path.write_bytes(b"lCRF binary model")
            weights_path = model_path.with_suffix(".json.gz")
            with gzip.open(weights_path, "wt", encoding="utf-8") as file_obj:
                json.dump(MODEL_DATA, file_obj)

            tagger = CRFTagger()
            tagger.open(str(model_path))

        self.assertEqual(tagger.labels, ["O"])

    def test_loads_bundled_thainer_weights_for_binary_model(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            model_path = Path(temp_dir) / "thainer_legacy.model"
            model_path.write_bytes(b"lCRF binary model")
            bundled_path = Path(temp_dir) / "thainer_crf_1_5_1.json.gz"
            with gzip.open(bundled_path, "wt", encoding="utf-8") as file_obj:
                json.dump(MODEL_DATA, file_obj)

            with patch("pythainlp.corpus.corpus_path", return_value=temp_dir):
                tagger = CRFTagger()
                tagger.open(str(model_path))

        self.assertEqual(tagger.labels, ["O"])

    def test_rejects_binary_crfsuite_without_weights(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            model_path = Path(temp_dir) / "model.crfsuite"
            model_path.write_bytes(b"lCRF binary model")
            with self.assertRaisesRegex(ValueError, "binary CRFsuite format"):
                CRFTagger().open(str(model_path))

    def test_rejects_thainer_binary_without_bundled_weights(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            model_path = Path(temp_dir) / "thainer_legacy.model"
            model_path.write_bytes(b"lCRF binary model")
            with patch("pythainlp.corpus.corpus_path", return_value=temp_dir):
                with self.assertRaisesRegex(
                    ValueError, "binary CRFsuite format"
                ):
                    CRFTagger().open(str(model_path))

    def test_loads_plain_json_weights(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            model_path = Path(temp_dir) / "model.json"
            model_path.write_text(json.dumps(MODEL_DATA), encoding="utf-8")

            tagger = CRFTagger(str(model_path))

        self.assertEqual(tagger.labels, ["O"])

    def test_thainer_falls_back_to_version_1_5_corpus(self) -> None:
        with (
            patch(
                "pythainlp.tag.thainer.get_corpus_path",
                side_effect=[None, "/unused/thainer.model"],
            ) as get_corpus_path,
            patch.object(CRFTagger, "open") as open_model,
        ):
            tagger = ThaiNameTagger(version="1.5")

        self.assertEqual(tagger.pos_tag_name, "blackboard")
        self.assertEqual(get_corpus_path.call_count, 2)
        open_model.assert_called_once_with("/unused/thainer.model")

    def test_thainer_raises_when_both_corpora_are_missing(self) -> None:
        with patch("pythainlp.tag.thainer.get_corpus_path", return_value=None):
            with self.assertRaisesRegex(FileNotFoundError, "Corpus 'thainer'"):
                ThaiNameTagger(version="1.5")

    def test_syllable_tokenize_alias_forwards_text(self) -> None:
        expected = ["สวัสดี"]
        with patch(
            "pythainlp.tokenize.ssg.segment", return_value=expected
        ) as segment:
            self.assertIs(ssg.syllable_tokenize("สวัสดี"), expected)
        segment.assert_called_once_with("สวัสดี")


if __name__ == "__main__":
    unittest.main()
