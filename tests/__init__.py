# -*- coding: utf-8 -*-
import unittest
from pythainlp.segment import segment
from pythainlp.rank import rank
from pythainlp.change import *
from pythainlp.number import numtowords
from pythainlp.postaggers import tag
class TestUM(unittest.TestCase):
	def segment_test(self):
		self.assertEqual(segment('ฉันรักภาษาไทยเพราะฉันเป็นคนไทย'),['ฉัน', 'รัก', 'ภาษา', 'ไทย', 'เพราะ', 'ฉัน', 'เป็น', 'คน', 'ไทย'])
	def rank_test(self):
		self.assertEqual(rank(["แมว","คน","แมว"]),Counter({'แมว': 2, 'คน': 1}))
	def change_test(self):
		self.assertEqual(texttothai("l;ylfu8iy["),'สวัสดีครับ')
	def number_test(self):
		self.assertEqual(numtowords(5611116.50),'ห้าล้านหกแสนหนึ่งหมื่นหนึ่งพันหนึ่งร้อยสิบหกบาทห้าสิบสตางค์')
	def tag_test(self):
		self.assertEqual(tag("คุณกำลังประชุม"),[('คุณ', 'PPRS'), ('กำลัง', 'XVBM'), ('ประชุม', 'VACT')])
def main():
    unittest.main()
if __name__ == '__main__':
    main()