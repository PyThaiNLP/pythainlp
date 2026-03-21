# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

# Tests for parsing functions that require torch and transformers
# These tests are NOT run in automated CI workflows due to:
# - Large dependencies (torch, transformers)
# - Python 3.13+ compatibility issues

import unittest


class ParseTestCaseN(unittest.TestCase):
    """Tests for parsing functions (requires torch and transformers)"""

    def test_dependency_parsing_returns_list(self):
        from pythainlp.parse import dependency_parsing

        result = dependency_parsing("แมวกินปลา")
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

    def test_dependency_parsing_result_structure(self):
        from pythainlp.parse import dependency_parsing

        result = dependency_parsing("แมวกินปลา")
        for item in result:
            self.assertIsInstance(item, dict)

    def test_dependency_parsing_empty_string(self):
        from pythainlp.parse import dependency_parsing

        result = dependency_parsing("")
        self.assertIsInstance(result, list)
