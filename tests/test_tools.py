# -*- coding: utf-8 -*-

import unittest

from pythainlp.tools import (
    get_full_data_path,
    get_pythainlp_data_path,
    get_pythainlp_path,
)


class TestToolsPackage(unittest.TestCase):
    def test_path(self):
        data_filename = "ttc_freq.txt"
        self.assertTrue(
            get_full_data_path(data_filename).endswith(data_filename)
        )
        self.assertIsInstance(get_pythainlp_data_path(), str)
        self.assertIsInstance(get_pythainlp_path(), str)
