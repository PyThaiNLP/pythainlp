# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

"""Coverage tests for the Cython fallback paths in pythainlp.util.thai.

Kept separate from test_util.py to isolate sys.modules/reload side-effects.
"""

import importlib
import unittest
from unittest.mock import patch


class TestThaiUtilPurePython(unittest.TestCase):
    """Call _py_* directly to keep the original function bodies covered."""

    def test_pure_python_is_thai_char(self):
        from pythainlp.util.thai import _py_is_thai_char

        self.assertTrue(_py_is_thai_char("ก"))
        self.assertTrue(_py_is_thai_char("๕"))
        self.assertFalse(_py_is_thai_char("A"))
        self.assertFalse(_py_is_thai_char(" "))
        with self.assertRaises(TypeError):
            _py_is_thai_char("")

    def test_pure_python_is_thai(self):
        from pythainlp.util.thai import _py_is_thai

        self.assertTrue(_py_is_thai("กาลเวลา"))
        self.assertFalse(_py_is_thai("กาล-เวลา"))
        self.assertTrue(_py_is_thai("กาล-เวลา", ignore_chars="-"))
        self.assertTrue(_py_is_thai(""))

    def test_pure_python_count_thai(self):
        from pythainlp.util.thai import _py_count_thai

        self.assertEqual(_py_count_thai("ไทย"), 100.0)
        self.assertEqual(_py_count_thai("Python"), 0.0)
        # ignore_chars="" → "1" is non-Thai, so 1/2 chars = 50%
        self.assertAlmostEqual(_py_count_thai("ก1", ignore_chars=""), 50.0)


class TestThaiUtilImportFallback(unittest.TestCase):
    """Cover the ``except ImportError: pass`` branch in thai.py.

    Patches sys.modules to make _thai_fast unimportable, reloads thai.py to
    execute the fallback path, then restores the module to its original state.
    """

    def test_cython_import_error_fallback(self):
        import pythainlp.util.thai as thai_mod

        try:
            with patch.dict(
                "sys.modules", {"pythainlp._ext._thai_fast": None}
            ):
                importlib.reload(thai_mod)
                self.assertTrue(thai_mod.is_thai_char("ก"))
                self.assertEqual(thai_mod.count_thai("ไทย"), 100.0)
        finally:
            # Guaranteed restore: runs whether assertions pass or fail
            importlib.reload(thai_mod)
