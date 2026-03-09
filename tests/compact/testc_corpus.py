# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

# Tests for corpus download/remove functions.
# These tests require network access and the "compact" dependency set.

import os
import tempfile
import unittest
from unittest.mock import patch

from pythainlp.corpus import (
    download,
    find_synonyms,
    get_corpus_db_detail,
    get_corpus_path,
    remove,
)


class CorpusDownloadTestCaseC(unittest.TestCase):
    def test_download_and_remove(self):
        """Test the full download/remove lifecycle for a test corpus."""
        # Invalid-URL / name-not-found cases
        self.assertFalse(
            download(name="test", url="wrongurl00AAfcX2df")
        )  # URL not exist
        self.assertFalse(
            download(name="XxxXXxxx817d37sf")
        )  # corpus name not exist

        # Full lifecycle: download, re-download, query, remove
        self.assertTrue(download("test"))  # download the first time
        self.assertTrue(download(name="test", force=True))  # force download
        self.assertTrue(download(name="test"))  # try download existing
        self.assertIsNotNone(get_corpus_db_detail("test"))  # corpus exists
        self.assertIsNotNone(get_corpus_path("test"))  # corpus exists
        self.assertTrue(remove("test"))  # remove existing
        self.assertFalse(remove("test"))  # remove non-existing

        # Corpus version not supported in this PyThaiNLP version
        # test 0.0.1 is for PyThaiNLP version <2.0
        self.assertFalse(download(name="test", version="0.0.1"))

    def test_download_ignores_offline_mode(self):
        """download() must work even when PYTHAINLP_OFFLINE=1.

        Explicit calls to download() are deliberate user actions and must
        not be blocked by the PYTHAINLP_OFFLINE environment variable.
        That variable only prevents the *automatic* download triggered by
        get_corpus_path() when a corpus is missing locally.
        """
        with patch.dict(os.environ, {"PYTHAINLP_OFFLINE": "1"}):
            result = download("test")
            self.assertTrue(result)

    def test_zip(self):
        """Test download and extraction of a zip corpus."""
        self.assertTrue(download("test_zip"))  # download first
        p = get_corpus_path("test_zip")
        self.assertTrue(os.path.isdir(p))
        self.assertTrue(remove("test_zip"))

    def test_find_synonyms(self):
        self.assertEqual(
            find_synonyms("หมู"), ["จรุก", "วราหะ", "วราห์", "ศูกร", "สุกร"]
        )
        self.assertEqual(find_synonyms("1"), [])


class ReadOnlyModeExplicitSaveTestCaseC(unittest.TestCase):
    """Test that user-initiated saves are allowed in read-only mode.

    Uses numpy and python-crfsuite (both in the compact dependency set).
    """

    def test_explicit_save_allowed_in_read_only(self):
        """Read-only mode must not block saves to a user-specified path.

        Read-only mode only blocks implicit background writes to PyThaiNLP's
        internal data directory.  Operations where the user explicitly
        specifies an output path must proceed normally.
        """
        import numpy as np

        from pythainlp.classify.param_free import GzipModel
        from pythainlp.tag._tag_perceptron import PerceptronTagger

        with patch.dict(
            os.environ,
            {"PYTHAINLP_READ_ONLY": "1"},
            clear=False,
        ):
            os.environ.pop("PYTHAINLP_READ_MODE", None)
            with tempfile.TemporaryDirectory() as tmpdir:
                # GzipModel.save — user explicitly provides the path
                model = object.__new__(GzipModel)
                model.training_data = np.array([("text", "label")])
                model.cx2_list = [4]
                out = os.path.join(tmpdir, "model.json")
                model.save(out)
                self.assertTrue(os.path.isfile(out))

                # PerceptronTagger.train — user explicitly provides save_loc
                tagger = PerceptronTagger()
                sentences = [[("กิน", "VV"), ("ข้าว", "NN")]]
                tagger_out = os.path.join(tmpdir, "tagger.json")
                tagger.train(sentences, save_loc=tagger_out, nr_iter=1)
                self.assertTrue(os.path.isfile(tagger_out))
