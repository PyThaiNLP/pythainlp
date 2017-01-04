# -*- coding: utf-8 -*-
import unittest
import optparse
from collections import Counter
from pythainlp.segment import segment
from pythainlp.rank import rank
from pythainlp.change import *
from pythainlp.number import numtowords
from pythainlp.postaggers import tag
class TestUM(unittest.TestCase):
	def testSegment(self):
		self.assertEqual(segment('ฉันรักภาษาไทยเพราะฉันเป็นคนไทย'),['ฉัน', 'รัก', 'ภาษา', 'ไทย', 'เพราะ', 'ฉัน', 'เป็น', 'คน', 'ไทย'])
	def testChange(self):
		self.assertEqual(texttothai("l;ylfu8iy["),'สวัสดีครับ')
	def testNumber(self):
		self.assertEqual(numtowords(5611116.50),'ห้าล้านหกแสนหนึ่งหมื่นหนึ่งพันหนึ่งร้อยสิบหกบาทห้าสิบสตางค์')
	def testTag(self):
		self.assertEqual(tag("คุณกำลังประชุม"),[('คุณ', 'PPRS'), ('กำลัง', 'XVBM'), ('ประชุม', 'VACT')])
if __name__ == '__main__':
    unittest.main()