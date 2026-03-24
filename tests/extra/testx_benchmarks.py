# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

import unittest

import numpy as np
import yaml

from pythainlp.benchmarks import (
    BleuScore,
    CharLevelStats,
    GlobalStats,
    RougeScore,
    TokenizationStats,
    WordLevelStats,
    bleu_score,
    rouge_score,
    word_tokenization,
)

with open("./tests/data/sentences.yml", "r", encoding="utf8") as stream:
    TEST_DATA = yaml.safe_load(stream)


class BenchmarksTestCaseX(unittest.TestCase):
    def test_preprocessing(self):
        self.assertIsNotNone(
            word_tokenization.preprocessing(
                txt="ทดสอบ การ ทำ ความสะอาด ข้อมูล<tag>ok</tag>"
            )
        )

    def test_benchmark_not_none(self):
        self.assertIsNotNone(
            word_tokenization.benchmark(
                ["วัน", "จัน", "ทร์", "สี", "เหลือง"],
                ["วัน", "จันทร์", "สี", "เหลือง"],
            )
        )

    def test_binary_representation(self):
        sentence = "อากาศ|ร้อน|มาก|ครับ"
        rept = word_tokenization._binary_representation(sentence)

        self.assertEqual(
            [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0], rept.tolist()
        )

    def test_compute_stats(self):
        for pair in TEST_DATA["sentences"]:
            exp, act = pair["expected"], pair["actual"]

            result = word_tokenization.compute_stats(
                word_tokenization.preprocessing(exp),
                word_tokenization.preprocessing(act),
            )

            self.assertIsNotNone(result)

    def test_compute_stats_return_type(self):
        """Test that compute_stats returns a TokenizationStats typed dict."""
        ref = word_tokenization.preprocessing("อากาศ|ร้อน|มาก")
        act = word_tokenization.preprocessing("อากาศ|ร้อนมาก")

        result: TokenizationStats = word_tokenization.compute_stats(ref, act)

        self.assertIsInstance(result, dict)
        self.assertIn("char_level", result)
        self.assertIn("word_level", result)
        self.assertIn("global", result)

        char: CharLevelStats = result["char_level"]
        self.assertIsInstance(char, dict)
        self.assertIsInstance(char["tp"], int)
        self.assertIsInstance(char["fp"], int)
        self.assertIsInstance(char["tn"], int)
        self.assertIsInstance(char["fn"], int)

        word: WordLevelStats = result["word_level"]
        self.assertIsInstance(word, dict)
        self.assertIsInstance(word["correctly_tokenised_words"], int)
        self.assertIsInstance(word["total_words_in_sample"], int)
        self.assertIsInstance(word["total_words_in_ref_sample"], int)

        glob: GlobalStats = result["global"]
        self.assertIsInstance(glob, dict)
        self.assertIsInstance(glob["tokenisation_indicators"], str)

    def test_benchmark(self):
        expected = []
        actual = []
        for pair in TEST_DATA["sentences"]:
            expected.append(pair["expected"])
            actual.append(pair["actual"])

        df = word_tokenization.benchmark(expected, actual)

        self.assertIsNotNone(df)

    def test_count_correctly_tokenised_words(self):
        for d in TEST_DATA["binary_sentences"]:
            sample = np.array(list(d["actual"])).astype(int)
            ref_sample = np.array(list(d["expected"])).astype(int)

            sb = list(word_tokenization._find_word_boundaries(sample))
            rb = list(word_tokenization._find_word_boundaries(ref_sample))

            # in binary [{0, 1}, ...]
            correctly_tokenized_words = (
                word_tokenization._find_words_correctly_tokenised(rb, sb)
            )

            self.assertEqual(
                np.sum(correctly_tokenized_words), d["expected_count"]
            )

    def test_words_correctly_tokenised(self):
        r = [(0, 2), (2, 10), (10, 12)]
        s = [(0, 10), (10, 12)]

        expected = "01"

        labels = word_tokenization._find_words_correctly_tokenised(r, s)
        self.assertEqual(expected, "".join(np.array(labels).astype(str)))

    def test_flatten_result(self):
        actual = word_tokenization._flatten_result(
            {"key1": {"v1": 6}, "key2": {"v2": 7}}
        )
        self.assertEqual(actual, {"key1:v1": 6, "key2:v2": 7})

    def test_bleu_score_single_reference(self):
        """Test BLEU score with single reference per hypothesis."""
        references = ["สวัสดีครับ วันนี้อากาศดีมาก"]
        hypotheses = ["สวัสดีค่ะ วันนี้อากาศดี"]

        score = bleu_score(references, hypotheses)

        self.assertIsNotNone(score)
        self.assertIn("bleu", score)
        self.assertGreater(score["bleu"], 0)
        self.assertLessEqual(score["bleu"], 100)

    def test_bleu_score_return_type(self):
        """Test that bleu_score returns a BleuScore typed dict."""
        references = ["สวัสดีครับ วันนี้อากาศดีมาก"]
        hypotheses = ["สวัสดีค่ะ วันนี้อากาศดี"]

        score: BleuScore = bleu_score(references, hypotheses)

        self.assertIsInstance(score, dict)
        self.assertIsInstance(score["bleu"], float)
        self.assertIsInstance(score["precisions"], list)
        self.assertTrue(all(isinstance(p, float) for p in score["precisions"]))
        self.assertIsInstance(score["bp"], float)
        self.assertIsInstance(score["length_ratio"], float)
        self.assertIsInstance(score["hyp_length"], int)
        self.assertIsInstance(score["ref_length"], int)

    def test_bleu_score_multiple_references(self):
        """Test BLEU score with multiple references per hypothesis."""
        references = [
            ["สวัสดีครับ", "สวัสดีค่ะ"],
            ["ลาก่อนครับ", "ลาก่อนค่ะ"],
        ]
        hypotheses = ["สวัสดี", "ลาก่อน"]

        score = bleu_score(references, hypotheses)

        self.assertIsNotNone(score)
        self.assertIn("bleu", score)
        self.assertGreaterEqual(score["bleu"], 0)
        self.assertLessEqual(score["bleu"], 100)

    def test_bleu_score_identical_text(self):
        """Test BLEU score when reference and hypothesis are identical."""
        references = ["สวัสดีครับ วันนี้อากาศดีมาก"]
        hypotheses = ["สวัสดีครับ วันนี้อากาศดีมาก"]

        score = bleu_score(references, hypotheses)

        # For identical text, BLEU should be 100 (with sufficient length)
        self.assertEqual(score["bleu"], 100.0)

    def test_bleu_score_different_engines(self):
        """Test BLEU score with different tokenization engines."""
        references = ["สวัสดีครับ"]
        hypotheses = ["สวัสดีค่ะ"]

        # Test with newmm (default)
        score_newmm = bleu_score(references, hypotheses, tokenize="newmm")
        self.assertIsNotNone(score_newmm)
        self.assertIn("bleu", score_newmm)

        # Test with longest
        score_longest = bleu_score(references, hypotheses, tokenize="longest")
        self.assertIsNotNone(score_longest)
        self.assertIn("bleu", score_longest)

    def test_bleu_score_lowercase(self):
        """Test BLEU score with lowercase option.

        Note: This test uses mixed Thai and English text since the lowercase
        parameter is primarily useful for languages with case distinctions.
        Thai doesn't have case, so this is relevant when processing mixed
        Thai-English content or for multilingual applications.
        """
        references = ["Hello สวัสดี World โลก"]
        hypotheses = ["hello สวัสดี world โลก"]

        score_no_lower = bleu_score(references, hypotheses, lowercase=False)
        score_lower = bleu_score(references, hypotheses, lowercase=True)

        # With lowercase, identical strings should get perfect score
        self.assertEqual(score_lower["bleu"], 100.0)
        # Without lowercase, different case should result in lower score
        self.assertLess(score_no_lower["bleu"], score_lower["bleu"])

    def test_rouge_score_basic(self):
        """Test ROUGE score with basic Thai text."""
        reference = "สวัสดีครับ วันนี้อากาศดีมาก"
        hypothesis = "สวัสดีค่ะ วันนี้อากาศดี"

        scores = rouge_score(reference, hypothesis)

        self.assertIsNotNone(scores)
        self.assertIn("rouge1", scores)
        self.assertIn("rouge2", scores)
        self.assertIn("rougeL", scores)

        # Each score is a RougeScore dict with precision, recall, fmeasure
        for key in ["rouge1", "rouge2", "rougeL"]:
            self.assertIsInstance(scores[key], dict)
            self.assertIsInstance(scores[key]["precision"], float)
            self.assertIsInstance(scores[key]["recall"], float)
            self.assertIsInstance(scores[key]["fmeasure"], float)
            self.assertGreaterEqual(scores[key]["precision"], 0.0)
            self.assertLessEqual(scores[key]["precision"], 1.0)
            self.assertGreaterEqual(scores[key]["recall"], 0.0)
            self.assertLessEqual(scores[key]["recall"], 1.0)
            self.assertGreaterEqual(scores[key]["fmeasure"], 0.0)
            self.assertLessEqual(scores[key]["fmeasure"], 1.0)

    def test_rouge_score_return_type(self):
        """Test that rouge_score returns dict[str, RougeScore] typed dicts."""
        reference = "สวัสดีครับ วันนี้อากาศดีมาก"
        hypothesis = "สวัสดีค่ะ วันนี้อากาศดี"

        scores: dict[str, RougeScore] = rouge_score(reference, hypothesis)

        self.assertIsInstance(scores, dict)
        for key in ["rouge1", "rouge2", "rougeL"]:
            score: RougeScore = scores[key]
            self.assertIsInstance(score, dict)
            self.assertIn("precision", score)
            self.assertIn("recall", score)
            self.assertIn("fmeasure", score)
            self.assertIsInstance(score["precision"], float)
            self.assertIsInstance(score["recall"], float)
            self.assertIsInstance(score["fmeasure"], float)

    def test_rouge_score_identical_text(self):
        """Test ROUGE score when reference and hypothesis are identical."""
        text = "สวัสดีครับ วันนี้อากาศดีมาก"

        scores = rouge_score(text, text)

        # All scores should be perfect (1.0)
        for key in ["rouge1", "rouge2", "rougeL"]:
            self.assertEqual(scores[key]["precision"], 1.0)
            self.assertEqual(scores[key]["recall"], 1.0)
            self.assertEqual(scores[key]["fmeasure"], 1.0)

    def test_rouge_score_custom_types(self):
        """Test ROUGE score with custom rouge types."""
        reference = "สวัสดีครับ"
        hypothesis = "สวัสดีค่ะ"

        # Only ROUGE-1
        scores = rouge_score(reference, hypothesis, rouge_types=["rouge1"])
        self.assertIn("rouge1", scores)
        self.assertNotIn("rouge2", scores)
        self.assertNotIn("rougeL", scores)

        # Only ROUGE-L
        scores = rouge_score(reference, hypothesis, rouge_types=["rougeL"])
        self.assertNotIn("rouge1", scores)
        self.assertNotIn("rouge2", scores)
        self.assertIn("rougeL", scores)

    def test_rouge_score_different_engines(self):
        """Test ROUGE score with different tokenization engines."""
        reference = "สวัสดีครับ"
        hypothesis = "สวัสดีค่ะ"

        # Test with newmm (default)
        scores_newmm = rouge_score(reference, hypothesis, tokenize="newmm")
        self.assertIsNotNone(scores_newmm)

        # Test with longest
        scores_longest = rouge_score(reference, hypothesis, tokenize="longest")
        self.assertIsNotNone(scores_longest)

    def test_rouge_score_no_overlap(self):
        """Test ROUGE score with completely different text."""
        reference = "สวัสดีครับ"
        hypothesis = "ลาก่อนค่ะ"

        scores = rouge_score(reference, hypothesis)

        # Scores should be 0 or very low since there's no overlap
        for key in ["rouge1", "rouge2", "rougeL"]:
            self.assertGreaterEqual(scores[key]["precision"], 0.0)
            self.assertGreaterEqual(scores[key]["recall"], 0.0)
            self.assertGreaterEqual(scores[key]["fmeasure"], 0.0)

    def test_word_error_rate_basic(self):
        """Test WER with basic Thai text."""
        from pythainlp.benchmarks import word_error_rate

        reference = "สวัสดีครับ วันนี้อากาศดีมาก"
        hypothesis = "สวัสดีค่ะ วันนี้อากาศดี"

        wer = word_error_rate(reference, hypothesis)

        self.assertIsNotNone(wer)
        self.assertGreaterEqual(wer, 0.0)
        # WER can be > 1.0 if hypothesis has many insertions
        self.assertIsInstance(wer, float)

    def test_word_error_rate_perfect_match(self):
        """Test WER when reference and hypothesis are identical."""
        from pythainlp.benchmarks import word_error_rate

        text = "สวัสดีครับ วันนี้อากาศดีมาก"

        wer = word_error_rate(text, text)

        # Perfect match should have WER = 0
        self.assertEqual(wer, 0.0)

    def test_word_error_rate_completely_different(self):
        """Test WER with completely different text."""
        from pythainlp.benchmarks import word_error_rate

        reference = "สวัสดีครับ"
        hypothesis = "ลาก่อนค่ะ"

        wer = word_error_rate(reference, hypothesis)

        # Should be > 0 since texts are different
        self.assertGreater(wer, 0.0)

    def test_word_error_rate_different_engines(self):
        """Test WER with different tokenization engines."""
        from pythainlp.benchmarks import word_error_rate

        reference = "สวัสดีครับ"
        hypothesis = "สวัสดีค่ะ"

        # Test with newmm (default)
        wer_newmm = word_error_rate(reference, hypothesis, tokenize="newmm")
        self.assertIsNotNone(wer_newmm)
        self.assertGreaterEqual(wer_newmm, 0.0)

        # Test with longest
        wer_longest = word_error_rate(reference, hypothesis, tokenize="longest")
        self.assertIsNotNone(wer_longest)
        self.assertGreaterEqual(wer_longest, 0.0)

    def test_word_error_rate_empty_reference(self):
        """Test WER with empty reference."""
        from pythainlp.benchmarks import word_error_rate

        reference = ""
        hypothesis = "สวัสดีครับ"

        wer = word_error_rate(reference, hypothesis)

        # Empty reference with non-empty hypothesis should return inf or 0
        self.assertTrue(wer == 0.0 or wer == float('inf'))

    def test_word_error_rate_insertions(self):
        """Test WER with insertions (hypothesis longer than reference)."""
        from pythainlp.benchmarks import word_error_rate

        reference = "สวัสดี"
        hypothesis = "สวัสดี ครับ วันนี้"

        wer = word_error_rate(reference, hypothesis)

        # WER can be > 1.0 due to insertions
        self.assertGreater(wer, 0.0)

    def test_character_error_rate_basic(self):
        """Test CER with basic Thai text."""
        from pythainlp.benchmarks import character_error_rate

        reference = "สวัสดีครับ"
        hypothesis = "สวัสดีค่ะ"

        cer = character_error_rate(reference, hypothesis)

        self.assertIsNotNone(cer)
        self.assertGreaterEqual(cer, 0.0)
        self.assertIsInstance(cer, float)

    def test_character_error_rate_perfect_match(self):
        """Test CER when reference and hypothesis are identical."""
        from pythainlp.benchmarks import character_error_rate

        text = "สวัสดีครับ วันนี้อากาศดีมาก"

        cer = character_error_rate(text, text)

        # Perfect match should have CER = 0
        self.assertEqual(cer, 0.0)

    def test_character_error_rate_completely_different(self):
        """Test CER with completely different text."""
        from pythainlp.benchmarks import character_error_rate

        reference = "สวัสดี"
        hypothesis = "ลาก่อน"

        cer = character_error_rate(reference, hypothesis)

        # Should be > 0 since texts are different
        self.assertGreater(cer, 0.0)

    def test_character_error_rate_empty_reference(self):
        """Test CER with empty reference."""
        from pythainlp.benchmarks import character_error_rate

        reference = ""
        hypothesis = "สวัสดีครับ"

        cer = character_error_rate(reference, hypothesis)

        # Empty reference with non-empty hypothesis should return inf or 0
        self.assertTrue(cer == 0.0 or cer == float('inf'))

    def test_character_error_rate_insertions(self):
        """Test CER with insertions (hypothesis longer than reference)."""
        from pythainlp.benchmarks import character_error_rate

        reference = "abc"
        hypothesis = "abcd"

        cer = character_error_rate(reference, hypothesis)

        # CER should be > 0 due to insertion
        self.assertGreater(cer, 0.0)
        # CER can be > 1.0 if there are many insertions
        self.assertLess(cer, 1.0)  # Single insertion should be < 1.0

    def test_character_error_rate_deletions(self):
        """Test CER with deletions (hypothesis shorter than reference)."""
        from pythainlp.benchmarks import character_error_rate

        reference = "abcd"
        hypothesis = "abc"

        cer = character_error_rate(reference, hypothesis)

        # CER should be > 0 due to deletion
        self.assertGreater(cer, 0.0)
        self.assertLess(cer, 1.0)
