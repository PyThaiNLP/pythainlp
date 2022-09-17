# -*- coding: utf-8 -*-

import unittest
from pythainlp.parse import dependency_parsing


class TestParsePackage(unittest.TestCase):
    def test_dependency_parsing(self):
        self.assertIsNotNone(dependency_parsing("ผมเป็นคนดี", engine="esupar"))
        self.assertIsNotNone(dependency_parsing("ผมเป็นคนดี", engine="transformers_ud"))
        self.assertIsNotNone(dependency_parsing("ผมเป็นคนดี", engine="spacy_thai"))
