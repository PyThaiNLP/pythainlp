# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

import os
import tempfile
import unittest
import warnings
from unittest.mock import patch

from pythainlp import (
    is_offline_mode,
    is_read_only_mode,
    is_unsafe_pickle_allowed,
)
from pythainlp.tools import (
    get_full_data_path,
    get_pythainlp_data_path,
    get_pythainlp_path,
)
from pythainlp.tools import (
    is_offline_mode as tools_is_offline_mode,
)
from pythainlp.tools import (
    is_read_only_mode as tools_is_read_only_mode,
)
from pythainlp.tools.core import safe_print, warn_deprecation


class ToolsTestCase(unittest.TestCase):
    def test_path(self):
        data_filename = "ttc_freq.txt"
        self.assertTrue(get_full_data_path(data_filename).endswith(data_filename))
        self.assertIsInstance(get_pythainlp_data_path(), str)
        self.assertIsInstance(get_pythainlp_path(), str)

    def test_custom_data_dir_new(self):
        """Test that PYTHAINLP_DATA environment variable is respected."""
        with tempfile.TemporaryDirectory() as temp_dir:
            custom_dir = os.path.join(temp_dir, "pythainlp-data")
            with patch.dict(
                os.environ,
                {"PYTHAINLP_DATA": custom_dir},
                clear=False,
            ):
                os.environ.pop("PYTHAINLP_DATA_DIR", None)
                path = get_pythainlp_data_path()
                self.assertEqual(path, custom_dir)
                self.assertTrue(os.path.isdir(path))

    def test_custom_data_dir(self):
        """Test that PYTHAINLP_DATA_DIR is accepted but emits a deprecation warning.

        This test verifies the functionality needed for distributed
        environments like PySpark, where setting PYTHAINLP_DATA_DIR
        inside worker functions is required.

        See: https://github.com/PyThaiNLP/pythainlp/issues/475
        """
        with tempfile.TemporaryDirectory() as temp_dir:
            custom_dir = os.path.join(temp_dir, "pythainlp-data")
            with patch.dict(
                os.environ,
                {"PYTHAINLP_DATA_DIR": custom_dir},
                clear=False,
            ):
                os.environ.pop("PYTHAINLP_DATA", None)
                with warnings.catch_warnings(record=True) as w:
                    warnings.simplefilter("always")
                    path = get_pythainlp_data_path()
                self.assertEqual(path, custom_dir)
                self.assertTrue(os.path.isdir(path))
                self.assertEqual(len(w), 1)
                self.assertTrue(issubclass(w[0].category, DeprecationWarning))
                self.assertIn("PYTHAINLP_DATA_DIR", str(w[0].message))
                self.assertIn("PYTHAINLP_DATA", str(w[0].message))

    def test_custom_data_dir_conflict(self):
        """Test that setting both PYTHAINLP_DATA and PYTHAINLP_DATA_DIR raises ValueError."""
        with tempfile.TemporaryDirectory() as temp_dir:
            with patch.dict(
                os.environ,
                {
                    "PYTHAINLP_DATA": os.path.join(temp_dir, "a"),
                    "PYTHAINLP_DATA_DIR": os.path.join(temp_dir, "b"),
                },
            ):
                with self.assertRaises(ValueError) as ctx:
                    get_pythainlp_data_path()
                self.assertIn("PYTHAINLP_DATA", str(ctx.exception))
                self.assertIn("PYTHAINLP_DATA_DIR", str(ctx.exception))

    def test_is_offline_mode(self):
        """Test is_offline_mode() reflects PYTHAINLP_OFFLINE env var."""
        # Truthy values
        for truthy in ("1", "true", "True", "TRUE", "yes", "YES", "on", "ON"):
            with patch.dict(os.environ, {"PYTHAINLP_OFFLINE": truthy}):
                self.assertTrue(
                    is_offline_mode(),
                    f"Expected offline for PYTHAINLP_OFFLINE={truthy!r}",
                )
        # Falsy values
        for falsy in (
            "",
            "0",
            "false",
            "False",
            "FALSE",
            "no",
            "NO",
            "off",
            "OFF",
        ):
            with patch.dict(os.environ, {"PYTHAINLP_OFFLINE": falsy}):
                self.assertFalse(
                    is_offline_mode(),
                    f"Expected online for PYTHAINLP_OFFLINE={falsy!r}",
                )
        # Same function is exposed via pythainlp.tools
        self.assertIs(is_offline_mode, tools_is_offline_mode)

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

        # Test with replacement symbol
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            warn_deprecation("old_func", replacing_symbol="new_func")
            self.assertEqual(len(w), 1)
            self.assertIn("old_func", str(w[0].message))
            self.assertIn("new_func", str(w[0].message))

        # Test with version information
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            warn_deprecation(
                "old_func", deprecated_version="1.0", removal_version="2.0"
            )
            self.assertEqual(len(w), 1)
            self.assertIn("1.0", str(w[0].message))
            self.assertIn("2.0", str(w[0].message))

        # Test with all parameters
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            warn_deprecation(
                "old_func",
                replacing_symbol="new_func",
                deprecated_version="1.0",
                removal_version="2.0",
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

    def test_is_read_only_mode_new_var(self):
        """Test is_read_only_mode() reflects PYTHAINLP_READ_ONLY env var."""
        # Truthy values
        for truthy in ("1", "true", "True", "TRUE", "yes", "YES", "on", "ON"):
            with patch.dict(
                os.environ,
                {"PYTHAINLP_READ_ONLY": truthy},
                clear=False,
            ):
                os.environ.pop("PYTHAINLP_READ_MODE", None)
                self.assertTrue(
                    is_read_only_mode(),
                    f"Expected read-only for PYTHAINLP_READ_ONLY={truthy!r}",
                )
        # Falsy values
        for falsy in ("", "0", "false", "False", "FALSE", "no", "NO", "off", "OFF"):
            with patch.dict(
                os.environ,
                {"PYTHAINLP_READ_ONLY": falsy},
                clear=False,
            ):
                os.environ.pop("PYTHAINLP_READ_MODE", None)
                self.assertFalse(
                    is_read_only_mode(),
                    f"Expected not read-only for PYTHAINLP_READ_ONLY={falsy!r}",
                )
        # Unset: should default to False
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("PYTHAINLP_READ_ONLY", None)
            os.environ.pop("PYTHAINLP_READ_MODE", None)
            self.assertFalse(is_read_only_mode())
        # Same function is exposed via pythainlp.tools
        self.assertIs(is_read_only_mode, tools_is_read_only_mode)

    def test_is_read_only_mode_legacy_var(self):
        """Test is_read_only_mode() emits DeprecationWarning for PYTHAINLP_READ_MODE."""
        with patch.dict(os.environ, {"PYTHAINLP_READ_MODE": "1"}, clear=False):
            os.environ.pop("PYTHAINLP_READ_ONLY", None)
            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always")
                result = is_read_only_mode()
            self.assertTrue(result)
            self.assertEqual(len(w), 1)
            self.assertTrue(issubclass(w[0].category, DeprecationWarning))
            self.assertIn("PYTHAINLP_READ_MODE", str(w[0].message))
            self.assertIn("PYTHAINLP_READ_ONLY", str(w[0].message))

        # PYTHAINLP_READ_MODE=0 should still warn and return False
        with patch.dict(os.environ, {"PYTHAINLP_READ_MODE": "0"}, clear=False):
            os.environ.pop("PYTHAINLP_READ_ONLY", None)
            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always")
                result = is_read_only_mode()
            self.assertFalse(result)
            self.assertEqual(len(w), 1)
            self.assertTrue(issubclass(w[0].category, DeprecationWarning))

    def test_is_read_only_mode_conflict(self):
        """Test is_read_only_mode() raises ValueError when both env vars are set."""
        with patch.dict(
            os.environ,
            {"PYTHAINLP_READ_ONLY": "1", "PYTHAINLP_READ_MODE": "1"},
        ):
            with self.assertRaises(ValueError) as ctx:
                is_read_only_mode()
            self.assertIn("PYTHAINLP_READ_ONLY", str(ctx.exception))
            self.assertIn("PYTHAINLP_READ_MODE", str(ctx.exception))

    def test_get_pythainlp_data_path_no_makedirs_in_read_only(self):
        """Test that get_pythainlp_data_path skips makedirs in read-only mode.

        Directory creation is an implicit side-effect the user may not be
        aware of.  Read-only mode must suppress it.
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            new_dir = os.path.join(tmpdir, "new-pythainlp-data")
            with patch.dict(
                os.environ,
                {"PYTHAINLP_DATA": new_dir, "PYTHAINLP_READ_ONLY": "1"},
                clear=False,
            ):
                os.environ.pop("PYTHAINLP_DATA_DIR", None)
                os.environ.pop("PYTHAINLP_READ_MODE", None)
                path = get_pythainlp_data_path()
                self.assertEqual(path, new_dir)
                # Directory must NOT be created in read-only mode
                self.assertFalse(
                    os.path.exists(new_dir),
                    "Data directory should not be created in read-only mode",
                )

    def test_is_unsafe_pickle_allowed(self):
        """Test is_unsafe_pickle_allowed() reflects PYTHAINLP_ALLOW_UNSAFE_PICKLE env var."""
        # Truthy values
        for truthy in ("1", "true", "True", "TRUE", "yes", "YES", "on", "ON"):
            with patch.dict(os.environ, {"PYTHAINLP_ALLOW_UNSAFE_PICKLE": truthy}):
                self.assertTrue(
                    is_unsafe_pickle_allowed(),
                    f"Expected True for PYTHAINLP_ALLOW_UNSAFE_PICKLE={truthy!r}",
                )
        # Falsy values
        for falsy in ("", "0", "false", "False", "FALSE", "no", "NO", "off", "OFF"):
            with patch.dict(os.environ, {"PYTHAINLP_ALLOW_UNSAFE_PICKLE": falsy}):
                self.assertFalse(
                    is_unsafe_pickle_allowed(),
                    f"Expected False for PYTHAINLP_ALLOW_UNSAFE_PICKLE={falsy!r}",
                )
        # Unset: should default to False
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("PYTHAINLP_ALLOW_UNSAFE_PICKLE", None)
            self.assertFalse(is_unsafe_pickle_allowed())
