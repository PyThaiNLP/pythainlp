# -*- coding: utf-8 -*-
import unittest
from pythainlp.segment import segment
from pythainlp.rank import rank
from pythainlp.change import *
from pythainlp.number import numtowords
from pythainlp.postaggers import tag
class TestUM(unittest.TestCase):
	def segment_test(self):
		assert segment('ฉันรักภาษาไทยเพราะฉันเป็นคนไทย') == ['ฉัน', 'รัก', 'ภาษา', 'ไทย', 'เพราะ', 'ฉัน', 'เป็น', 'คน', 'ไทย']
	def rank_test(self):
		assert rank(["แมว","คน","แมว"]) == Counter({'แมว': 2, 'คน': 1})
	def change_test(self):
		assert texttothai("l;ylfu8iy[") == 'สวัสดีครับ'
	def number_test(self):
		assert numtowords(5611116.50) == 'ห้าล้านหกแสนหนึ่งหมื่นหนึ่งพันหนึ่งร้อยสิบหกบาทห้าสิบสตางค์'
	def tag_test(self):
		assert tag("คุณกำลังประชุม") == [('คุณ', 'PPRS'), ('กำลัง', 'XVBM'), ('ประชุม', 'VACT')]
def main():
	fooSuite = unittest.TestLoader().loadTestsFromTestCase(TestUM)
if __name__ == '__main__':
    main()