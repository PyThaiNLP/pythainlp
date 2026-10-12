# SPDX-FileCopyrightText: 2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

"""Test Laya code paths without downloading model files."""

from __future__ import annotations

import json
import tempfile
import types
import unittest
from pathlib import Path
from typing import Any, cast
from unittest.mock import Mock, patch

import numpy as np

from pythainlp.classify import Laya, LayaModel
from pythainlp.classify.laya import (
    _build_prefix,
    _build_sequence,
    _clamp_temperature,
    _collate_items,
    _confidence_from_probs,
    _normalize_choice_criteria,
    _render_criterion,
    _render_options,
    _serialize_state,
    _temp_bucket,
    _TokenizerWrapper,
)


class FakeTokenizer(_TokenizerWrapper):
    """Provide predictable token IDs without a tokenizer dependency."""

    def __init__(self) -> None:
        self.cls_token = "[CLS]"  # noqa: S105
        self.cls_token_id = 101
        self.sep_token = "[SEP]"  # noqa: S105
        self.sep_token_id = 102
        self.pad_token = "[PAD]"  # noqa: S105
        self.pad_token_id = 0
        self.mask_token = "[MASK]"  # noqa: S105
        self.mask_token_id = 103

    def __call__(
        self, text: str, add_special_tokens: bool = False
    ) -> dict[str, list[int]]:
        return {"input_ids": [ord(char) for char in text]}


class FakeSession:
    """Return deterministic logits for batched model calls."""

    def run(
        self, output_names: Any, batch: dict[str, Any]
    ) -> tuple[np.ndarray[Any, Any], np.ndarray[Any, Any]]:
        rows = batch["input_ids"].shape[0]
        logits = np.tile(np.array([[2.0, 0.0]], dtype=np.float32), (rows, 1))
        actions = np.zeros((rows, 2), dtype=np.float32)
        return logits, actions


