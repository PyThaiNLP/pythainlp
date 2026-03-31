# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

import os
import unittest
from unittest.mock import mock_open, patch

from pythainlp.corpus import (
    countries,
    download,
    get_corpus_db,
    get_corpus_db_detail,
    get_corpus_default_db,
    get_corpus_path,
    oscar,
    phupha,
    provinces,
    thai_family_names,
    thai_female_names,
    thai_icu_words,
    thai_male_names,
    thai_negations,
    thai_orst_words,
    thai_stopwords,
    thai_syllables,
    thai_synonyms,
    thai_volubilis_words,
    thai_wikipedia_titles,
    thai_words,
    tnc,
    ttc,
)
from pythainlp.corpus.core import _check_version, _version2int
from pythainlp.corpus.util import revise_newmm_default_wordset


class CorpusTestCase(unittest.TestCase):
    def test_corpus(self):
        self.assertIsInstance(thai_negations(), frozenset)
        self.assertGreater(len(thai_negations()), 0)
        self.assertIsInstance(thai_stopwords(), frozenset)
        self.assertGreater(len(thai_stopwords()), 0)
        self.assertIsInstance(thai_syllables(), frozenset)
        self.assertGreater(len(thai_syllables()), 0)
        self.assertIsInstance(thai_synonyms(), dict)
        self.assertGreater(len(thai_synonyms()), 0)

        self.assertIsInstance(thai_icu_words(), frozenset)
        self.assertGreater(len(thai_icu_words()), 0)
        self.assertIsInstance(thai_orst_words(), frozenset)
        self.assertGreater(len(thai_orst_words()), 0)
        self.assertIsInstance(thai_volubilis_words(), frozenset)
        self.assertGreater(len(thai_volubilis_words()), 0)
        self.assertIsInstance(thai_wikipedia_titles(), frozenset)
        self.assertGreater(len(thai_wikipedia_titles()), 0)
        self.assertIsInstance(thai_words(), frozenset)
        self.assertGreater(len(thai_words()), 0)

        self.assertIsInstance(countries(), frozenset)
        self.assertGreater(len(countries()), 0)
        self.assertIsInstance(provinces(), frozenset)
        self.assertGreater(len(provinces()), 0)
        self.assertIsInstance(provinces(details=True), list)
        self.assertEqual(
            len(provinces(details=False)), len(provinces(details=True))
        )

        self.assertIsInstance(thai_family_names(), frozenset)
        self.assertIsInstance(list(thai_family_names())[0], str)
        self.assertIsInstance(thai_female_names(), frozenset)
        self.assertIsInstance(thai_male_names(), frozenset)

        # Tying not to download big files here, it slow down the test

        self.assertIsNone(get_corpus_default_db("3XKg0013", "1.2.345"))

        # BEGIN - Test non-exists
        # self.assertIsInstance(
        #     get_corpus_db("https://example.com/XXXXXX0lkjasd/SXfmskdjKKXXX"),
        #     Response,
        # )  # URL does not exist, should get 404 response
        self.assertIsNone(get_corpus_db("XXXlkja3sfdXX"))  # Invalid URL
        self.assertEqual(
            get_corpus_db_detail("XXXmx3KSXX"), {}
        )  # corpus does not exist
        self.assertEqual(
            get_corpus_db_detail("XXXmx3KSXX", version="0.2"), {}
        )  # corpus does not exist
        self.assertIsNone(get_corpus_path("XXXkdjfBzc"))  # query non-existing
        # END - Test non-exists

    def test_oscar(self):
        # Mock the oscar corpus file to avoid slow download and parsing
        # Format: word,count
        # Note: A line starting with space becomes empty string after strip()
        mock_oscar_data = """word,count
คน,1000
ไทย,500
ภาษา,300
 ,100
"test",50
"""
        mock_path = "/mock/path/oscar_icu"

        with patch(
            "pythainlp.corpus.oscar.get_corpus_path", return_value=mock_path
        ):
            with patch("builtins.open", mock_open(read_data=mock_oscar_data)):
                result = oscar.word_freqs()
                self.assertIsNotNone(result)
                self.assertIsInstance(result, list)
                self.assertGreater(len(result), 0)
                # Verify parsing logic
                self.assertEqual(result[0], ("คน", 1000))
                # Space line becomes empty string (not <s/>) due to strip()
                self.assertIn(("", 100), result)
                # Verify quoted values are filtered out
                for word, _ in result:
                    self.assertNotIn('"', word)

                # Reset mock for unigram test
                with patch(
                    "builtins.open", mock_open(read_data=mock_oscar_data)
                ):
                    result_unigram = oscar.unigram_word_freqs()
                    self.assertIsNotNone(result_unigram)
                    self.assertIsInstance(result_unigram, dict)
                    self.assertGreater(len(result_unigram), 0)
                    self.assertEqual(result_unigram["คน"], 1000)

    def test_tnc(self):
        # Mock TNC unigram corpus
        mock_unigram_data = """คน	1000
ไทย	500
ภาษา	300"""

        # Mock TNC bigram corpus
        mock_bigram_data = """คน	ไทย	100
ไทย	ภาษา	50
ภาษา	ไทย	30"""

        # Mock TNC trigram corpus
        mock_trigram_data = """คน	ไทย	ภาษา	10
ไทย	ภาษา	ไทย	5
ภาษา	ไทย	คน	3"""

        # Test unigram functions
        with patch(
            "pythainlp.corpus.tnc.get_corpus",
            return_value=frozenset(mock_unigram_data.split("\n")),
        ):
            result = tnc.word_freqs()
            self.assertIsNotNone(result)
            self.assertIsInstance(result, list)
            self.assertGreater(len(result), 0)
            # Check that at least one expected entry exists (order not guaranteed)
            self.assertIn(("คน", 1000), result)

            result_unigram = tnc.unigram_word_freqs()
            self.assertIsNotNone(result_unigram)
            self.assertIsInstance(result_unigram, dict)
            self.assertGreater(len(result_unigram), 0)
            self.assertEqual(result_unigram["คน"], 1000)

        # Test bigram function
        mock_bigram_path = "/mock/path/bigram"
        with patch(
            "pythainlp.corpus.tnc.get_corpus_path",
            return_value=mock_bigram_path,
        ):
            with patch("builtins.open", mock_open(read_data=mock_bigram_data)):
                result_bigram = tnc.bigram_word_freqs()
                self.assertIsNotNone(result_bigram)
                self.assertIsInstance(result_bigram, dict)
                self.assertGreater(len(result_bigram), 0)
                self.assertEqual(result_bigram[("คน", "ไทย")], 100)

        # Test trigram function
        mock_trigram_path = "/mock/path/trigram"
        with patch(
            "pythainlp.corpus.tnc.get_corpus_path",
            return_value=mock_trigram_path,
        ):
            with patch(
                "builtins.open", mock_open(read_data=mock_trigram_data)
            ):
                result_trigram = tnc.trigram_word_freqs()
                self.assertIsNotNone(result_trigram)
                self.assertIsInstance(result_trigram, dict)
                self.assertGreater(len(result_trigram), 0)
                self.assertEqual(result_trigram[("คน", "ไทย", "ภาษา")], 10)

    def test_phupha(self):
        # Test word_freqs() returns list of tuples
        word_freqs_result = phupha.word_freqs()
        self.assertIsNotNone(word_freqs_result)
        self.assertIsInstance(word_freqs_result, list)
        self.assertGreater(len(word_freqs_result), 0)
        # Check first item is a tuple of (str, int)
        self.assertIsInstance(word_freqs_result[0], tuple)
        self.assertEqual(len(word_freqs_result[0]), 2)
        self.assertIsInstance(word_freqs_result[0][0], str)
        self.assertIsInstance(word_freqs_result[0][1], int)

        # Test unigram_word_freqs() returns dict
        unigram_result = phupha.unigram_word_freqs()
        self.assertIsNotNone(unigram_result)
        self.assertIsInstance(unigram_result, dict)
        self.assertGreater(len(unigram_result), 0)

        # Check that common Thai words exist
        self.assertIn("ไทย", unigram_result)
        self.assertGreater(unigram_result["ไทย"], 0)

        # Verify the full dataset is available (not pre-filtered)
        # The full dataset should have more words than just ORST
        self.assertGreater(len(word_freqs_result), 38000)

    def test_ttc(self):
        # Mock TTC corpus
        mock_ttc_data = """คน	1000
ไทย	500
ภาษา	300"""

        with patch(
            "pythainlp.corpus.ttc.get_corpus",
            return_value=frozenset(mock_ttc_data.split("\n")),
        ):
            result = ttc.word_freqs()
            self.assertIsNotNone(result)
            self.assertIsInstance(result, list)
            self.assertGreater(len(result), 0)
            # Check that at least one expected entry exists (order not guaranteed)
            self.assertIn(("คน", 1000), result)

            result_unigram = ttc.unigram_word_freqs()
            self.assertIsNotNone(result_unigram)
            self.assertIsInstance(result_unigram, dict)
            self.assertGreater(len(result_unigram), 0)
            self.assertEqual(result_unigram["คน"], 1000)

    def test_get_corpus_path_offline_mode(self):
        """Test get_corpus_path() behavior with PYTHAINLP_OFFLINE env var."""
        # Unknown corpus name: download is attempted (it fails) → None
        with patch.dict(os.environ, {"PYTHAINLP_OFFLINE": ""}):
            self.assertIsNone(get_corpus_path("XXXkdjfBzc_nonexistent"))

        # When PYTHAINLP_OFFLINE=1 and corpus not in local catalog → raises
        with patch.dict(os.environ, {"PYTHAINLP_OFFLINE": "1"}):
            with patch(
                "pythainlp.corpus.core.get_corpus_db_detail",
                return_value={},
            ):
                with self.assertRaises(FileNotFoundError) as ctx:
                    get_corpus_path("some_corpus")
                self.assertIn("PYTHAINLP_OFFLINE", str(ctx.exception))

        # When PYTHAINLP_OFFLINE=1 and file registered but missing → raises
        fake_db_detail = {"name": "fake_corpus", "filename": "fake_file.txt"}
        with patch.dict(os.environ, {"PYTHAINLP_OFFLINE": "1"}):
            with patch(
                "pythainlp.corpus.core.get_corpus_db_detail",
                return_value=fake_db_detail,
            ):
                with patch("os.path.exists", return_value=False):
                    with self.assertRaises(FileNotFoundError) as ctx:
                        get_corpus_path("fake_corpus")
                    self.assertIn("PYTHAINLP_OFFLINE", str(ctx.exception))

        # When PYTHAINLP_OFFLINE=1 and file exists → returns path normally
        with patch.dict(os.environ, {"PYTHAINLP_OFFLINE": "1"}):
            with patch(
                "pythainlp.corpus.core.get_corpus_db_detail",
                return_value=fake_db_detail,
            ):
                with patch("os.path.exists", return_value=True):
                    result = get_corpus_path("fake_corpus")
                    self.assertIsNotNone(result)
                    self.assertNotEqual(result, "")

    def test_download_read_only_mode(self):
        """Test that download() returns False when read-only mode is active.

        When the data directory is read-only (e.g. a read-only mounted volume),
        download() must not attempt any network or file-system operations and
        must return False immediately.  This is stricter than offline mode:
        PYTHAINLP_OFFLINE only prevents *automatic* downloads; PYTHAINLP_READ_ONLY
        also prevents explicit download() calls.
        """
        # Corpus not in cache — must fail in read-only mode.
        with patch(
            "pythainlp.corpus.core.is_read_only_mode", return_value=True
        ):
            result = download("not_a_real_corpus_xyz123")
            self.assertFalse(result)

        # Sanity-check: with read-only mode off, the call is at least
        # attempted (returns False because the corpus does not exist remotely,
        # not because of read-only mode).
        with patch(
            "pythainlp.corpus.core.is_read_only_mode", return_value=False
        ):
            with patch(
                "pythainlp.corpus.core.get_corpus_db",
                return_value=None,
            ):
                result = download("not_a_real_corpus_xyz123")
                self.assertFalse(result)

    def test_revise_wordset(self):
        training_data = [
            ["ถวิล อุดล", " ", "เป็น", "นักการเมือง", "หนึ่ง", "ใน"],
            ["สี่เสืออีสาน", " ", "ซึ่ง", "ประกอบ", "ด้วย", "ตัว", "นายถวิล"],
            ["เอง", " ", "นายทองอินทร์ ภูริพัฒน์", " ", "นายเตียง ศิริขันธ์"],
            [" ", "และ", "นายจำลอง ดาวเรือง", " ", "และ", "เป็น", "รัฐมนตรี"],
            ["ที่", "ถูก", "สังหาร", "เมื่อ", "ปี", " ", "พ.ศ.", " ", "2492"],
        ]
        self.assertIsInstance(revise_newmm_default_wordset(training_data), set)


