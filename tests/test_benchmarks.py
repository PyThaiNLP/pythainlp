import datetime
import os
import sys
import unittest

from pythainlp.benchmarks import *


class TestBenchmarksPackage(unittest.TestCase):

    def test_preprocessing(self):
        self.assertIsNotNone(preprocessing(
            sample="ทดสอบ การ ทำ ความสะอาด ข้อมูล<tag>ok</tag>"))

    def test_benchmark(self):
        self.assertIsNotNone(benchmark(["วัน", "จัน", "ทร์", "สี", "เหลือง"], [
                             "วัน", "จันทร์", "สี", "เหลือง"]))
