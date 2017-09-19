# -*- coding: utf-8 -*-
from __future__ import absolute_import,unicode_literals
import unittest,six,sys
from collections import Counter
from pythainlp.corpus import alphabet,wordnet,country,tone,provinces,stopwords,newthaiword,thaiword
from pythainlp.keywords import *
from pythainlp.tokenize import word_tokenize,tcc,etcc
from pythainlp.rank import rank
from pythainlp.change import texttothai,texttoeng
from pythainlp.number import numtowords
from pythainlp.tag import pos_tag
from pythainlp.romanization import romanization
from pythainlp.date import now,reign_year_to_ad
from pythainlp.soundex import LK82,Udom83
from pythainlp.MetaSound import MetaSound
from pythainlp.spell import spell
from collections import namedtuple
from pythainlp.collation import collation
from pythainlp.util import normalize
from pythainlp.summarize import summarize_text
class TestUM(unittest.TestCase):
	"""
	ระบบทดสอบการทำงานของโค้ดของ PyThaiNLP 1.5
	"""
	def test_segment(self):
		self.assertEqual(word_tokenize('ฉันรักภาษาไทยเพราะฉันเป็นคนไทย'),[u'ฉัน', u'รัก', u'ภาษา', u'ไทย', u'เพราะ', u'ฉัน', u'เป็น', u'คน', u'ไทย'])
	def test_segment_dict(self):
		self.assertEqual(word_tokenize('ฉันรักภาษาไทยเพราะฉันเป็นคนไทย',engine='dict'),[u'ฉัน', u'รัก', u'ภาษาไทย', u'เพราะ', u'ฉัน', u'เป็น', u'คนไทย'])
	def test_segment_mm(self):
		self.assertEqual(word_tokenize('ฉันรักภาษาไทยเพราะฉันเป็นคนไทย',engine='mm'),[u'ฉัน', u'รัก', u'ภาษาไทย', u'เพราะ', u'ฉัน', u'เป็น', u'คนไทย'])
	def test_segment_newmm(self):
		self.assertEqual(word_tokenize('ฉันรักภาษาไทยเพราะฉันเป็นคนไทย',engine='newmm'),[u'ฉัน', u'รัก', u'ภาษาไทย', u'เพราะ', u'ฉัน', u'เป็น', u'คนไทย'])
	def test_segment_longest_matching(self):
		self.assertEqual(word_tokenize('ฉันรักภาษาไทยเพราะฉันเป็นคนไทย',engine='longest-matching'),[u'ฉัน', u'รัก', u'ภาษาไทย', u'เพราะ', u'ฉัน', u'เป็น', u'คนไทย'])
	def test_rank(self):
		self.assertEqual(rank(["แมว","คน","แมว"]),Counter({'แมว': 2, 'คน': 1}))
	def test_change(self):
		self.assertEqual(texttothai("l;ylfu8iy["),'สวัสดีครับ')
		self.assertEqual(texttoeng('สวัสดีครับ'),"l;ylfu8iy[")
	def test_romanization1(self):
		self.assertEqual(romanization("แมว"),'mæw')
	def test_romanization2(self):
		self.assertEqual(romanization("แมว",engine="royin"),'maeo')
		self.assertEqual(romanization("เดือน",engine="royin"),'duean')
		self.assertEqual(romanization("ดู",engine="royin"),'du')
		self.assertEqual(romanization("ดำ",engine="royin"),'dam')
		self.assertEqual(romanization("บัว",engine="royin"),'bua')
	def test_number(self):
		self.assertEqual(numtowords(5611116.50),'ห้าล้านหกแสนหนึ่งหมื่นหนึ่งพันหนึ่งร้อยสิบหกบาทห้าสิบสตางค์')
	def test_tcc(self):
		self.assertEqual(tcc.tcc('ประเทศไทย'),'ป/ระ/เท/ศ/ไท/ย')
	def test_etcc(self):
		self.assertEqual(etcc.etcc('คืนความสุข'),'/คืน/ความสุข')
	def test_lk82(self):
		self.assertEqual(LK82('รถ'),'ร3000')
		self.assertEqual(Udom83('รถ'),'ร800000')
	def test_ms(self):
		self.assertEqual(MetaSound('คน'),'15')
	def test_wordnet(self):
		self.assertEqual(wordnet.synset('spy.n.01').lemma_names('tha'),['สปาย', 'สายลับ'])
		self.assertEqual(wordnet.langs()!=None,True)
	def test_stopword(self):
		self.assertEqual(stopwords.words('thai')!=None,True)
	def test_spell(self):
		self.assertEqual(spell('เน้ร')!=None,True)
	def test_date(self):
		self.assertEqual(now()!=None,True)
		self.assertEqual(reign_year_to_ad(2,10),2017)
	def test_summarize(self):
		self.assertEqual(summarize_text(text="อาหาร หมายถึง ของแข็งหรือของเหลว ที่กินหรือดื่มเข้าสู่ร่างกายแล้ว จะทำให้เกิดพลังงานและความร้อนแก่ร่างกาย ทำให้ร่างกายเจริญเติบโต ซ่อมแซมส่วนที่สึกหรอ ควบคุมการเปลี่ยนแปลงต่างๆ ในร่างกาย ช่วยทำให้อวัยวะต่างๆ ทำงานได้อย่างปกติ อาหารจะต้องไม่มีพิษและไม่เกิดโทษต่อร่างกาย",n=1,engine='frequency'),[u'อาหารจะต้องไม่มีพิษและไม่เกิดโทษต่อร่างกาย'])
	def test_corpus(self):
		self.assertEqual(alphabet.get_data()!=None,True)
		self.assertEqual(country.get_data()!=None,True)
		self.assertEqual(tone.get_data()!=None,True)
		self.assertEqual(provinces.get_data()!=None,True)
		self.assertEqual(len(newthaiword.get_data())>len(thaiword.get_data()),True)
	def test_collation(self):
    		self.assertEqual(collation(['ไก่','กก']),[u'กก', u'ไก่'])
	def test_normalize(self):
    		self.assertEqual(normalize("เเปลก"),"แปลก")
	def test_keywords(self):
    		self.assertEqual(find_keyword(word_tokenize("แมวกินปลาอร่อยรู้ไหมว่าแมวเป็นแมวรู้ไหมนะแมว",engine='newmm')),{u'แมว': 4})
	def test_tag(self):
		self.assertEqual(pos_tag(word_tokenize("คุณกำลังประชุม"),engine='old'),[('คุณ', 'PPRS'), ('กำลัง', 'XVBM'), ('ประชุม', 'VACT')])
		if sys.version_info >= (3,4):
			self.assertEqual(str(type(pos_tag(word_tokenize("ผมรักคุณ"),engine='artagger'))),"<class 'list'>")
if __name__ == '__main__':
    unittest.main()
