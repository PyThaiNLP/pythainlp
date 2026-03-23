# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""
Test corpus catalog download and query functionality.

These tests verify that the corpus catalog can be downloaded from
the remote server and queried correctly.
"""

import os
import tempfile
import unittest
from unittest.mock import patch

from pythainlp.corpus import (
    corpus_db_path,
    corpus_db_url,
    get_corpus_db,
    get_corpus_db_detail,
)


class CorpusCatalogTestCase(unittest.TestCase):
    """Test corpus catalog functionality."""

    def test_catalog_url(self):
        """Test that corpus catalog URL is valid and accessible."""
        url = corpus_db_url()
        self.assertIsNotNone(url)
        self.assertIsInstance(url, str)
        self.assertTrue(url.startswith("https://"))
        self.assertIn("pythainlp", url.lower())

    def test_catalog_path(self):
        """Test that corpus catalog path is valid."""
        path = corpus_db_path()
        self.assertIsNotNone(path)
        self.assertIsInstance(path, str)
        self.assertTrue(path.endswith("db.json"))

    def test_catalog_download(self):
        """Test that corpus catalog can be downloaded from remote server."""
        url = corpus_db_url()
        catalog = get_corpus_db(url)

        self.assertIsNotNone(catalog, "Catalog download should succeed")
        self.assertTrue(hasattr(catalog, "json"), "Catalog should have json method")
        self.assertTrue(
            hasattr(catalog, "status_code"), "Catalog should have status_code"
        )

    def test_catalog_structure(self):
        """Test that downloaded catalog has valid JSON structure."""
        url = corpus_db_url()
        catalog = get_corpus_db(url)

        self.assertIsNotNone(catalog)
        assert catalog is not None  # narrowing for type checker
        catalog_data = catalog.json()

        self.assertIsInstance(catalog_data, dict, "Catalog should be a dictionary")
        self.assertGreater(
            len(catalog_data), 0, "Catalog should contain at least one corpus"
        )

        # Check that catalog entries have expected structure
        for corpus_name, corpus_info in list(catalog_data.items())[:5]:
            self.assertIsInstance(corpus_name, str)
            self.assertIsInstance(corpus_info, dict)
            self.assertIn("latest_version", corpus_info)
            self.assertIn("versions", corpus_info)
            self.assertIsInstance(corpus_info["versions"], dict)

    def test_catalog_known_entries(self):
        """Test that catalog contains known corpus entries."""
        url = corpus_db_url()
        catalog = get_corpus_db(url)

        self.assertIsNotNone(catalog)
        assert catalog is not None  # narrowing for type checker
        catalog_data = catalog.json()

        # Check for some known corpus entries
        # "test" is a standard test corpus that should always exist
        self.assertIn("test", catalog_data, "Catalog should contain 'test' corpus")

        # Verify the test corpus has required fields
        test_corpus = catalog_data["test"]
        self.assertIn("latest_version", test_corpus)
        self.assertIn("versions", test_corpus)

    def test_corpus_detail_query(self):
        """Test querying details for specific corpus from local database."""
        # This tests the local query function
        # First, ensure we have a local database by attempting a download/query
        url = corpus_db_url()
        catalog = get_corpus_db(url)
        self.assertIsNotNone(catalog)

        # Test querying a corpus that may exist locally
        # get_corpus_db_detail reads from local db.json file
        detail = get_corpus_db_detail("test")
        # Detail could be empty if not downloaded, but should return a dict
        self.assertIsInstance(detail, dict)

        # Test querying non-existent corpus
        detail_nonexist = get_corpus_db_detail("NONEXISTENT_CORPUS_12345")
        self.assertIsInstance(detail_nonexist, dict)
        self.assertEqual(len(detail_nonexist), 0, "Non-existent corpus should return empty dict")

    def test_no_db_json_created_on_import(self):
        """Test that importing pythainlp.corpus does not create db.json."""
        with tempfile.TemporaryDirectory() as tmpdir:
            non_existent_path = os.path.join(tmpdir, "db.json")

            with patch(
                "pythainlp.corpus._CORPUS_DB_PATH",
                non_existent_path,
            ):
                import importlib

                import pythainlp.corpus as corpus_module
                importlib.reload(corpus_module)
                self.assertFalse(
                    os.path.exists(non_existent_path),
                    "db.json should NOT be created on import when it does not exist",
                )

    def test_get_corpus_db_detail_no_db_json(self):
        """Test that get_corpus_db_detail returns empty dict when db.json is absent."""
        with tempfile.TemporaryDirectory() as tmpdir:
            non_existent_path = os.path.join(tmpdir, "nonexistent_db.json")
            with patch(
                "pythainlp.corpus.core.corpus_db_path",
                return_value=non_existent_path,
            ):
                detail = get_corpus_db_detail("any_corpus")
        self.assertIsInstance(detail, dict)
        self.assertEqual(detail, {})

    def test_catalog_version_info(self):
        """Test that catalog entries contain valid version information."""
        url = corpus_db_url()
        catalog = get_corpus_db(url)

        self.assertIsNotNone(catalog)
        assert catalog is not None  # narrowing for type checker
        catalog_data = catalog.json()

        # Check version information for test corpus
        if "test" in catalog_data:
            test_corpus = catalog_data["test"]
            versions = test_corpus.get("versions", {})

            self.assertIsInstance(versions, dict)
            if versions:
                # Check structure of version entries
                for version_key, version_info in list(versions.items())[:1]:
                    self.assertIsInstance(version_key, str)
                    self.assertIsInstance(version_info, dict)
                    # Version info should have these fields
                    self.assertIn("filename", version_info)
                    self.assertIn("download_url", version_info)
