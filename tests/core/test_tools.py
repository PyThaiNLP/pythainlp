# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

import os
import shutil
import unittest

from pythainlp.tools import (
    get_full_data_path,
    get_pythainlp_data_path,
    get_pythainlp_path,
)


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

        try:
            # Test with custom directory
            custom_dir = "./test-pythainlp-data"
            os.environ["PYTHAINLP_DATA_DIR"] = custom_dir

            # Get path should return the custom directory
            path = get_pythainlp_data_path()

            # Verify the path contains our custom directory
            self.assertIn("test-pythainlp-data", path)

            # Verify directory was created
            self.assertTrue(os.path.exists(path))
            self.assertTrue(os.path.isdir(path))

            # Clean up test directory
            if os.path.exists(path) and "test-pythainlp-data" in path:
                shutil.rmtree(path)

        finally:
            # Restore original value
            if original_value is not None:
                os.environ["PYTHAINLP_DATA_DIR"] = original_value
            elif "PYTHAINLP_DATA_DIR" in os.environ:
                del os.environ["PYTHAINLP_DATA_DIR"]
