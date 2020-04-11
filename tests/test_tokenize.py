# -*- coding: utf-8 -*-

import os
import unittest

from pythainlp.corpus import _CORPUS_PATH, thai_words
from pythainlp.corpus.common import _THAI_WORDS_FILENAME
from pythainlp.tokenize import DEFAULT_DICT_TRIE, Tokenizer, attacut
from pythainlp.tokenize import deepcut as tokenize_deepcut
from pythainlp.tokenize import (
    dict_trie,
    etcc,
    longest,
    multi_cut,
    newmm,
)
from pythainlp.tokenize import pyicu as tokenize_pyicu
from pythainlp.tokenize import (
    sent_tokenize,
    subword_tokenize,
    syllable_tokenize,
    tcc,
    word_tokenize,
)
from pythainlp.tokenize.ssg import segment as ssg_segment


class TestTokenizePackage(unittest.TestCase):

    def test_Tokenizer(self):
        t_test = Tokenizer(DEFAULT_DICT_TRIE)
        self.assertEqual(t_test.word_tokenize(""), [])
        t_test.set_tokenize_engine("longest")
        self.assertEqual(t_test.word_tokenize(None), [])

        t_test = Tokenizer()
        self.assertEqual(t_test.word_tokenize("ก"), ["ก"])

    def test_etcc(self):
        self.assertEqual(etcc.segment(None), [])
        self.assertEqual(etcc.segment(""), [])
        self.assertIsInstance(etcc.segment("คืนความสุข"), list)
        self.assertEqual(
            etcc.segment("หาเงินเพื่อเรียน"),
            ["หา", "เงิน", "เพื่", "อ", "เรีย", "น"]
        )
        self.assertEqual(
            etcc.segment("หนังสือ"),
            ["ห", "นัง", "สือ"]
        )
        self.assertIsNotNone(
            etcc.segment(
                "หมูแมวเหล่านี้ด้วยเหตุผลเชื่อมโยงทางกรรมพันธุ์"
                + "สัตว์มีแขนขาหน้าหัวเราะเพราะแข็งขืน"
            )
        )

    def test_word_tokenize(self):
        self.assertEqual(word_tokenize(""), [])
        self.assertEqual(
            word_tokenize("ฉันรักภาษาไทยเพราะฉันเป็นคนไทย"),
            ["ฉัน", "รัก", "ภาษาไทย", "เพราะ", "ฉัน", "เป็น", "คนไทย"],
        )

        self.assertIsNotNone(
            word_tokenize("หมอนทองตากลมหูว์MBK39", engine="newmm")
        )
        self.assertIsNotNone(
            word_tokenize("หมอนทองตากลมหูว์MBK39", engine="mm")
        )
        self.assertIsNotNone(
            word_tokenize("หมอนทองตากลมหูว์MBK39", engine="longest")
        )
        self.assertIsNotNone(
            word_tokenize("หมอนทองตากลมหูว์MBK39", engine="icu")
        )
        self.assertIsNotNone(
            word_tokenize("หมอนทองตากลมหูว์MBK39", engine="deepcut")
        )
        self.assertIsNotNone(
            word_tokenize("หมอนทองตากลมหูว์MBK39", engine="attacut")
        )
        self.assertRaises(
            ValueError,
            lambda: word_tokenize("หมอนทองตากลมหูว์MBK39", engine="XX")
        )  # XX engine does not exist.

        self.assertIsNotNone(dict_trie(()))
        self.assertIsNotNone(dict_trie(("ทดสอบ", "สร้าง", "Trie")))
        self.assertIsNotNone(dict_trie(["ทดสอบ", "สร้าง", "Trie"]))
        self.assertIsNotNone(dict_trie({"ทดสอบ", "สร้าง", "Trie"}))
        self.assertIsNotNone(dict_trie(thai_words()))
        self.assertIsNotNone(dict_trie(DEFAULT_DICT_TRIE))
        self.assertIsNotNone(
            dict_trie(os.path.join(_CORPUS_PATH, _THAI_WORDS_FILENAME))
        )

        self.assertTrue(
            "ไฟ" in word_tokenize("รถไฟฟ้า", custom_dict=dict_trie(["ไฟ"]))
        )

    def test_word_tokenize_deepcut(self):
        self.assertEqual(tokenize_deepcut.segment(None), [])
        self.assertEqual(tokenize_deepcut.segment(""), [])
        self.assertIsNotNone(
            tokenize_deepcut.segment("ทดสอบ", DEFAULT_DICT_TRIE)
        )
        self.assertIsNotNone(tokenize_deepcut.segment("ทดสอบ", ["ทด", "สอบ"]))
        self.assertIsNotNone(word_tokenize("ทดสอบ", engine="deepcut"))
        self.assertIsNotNone(
            word_tokenize(
                "ทดสอบ", engine="deepcut", custom_dict=DEFAULT_DICT_TRIE
            )
        )

    def test_word_tokenize_icu(self):
        self.assertEqual(tokenize_pyicu.segment(None), [])
        self.assertEqual(tokenize_pyicu.segment(""), [])
        self.assertEqual(
            word_tokenize("ฉันรักภาษาไทยเพราะฉันเป็นคนไทย", engine="icu"),
            ["ฉัน", "รัก", "ภาษา", "ไทย", "เพราะ", "ฉัน", "เป็น", "คน", "ไทย"],
        )

    def test_word_tokenize_longest(self):
        self.assertEqual(longest.segment(None), [])
        self.assertEqual(longest.segment(""), [])
        self.assertIsInstance(
            longest.segment("กรุงเทพฯมากๆเพราโพาง BKKฯ"), list
        )
        self.assertEqual(
            word_tokenize("ฉันรักภาษาไทยเพราะฉันเป็นคนไทย", engine="longest"),
            ["ฉัน", "รัก", "ภาษาไทย", "เพราะ", "ฉัน", "เป็น", "คนไทย"],
        )
        longest_tokenizer = Tokenizer(["ปวด", "เฉียบ", "พลัน", "เฉียบพลัน"])
        self.assertEqual(
            longest_tokenizer.word_tokenize("ปวดเฉียบพลัน"),
            ["ปวด", "เฉียบพลัน"],
        )
        self.assertEqual(
            longest_tokenizer.word_tokenize("เฉียบพลัน"),
            ["เฉียบพลัน"],
        )

    def test_word_tokenize_mm(self):
        self.assertEqual(multi_cut.segment(None), [])
        self.assertEqual(multi_cut.segment(""), [])
        self.assertEqual(word_tokenize("", engine="mm"), [])
        self.assertEqual(
            word_tokenize("ฉันรักภาษาไทยเพราะฉันเป็นคนไทย", engine="mm"),
            ["ฉัน", "รัก", "ภาษาไทย", "เพราะ", "ฉัน", "เป็น", "คนไทย"],
        )

        self.assertIsNotNone(multi_cut.mmcut("ทดสอบ"))

        self.assertIsNotNone(
            multi_cut.find_all_segment("รถไฟฟ้ากรุงเทพมหานครBTS")
        )
        self.assertEqual(multi_cut.find_all_segment(None), [])

    def test_word_tokenize_newmm(self):
        self.assertEqual(newmm.segment(None), [])
        self.assertEqual(newmm.segment(""), [])
        self.assertEqual(
            word_tokenize("ฉันรักภาษาไทยเพราะฉันเป็นคนไทย", engine="newmm"),
            ["ฉัน", "รัก", "ภาษาไทย", "เพราะ", "ฉัน", "เป็น", "คนไทย"],
        )
        self.assertEqual(
            word_tokenize(
                "สวัสดีครับ สบายดีไหมครับ",
                engine="newmm",
                keep_whitespace=True,
            ),
            ["สวัสดี", "ครับ", " ", "สบายดี", "ไหม", "ครับ"],
        )
        self.assertEqual(
            word_tokenize("จุ๋มง่วงนอนยัง", engine="newmm"),
            ["จุ๋ม", "ง่วงนอน", "ยัง"],
        )
        self.assertEqual(
            word_tokenize("จุ๋มง่วง", engine="newmm"), ["จุ๋ม", "ง่วง"]
        )
        self.assertEqual(
            word_tokenize(
                "จุ๋ม   ง่วง", engine="newmm", keep_whitespace=False
            ),
            ["จุ๋ม", "ง่วง"],
        )

        long_text = """
    ไต้หวัน (แป่ะเอ๋ยี้: Tâi-oân; ไต่อวัน) หรือ ไถวาน (อักษรโรมัน: Taiwan; จีนตัวย่อ: 台湾; จีนตัวเต็ม: 臺灣/台灣; พินอิน: Táiwān; ไถวาน) หรือชื่อทางการว่า สาธารณรัฐจีน (อังกฤษ: Republic of China; จีนตัวย่อ: 中华民国; จีนตัวเต็ม: 中華民國; พินอิน: Zhōnghuá Mínguó) เป็นรัฐในทวีปเอเชียตะวันออก[7][8][9] ปัจจุบันประกอบด้วยเกาะใหญ่ 5 แห่ง คือ จินเหมิน (金門), ไต้หวัน, เผิงหู (澎湖), หมาจู่ (馬祖), และอูชิว (烏坵) กับทั้งเกาะเล็กเกาะน้อยอีกจำนวนหนึ่ง ท้องที่ดังกล่าวเรียกรวมกันว่า "พื้นที่ไต้หวัน" (臺灣地區)
    ไต้หวันด้านตะวันตกติดกับจีนแผ่นดินใหญ่ ด้านตะวันออกและตะวันออกเฉียงเหนือติดกับญี่ปุ่น และด้านใต้ติดกับฟิลิปปินส์ กรุงไทเปเป็นเมืองหลวง[10] ส่วนไทเปใหม่เป็นเขตปกครองที่จัดตั้งขึ้นใหม่ กินพื้นที่กรุงไทเป และเป็นเขตซึ่งประชากรหนาแน่นที่สุดในเวลานี้
    เกาะไต้หวันนั้นเดิมเป็นที่อยู่ของชนพื้นเมือง และมีชาวจีนจากแผ่นดินใหญ่เข้ามาอาศัยร่วมด้วย จนกระทั่งชาววิลันดาและสเปนเดินทางเข้ามาในยุคสำรวจเมื่อศตวรรษที่ 17 และมาตั้งบ้านเรือนกลายเป็นนิคมใหญ่โต ต่อมาในปี 1662 ราชวงศ์หมิงในแผ่นดินใหญ่ถูกราชวงศ์ชิงแทนที่ เจิ้ง เฉิงกง (鄭成功) ขุนศึกหมิง รวมกำลังหนีมาถึงเกาะไต้หวัน และเข้ารุกไล่ฝรั่งออกไปได้อย่างราบคาบ เขาจึงตั้งราชอาณาจักรตงหนิง (東寧) ขึ้นบนเกาะเพื่อ "โค่นชิงฟื้นหมิง" (反清復明) แต่ในปี 1683 ราชวงศ์ชิงปราบปรามอาณาจักรตงหนิงและเข้าครอบครองไต้หวันเป็นผลสำเร็จ ไต้หวันจึงกลายเป็นมณฑลหนึ่งของจีน อย่างไรก็ดี ความบาดหมางระหว่างจีนกับญี่ปุ่นเป็นเหตุให้ญี่ปุ่นได้ไต้หวันไปในปี 1895
    ก่อนเสียไต้หวันคืนให้แก่จีนหลังสงครามโลกครั้งที่สอง ช่วงนั้น มีการเปลี่ยนแปลงการปกครองในจีน พรรคก๊กมินตั๋ง (國民黨) ได้เป็นใหญ่ แต่ไม่นานก็เสียทีให้แก่พรรคคอมมิวนิสต์จีน (共产党) พรรคก๊กมินตั๋งจึงหนีมายังเกาะไต้หวันและสถาปนาสาธารณรัฐจีนขึ้นบนเกาะไต้หวันแยกต่างหาก ส่วนฝ่ายคอมมิวนิสต์จีนที่เป็นฝ่ายได้รับชัยชนะได้สถาปนาสาธารณรัฐประชาชนจีนบนแผ่นดินใหญ่ อย่างไรก็ดี จีนยังคงถือว่า ไต้หวันเป็นมณฑลหนึ่งของตน และไต้หวันเองก็ยังมิได้รับการยอมรับจากนานาชาติว่าเป็นประเทศเอกราชมาจนบัดนี้
    ในช่วงทศวรรษ 1980 ถึงต้นทศวรรษ 1990 การเมืองการปกครองสาธารณรัฐจีน (ไต้หวัน) ได้เจริญรุ่งเรืองจนเป็นประชาธิปไตยที่มีพรรคการเมืองหลายพรรคและมีการเลือกตั้งทั่วหน้า อนึ่ง ในช่วงกลางศตวรรษที่ 20 เศรษฐกิจไต้หวันงอกงามอย่างรวดเร็ว ไต้หวันจึงกลายเป็นประเทศพัฒนาแล้ว ทั้งได้ชื่อว่าเป็นหนึ่งในสี่เสือแห่งเอเชีย มีอุตสาหกรรมล้ำหน้า และมีเศรษฐกิจใหญ่โตเป็นอันดับที่ 19 ของโลก[11][12] อุตสาหกรรมที่ใช้เทคโนโลยีชั้นสูงของไต้หวันยังมีบทบาทสำคัญมากในเศรษฐกิจโลก เป็นเหตุให้ไต้หวันได้เป็นสมาชิกองค์การการค้าโลกและความร่วมมือทางเศรษฐกิจเอเชีย-แปซิฟิก นอกจากนี้ เสรีภาพของสื่อมวลชน เสรีภาพทางเศรษฐกิจ การสาธารณสุข[13]การศึกษา และดัชนีการพัฒนามนุษย์ในไต้หวันยังได้รับการจัดอยู่ในอันดับสูงด้วย[14][4][15]
    สาธารณรัฐจีน มีลักษณะเป็นกลุ่มเกาะ ทำให้ภูมิประเทศติดกับทะเล ไม่ติดกับประเทศใดเลย ห่างจากเกาะไปทางทิศเหนือและทิศตะวันตกเป็นสาธารณรัฐประชาชนจีน ทิศใต้เป็นประเทศฟิลิปปินส์และทะเลจีนใต้ ส่วนทิศตะวันออกเป็นมหาสมุทรแปซิฟิก
    ในปี ค.ศ. 1638 หลังการพ่ายแพ้ของหลานชายของเจิ้ง เฉิงกง จากการบุกโจมตีทางทัพเรือของราชวงศ์ชิงแมนจูที่นำทัพโดยชื่อ หลางจากทางตอนใต้ของมณฑลฝูเจี้ยน ทำให้ราชวงศ์ชิงผนวกยึดเกาะไต้หวันมาเป็นส่วนหนึ่งได้สำเร็จ และวางไว้ภายใต้เขตอำนาจของมณฑลฝูเจี้ยน ราชสำนักของราชวงศ์ชิงพยายามลดการละเมิดลิขสิทธิ์และความไม่ลงรอยกันในพื้นที่โดยออกกฎหมายเพื่อจัดการตรวจคนเข้าเมืองและเคารพสิทธิในที่ดินของชนพื้นเมืองไต้หวัน ผู้อพยพจากฝูเจี้ยนทางใต้ส่วนใหญ่ยังคงเดินทางไปไต้หวัน เขตแดนระหว่างดินแดนที่เสียภาษีและสิ่งที่ถูกพิจารณาว่าเป็นดินแดน "เขตอันตราย" เปลี่ยนไปทางทิศตะวันออกโดยชาวพื้นเมืองบางคนเข้ารีตรับวัฒนธรรมแบบจีน ในขณะที่คนอื่น ๆ ถอยกลับเข้าไปในภูเขา ในช่วงเวลานี้มีความขัดแย้งจำนวนมากระหว่างกลุ่มชาวจีนฮั่นด้วยกันเองจากภูมิภาคต่าง ๆ ของฝูเจี้ยนทางใต้โดยเฉพาะอย่างยิ่งระหว่างเฉวียนโจวกับฉางโจว และระหว่างฝูเจี้ยนตอนใต้และชาวพื้นเมืองไต้หวัน
    พ.ศ. 2454 (ค.ศ. 1911) การจลาจลอู่ฮั่นในประเทศจีน เป็นจุดเริ่มต้นการล่มสลายของราชวงศ์ชิง เมื่อพรรคคอมมิวนิสต์จีนเข้ามามีอำนาจในจีนแผ่นดินใหญ่เมื่อ พ.ศ. 2492 (ค.ศ. 1949) พรรคก๊กมินตั๋ง พรรคการเมืองเมืองชาตินิยมของจีนที่เป็นฝ่ายแพ้ก็พาผู้คนอพยพหนีออกจากแผ่นดินใหญ่มาตั้งหลักที่ไต้หวัน เพื่อวางแผนกลับไปครองอำนาจในจีนต่อไป
    ชาวจีนมากกว่า 1 ล้าน 5 แสนคน อพยพตามมาอยู่ที่เกาะไต้หวันในยุคที่ เหมา เจ๋อตง มีอำนาจเต็มที่ในจีนแผ่นดินใหญ่ ผู้นำของประเทศทั้งสองจีน คือผู้นำพรรคคอมมิวนิสต์กับผู้นำสาธารณรัฐจีนบนเกาะไต้หวัน แย่งกันเป็นกระบอกเสียงของประชาชนจีนในเวทีโลก แต่เสียงของนานาประเทศส่วนใหญ่เกรงอิทธิพลของจีนแผ่นดินใหญ่ จึงให้การยอมรับจีนแผ่นดินใหญ่มากกว่า
    ในปี พ.ศ. 2514 (ค.ศ. 1971) ก่อนที่นายพล เจียง ไคเช็ก (General Chiang Kaishek) (ภาษาจีน:蔣中正) จะถึงอสัญกรรมไม่กี่ปี สาธารณรัฐจีนซึ่งเป็นประเทศที่ร่วมก่อตั้งองค์การสหประชาชาติได้สูญเสียสมาชิกภาพในฐานะตัวแทนชาวจีนให้กับสาธารณรัฐประชาชนจีน ในปี พ.ศ. 2521 (ค.ศ. 1978) สหประชาชาติก็ประกาศรับรองจีนเดียวคือจีนแผ่นดินใหญ่และตัดสัมพันธ์ทางการเมืองกับสาธารณรัฐจีน ทั้งสหรัฐอเมริกาก็ได้ถอนการรับรองว่าสาธารณรัฐจีนมีฐานะเป็นรัฐ ไต้หวันจึงกลายเป็นเพียงดินแดนที่จีนอ้างว่าเป็นส่วนหนึ่งของประเทศสาธารณรัฐประชาชนจีนตั้งแต่นั้นเป็นต้นมา
    เมื่อเจียง ไคเช็ก ถึงแก่อสัญกรรมในปี พ.ศ. 2518 (ค.ศ. 1975) ลูกชายที่ชื่อ เจี่ยง จิงกั๋ว (Chiang Chingkuo) ได้เป็นผู้สืบทอดการปกครองไต้หวันต่อและเริ่มกระบวนการ วางรากฐานไปสู่ประชาธิปไตย
    หลังจากที่ประธานาธิบดี เจียง จิงกั๋ว เสียชีวิต ไต้หวันจึงได้เข้าสู่ระบอบประชาธิปไตยเต็มรูปแบบ ประธานาธิบดีคนใหม่ ซึ่งเกิดในไต้หวัน ชื่อ หลี่ เติงฮุย (Lee Tenghui) ขึ้นบริหารประเทศ โดยการสนับสนุนของเจี่ยง จิงกั๋ว (Chiang Chingkuo) ทั้งที่ หลี่ เติงฮุย (Lee Tenghui) นั้นเคลื่อนไหวสนับสนุนเอกราชไต้หวัน นาย รัฐบาลจีนที่ปักกิ่งได้ตั้งฉายาประธานาธิบดีไต้หวันคนใหม่ว่า "จิ้งจกปากหวาน" (A sweet-Talking Chameleon) ช่วงเวลาที่นายหลี่ เติงฮุย เป็นประธานาธิบดี การเมืองของไต้หวันเกิดการแตกแยกออกเป็น 3 ฝ่ายคือ 1) พวกก๊กมินตั๋ง ที่ต้องการกลับไปรวมประเทศกับจีนแผ่นดินใหญ่ (รวมจีนแผ่นดินใหญ่ภายใต้การปกครองของสาธารณรัฐจีน) 2) พวกที่ต้องการให้ไต้หวันเป็นประเทศอิสระไม่เกี่ยวข้องกับจีนแผ่นดินใหญ่ และ 3) พวกที่ต้องการดำรงฐานะของประเทศไว้ดังเดิมต่อไป
    ไต้หวันกับจีนแผ่นดินใหญ่นัดเจรจาหาทางออกของข้อขัดแย้งทางการเมืองครั้งแรกที่สิงคโปร์เมื่อปี พ.ศ. 2536 (ค.ศ. 1993) แต่ปรากฏว่าจีนแผ่นดินใหญ่ประวิงเวลาการลงนามในสัญญาหลายฉบับที่เป็นข้อตกลงร่วมกัน ทำให้ผลของการเจรจาคราวนั้นไม่ก้าวหน้าไปถึงไหน ความสัมพันธ์ระหว่างสองจีนเลวร้ายลงทุกที เมื่อประธานาธิบดี หลี่ เติงฮุย เดินทางไปเยือนสหรัฐอเมริกาและได้รับการยอมรับอย่างเอิกเกริก ทำให้จีนแผ่นดินใหญ่ไม่พอใจเป็นอย่างมาก จึงกระทำการข่มขวัญไต้หวันกับประเทศที่ให้การสนับสนุนไต้หวัน ด้วยการทำการซ้อมรบขึ้นใกล้ ๆ เกาะไต้หวัน สหรัฐอเมริกาออกมาแสดงอาการปกป้องคุ้มครองไต้หวันด้วยการส่งกำลังกองเรือรบของสหรัฐฯ มาป้วนเปี้ยนอยู่ในน่านน้ำที่จีนซ้อมรบ
    ขณะที่โลกกำลังล่อแหลมกับสถานการณ์ที่ตึงเครียดในน่านน้ำจีนมากขึ้นทุกทีนั้น ไต้หวันก็จัดให้มีการเลือกตั้งครั้งใหม่ และในการเลือกตั้งครั้งใหม่นั้นเอง ไต้หวันก็ได้นายหลี่ เติงฮุย เป็นประธานาธิบดีอีกครั้ง
    ไต้หวันเข้าสู่สภาวะวิกฤต เมื่อเกิดแผ่นดินไหวครั้งร้ายแรงที่สุดในประวัติศาสตร์ในเดือนกันยายน พ.ศ. 2542 (ค.ศ. 1999) ทำให้ประชากรส่วนมากที่เป็นชาวพื้นเมืองเสียชีวิตไป 2,000 คน ทั้งเมืองมีแต่เศษซากสิ่งปรักหักพังที่เกิดจากภัยธรรมชาติ และช่วงนี้ไต้หวันต้องเผชิญความยากลำบากจากภัยธรรมชาติร้ายแรง จีนแผ่นดินใหญ่ก็เพิ่มความกดดันไม่ให้นานาชาติเข้ามายุ่งเกี่ยวกับไต้หวันแม้ในยามคับขันเช่นนี้ โดยออกมาประกาศว่า หากมีประเทศใดจะเข้าไปให้ความช่วยเหลือไต้หวัน จะต้องได้รับอนุญาตจากจีนก่อน ซึ่งคำประกาศของจีนแผ่นดินใหญ่สวนทางกับเมตตาธรรมของประเทศทั่วโลกที่ต้องการให้ความช่วยเหลือไต้หวัน
    เดือนมีนาคม พ.ศ. 2543 (ค.ศ. 2000) มีการเลือกตั้งใหม่ในไต้หวัน ชาวไต้หวันเลือกผู้แทนจากพรรคประชาธิปไตยก้าวหน้า คือ นายเฉิน สุยเปี่ยน (Chen Shui-bian) เป็นประธานาธิบดีคนใหม่ของไต้หวัน ผู้ประกาศนโยบายการเมืองแข็งกร้าวว่าไต้หวันต้องการแยกตัวเป็นอิสระจากจีนแผ่นดินใหญ่ ยุติยุคของพรรคชาตินิยมที่ยังฝักใฝ่แผ่นดินใหญ่อยู่ จีนแผ่นดินใหญ่จึงถือว่าเป็นกบฏต่อการปกครองของจีน เพราะแต่ไหนแต่ไรมา ไต้หวันไม่เคยประกาศอย่างเป็นทางการว่าไต้หวันเป็นประเทศอิสระแยกจากจีน และจีนพูดอยู่เสมอว่าไต้หวันเป็นเด็กในปกครองที่ค่อนข้างจะหัวดื้อและเกเร หากไต้หวันประกาศว่าเป็นอิสระจากจีนเมื่อใด จีนก็จะยกกำลังจัดการกับไต้หวันทันที
    ในขณะที่ความสัมพันธ์ทางการเมืองระหว่างสองจีนในสายตาชาวโลกเลวร้ายลง จีนทั้งสองกลับมีการติดต่อทางการค้ากันมากขึ้น มีการผ่อนปรนอนุญาตให้ชาวไต้หวันเดินทางไปจีนแผ่นดินใหญ่เพื่อเยี่ยมญาติได้ เกิดปรากฏการสำคัญคือนักธุรกิจไต้หวันหอบเงินทุนมากกว่า 20,000 ล้านดอลลาร์สหรัฐ ไปลงทุนดำเนินธุรกิจทางตอนใต้ของจีนแผ่นดินใหญ่ จนกระทั่งขณะนี้ชาวไต้หวันกลายเป็นนักลงทุนรายใหญ่เป็นลำดับ 2 ของจีน
    วันที่ 24 พฤษภาคม 2560 ศาลรัฐธรรมนูญวินิจฉัยว่ากฎหมายสมรสปัจจุบันในเวลานั้นละเมิดรัฐธรรมนูญโดยปฏิเสธสิทธิสมรสของคู่รักเพศเดียวกันชาวไต้หวัน ศาลวินิจฉัยว่าหากสภานิติบัญญัติไม่ผ่านการแก้ไขกฎหมายที่เพียงพอต่อกฎหมายสมรสของไต้หวันภายในสองปี การสมรสเพศเดียวกันจะชอบด้วยกฎหมายโดยอัตโนมัติในไต้หวัน[17] วันที่ 17 พฤษภาคม 2562 สภานิติบัญญัติไต้หวันอนุมัติร่างกฎหมายทำให้การสมรสเพศเดียวกันชอบด้วยกฎหมาย ทำให้เป็นประเทศแรกในทวีปเอเชียที่ผ่านกฎหมายดังกล่าว[18][19]
    """
        self.assertIsInstance(word_tokenize(long_text, engine="newmm"), list)
        self.assertIsInstance(
            word_tokenize(long_text, engine="newmm-safe"), list
        )

        danger_text1 = """
    ชิชิชิชิชิชิชิชิชิชิชิชิชิชิชิชิชิชิชิชิชิชิชิชิชิชิชิชิชิชิชิชิชิชิชิชิชิชิชิชิชิชิชิชิชิชิชิชิชิชิชิชิชิชิชิชิชิชิชิชิชิ
    """
        danger_text2 = """
    ด้านหน้าด้านหน้าด้านหน้าด้านหน้าด้านหน้าด้านหน้าด้านหน้าด้านหน้าด้านหน้าด้านหน้าด้านหน้าด้านหน้าด้านหน้าด้าน
    """
        danger_text3 = """
    ด้านหน้าด้านหน้าด้านหน้าด้านหน้าด้านหน้าด้านหน้าด้านหน้าด้านหน้าด้านหน้าด้านหน้าด้านหน้าด้านหน้าด้านหน้าด้านหน้าด้านหน้าด้านหน้าด้านหน้าด้านหน้าด้านหน้าด้านกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกก
    """
        self.assertIsInstance(
            word_tokenize(danger_text1, engine="newmm"), list
        )
        self.assertIsInstance(
            word_tokenize(danger_text2, engine="newmm"), list
        )
        self.assertIsInstance(
            word_tokenize(danger_text3, engine="newmm"), list
        )
        self.assertIsInstance(
            word_tokenize(danger_text1, engine="newmm-safe"), list
        )
        self.assertIsInstance(
            word_tokenize(danger_text2, engine="newmm-safe"), list
        )
        self.assertIsInstance(
            word_tokenize(danger_text3, engine="newmm-safe"), list
        )

    def test_word_tokenize_attacut(self):
        self.assertEqual(attacut.segment(None), [])
        self.assertEqual(attacut.segment(""), [])
        self.assertEqual(
            word_tokenize("ฉันรักภาษาไทยเพราะฉันเป็นคนไทย", engine="attacut"),
            ["ฉัน", "รัก", "ภาษา", "ไทย", "เพราะ", "ฉัน", "เป็น", "คน", "ไทย"],
        )

    def test_sent_tokenize(self):
        self.assertEqual(sent_tokenize(None), [])
        self.assertEqual(sent_tokenize(""), [])
        self.assertEqual(
            sent_tokenize("รักน้ำ  รักปลา  ", engine="whitespace"),
            ["รักน้ำ", "รักปลา", ""],
        )
        self.assertEqual(
            sent_tokenize("รักน้ำ  รักปลา  ", engine="whitespace+newline"),
            ["รักน้ำ", "รักปลา"],
        )
        self.assertEqual(
            sent_tokenize("วันนี้ฉันกินข้าว และโดดเรียน", engine="crfcut"),
            ["วันนี้ฉันกินข้าว และโดดเรียน"],
        )
        self.assertEqual(
            sent_tokenize("น้ำพึ่งเรือ แต่เสือพึ่งป่า", engine="crfcut"),
            ["น้ำพึ่งเรือ ", "แต่เสือพึ่งป่า"],
        )
        self.assertEqual(
            sent_tokenize("น้ำพึ่งเรือ แต่เสือพึ่งป่า", engine=""),
            ["น้ำพึ่งเรือ ", "แต่เสือพึ่งป่า"],
        )
        self.assertEqual(
            sent_tokenize("วันนี้ฉันกินข้าว และโดดเรียน"),
            ["วันนี้ฉันกินข้าว และโดดเรียน"],
        )
        self.assertEqual(
            sent_tokenize("น้ำพึ่งเรือ แต่เสือพึ่งป่า"),
            ["น้ำพึ่งเรือ ", "แต่เสือพึ่งป่า"],
        )
        self.assertIsNotNone(
            sent_tokenize("น้ำพึ่งเรือ แต่เสือพึ่งป่า", 
            keep_whitespace = False,
            engine = "whitespace"),
        )
    def test_ssg_tokenize(self):
        self.assertEqual(ssg_segment(None), [])
        self.assertEqual(ssg_segment(""), [])
        self.assertTrue(
            "ดาว" in syllable_tokenize("สวัสดีดาวอังคาร", engine="ssg")
        )
    def test_subword_tokenize(self):
        self.assertEqual(subword_tokenize(None), [])
        self.assertEqual(subword_tokenize(""), [])

        self.assertIsInstance(
            subword_tokenize("สวัสดีดาวอังคาร", engine="tcc"), list
        )
        self.assertFalse(
            "า" in subword_tokenize("สวัสดีดาวอังคาร", engine="tcc")
        )

        self.assertEqual(subword_tokenize(None, engine="etcc"), [])
        self.assertEqual(subword_tokenize("", engine="etcc"), [])
        self.assertIsInstance(
            subword_tokenize("สวัสดิีดาวอังคาร", engine="etcc"), list
        )
        self.assertFalse(
            "า" in subword_tokenize("สวัสดีดาวอังคาร", engine="etcc")
        )
        self.assertIsInstance(
            subword_tokenize("เบียร์สิงห์", engine="etcc"), list
        )

    def test_syllable_tokenize(self):
        self.assertEqual(syllable_tokenize(None), [])
        self.assertEqual(syllable_tokenize(""), [])
        self.assertEqual(
            syllable_tokenize("สวัสดีชาวโลก"), ["สวัส", "ดี", "ชาว", "โลก"]
        )
        self.assertFalse("า" in syllable_tokenize("สวัสดีชาวโลก"))

        self.assertEqual(syllable_tokenize(None, engine="ssg"), [])
        self.assertEqual(syllable_tokenize("", engine="ssg"), [])
        self.assertEqual(
            syllable_tokenize("แมวกินปลา", engine="ssg"), ["แมว", "กิน", "ปลา"]
        )
        self.assertTrue(
            "ดาว" in syllable_tokenize("สวัสดีดาวอังคาร", engine="ssg")
        )
        self.assertFalse(
            "า" in syllable_tokenize("สวัสดีดาวอังคาร", engine="ssg")
        )

    def test_tcc(self):
        self.assertEqual(tcc.segment(None), [])
        self.assertEqual(tcc.segment(""), [])
        self.assertEqual(
            tcc.segment("ประเทศไทย"), ["ป", "ระ", "เท", "ศ", "ไท", "ย"]
        )

        self.assertEqual(list(tcc.tcc("")), [])
        self.assertEqual(tcc.tcc_pos(""), set())
