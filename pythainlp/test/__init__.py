# -*- coding: utf-8 -*-
from __future__ import absolute_import,unicode_literals
import unittest,six,sys
from collections import Counter
from pythainlp.corpus import alphabet
from pythainlp.corpus import wordnet
from pythainlp.tokenize import word_tokenize
from pythainlp.rank import rank
from pythainlp.change import *
from pythainlp.number import numtowords
from pythainlp.tag import pos_tag
from pythainlp.romanization import romanization
from pythainlp.date import now
from pythainlp.tokenize import tcc,etcc
from pythainlp.soundex import LK82
from pythainlp.corpus import stopwords
from pythainlp.MetaSound import *
from collections import namedtuple
Synset = namedtuple('Synset', 'synset li')
class TestUM(unittest.TestCase):
	def testSegment(self):
		self.assertEqual(word_tokenize('ฉันรักภาษาไทยเพราะฉันเป็นคนไทย'),[u'ฉัน', u'รัก', u'ภาษา', u'ไทย', u'เพราะ', u'ฉัน', u'เป็น', u'คน', u'ไทย'])
	def testSegmentDict(self):
		self.assertEqual(word_tokenize('ฉันรักภาษาไทยเพราะฉันเป็นคนไทย',engine='dict'),[u'ฉัน', u'รัก', u'ภาษาไทย', u'เพราะ', u'ฉัน', u'เป็น', u'คนไทย'])
	def testSegmentMM(self):
		self.assertEqual(word_tokenize('ฉันรักภาษาไทยเพราะฉันเป็นคนไทย',engine='mm'),[u'ฉัน', u'รัก', u'ภาษาไทย', u'เพราะ', u'ฉัน', u'เป็น', u'คนไทย'])
	def testRank(self):
		self.assertEqual(rank(["แมว","คน","แมว"]),Counter({'แมว': 2, 'คน': 1}))
	def testChange(self):
		self.assertEqual(texttothai("l;ylfu8iy["),'สวัสดีครับ')
		self.assertEqual(texttoeng('สวัสดีครับ'),"l;ylfu8iy[")
	def testRomanization1(self):
		self.assertEqual(romanization("แมว"),'mæw')
	def testRomanization2(self):
		self.assertEqual(romanization("แมว",engine="royin"),'maeo')
	def testNumber(self):
		self.assertEqual(numtowords(5611116.50),'ห้าล้านหกแสนหนึ่งหมื่นหนึ่งพันหนึ่งร้อยสิบหกบาทห้าสิบสตางค์')
	def testTCC(self):
		self.assertEqual(tcc.tcc('ประเทศไทย'),'ป/ระ/เท/ศ/ไท/ย')
	def testETCC(self):
		self.assertEqual(etcc.etcc('คืนความสุข'),'/คืน/ความสุข')
	def testLK82(self):
		self.assertEqual(LK82('รถ'),'ร3000')
	def testMS(self):
		self.assertEqual(MetaSound('คน'),'15')
	def testWORDNET(self):
		self.assertEqual(wordnet.synset('spy.n.01').lemma_names('tha'),['สปาย', 'สายลับ'])
		self.assertEqual(wordnet.langs()!=None,True)
	def testSTOPWORD(self):
		self.assertEqual(stopwords.words('thai')!=None,True)
	def testTag(self):
		self.assertEqual(pos_tag(word_tokenize("คุณกำลังประชุม"),engine='old'),[('คุณ', 'PPRS'), ('กำลัง', 'XVBM'), ('ประชุม', 'VACT')])
	def testTagnew(self):
    		if sys.version_info > (3,3):
    				self.assertEqual(pos_tag(word_tokenize("ผมรักคุณ"),engine='artagger'),[('ผม', 'PPRS'), ('รัก', 'VSTA'), ('คุณ', 'PPRS')])
if __name__ == '__main__':
    unittest.main()