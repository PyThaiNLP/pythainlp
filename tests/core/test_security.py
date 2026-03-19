# SPDX-FileCopyrightText: 2026 PyThaiNLP Project
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

from pythainlp.corpus import corpus_path
from pythainlp.corpus.core import (
    _is_within_directory,
    _safe_extract_tar,
    _safe_extract_zip,
)
from pythainlp.tools import get_full_data_path
from pythainlp.tools.path import _safe_path_join, get_pythainlp_data_path


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
                _is_within_directory(
                    tmpdir, os.path.join(tmpdir, "..", "..", "file.txt")
                )
            )
            self.assertFalse(_is_within_directory(tmpdir, "/etc/passwd"))

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
                # Error message may vary between Python versions
                # Check for either "path traversal" or "outside"
                error_msg = str(context.exception).lower()
                self.assertTrue(
                    "path traversal" in error_msg or "outside" in error_msg,
                    f"Expected security error message, got: {context.exception}",
                )

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

    def test_safe_extract_tar_rejects_symlink_escape(self):
        """Test that safe tar extraction rejects symlinks pointing outside."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a tar archive with a symlink pointing outside
            tar_path = os.path.join(tmpdir, "symlink_attack.tar")

            # Create a temporary file to link to
            temp_file = os.path.join(tmpdir, "temp.txt")
            with open(temp_file, "wb") as f:
                f.write(b"test")

            # Create archive with symlink
            with tarfile.open(tar_path, "w") as tar:
                # Add a symlink that points outside the extraction directory
                info = tarfile.TarInfo(name="evil_symlink")
                info.type = tarfile.SYMTYPE
                info.linkname = "../../etc/passwd"  # Points outside
                tar.addfile(info)

            # Attempt to extract
            extract_dir = os.path.join(tmpdir, "extract")
            os.makedirs(extract_dir)
            with tarfile.open(tar_path, "r") as tar:
                with self.assertRaises(ValueError) as context:
                    _safe_extract_tar(tar, extract_dir)
                # Should mention symlink in error
                self.assertIn("symlink", str(context.exception).lower())

    def test_is_within_directory_with_symlinks(self):
        """Test path validation handles symlinks correctly."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a directory structure with symlinks
            safe_dir = os.path.join(tmpdir, "safe")
            os.makedirs(safe_dir)

            # Create a symlink inside safe_dir pointing outside
            outside_dir = os.path.join(tmpdir, "outside")
            os.makedirs(outside_dir)

            symlink_path = os.path.join(safe_dir, "link_to_outside")
            os.symlink(outside_dir, symlink_path)

            # The symlink itself (by path) is inside safe_dir
            # _is_within_directory checks the path, not where it points
            self.assertTrue(_is_within_directory(safe_dir, symlink_path))

            # A file path through the symlink (by path) is also inside
            file_through_link = os.path.join(symlink_path, "file.txt")
            self.assertTrue(_is_within_directory(safe_dir, file_through_link))

            # Note: The actual symlink target validation is done separately
            # in the _safe_extract_tar and _safe_extract_zip functions,
            # which check where symlinks actually point to.


    def test_get_full_data_path_safe(self):
        """Test that get_full_data_path returns a path within the data directory."""
        result = get_full_data_path("ttc_freq.txt")
        self.assertTrue(_is_within_directory(get_pythainlp_data_path(), result))

    def test_get_full_data_path_rejects_traversal(self):
        """Test that get_full_data_path rejects path traversal attempts."""
        with self.assertRaises(ValueError) as ctx:
            get_full_data_path("../../etc/passwd")
        self.assertIn("path traversal", str(ctx.exception).lower())

    def test_get_full_data_path_rejects_multiple_traversal(self):
        """Test that get_full_data_path rejects multiple parent directory traversal."""
        with self.assertRaises(ValueError) as ctx:
            get_full_data_path("../../../root/.ssh/id_rsa")
        self.assertIn("path traversal", str(ctx.exception).lower())

    def test_safe_path_join_bundled_corpus_safe(self):
        """Test _safe_path_join with corpus_path() base accepts safe filenames."""
        result = _safe_path_join(corpus_path(), "negations_th.txt")
        self.assertTrue(_is_within_directory(corpus_path(), result))

    def test_safe_path_join_bundled_corpus_rejects_traversal(self):
        """Test _safe_path_join with corpus_path() base rejects traversal."""
        with self.assertRaises(ValueError) as ctx:
            _safe_path_join(corpus_path(), "../../etc/passwd")
        self.assertIn("path traversal", str(ctx.exception).lower())

    def test_safe_path_join_with_tmpdir_safe(self):
        """Test _safe_path_join accepts safe sub-paths within a temp directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = _safe_path_join(tmpdir, "model.txt")
            self.assertTrue(_is_within_directory(tmpdir, result))

    def test_safe_path_join_with_tmpdir_rejects_traversal(self):
        """Test _safe_path_join rejects traversal escape from a temp directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with self.assertRaises(ValueError) as ctx:
                _safe_path_join(tmpdir, "../../etc/passwd")
            self.assertIn("path traversal", str(ctx.exception).lower())


if __name__ == "__main__":
    unittest.main()
