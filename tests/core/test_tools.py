# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

import os
import tempfile
import unittest
import warnings

from pythainlp.tools import (
    get_full_data_path,
    get_pythainlp_data_path,
    get_pythainlp_path,
)
from pythainlp.tools.core import safe_print, warn_deprecation


class ToolsTestCase(unittest.TestCase):
    def test_path(self):
        data_filename = "ttc_freq.txt"
        self.assertTrue(
            get_full_data_path(data_filename).endswith(data_filename)
        )
        self.assertIsInstance(get_pythainlp_data_path(), str)
        self.assertIsInstance(get_pythainlp_path(), str)

    def test_custom_data_dir(self):
        """Test that PYTHAINLP_DATA_DIR environment variable is respected.

        This test verifies the functionality needed for distributed
        environments like PySpark, where setting PYTHAINLP_DATA_DIR
        inside worker functions is required.

        See: https://github.com/PyThaiNLP/pythainlp/issues/475
        """
        # Save original value
        original_value = os.environ.get("PYTHAINLP_DATA_DIR")

        # Use temporary directory for hermetic test
        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                # Test with custom directory
                custom_dir = os.path.join(temp_dir, "pythainlp-data")
                os.environ["PYTHAINLP_DATA_DIR"] = custom_dir

                # Get path should return the custom directory
                path = get_pythainlp_data_path()

                # Verify the path matches our custom directory
                self.assertEqual(path, custom_dir)

                # Verify directory was created
                self.assertTrue(os.path.exists(path))
                self.assertTrue(os.path.isdir(path))

            finally:
                # Restore original value
                if original_value is not None:
                    os.environ["PYTHAINLP_DATA_DIR"] = original_value
                elif "PYTHAINLP_DATA_DIR" in os.environ:
                    del os.environ["PYTHAINLP_DATA_DIR"]

    def test_warn_deprecation(self):
        """Test deprecation warning function."""
        # Test basic deprecation warning
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            warn_deprecation("old_func")
            self.assertEqual(len(w), 1)
            self.assertTrue(issubclass(w[0].category, DeprecationWarning))
            self.assertIn("old_func", str(w[0].message))
            self.assertIn("deprecated", str(w[0].message))

        # Test with replacement function
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            warn_deprecation("old_func", replacing_func="new_func")
            self.assertEqual(len(w), 1)
            self.assertIn("old_func", str(w[0].message))
            self.assertIn("new_func", str(w[0].message))

        # Test with version information
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            warn_deprecation(
                "old_func",
                deprecated_version="1.0",
                removal_version="2.0"
            )
            self.assertEqual(len(w), 1)
            self.assertIn("1.0", str(w[0].message))
            self.assertIn("2.0", str(w[0].message))

        # Test with all parameters
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            warn_deprecation(
                "old_func",
                replacing_func="new_func",
                deprecated_version="1.0",
                removal_version="2.0"
            )
            self.assertEqual(len(w), 1)
            message = str(w[0].message)
            self.assertIn("old_func", message)
            self.assertIn("new_func", message)
            self.assertIn("1.0", message)
            self.assertIn("2.0", message)

    def test_safe_print(self):
        """Test safe_print function."""
        # Test normal printing
        safe_print("Hello, World!")
        safe_print("สวัสดีครับ")

        # Test with Unicode characters
        safe_print("Hello 👋 World")
        safe_print("ภาษาไทย")

        # Test with empty string
        safe_print("")

        # Test with special characters
        safe_print("\n\t")

        # Note: Testing actual UnicodeEncodeError is environment-dependent
        # and would require mocking sys.stdout.encoding
