# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""
Security tests for path traversal protection and safe archive extraction.
"""

import os
import tarfile
import tempfile
import unittest
import zipfile

from pythainlp.corpus.core import (
    _is_within_directory,
    _safe_extract_tar,
    _safe_extract_zip,
)


class SecurityTestCase(unittest.TestCase):
    """Test security-related functionality."""

    def test_is_within_directory(self):
        """Test path validation against traversal attacks."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Safe paths - should return True
            self.assertTrue(
                _is_within_directory(tmpdir, os.path.join(tmpdir, "file.txt"))
            )
            self.assertTrue(
                _is_within_directory(tmpdir, os.path.join(tmpdir, "subdir", "file.txt"))
            )
            self.assertTrue(_is_within_directory(tmpdir, tmpdir))

            # Path traversal attempts - should return False
            self.assertFalse(
                _is_within_directory(tmpdir, os.path.join(tmpdir, "..", "file.txt"))
            )
            self.assertFalse(
                _is_within_directory(tmpdir, os.path.join(tmpdir, "..", "..", "file.txt"))
            )
            self.assertFalse(
                _is_within_directory(tmpdir, "/etc/passwd")
            )

    def test_safe_extract_tar_with_safe_archive(self):
        """Test safe tar extraction with a legitimate archive."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a safe tar archive
            tar_path = os.path.join(tmpdir, "safe.tar")
            with tarfile.open(tar_path, "w") as tar:
                # Add a simple file
                test_content = b"test content"
                test_file = os.path.join(tmpdir, "test.txt")
                with open(test_file, "wb") as f:
                    f.write(test_content)
                tar.add(test_file, arcname="test.txt")

            # Extract to a different directory
            extract_dir = os.path.join(tmpdir, "extract")
            os.makedirs(extract_dir)
            with tarfile.open(tar_path, "r") as tar:
                _safe_extract_tar(tar, extract_dir)

            # Verify extraction succeeded
            extracted_file = os.path.join(extract_dir, "test.txt")
            self.assertTrue(os.path.exists(extracted_file))
            with open(extracted_file, "rb") as f:
                self.assertEqual(f.read(), test_content)

    def test_safe_extract_tar_rejects_path_traversal(self):
        """Test that safe tar extraction rejects path traversal attempts."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a malicious tar archive with path traversal
            tar_path = os.path.join(tmpdir, "malicious.tar")
            with tarfile.open(tar_path, "w") as tar:
                test_file = os.path.join(tmpdir, "test.txt")
                with open(test_file, "wb") as f:
                    f.write(b"malicious content")
                # Add with a path traversal name
                tar.add(test_file, arcname="../../../etc/malicious.txt")

            # Attempt to extract
            extract_dir = os.path.join(tmpdir, "extract")
            os.makedirs(extract_dir)
            with tarfile.open(tar_path, "r") as tar:
                with self.assertRaises(ValueError) as context:
                    _safe_extract_tar(tar, extract_dir)
                self.assertIn("path traversal", str(context.exception).lower())

    def test_safe_extract_zip_with_safe_archive(self):
        """Test safe zip extraction with a legitimate archive."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a safe zip archive
            zip_path = os.path.join(tmpdir, "safe.zip")
            with zipfile.ZipFile(zip_path, "w") as zf:
                test_content = b"test content"
                zf.writestr("test.txt", test_content)

            # Extract to a different directory
            extract_dir = os.path.join(tmpdir, "extract")
            os.makedirs(extract_dir)
            with zipfile.ZipFile(zip_path, "r") as zf:
                _safe_extract_zip(zf, extract_dir)

            # Verify extraction succeeded
            extracted_file = os.path.join(extract_dir, "test.txt")
            self.assertTrue(os.path.exists(extracted_file))
            with open(extracted_file, "rb") as f:
                self.assertEqual(f.read(), test_content)

    def test_safe_extract_zip_rejects_path_traversal(self):
        """Test that safe zip extraction rejects path traversal attempts."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a malicious zip archive with path traversal
            zip_path = os.path.join(tmpdir, "malicious.zip")
            with zipfile.ZipFile(zip_path, "w") as zf:
                zf.writestr("../../../etc/malicious.txt", b"malicious content")

            # Attempt to extract
            extract_dir = os.path.join(tmpdir, "extract")
            os.makedirs(extract_dir)
            with zipfile.ZipFile(zip_path, "r") as zf:
                with self.assertRaises(ValueError) as context:
                    _safe_extract_zip(zf, extract_dir)
                self.assertIn("path traversal", str(context.exception).lower())


if __name__ == "__main__":
    unittest.main()
