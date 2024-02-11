# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0

import unittest
from pythainlp.parse import dependency_parsing


class TestParsePackage(unittest.TestCase):
    def test_dependency_parsing(self):
        self.assertIsNotNone(dependency_parsing("ผมเป็นคนดี", engine="esupar"))
        self.assertIsNotNone(
            dependency_parsing("ผมเป็นคนดี", engine="esupar", tag="list")
        )
        # self.assertIsNotNone(dependency_parsing("ผมเป็นคนดี", engine="transformers_ud"))
        # self.assertIsNotNone(dependency_parsing("ผมเป็นคนดี", engine="transformers_ud", tag="list"))
        # self.assertIsNotNone(dependency_parsing("ผมเป็นคนดี", engine="spacy_thai"))
        # self.assertIsNotNone(dependency_parsing("ผมเป็นคนดี", engine="spacy_thai", tag="list"))
        # self.assertIsNotNone(dependency_parsing("ผมเป็นคนดี", engine="ud_goeswith"))
        # self.assertIsNotNone(dependency_parsing("ผมเป็นคนดี", engine="ud_goeswith", tag="list"))