class LayaHelpersTestCaseN(unittest.TestCase):
    """Test Laya helpers and inference without loading model files."""

    @staticmethod
    def make_model(batch_size: int = 2) -> LayaModel:
        model = object.__new__(LayaModel)
        model.batch_size = batch_size
        model._max_len = 128
        model._head_max_len = 64
        model._temperature = [1.0, 1.0, 1.0]
        model._temperature_by_options = {}
        model._tokenizer = FakeTokenizer()
        model._session = FakeSession()
        return model

    def test_scalar_helpers(self) -> None:
        cases = (
            ("invalid", 1.0),
            (None, 1.0),
            (float("nan"), 1.0),
            (float("inf"), 1.0),
            (0.1, 0.5),
            (10.0, 5.0),
            (2.0, 2.0),
        )
        for value, expected in cases:
            with self.subTest(value=value):
                self.assertEqual(_clamp_temperature(value), expected)

        self.assertEqual(_confidence_from_probs(np.array([1.0]), 1), 1.0)
        self.assertAlmostEqual(
            _confidence_from_probs(np.array([0.5, 0.5]), 2), 0
        )
        self.assertAlmostEqual(
            _confidence_from_probs(np.array([1.0, 0.0]), 2), 1
        )
        for count, expected_suffix in (
            (2, "2"),
            (5, "3-5"),
            (10, "6-10"),
            (11, "11+"),
        ):
            self.assertTrue(_temp_bucket(0, count).endswith(expected_suffix))
        self.assertEqual(_temp_bucket(1, 3), "score:3-5")
        self.assertEqual(_temp_bucket(2, 3), "noul:3-5")
        self.assertEqual(_serialize_state("text"), "text")
        self.assertEqual(
            _serialize_state({"ข้อความ": "ไทย"}), '{"ข้อความ": "ไทย"}'
        )
        self.assertEqual(_render_criterion("text"), "text")
        self.assertEqual(_render_criterion(["a", "b"]), '["a", "b"]')

    def test_choice_normalization_and_question_validation(self) -> None:
        self.assertEqual(
            _normalize_choice_criteria(["A", "B"]), {"A": None, "B": None}
        )
        self.assertEqual(
            _normalize_choice_criteria({"A": "first"}), {"A": "first"}
        )
        for criteria, message in (
            ([], "must not be empty"),
            ([1], "must be strings"),
            (["A", "A"], "must be unique"),
            ({}, "non-empty dictionary"),
            ({1: "bad"}, "must be strings"),
            (None, "non-empty dictionary"),
        ):
            with self.subTest(criteria=criteria):
                with self.assertRaisesRegex(ValueError, message):
                    _normalize_choice_criteria(criteria)

        good_questions = (
            (
                {
                    "type": "choice",
                    "instructions": "choose",
                    "criteria": ["A", "B"],
                },
                {
                    "t": "choice",
                    "ins": "choose",
                    "crit": {"A": None, "B": None},
                },
            ),
            (
                {
                    "type": "score",
                    "instructions": {"score": "quality"},
                    "criteria": ["low", "high"],
                },
                {
                    "t": "score",
                    "ins": '{"score": "quality"}',
                    "crit": ["low", "high"],
                },
            ),
            (
                {"type": "noul", "instructions": "valid?", "criteria": None},
                {"t": "noul", "ins": "valid?", "crit": None},
            ),
        )
        for question, expected in good_questions:
            self.assertEqual(LayaModel._to_internal(question), expected)

        bad_questions: tuple[tuple[Any, str], ...] = (
            (None, "must be a dictionary"),
            ({}, "Unknown question type"),
            (
                {"type": "unknown", "instructions": "x"},
                "Unknown question type",
            ),
            ({"type": "choice"}, "missing 'instructions'"),
            (
                {"type": "score", "instructions": "x", "criteria": []},
                "non-empty list",
            ),
            (
                {"type": "score", "instructions": "x", "criteria": "bad"},
                "non-empty list",
            ),
            (
                {"type": "noul", "instructions": "x", "criteria": []},
                "must be a dictionary",
            ),
        )
        for bad_question, message in bad_questions:
            with self.subTest(question=bad_question):
                with self.assertRaisesRegex(ValueError, message):
                    LayaModel._to_internal(
                        cast("dict[str, Any]", bad_question)
                    )

    def test_render_options(self) -> None:
        self.assertEqual(_render_options({"t": "choice", "crit": None}), [])
        self.assertEqual(_render_options({"t": "score", "crit": None}), [])
        self.assertEqual(
            _render_options({"t": "choice", "crit": {"A": None, "B": "yes"}}),
            ["A", "B: yes"],
        )
        self.assertEqual(
            _render_options({"t": "score", "crit": ["low", 2]}),
            ["level 0: low", "level 1: 2"],
        )
        self.assertEqual(
            _render_options({"t": "noul", "crit": None}),
            [
                "false: no, the statement does not hold",
                "true: yes, the statement holds",
            ],
        )
        self.assertEqual(
            _render_options({"t": "noul", "crit": {"false": 0, "true": ""}}),
            ["false: 0", "true: yes, the statement holds"],
        )

    def test_prefix_sequence_and_batch(self) -> None:
        tokenizer = FakeTokenizer()
        question = {
            "t": "choice",
            "ins": "choose [MASK]",
            "crit": {"A": "one", "B": "two"},
        }
        prefix, markers = _build_prefix(tokenizer, question)
        self.assertEqual(prefix[0], tokenizer.cls_token_id)
        self.assertEqual(prefix[-1], tokenizer.sep_token_id)
        self.assertEqual(len(markers), 2)
        self.assertTrue(
            all(
                prefix[position] == tokenizer.mask_token_id
                for position in markers
            )
        )
        limited, _ = _build_prefix(
            tokenizer,
            {
                "t": "choice",
                "ins": "instruction",
                "crit": {"A": "a" * 60, "B": "b" * 60},
            },
            head_max_len=20,
        )
        self.assertEqual(len(limited), 23)

        right_ids, right_markers = _build_sequence(
            tokenizer, "abcdef", question, max_len=len(prefix) + 4
        )
        left_ids, left_markers = _build_sequence(
            tokenizer,
            "abcdef",
            question,
            max_len=len(prefix) + 4,
            truncate_left=True,
        )
        self.assertEqual(right_ids[-4:-1], [ord(char) for char in "abc"])
        self.assertEqual(left_ids[-4:-1], [ord(char) for char in "def"])
        self.assertEqual(right_markers, left_markers)
        batch = _collate_items(
            [
                {"ids": [1, 2], "markers": [1], "qtype": 0},
                {"ids": [3], "markers": [0, 0], "qtype": 2},
            ],
            9,
        )
        self.assertEqual(batch["input_ids"].tolist(), [[1, 2], [3, 9]])
        self.assertEqual(batch["attention_mask"].tolist(), [[1, 1], [1, 0]])
        self.assertEqual(
            batch["marker_mask"].tolist(), [[True, False], [True, True]]
        )
        self.assertEqual(batch["qtype"].tolist(), [0, 2])
        with self.assertRaisesRegex(ValueError, "empty batch"):
            _collate_items([], 0)

    def test_model_inference_and_validation(self) -> None:
        model = self.make_model()
        output = model.system_one(
            "state",
            {
                "choice": {
                    "type": "choice",
                    "instructions": "choose",
                    "criteria": ["first", "second"],
                },
                "score": {
                    "type": "score",
                    "instructions": "score",
                    "criteria": ["low", "high"],
                },
                "yesno": {"type": "noul", "instructions": "true?"},
            },
        )
        self.assertEqual(output["answers"]["choice"]["choice"], "first")
        self.assertIn("probabilities", output["answers"]["score"])
        self.assertIn("noul", output["answers"]["yesno"])
        self.assertEqual(output["usage"]["output_tokens"], 0)
        self.assertEqual(model.classify("state", ["A", "B"]), "A")
        self.assertIsInstance(
            model.classify("state", ["A", "B"], return_details=True), dict
        )
        self.assertEqual(
            model.classify_batch(["a", "b"], ["A", "B"]), ["A", "A"]
        )
        self.assertEqual(model.classify_batch([], ["A", "B"]), [])
        self.assertEqual(model.predict("s", choices=["A", "B"]), "A")
        self.assertIsInstance(
            model.predict(
                "s", questions={"q": {"type": "noul", "instructions": "x"}}
            ),
            dict,
        )

        with self.assertRaisesRegex(ValueError, "non-empty dictionary"):
            model.system_one("state", {})
        with self.assertRaisesRegex(ValueError, "too many options"):
            model._max_len = 2
            model.system_one(
                "state",
                {
                    "q": {
                        "type": "choice",
                        "instructions": "choose",
                        "criteria": ["A", "B"],
                    }
                },
            )
        with self.assertRaisesRegex(
            ValueError, "Either 'choices' or 'questions'"
        ):
            model.predict("state")

    def test_initialization(self) -> None:
        onnx_module = types.ModuleType("onnxruntime")
        setattr(onnx_module, "InferenceSession", Mock())
        tokenizer = FakeTokenizer()
        with tempfile.TemporaryDirectory() as directory:
            config_path = Path(directory) / "rl_agent_config.json"
            for content, expected_temps in (
                ("{}", [1.0, 1.0, 1.0]),
                ("not json", [1.0, 1.0, 1.0]),
                ('{"temperature": [0.1, 2.0, 10.0]}', [0.5, 2.0, 5.0]),
            ):
                config_path.write_text(content, encoding="utf-8")
                with (
                    patch.dict("sys.modules", {"onnxruntime": onnx_module}),
                    patch.object(
                        LayaModel,
                        "_resolve_files",
                        return_value=(
                            "model.onnx",
                            str(config_path),
                            "tokenizer.json",
                            "tokenizer_config.json",
                        ),
                    ),
                    patch(
                        "pythainlp.classify.laya._TokenizerWrapper",
                        return_value=tokenizer,
                    ),
                ):
                    model = LayaModel(providers=["mock"], batch_size=2)
                self.assertEqual(model._temperature, expected_temps)
                self.assertEqual(model.providers, ["mock"])

            with (
                patch.dict("sys.modules", {"onnxruntime": onnx_module}),
                patch.object(
                    LayaModel,
                    "_resolve_files",
                    return_value=(
                        "model.onnx",
                        None,
                        "tokenizer.json",
                        "tokenizer_config.json",
                    ),
                ),
                patch(
                    "pythainlp.classify.laya._TokenizerWrapper",
                    return_value=tokenizer,
                ),
            ):
                model = LayaModel()
            self.assertEqual(model._temperature, [1.0, 1.0, 1.0])

        with patch.dict("sys.modules", {"numpy": None}):
            with self.assertRaisesRegex(ModuleNotFoundError, "Please install"):
                LayaModel()
        with patch.dict("sys.modules", {"onnxruntime": onnx_module}):
            with self.assertRaisesRegex(ValueError, "positive integer"):
                LayaModel(batch_size=0)

    def test_local_and_remote_file_resolution(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            token_dir = root / "tokenizer"
            token_dir.mkdir()
            self.assertEqual(
                LayaModel._resolve_files(str(root), None)[2],
                str(token_dir / "tokenizer.json"),
            )
            config = root / "rl_agent_config.json"
            config.write_text("{}", encoding="utf-8")
            self.assertEqual(
                LayaModel._resolve_files(str(root), None)[1], str(config)
            )
            config.unlink()
            token_dir.rmdir()
            self.assertEqual(
                LayaModel._resolve_files(str(root), None)[2],
                str(root / "tokenizer.json"),
            )

        class MissingFileError(Exception):
            pass

        hub_utils = types.ModuleType("huggingface_hub.utils")
        setattr(hub_utils, "EntryNotFoundError", MissingFileError)
        hub_module = types.ModuleType("huggingface_hub")
        setattr(hub_module, "utils", hub_utils)
        with (
            patch.dict(
                "sys.modules",
                {
                    "huggingface_hub": hub_module,
                    "huggingface_hub.utils": hub_utils,
                },
            ),
            patch(
                "pythainlp.classify.laya.get_hf_hub",
                side_effect=[
                    "/model.onnx",
                    MissingFileError(),
                    "/tokenizer.json",
                    "/tokenizer_config.json",
                ],
            ) as download,
        ):
            paths = LayaModel._resolve_files("repo/name", "revision")
        self.assertEqual(
            paths,
            ("/model.onnx", None, "/tokenizer.json", "/tokenizer_config.json"),
        )
        self.assertEqual(download.call_count, 4)

    def test_tokenizer_backends_and_errors(self) -> None:
        token_ids = {"[CLS]": 101, "[SEP]": 102, "[PAD]": 0, "[MASK]": 103}
        config = {
            "cls_token": {"content": "[CLS]"},
            "sep_token": "[SEP]",
            "pad_token": "[PAD]",
            "mask_token": "[MASK]",
        }
        with tempfile.TemporaryDirectory() as directory:
            config_path = Path(directory) / "tokenizer_config.json"
            config_path.write_text(json.dumps(config), encoding="utf-8")
            backend = Mock()
            backend.token_to_id.side_effect = token_ids.get
            backend.encode.return_value.ids = [1, 2]
            tokenizers_module = types.ModuleType("tokenizers")
            setattr(
                tokenizers_module,
                "Tokenizer",
                Mock(from_file=Mock(return_value=backend)),
            )
            with patch.dict("sys.modules", {"tokenizers": tokenizers_module}):
                tokenizer = _TokenizerWrapper(
                    "tokenizer.json", str(config_path)
                )
            self.assertEqual(tokenizer("text"), {"input_ids": [1, 2]})

            hf_backend = Mock()
            hf_backend.convert_tokens_to_ids.side_effect = token_ids.get
            hf_backend.return_value = {"input_ids": [3, 4]}
            transformers_module = types.ModuleType("transformers")
            setattr(
                transformers_module,
                "AutoTokenizer",
                Mock(from_pretrained=Mock(return_value=hf_backend)),
            )
            with patch.dict(
                "sys.modules",
                {"tokenizers": None, "transformers": transformers_module},
            ):
                hf_tokenizer = _TokenizerWrapper(
                    str(Path(directory) / "tokenizer.json"), str(config_path)
                )
            self.assertEqual(hf_tokenizer("text"), {"input_ids": [3, 4]})

            for bad_config, message in (
                ({**config, "mask_token": None}, "missing mask_token"),
                ({**config, "mask_token": "missing"}, "cannot map token"),
            ):
                config_path.write_text(
                    json.dumps(bad_config), encoding="utf-8"
                )
                with patch.dict(
                    "sys.modules", {"tokenizers": tokenizers_module}
                ):
                    with self.assertRaisesRegex(ValueError, message):
                        _TokenizerWrapper("tokenizer.json", str(config_path))
            with patch.dict(
                "sys.modules", {"tokenizers": None, "transformers": None}
            ):
                with self.assertRaisesRegex(
                    ModuleNotFoundError, "Please install"
                ):
                    _TokenizerWrapper("tokenizer.json", str(config_path))


class PublicAliasTestCaseN(unittest.TestCase):
    """Test public alias identity."""

    def test_laya_alias(self) -> None:
        self.assertIs(Laya, LayaModel)
