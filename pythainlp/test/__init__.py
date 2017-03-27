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
import pythainlp.Text
from collections import namedtuple
import six
Synset = namedtuple('Synset', 'synset li')
class TestUM(unittest.TestCase):
	def testSegment(self):
		self.assertEqual(segment('ฉันรักภาษาไทย'),[u'ฉัน', u'รัก', u'ภาษา', u'ไทย'])
	def testSegmentDict(self):
		self.assertEqual(segmentdict('ฉันรักภาษาไทยเพราะฉันเป็นคนไทย'),[u'ฉัน', u'รัก', u'ภาษาไทย', u'เพราะ', u'ฉัน', u'เป็น', u'คนไทย'])
	def testRank(self):
		self.assertEqual(rank([u"แมว",u"คน",u"แมว"]),Counter({u'แมว': 2, u'คน': 1}))
	def testChange(self):
		self.assertEqual(texttothai("l;ylfu8iy["),u'สวัสดีครับ')
	def testRomanization(self):
		self.assertEqual(romanization("แมว"),'mæw'.encode('utf-16'))
	def testNumber(self):
		self.assertEqual(numtowords(5611116.50),u'ห้าล้านหกแสนหนึ่งหมื่นหนึ่งพันหนึ่งร้อยสิบหกบาทห้าสิบสตางค์')
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
	def testText(self):
		self.assertEqual(str(type(pythainlp.Text("ผลักดันกลับ"))),"<class 'nltk.text.Text'>")
if __name__ == '__main__':
    unittest.main()