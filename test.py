# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
import unittest
from collections import Counter
from pythainlp.corpus import alphabet
from pythainlp.segment import segment
from pythainlp.rank import rank
from pythainlp.change import *
from pythainlp.number import numtowords
from pythainlp.postaggers import tag
from pythainlp.romanization import romanization
class TestUM(unittest.TestCase):
	def testSegment(self):
		self.assertEqual(segment('ฉันรักภาษาไทยเพราะฉันเป็นคนไทย'),['ฉัน', 'รัก', 'ภาษา', 'ไทย', 'เพราะ', 'ฉัน', 'เป็น', 'คน', 'ไทย'])
	def testRank(self):
		self.assertEqual(rank(["แมว","คน","แมว"]),Counter({'แมว': 2, 'คน': 1}))
	def testChange(self):
		self.assertEqual(texttothai("l;ylfu8iy["),'สวัสดีครับ')
	def testRomanization(self):
		self.assertEqual(romanization("แมว"),'mæw')
	def testNumber(self):
		self.assertEqual(numtowords(5611116.50),'ห้าล้านหกแสนหนึ่งหมื่นหนึ่งพันหนึ่งร้อยสิบหกบาทห้าสิบสตางค์')
	def testTag(self):
		self.assertEqual(tag("คุณกำลังประชุม"),[('คุณ', 'PPRS'), ('กำลัง', 'XVBM'), ('ประชุม', 'VACT')])
	def testAlphabet(self):
		self.assertEqual(str(type(alphabet.get_data())),"<class 'list'>")
if __name__ == '__main__':
    unittest.main()