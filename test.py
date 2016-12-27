# -*- coding: utf-8 -*-
import unittest
import optparse
from pythainlp.segment import segment
from pythainlp.rank import rank
from pythainlp.change import *
from pythainlp.number import numtowords
from pythainlp.postaggers import tag
class TestUM(unittest.TestCase):
	def segment_test(self):
		self.assertTrue(segment('ฉันรักภาษาไทยเพราะฉันเป็นคนไทย') == ['ฉัน', 'รัก', 'ภาษา', 'ไทย', 'เพราะ', 'ฉัน', 'เป็น', 'คน', 'ไทย'])
	def rank_test(self):
		self.assertTrue(rank(["แมว","คน","แมว"]) == Counter({'แมว': 2, 'คน': 1}))
	def change_test(self):
		self.assertTrue(texttothai("l;ylfu8iy[") == 'สวัสดีครับ')
	def number_test(self):
		self.assertTrue(numtowords(5611116.50) == 'ห้าล้านหกแสนหนึ่งหมื่นหนึ่งพันหนึ่งร้อยสิบหกบาทห้าสิบสตางค์')
	def tag_test(self):
		self.assertTrue(tag("คุณกำลังประชุม") == [('คุณ', 'PPRS'), ('กำลัง', 'XVBM'), ('ประชุม', 'VACT')])
if __name__ == '__main__':
    (options, args) = parser.parse_args()
    if options.run_tests:
        unittest.main(argv=sys.argv[:1], verbosity=not options.quiet and 2 or 0)
