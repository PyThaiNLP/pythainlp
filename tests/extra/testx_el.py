# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

import unittest

from pythainlp.el import EntityLinker


class ElTestCaseX(unittest.TestCase):
    def test_EntityLinker(self):
        with self.assertRaises(NotImplementedError):
            EntityLinker(model_name="cat")
        with self.assertRaises(NotImplementedError):
            EntityLinker(tag="cat")
