# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

# Tests for Laya classification functions that require ONNX Runtime
# These tests are NOT run in automated CI workflows due to:
# - Large dependencies (onnxruntime, huggingface-hub, tokenizers)
# - Model download size (~650 MB)

import os
import unittest
import numpy as np

from pythainlp.classify import Laya, LayaModel
from pythainlp.classify.laya import (
    _clamp_temperature,
    _confidence_from_probs,
    _render_criterion,
    _render_options,
    _serialize_state,
    _temp_bucket,
)


class ClassifyONNXTestCaseN(unittest.TestCase):
    """Tests for ONNX-based Laya classification (requires onnxruntime)."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.model = LayaModel()

    def test_alias(self) -> None:
        self.assertIs(Laya, LayaModel)

    def test_classify_choice_list(self) -> None:
        text = "อาหารอร่อยมาก บรรยากาศดี พนักงานบริการยอดเยี่ยม"
        choices = ["Positive", "Negative", "Neutral"]
        res = self.model.classify(
            text, choices=choices, prompt="What is the sentiment of the text?"
        )
        self.assertIsInstance(res, str)
        self.assertEqual(res, "Positive")

    def test_classify_negative(self) -> None:
        text = "แย่มาก อาหารไม่สุก บริการช้า รอนานมาก ไม่ประทับใจเลย"
        choices = ["Positive", "Negative", "Neutral"]
        res = self.model.classify(
            text, choices=choices, prompt="What is the sentiment of the text?"
        )
        self.assertEqual(res, "Negative")

    def test_classify_choice_dict_with_details(self) -> None:
        text = "อาหารอร่อยมาก"
        choices = {
            "Positive": "ข้อความแสดงความสุข ดีใจ ชมเชย",
            "Negative": "ข้อความแสดงความทุกข์ เสียใจ ตำหนิ",
        }
        res = self.model.classify(
            text, choices=choices, return_details=True
        )
        self.assertIsInstance(res, dict)
        self.assertEqual(res["type"], "choice")
        self.assertEqual(res["choice"], "Positive")
        self.assertIn("confidence", res)
        self.assertIn("probabilities", res)
        self.assertIn("action", res)
        self.assertGreater(res["probabilities"]["Positive"], 0.5)

    def test_classify_batch(self) -> None:
        texts = [
            "อาหารอร่อยมาก บรรยากาศดี",
            "บริการแย่มาก อาหารไม่อร่อย",
        ]
        choices = ["Positive", "Negative"]
        res = self.model.classify_batch(texts, choices=choices)
        self.assertIsInstance(res, list)
        self.assertEqual(len(res), 2)
        self.assertEqual(res[0], "Positive")
        self.assertEqual(res[1], "Negative")

    def test_classify_batch_empty(self) -> None:
        res = self.model.classify_batch([], choices=["A", "B"])
        self.assertEqual(res, [])

    def test_predict_with_choices(self) -> None:
        text = "ฉันรู้สึกมีความสุขมาก"
        res = self.model.predict(
            text, choices=["Positive", "Negative", "Neutral"]
        )
        self.assertEqual(res, "Positive")

    def test_predict_with_questions(self) -> None:
        text = "กรุณาคืนเงินให้ฉันด้วย เพราะสินค้าชำรุดเสียหาย"
        questions = {
            "refund": {
                "type": "noul",
                "instructions": "ข้อความนี้ขอเงินคืนหรือไม่?",
            }
        }
        res = self.model.predict(text, questions=questions)
        self.assertIsInstance(res, dict)
        self.assertIn("answers", res)
        self.assertIn("refund", res["answers"])
        answer = res["answers"]["refund"]
        self.assertEqual(answer["type"], "noul")
        self.assertGreater(answer["noul"], 0.5)

    def test_system_one_choice_and_score(self) -> None:
        text = "ข่าวการแข่งขันฟุตบอลพรีเมียร์ลีกเมื่อคืนนี้ ลิเวอร์พูลชนะ 3-0"
        questions = {
            "topic": {
                "type": "choice",
                "instructions": "หัวข้อของข้อความนี้คืออะไร?",
                "criteria": ["กีฬา", "การเมือง", "บันเทิง"],
            },
            "relevance": {
                "type": "score",
                "instructions": "ความเกี่ยวข้องกับกีฬา",
                "criteria": ["ไม่เกี่ยวข้อง", "เกี่ยวข้องมาก"],
            },
        }
        res = self.model.system_one(text, questions)
        self.assertIsInstance(res, dict)
        self.assertEqual(res["answers"]["topic"]["choice"], "กีฬา")
        self.assertEqual(res["answers"]["relevance"]["type"], "score")
        self.assertIn("usage", res)

    def test_structured_state_input(self) -> None:
        state_dict = {"body": "อาหารอร่อยมาก", "author": "ลูกค้า"}
        res = self.model.classify(
            state_dict, choices=["Positive", "Negative"]
        )
        self.assertEqual(res, "Positive")

        state_list = ["อาหารอร่อยมาก", "บริการดี"]
        res = self.model.classify(
            state_list, choices=["Positive", "Negative"]
        )
        self.assertEqual(res, "Positive")

    def test_local_model_path_and_chunking(self) -> None:
        model_dir = os.path.dirname(self.model.model_path)
        local_model = LayaModel(model_path=model_dir, batch_size=1)
        questions = {
            "q1": {
                "type": "choice",
                "instructions": "ความรู้สึก",
                "criteria": ["บวก", "ลบ"],
            },
            "q2": {
                "type": "noul",
                "instructions": "เป็นประโยคคำถามหรือไม่?",
            },
        }
        res = local_model.system_one("อาหารอร่อย", questions)
        self.assertIn("q1", res["answers"])
        self.assertIn("q2", res["answers"])

    def test_helper_functions(self) -> None:
        # _clamp_temperature
        self.assertEqual(_clamp_temperature("invalid"), 1.0)
        self.assertEqual(_clamp_temperature(float("nan")), 1.0)
        self.assertEqual(_clamp_temperature(float("inf")), 1.0)
        self.assertEqual(_clamp_temperature(0.1), 0.5)
        self.assertEqual(_clamp_temperature(10.0), 5.0)
        self.assertEqual(_clamp_temperature(2.0), 2.0)

        # _confidence_from_probs
        self.assertEqual(_confidence_from_probs(np.array([1.0]), 1), 1.0)
        self.assertGreaterEqual(
            _confidence_from_probs(np.array([0.9, 0.1]), 2), 0.0
        )

        # _temp_bucket
        self.assertEqual(_temp_bucket(0, 2), "choice:2")
        self.assertEqual(_temp_bucket(0, 4), "choice:3-5")
        self.assertEqual(_temp_bucket(0, 8), "choice:6-10")
        self.assertEqual(_temp_bucket(0, 20), "choice:11+")

        # _serialize_state
        self.assertEqual(_serialize_state("text"), "text")
        self.assertEqual(_serialize_state({"k": "v"}), '{"k": "v"}')

        # _render_criterion
        self.assertEqual(_render_criterion("text"), "text")
        self.assertEqual(_render_criterion(["a", "b"]), '["a", "b"]')

        # _render_options
        self.assertEqual(_render_options({"t": "choice", "crit": None}), [])
        self.assertEqual(_render_options({"t": "score", "crit": None}), [])
        noul_opts = _render_options({"t": "noul", "crit": {"false": "no", "true": "yes"}})
        self.assertEqual(len(noul_opts), 2)

    def test_invalid_parameters(self) -> None:
        with self.assertRaises(ValueError):
            self.model.classify("test", choices=[])

        with self.assertRaises(ValueError):
            self.model.classify("test", choices=["A", "A"])

        with self.assertRaises(ValueError):
            self.model.classify("test", choices=[1, 2])  # type: ignore[arg-type]

        with self.assertRaises(ValueError):
            self.model.predict("test")

        with self.assertRaises(ValueError):
            self.model.system_one("test", questions={})

        with self.assertRaises(ValueError):
            self.model.system_one(
                "test",
                questions={
                    "q": {"type": "unknown", "instructions": "test"}
                },
            )

        with self.assertRaises(ValueError):
            self.model.system_one(
                "test",
                questions={"q": "not a dictionary"},  # type: ignore[dict-item]
            )

        with self.assertRaises(ValueError):
            self.model.system_one(
                "test",
                questions={"q": {"type": "choice", "criteria": ["A"]}},
            )

        with self.assertRaises(ValueError):
            self.model.system_one(
                "test",
                questions={"q": {"type": "score", "instructions": "test", "criteria": []}},
            )

        with self.assertRaises(ValueError):
            self.model.system_one(
                "test",
                questions={"q": {"type": "score", "instructions": "test", "criteria": "not a list"}},  # type: ignore[dict-item]
            )

        with self.assertRaises(ValueError):
            self.model.system_one(
                "test",
                questions={"q": {"type": "noul", "instructions": "test", "criteria": "not a dict"}},  # type: ignore[dict-item]
            )

        with self.assertRaises(ValueError):
            LayaModel(batch_size=0)


if __name__ == "__main__":
    unittest.main()
