# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0

import unittest

import numpy as np
import yaml
from pythainlp.benchmarks import word_tokenization

with open("./tests/data/sentences.yml", "r", encoding="utf8") as stream:
    TEST_DATA = yaml.safe_load(stream)


class TestBenchmarksPackage(unittest.TestCase):
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
        result = {"key1": {"v1": 6}, "key2": {"v2": 7}}

        actual = word_tokenization._flatten_result(result)
        self.assertEqual(actual, {"key1:v1": 6, "key2:v2": 7})
