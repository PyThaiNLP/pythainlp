# -*- coding: utf-8 -*-
from __future__ import absolute_import
import unittest
from collections import Counter
from pythainlp.corpus import alphabet
from pythainlp.corpus import wordnet
from pythainlp.segment import segment
from pythainlp.segment.dict import segment as segmentdict
from pythainlp.rank import rank
from pythainlp.change import *
from pythainlp.number import numtowords
from pythainlp.postaggers import tag
from pythainlp.romanization import romanization
from pythainlp.date import now
from pythainlp.sentiment import sentiment
from collections import namedtuple
Synset = namedtuple('Synset', 'synset li')
class TestUM(unittest.TestCase):
	def testSegment(self):
		self.assertEqual(segment('ฉันรักภาษาไทยเพราะฉันเป็นคนไทย'),['ฉัน', 'รัก', 'ภาษา', 'ไทย', 'เพราะ', 'ฉัน', 'เป็น', 'คน', 'ไทย'])
	def testSegmentDict(self):
		self.assertEqual(segmentdict('ฉันรักภาษาไทยเพราะฉันเป็นคนไทย'),['ฉัน', 'รัก', 'ภาษาไทย', 'เพราะ', 'ฉัน', 'เป็น', 'คนไทย'])
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
	def testNow(self):
		self.assertEqual(type(now()),type('7 มกราคม 2560 20:23:01'))
	def testSentiment(self):
		self.assertEqual('pos',sentiment('สวัสดีครับ'))
	def testWordNet(self):
		self.assertEqual(wordnet.getSynset("ผลักดันกลับ"),Synset(synset='02503365-v', li='ผลักดันกลับ'))
if __name__ == '__main__':
    unittest.main()