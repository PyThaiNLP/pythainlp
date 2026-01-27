# SPDX-FileCopyrightText: 2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Thread-safety tests for word tokenization engines."""

import threading
import unittest

from pythainlp.corpus.common import thai_words
from pythainlp.tokenize import word_tokenize
from pythainlp.util import dict_trie


class TestThreadSafety(unittest.TestCase):
    """Test thread safety of word_tokenize() functions."""

    def setUp(self):
        """Set up test data."""
        self.test_texts = [
            "ผมรักประเทศไทย",
            "วันนี้อากาศดีมาก",
            "เขาไปโรงเรียนทุกวัน",
            "ฉันชอบกินอาหารไทย",
            "พวกเราเรียนภาษาไทย",
        ]

    def _tokenize_worker(
        self,
        text: str,
        engine: str,
        results: list,
        index: int,
        custom_dict=None,
        iterations: int = 10,
    ):
        """Worker function for thread testing."""
        try:
            for _ in range(iterations):
                tokens = word_tokenize(
                    text, engine=engine, custom_dict=custom_dict
                )
                # Store result for later verification
                if results[index] is None:
                    results[index] = tokens
                elif results[index] != tokens:
                    # Different results indicate a thread-safety issue
                    results[index] = "INCONSISTENT"
        except Exception as e:
            results[index] = f"ERROR: {str(e)}"

    def test_newmm_thread_safety(self):
        """Test thread safety of newmm engine."""
        num_threads = 10
        results = [None] * num_threads
        threads = []

        text = self.test_texts[0]
        for i in range(num_threads):
            thread = threading.Thread(
                target=self._tokenize_worker,
                args=(text, "newmm", results, i),
            )
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        # All threads should produce the same result
        first_result = results[0]
        self.assertIsNotNone(first_result)
        self.assertNotEqual(first_result, "INCONSISTENT")
        for result in results:
            self.assertEqual(result, first_result)

    def test_newmm_safe_thread_safety(self):
        """Test thread safety of newmm-safe engine."""
        num_threads = 10
        results = [None] * num_threads
        threads = []

        text = self.test_texts[0]
        for i in range(num_threads):
            thread = threading.Thread(
                target=self._tokenize_worker,
                args=(text, "newmm-safe", results, i),
            )
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        # All threads should produce the same result
        first_result = results[0]
        self.assertIsNotNone(first_result)
        self.assertNotEqual(first_result, "INCONSISTENT")
        for result in results:
            self.assertEqual(result, first_result)

    def test_longest_thread_safety(self):
        """Test thread safety of longest engine."""
        num_threads = 10
        results = [None] * num_threads
        threads = []

        text = self.test_texts[0]
        for i in range(num_threads):
            thread = threading.Thread(
                target=self._tokenize_worker,
                args=(text, "longest", results, i),
            )
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        # All threads should produce the same result
        first_result = results[0]
        self.assertIsNotNone(first_result)
        self.assertNotEqual(first_result, "INCONSISTENT")
        self.assertNotIn("ERROR:", str(first_result))
        for result in results:
            self.assertEqual(result, first_result)

    def test_longest_thread_safety_with_custom_dict(self):
        """Test thread safety of longest engine with custom dictionary."""
        num_threads = 10
        results = [None] * num_threads
        threads = []

        # Create a custom dictionary
        custom_words = set(thai_words())
        custom_words.add("พวกเรา")
        custom_dict = dict_trie(custom_words)

        text = self.test_texts[4]  # "พวกเราเรียนภาษาไทย"
        for i in range(num_threads):
            thread = threading.Thread(
                target=self._tokenize_worker,
                args=(text, "longest", results, i, custom_dict),
            )
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        # All threads should produce the same result
        first_result = results[0]
        self.assertIsNotNone(first_result)
        self.assertNotEqual(first_result, "INCONSISTENT")
        self.assertNotIn("ERROR:", str(first_result))
        for result in results:
            self.assertEqual(result, first_result)

    def test_longest_race_condition_multiple_dicts(self):
        """Test race condition with multiple dictionaries being registered."""
        num_threads = 20
        results = [None] * num_threads
        threads = []

        text = self.test_texts[0]
        # Each thread uses a slightly different custom dictionary
        # to trigger the cache registration race condition
        for i in range(num_threads):
            custom_words = set(thai_words())
            # Add a unique word per thread to create different dict objects
            custom_words.add(f"คำทดสอบ{i}")
            custom_dict = dict_trie(custom_words)

            thread = threading.Thread(
                target=self._tokenize_worker,
                args=(text, "longest", results, i, custom_dict, 5),
            )
            threads.append(thread)

        # Start all threads at once to maximize race condition chance
        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        # All threads should succeed
        # (but may have different results due to different dicts)
        for i, result in enumerate(results):
            self.assertIsNotNone(result, f"Thread {i} returned None")
            self.assertNotEqual(
                result, "INCONSISTENT", f"Thread {i} inconsistent"
            )
            self.assertNotIn(
                "ERROR:", str(result), f"Thread {i} error: {result}"
            )

    def test_multi_text_concurrent_tokenization(self):
        """Test concurrent tokenization of different texts."""
        num_threads = len(self.test_texts)
        results = [None] * num_threads
        threads = []

        # Each thread processes a different text
        for i, text in enumerate(self.test_texts):
            thread = threading.Thread(
                target=self._tokenize_worker,
                args=(text, "longest", results, i),
            )
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        # All threads should succeed
        for i, result in enumerate(results):
            self.assertIsNotNone(result, f"Thread {i} returned None")
            self.assertNotEqual(
                result, "INCONSISTENT", f"Thread {i} inconsistent"
            )
            self.assertNotIn(
                "ERROR:", str(result), f"Thread {i} error: {result}"
            )
            self.assertIsInstance(result, list, f"Thread {i} wrong type")

    def test_mm_thread_safety(self):
        """Test thread safety of mm (multi_cut) engine."""
        num_threads = 10
        results = [None] * num_threads
        threads = []

        text = self.test_texts[0]
        for i in range(num_threads):
            thread = threading.Thread(
                target=self._tokenize_worker,
                args=(text, "mm", results, i),
            )
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        # All threads should produce the same result
        first_result = results[0]
        self.assertIsNotNone(first_result)
        self.assertNotEqual(first_result, "INCONSISTENT")
        for result in results:
            self.assertEqual(result, first_result)

    def test_icu_thread_safety(self):
        """Test thread safety of icu engine (if available)."""
        try:
            from icu import BreakIterator  # noqa: F401
        except ImportError:
            self.skipTest("PyICU not installed")

        num_threads = 10
        results = [None] * num_threads
        threads = []

        text = self.test_texts[0]
        for i in range(num_threads):
            thread = threading.Thread(
                target=self._tokenize_worker,
                args=(text, "icu", results, i),
            )
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        # All threads should produce the same result
        first_result = results[0]
        self.assertIsNotNone(first_result)
        self.assertNotEqual(first_result, "INCONSISTENT")
        self.assertNotIn("ERROR:", str(first_result))
        for result in results:
            self.assertEqual(result, first_result)

    def test_attacut_thread_safety(self):
        """Test thread safety of attacut engine (if available)."""
        try:
            from attacut import Tokenizer  # noqa: F401
        except ImportError:
            self.skipTest("attacut not installed")

        num_threads = 10
        results = [None] * num_threads
        threads = []

        text = self.test_texts[0]
        for i in range(num_threads):
            thread = threading.Thread(
                target=self._tokenize_worker,
                args=(text, "attacut", results, i),
            )
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        # All threads should produce the same result
        first_result = results[0]
        self.assertIsNotNone(first_result)
        self.assertNotEqual(first_result, "INCONSISTENT")
        self.assertNotIn("ERROR:", str(first_result))
        for result in results:
            self.assertEqual(result, first_result)


if __name__ == "__main__":
    unittest.main()