class DefensiveLoadingTestCase(unittest.TestCase):
    """Tests for warning-based defensive loading in corpus/common.py."""

    # ------------------------------------------------------------------
    # provinces()
    # ------------------------------------------------------------------

    def test_provinces_skips_short_line_with_warning(self):
        import pythainlp.corpus.common as m

        with patch.object(m, "_THAI_THAILAND_PROVINCES", frozenset()):
            with patch.object(m, "_THAI_THAILAND_PROVINCES_DETAILS", []):
                with patch(
                    "pythainlp.corpus.common.get_corpus_as_is",
                    return_value=["กรุงเทพ,กทม"],  # only 2 fields, needs 4
                ):
                    with self.assertWarns(UserWarning) as cm:
                        result = m.provinces()
                    self.assertEqual(len(result), 0)
                    self.assertIn("too few fields", str(cm.warning))

    def test_provinces_skips_blank_field_with_warning(self):
        import pythainlp.corpus.common as m

        with patch.object(m, "_THAI_THAILAND_PROVINCES", frozenset()):
            with patch.object(m, "_THAI_THAILAND_PROVINCES_DETAILS", []):
                with patch(
                    "pythainlp.corpus.common.get_corpus_as_is",
                    return_value=["กรุงเทพ,,Bangkok,BKK"],  # blank abbr_th
                ):
                    with self.assertWarns(UserWarning) as cm:
                        result = m.provinces()
                    self.assertEqual(len(result), 0)
                    self.assertIn("blank or empty", str(cm.warning))

    def test_provinces_skips_whitespace_only_field_with_warning(self):
        import pythainlp.corpus.common as m

        with patch.object(m, "_THAI_THAILAND_PROVINCES", frozenset()):
            with patch.object(m, "_THAI_THAILAND_PROVINCES_DETAILS", []):
                with patch(
                    "pythainlp.corpus.common.get_corpus_as_is",
                    return_value=["กรุงเทพ,   ,Bangkok,BKK"],  # whitespace-only abbr_th
                ):
                    with self.assertWarns(UserWarning):
                        result = m.provinces()
                    self.assertEqual(len(result), 0)

    def test_provinces_loads_valid_entry(self):
        import pythainlp.corpus.common as m

        with patch.object(m, "_THAI_THAILAND_PROVINCES", frozenset()):
            with patch.object(m, "_THAI_THAILAND_PROVINCES_DETAILS", []):
                with patch(
                    "pythainlp.corpus.common.get_corpus_as_is",
                    return_value=["กรุงเทพมหานคร,กทม,Bangkok,BKK"],
                ):
                    result = m.provinces()
                    self.assertIn("กรุงเทพมหานคร", result)

    # ------------------------------------------------------------------
    # thai_dict()
    # ------------------------------------------------------------------

    def test_thai_dict_skips_none_word_with_warning(self):
        import pythainlp.corpus.common as m

        mock_rows = [
            {"word": "แมว", "meaning": "cat"},
            {"word": None, "meaning": "some meaning"},  # None word
        ]
        with patch.object(m, "_THAI_DICT", {}):
            with patch(
                "pythainlp.corpus.common.get_corpus_path",
                return_value="/mock/path",
            ):
                with patch("builtins.open", mock_open()):
                    with patch("csv.DictReader", return_value=mock_rows):
                        with self.assertWarns(UserWarning) as cm:
                            result = m.thai_dict()
                        self.assertEqual(result["word"], ["แมว"])
                        self.assertIn("missing or empty", str(cm.warning))

    def test_thai_dict_skips_empty_word_with_warning(self):
        import pythainlp.corpus.common as m

        mock_rows = [
            {"word": "แมว", "meaning": "cat"},
            {"word": "", "meaning": "empty word field"},  # empty word
        ]
        with patch.object(m, "_THAI_DICT", {}):
            with patch(
                "pythainlp.corpus.common.get_corpus_path",
                return_value="/mock/path",
            ):
                with patch("builtins.open", mock_open()):
                    with patch("csv.DictReader", return_value=mock_rows):
                        with self.assertWarns(UserWarning):
                            result = m.thai_dict()
                        self.assertEqual(result["word"], ["แมว"])

    def test_thai_dict_skips_whitespace_only_word_with_warning(self):
        import pythainlp.corpus.common as m

        mock_rows = [
            {"word": "แมว", "meaning": "cat"},
            {"word": "   ", "meaning": "whitespace word"},
        ]
        with patch.object(m, "_THAI_DICT", {}):
            with patch(
                "pythainlp.corpus.common.get_corpus_path",
                return_value="/mock/path",
            ):
                with patch("builtins.open", mock_open()):
                    with patch("csv.DictReader", return_value=mock_rows):
                        with self.assertWarns(UserWarning):
                            result = m.thai_dict()
                        self.assertEqual(result["word"], ["แมว"])

    def test_thai_dict_skips_none_meaning_with_warning(self):
        import pythainlp.corpus.common as m

        mock_rows = [
            {"word": "แมว", "meaning": "cat"},
            {"word": "หมา", "meaning": None},  # None meaning (short CSV row)
        ]
        with patch.object(m, "_THAI_DICT", {}):
            with patch(
                "pythainlp.corpus.common.get_corpus_path",
                return_value="/mock/path",
            ):
                with patch("builtins.open", mock_open()):
                    with patch("csv.DictReader", return_value=mock_rows):
                        with self.assertWarns(UserWarning):
                            result = m.thai_dict()
                        self.assertEqual(result["word"], ["แมว"])

    def test_thai_dict_returns_empty_when_no_path(self):
        import pythainlp.corpus.common as m

        with patch.object(m, "_THAI_DICT", {}):
            with patch(
                "pythainlp.corpus.common.get_corpus_path", return_value=None
            ):
                result = m.thai_dict()
                self.assertEqual(result, {})

    # ------------------------------------------------------------------
    # thai_wsd_dict()
    # ------------------------------------------------------------------

    def test_thai_wsd_dict_skips_none_meaning_with_warning(self):
        import pythainlp.corpus.common as m

        # None meaning causes TypeError in ast.literal_eval
        mock_source = {"word": ["แมว"], "meaning": [None]}
        with patch.object(m, "_THAI_WSD_DICT", {}):
            with patch("pythainlp.corpus.common.thai_dict", return_value=mock_source):
                with self.assertWarns(UserWarning) as cm:
                    result = m.thai_wsd_dict()
                self.assertEqual(result["word"], [])
                self.assertIn("could not be parsed", str(cm.warning))

    def test_thai_wsd_dict_skips_unparseable_meaning_with_warning(self):
        import pythainlp.corpus.common as m

        mock_source = {"word": ["แมว"], "meaning": ["not valid python literal!!!"]}
        with patch.object(m, "_THAI_WSD_DICT", {}):
            with patch("pythainlp.corpus.common.thai_dict", return_value=mock_source):
                with self.assertWarns(UserWarning) as cm:
                    result = m.thai_wsd_dict()
                self.assertEqual(result["word"], [])
                self.assertIn("could not be parsed", str(cm.warning))

    def test_thai_wsd_dict_skips_non_dict_meaning_with_warning(self):
        import pythainlp.corpus.common as m

        # Parses OK but yields a list, not a dict
        mock_source = {"word": ["แมว"], "meaning": ["['cat', 'kitty']"]}
        with patch.object(m, "_THAI_WSD_DICT", {}):
            with patch("pythainlp.corpus.common.thai_dict", return_value=mock_source):
                with self.assertWarns(UserWarning) as cm:
                    result = m.thai_wsd_dict()
                self.assertEqual(result["word"], [])
                self.assertIn("expected dict", str(cm.warning))

    # ------------------------------------------------------------------
    # thai_synonyms()
    # ------------------------------------------------------------------

    def test_thai_synonyms_skips_none_synonym_with_warning(self):
        import pythainlp.corpus.common as m

        mock_rows = [
            {"word": "แมว", "pos": "n", "synonym": "cat|kitty"},
            {"word": "หมา", "pos": "n", "synonym": None},  # None synonym
        ]
        with patch.object(m, "_THAI_SYNONYMS", {}):
            with patch(
                "pythainlp.corpus.common.get_corpus_path",
                return_value="/mock/path",
            ):
                with patch("builtins.open", mock_open()):
                    with patch("csv.DictReader", return_value=mock_rows):
                        with self.assertWarns(UserWarning):
                            result = m.thai_synonyms()
                        self.assertEqual(result["word"], ["แมว"])
                        self.assertEqual(result["synonym"], [["cat", "kitty"]])

    def test_thai_synonyms_skips_none_word_with_warning(self):
        import pythainlp.corpus.common as m

        mock_rows = [
            {"word": "แมว", "pos": "n", "synonym": "cat|kitty"},
            {"word": None, "pos": "n", "synonym": "dog"},  # None word
        ]
        with patch.object(m, "_THAI_SYNONYMS", {}):
            with patch(
                "pythainlp.corpus.common.get_corpus_path",
                return_value="/mock/path",
            ):
                with patch("builtins.open", mock_open()):
                    with patch("csv.DictReader", return_value=mock_rows):
                        with self.assertWarns(UserWarning):
                            result = m.thai_synonyms()
                        self.assertEqual(result["word"], ["แมว"])

    def test_thai_synonyms_skips_none_pos_with_warning(self):
        import pythainlp.corpus.common as m

        mock_rows = [
            {"word": "แมว", "pos": "n", "synonym": "cat|kitty"},
            {"word": "หมา", "pos": None, "synonym": "dog"},  # None pos
        ]
        with patch.object(m, "_THAI_SYNONYMS", {}):
            with patch(
                "pythainlp.corpus.common.get_corpus_path",
                return_value="/mock/path",
            ):
                with patch("builtins.open", mock_open()):
                    with patch("csv.DictReader", return_value=mock_rows):
                        with self.assertWarns(UserWarning):
                            result = m.thai_synonyms()
                        self.assertEqual(result["word"], ["แมว"])

    def test_thai_synonyms_skips_empty_pos_with_warning(self):
        import pythainlp.corpus.common as m

        mock_rows = [
            {"word": "แมว", "pos": "n", "synonym": "cat|kitty"},
            {"word": "หมา", "pos": "", "synonym": "dog"},  # empty pos
        ]
        with patch.object(m, "_THAI_SYNONYMS", {}):
            with patch(
                "pythainlp.corpus.common.get_corpus_path",
                return_value="/mock/path",
            ):
                with patch("builtins.open", mock_open()):
                    with patch("csv.DictReader", return_value=mock_rows):
                        with self.assertWarns(UserWarning):
                            result = m.thai_synonyms()
                        self.assertEqual(result["word"], ["แมว"])

    def test_thai_synonyms_skips_whitespace_only_fields_with_warning(self):
        import pythainlp.corpus.common as m

        mock_rows = [
            {"word": "แมว", "pos": "n", "synonym": "cat|kitty"},
            {"word": "  ", "pos": "n", "synonym": "dog"},   # whitespace word
            {"word": "หมา", "pos": "  ", "synonym": "dog"}, # whitespace pos
            {"word": "ปลา", "pos": "n", "synonym": "  "},   # whitespace synonym
        ]
        with patch.object(m, "_THAI_SYNONYMS", {}):
            with patch(
                "pythainlp.corpus.common.get_corpus_path",
                return_value="/mock/path",
            ):
                with patch("builtins.open", mock_open()):
                    with patch("csv.DictReader", return_value=mock_rows):
                        with self.assertWarns(UserWarning):
                            result = m.thai_synonyms()
                        self.assertEqual(result["word"], ["แมว"])

    def test_thai_synonyms_loads_valid_rows(self):
        import pythainlp.corpus.common as m

        mock_rows = [
            {"word": "แมว", "pos": "n", "synonym": "cat|kitty"},
            {"word": "หมา", "pos": "n", "synonym": "dog"},
        ]
        with patch.object(m, "_THAI_SYNONYMS", {}):
            with patch(
                "pythainlp.corpus.common.get_corpus_path",
                return_value="/mock/path",
            ):
                with patch("builtins.open", mock_open()):
                    with patch("csv.DictReader", return_value=mock_rows):
                        result = m.thai_synonyms()
                        self.assertEqual(result["word"], ["แมว", "หมา"])
                        self.assertEqual(result["pos"], ["n", "n"])
                        self.assertEqual(
                            result["synonym"], [["cat", "kitty"], ["dog"]]
                        )

    def test_check_version(self):
        # Reproduce: _check_version with <= and < used temp[0] which
        # only gets the first character of the version string instead
        # of the full version, causing incorrect comparisons.
        self.assertTrue(_check_version("*"))
        self.assertTrue(_check_version("<=9999.9.9"))
        self.assertTrue(_check_version("<9999.9.9"))
        self.assertTrue(_check_version(">=0.0.1"))
        self.assertTrue(_check_version(">0.0.1"))
        self.assertFalse(_check_version("<=0.0.1"))
        self.assertFalse(_check_version("<0.0.1"))
        # version2int consistency
        self.assertNotEqual(_version2int("5.3.3"), _version2int("5"))
        self.assertEqual(_version2int("2.0"), _version2int("2.0.0"))
