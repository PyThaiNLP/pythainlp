# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

import unittest

from pythainlp.lm import Qwen3


class LMTestCaseX(unittest.TestCase):
    def test_qwen3_initialization(self):
        # Test that Qwen3 can be instantiated
        try:
            model = Qwen3()
            self.assertIsNotNone(model)
            self.assertIsNone(model.model)
            self.assertIsNone(model.tokenizer)
        except ImportError:
            # Skip if dependencies not installed
            self.skipTest("Qwen3 dependencies not installed")

    def test_qwen3_generate_without_load(self):
        # Test that generate raises error when model is not loaded
        try:
            model = Qwen3()
            with self.assertRaises(RuntimeError):
                model.generate("test")
        except ImportError:
            # Skip if dependencies not installed
            self.skipTest("Qwen3 dependencies not installed")

    def test_qwen3_chat_without_load(self):
        # Test that chat raises error when model is not loaded
        try:
            model = Qwen3()
            with self.assertRaises(RuntimeError):
                model.chat([{"role": "user", "content": "test"}])
        except ImportError:
            # Skip if dependencies not installed
            self.skipTest("Qwen3 dependencies not installed")
