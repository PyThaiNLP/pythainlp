# -*- coding: utf-8 -*-
import unittest
import pythainlp
from pythainlp.rank import rank
from pythainlp.romanization import romanization
from pythainlp.change import *
from pythainlp.number import numtowords
from pythainlp.postaggers import tag
class TestUM(unittest.TestCase):
	def setUp(self):
		pass
	def segment_test(self):
		self.assertEqual(pythainlp.segment.segment('ฉันรักภาษาไทยเพราะฉันเป็นคนไทย'))
	def rank_test(self):
		self.assertEqual(pythainlp.rank.rank(["แมว","คน","แมว"]))
	def change_test(self):
		self.assertEqual(pythainlp.change.texttothai("l;ylfu8iy["))
	def number_test(self):
		self.assertEqual(pythainlp.number.numtowords(5611116.50))
	def tag_test(self):
		self.assertEqual(pythainlp.postaggers.tag("คุณกำลังประชุม"))
if __name__ == '__main__':
    unittest.main()