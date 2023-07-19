# -*- coding: utf-8 -*-
import unittest
from pythainlp.el import EntityLinker


class TestElPackage(unittest.TestCase):
    def test_EntityLinker(self):
        with self.assertRaises(NotImplementedError):
            EntityLinker(model_name="cat")
        with self.assertRaises(NotImplementedError):
            EntityLinker(tag="cat")
