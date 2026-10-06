# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Regression test for ThaiTextProcessor.preprocess.

The module is imported under a private name with a fake ``transformers``
package, because importing it downloads the real tokenizer.
"""

import importlib.util
import sys
import types
import unittest
from pathlib import Path
from typing import Any
from unittest import mock

import pythainlp


def _import_phayathaibert() -> Any:
    """Load phayathaibert/core.py with a fake ``transformers``.

    Neither ``sys.modules`` nor the ``pythainlp.phayathaibert`` package
    attribute is changed.
    """
    fake = types.ModuleType("transformers")
    tokenizer_class = mock.Mock()
    fake.CamembertTokenizer = tokenizer_class  # type: ignore[attr-defined]
    path = Path(pythainlp.__file__).parent / "phayathaibert" / "core.py"
    spec = importlib.util.spec_from_file_location(
        "phayathaibert_under_test", path
    )
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    with mock.patch.dict(sys.modules, {"transformers": fake}):
        spec.loader.exec_module(module)
    return module


class ThaiTextProcessorPreprocessTestCase(unittest.TestCase):
    processor: Any

    @classmethod
    def setUpClass(cls) -> None:
        cls.processor = _import_phayathaibert().ThaiTextProcessor()

    def test_default_rules(self) -> None:
        # Before the fix, the default rules were unbound methods, and
        # every call without pre_rules raised TypeError.
        self.assertEqual(
            self.processor.preprocess("Hey  (what)\n\nUP"), "hey<_>(what)<_>up"
        )

    def test_default_rules_with_custom_tokenizer(self) -> None:
        # The default rules lowercase, collapse spaces, and mark each
        # space with "<_>" before the tokenizer runs.
        result = self.processor.preprocess("A  B", tok_func=lambda t: [t])
        self.assertEqual(result, "a<_>b")

    def test_custom_rules_and_tokenizer(self) -> None:
        result = self.processor.preprocess(
            "ab",
            pre_rules=[str.upper, lambda t: t + "!"],
            tok_func=list,
        )
        self.assertEqual(result, "AB!")

    def test_empty_rules_keep_text(self) -> None:
        self.assertEqual(
            self.processor.preprocess("Ab", pre_rules=[], tok_func=list),
            "ab",
        )


if __name__ == "__main__":
    unittest.main()
