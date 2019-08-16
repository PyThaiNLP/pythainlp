import datetime
import os
import sys
import unittest
import yaml
import numpy as np

from pythainlp.benchmarks import word_tokenisation

with open("./tests/data/sentences.yml", 'r') as stream:
    TEST_DATA = yaml.safe_load(stream)

class TestBenchmarksPackage(unittest.TestCase):

    def test_preprocessing(self):
        self.assertIsNotNone(word_tokenisation.preprocessing(
            sample="ทดสอบ การ ทำ ความสะอาด ข้อมูล<tag>ok</tag>"
        ))

    def test_benchmark(self):
        self.assertIsNotNone(word_tokenisation.benchmark(
            ["วัน", "จัน", "ทร์", "สี", "เหลือง"],
            ["วัน", "จันทร์", "สี", "เหลือง"]
        ))

    def test_binary_representation(self):
        sentence = "อากาศ|ร้อน|มาก|ครับ"
        rept, _ = word_tokenisation._binary_representation(sentence)

        self.assertEqual(
            [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
            rept.tolist()
        )

    def test_compute_stats(self):
        for pair in TEST_DATA['sentences']:
            exp, act = pair['expected'], pair['actual']

            result = word_tokenisation._compute_stats(
                word_tokenisation.preprocessing(exp),
                word_tokenisation.preprocessing(act)
            ) 

            self.assertIsNotNone(result)

    def test_benchmark(self):
        expected = []
        actual = []
        for pair in TEST_DATA['sentences']:
            expected.append(pair['expected'])
            actual.append(pair['actual'])

        df = word_tokenisation.benchmark(expected, actual)

        print(df.describe())

        self.assertIsNotNone(df)

    def test_count_correctly_tokenised_words(self):
        for d in TEST_DATA['binary_sentences']:
            sample = np.array(list(d['actual'])).astype(int)
            ref_sample = np.array(list(d['expected'])).astype(int)

            wb = list(word_tokenisation._find_word_boudaries(ref_sample))

            self.assertEqual(
                word_tokenisation._count_correctly_tokenised_words(sample, wb),
                d['expected_count']
            )

    def test_words_correctly_tokenised(self):
        r = [(0, 2), (2, 10), (10, 12) ]
        s = [(0, 10), (10, 12)]

        expected = "01"

        labels = word_tokenisation._find_words_correctly_tokenised(r, s)
        self.assertEqual(expected, "".join(np.array(labels).astype(str)))