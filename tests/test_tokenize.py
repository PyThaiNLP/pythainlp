# -*- coding: utf-8 -*-

import unittest

from pythainlp.tokenize import (
    DEFAULT_WORD_DICT_TRIE,
    Tokenizer,
    attacut,
    clause_tokenize,
)
from pythainlp.tokenize import deepcut as tokenize_deepcut
from pythainlp.tokenize import etcc, longest, multi_cut, newmm
from pythainlp.tokenize import pyicu as tokenize_pyicu
from pythainlp.tokenize import (
    sent_tokenize,
    subword_tokenize,
    syllable_tokenize,
    tcc,
    word_tokenize,
)
from pythainlp.tokenize.ssg import segment as ssg_segment
from pythainlp.util import dict_trie


class TestTokenizePackage(unittest.TestCase):
    def setUp(self):
        self.text_1 = "หมอนทองตากลมหูว์MBK39"
        self.text_2 = "ทดสอบ"

        self.long_text = (
            "ไต้หวัน (แป่ะเอ๋ยี้: Tâi-oân; ไต่อวัน) หรือ ไถวาน "
            "(อักษรโรมัน: Taiwan; จีนตัวย่อ: 台湾; จีนตัวเต็ม: 臺灣/台灣; พินอิน: "
            "Táiwān; ไถวาน) หรือชื่อทางการว่า สาธารณรัฐจีน (จีนตัวย่อ: 中华民国; "
            "จีนตัวเต็ม: 中華民國; พินอิน: Zhōnghuá "
            "Mínguó) เป็นรัฐในทวีปเอเชียตะวันออก[7][8][9] ปัจจุบันประกอบด้วย"
            "เกาะใหญ่ 5 แห่ง คือ จินเหมิน (金門), ไต้หวัน, เผิงหู (澎湖), หมาจู่ "
            "(馬祖), และอูชิว (烏坵) กับทั้งเกาะเล็กเกาะน้อยอีกจำนวนหนึ่ง "
            'ท้องที่ดังกล่าวเรียกรวมกันว่า "พื้นที่ไต้หวัน" (臺灣地區)\n'
            "ไต้หวันด้านตะวันตกติดกับจีนแผ่นดินใหญ่ ด้านตะวันออกและตะวันออก"
            "เฉียงเหนือติดกับญี่ปุ่น และด้านใต้ติดกับฟิลิปปินส์ กรุงไทเปเป็น"
            "เมืองหลวง ส่วนไทเปใหม่เป็นเขตปกครองที่จัดตั้งขึ้นใหม่ กินพื้นที่"
            "กรุงไทเปและเป็นเขตซึ่งประชากรหนาแน่นที่สุดในเวลานี้\n"
            "เกาะไต้หวันเดิมเป็นที่อยู่ของชนพื้นเมือง และมีชาวจีนจากแผ่นดิน"
            "ใหญ่เข้ามาอาศัยร่วมด้วย จนกระทั่งชาววิลันดาและสเปนเดินทางเข้า"
            "มาในยุคสำรวจเมื่อศตวรรษที่ 17 และมาตั้งบ้านเรือนกลายเป็นนิคม"
            "ใหญ่โต ต่อมาปี 1662 ราชวงศ์หมิงในแผ่นดินใหญ่ถูกราชวงศ์ชิงแทนที่ "
            "เจิ้ง เฉิงกง (鄭成功) ขุนศึกหมิง รวมกำลังหนีมาถึงเกาะไต้หวัน "
            "และรุกไล่ฝรั่งออกไปได้อย่างราบคาบ เขาจึงตั้งราชอาณาจักรตงหนิง "
            '(東寧) ขึ้นบนเกาะเพื่อ "โค่นชิงฟื้นหมิง" แต่ในปี 1683 ราชวงศ์'
            "ชิงปราบปรามอาณาจักรตงหนิงและเข้าครอบครองไต้หวันเป็นผลสำเร็จ "
            "ไต้หวันจึงกลายเป็นมณฑลหนึ่งของจีน อย่างไรก็ดี ความบาดหมางระหว่าง"
            "จีนกับญี่ปุ่นเป็นเหตุให้ญี่ปุ่นได้ไต้หวันไปในปี 1895\n"
            "ก่อนเสียไต้หวันคืนแก่จีนหลังสงครามโลกครั้งที่สอง ช่วงนั้น มีการ"
            "เปลี่ยนแปลงการปกครองในจีน พรรคก๊กมินตั๋ง ได้เป็นใหญ่ "
            "แต่ไม่นานก็เสียทีให้แก่พรรคคอมมิวนิสต์จีน พรรคก๊กมินตั๋งจึงหนี"
            "มายังเกาะไต้หวันและสถาปนาสาธารณรัฐจีนขึ้นบนเกาะแยกต่างหาก "
            "ส่วนฝ่ายคอมมิวนิสต์จีนที่เป็นฝ่ายได้รับชัยชนะได้สถาปนาสาธารณรัฐ"
            "ประชาชนจีนบนแผ่นดินใหญ่ อย่างไรก็ดี จีนยังคงถือว่า ไต้หวันเป็น"
            "มณฑลหนึ่งของตน และไต้หวันเองก็ยังมิได้รับการยอมรับจากนานาชาติ"
            "ว่าเป็นประเทศเอกราชมาจนบัดนี้\n"
            "ในช่วงทศวรรษ 1980 ถึงต้นทศวรรษ 1990 การเมืองการปกครอง"
            "สาธารณรัฐจีน (ไต้หวัน) เจริญรุ่งเรืองจนเป็นประชาธิปไตยที่มีพรรค"
            "การเมืองหลายพรรคและมีการเลือกตั้งทั่วหน้า ในช่วงกลางศตวรรษที่ "
            "20 เศรษฐกิจไต้หวันงอกงามอย่างรวดเร็ว ไต้หวันจึงกลายเป็นประเทศ"
            "พัฒนาแล้ว ได้ชื่อว่าเป็นหนึ่งในสี่เสือแห่งเอเชีย มีอุตสาหกรรม"
            "ล้ำหน้า และมีเศรษฐกิจใหญ่โตเป็นอันดับที่ 19 ของโลก[11][12] "
            "อุตสาหกรรมที่ใช้เทคโนโลยีชั้นสูงของไต้หวันยังมีบทบาทสำคัญมากใน"
            "เศรษฐกิจโลก เป็นเหตุให้ไต้หวันได้เป็นสมาชิกองค์การการค้าโลกและ"
            "ความร่วมมือทางเศรษฐกิจเอเชีย-แปซิฟิก เสรีภาพของสื่อมวลชน เสรี"
            "ภาพทางเศรษฐกิจ การสาธารณสุข[13]การศึกษา และดัชนีการพัฒนามนุษย์ใน"
            "ไต้หวันยังได้รับการจัดอยู่ในอันดับสูงด้วย[14][4][15]\n"
            "สาธารณรัฐจีน มีลักษณะเป็นกลุ่มเกาะ ภูมิประเทศติดกับทะเล ไม่ติด"
            "กับประเทศใดเลย ห่างจากเกาะทางทิศเหนือและทิศตะวันตกเป็นสาธารณรัฐ"
            "ประชาชนจีน ทิศใต้เป็นประเทศฟิลิปปินส์และทะเลจีนใต้ ส่วนทิศ"
            "ตะวันออกเป็นมหาสมุทรแปซิฟิก\n"
            "ในปี ค.ศ. 1638 หลังการพ่ายแพ้ของหลานชายของเจิ้ง เฉิงกง "
            "จากการบุกโจมตีทางทัพเรือของราชวงศ์ชิงแมนจูที่นำทัพโดยชื่อ หลาง"
            "จากทางใต้ของมณฑลฝูเจี้ยน ทำให้ราชวงศ์ชิงผนวกยึดเกาะไต้หวันเป็น"
            "ส่วนหนึ่งสำเร็จ และวางไว้ภายใต้เขตอำนาจของมณฑลฝูเจี้ยน ราชสำนัก"
            "ราชวงศ์ชิงพยายามลดการละเมิดสิทธิ์และความไม่ลงรอยกันในพื้นที่โดย"
            "ออกกฎหมายเพื่อจัดการตรวจคนเข้าเมืองและเคารพสิทธิในที่ดินของชน"
            "พื้นเมืองไต้หวัน ผู้อพยพจากฝูเจี้ยนทางใต้ส่วนใหญ่ยังคงเดินทางไป"
            "ไต้หวัน เขตแดนระหว่างดินแดนที่เสียภาษีและสิ่งที่ถูกพิจารณาว่า"
            'เป็นดินแดน "เขตอันตราย" เปลี่ยนไปทางทิศตะวันออกโดยชาวพื้นเมือง'
            "บางคนเข้ารีตรับวัฒนธรรมแบบจีน ในขณะที่คนอื่นถอยกลับเข้าในภูเขา "
            "ในช่วงเวลานี้มีความขัดแย้งจำนวนมากระหว่างกลุ่มชาวฮั่นด้วยกันเอง"
            "จากภูมิภาคต่าง ๆ ของฝูเจี้ยนทางใต้โดยเฉพาะอย่างยิ่งระหว่างเฉวียน"
            "โจวกับฉางโจว และระหว่างฝูเจี้ยนตอนใต้และชาวพื้นเมืองไต้หวัน\n"
            "พ.ศ. 2454 (ค.ศ. 1911) การจลาจลอู่ฮั่นในประเทศจีน เป็นจุดเริ่มต้น"
            "การล่มสลายของราชวงศ์ชิง เมื่อพรรคคอมมิวนิสต์จีนเข้ามีอำนาจในจีน"
            "แผ่นดินใหญ่เมื่อ พ.ศ. 2492 (1949) พรรคก๊กมินตั๋ง พรรคการเมือง"
            "ชาตินิยมของจีนที่เป็นฝ่ายแพ้ก็พาผู้คนอพยพหนีออกจากแผ่นดินใหญ่มา"
            "ตั้งหลักที่ไต้หวัน เพื่อวางแผนกลับไปครองอำนาจในจีนต่อไป\n"
            "ชาวจีนมากกว่า 1 ล้าน 5 แสนคน อพยพตามมาอยู่ที่เกาะไต้หวันในยุคที่"
            "เหมา เจ๋อตง มีอำนาจเต็มที่ในจีนแผ่นดินใหญ่ ผู้นำของประเทศทั้งสอง"
            "จีนคือผู้นำพรรคคอมมิวนิสต์กับผู้นำสาธารณรัฐจีนบนเกาะไต้หวัน แย่ง"
            "กันเป็นกระบอกเสียงของประชาชนจีนในเวทีโลก แต่เสียงของนานาประเทศ"
            "ส่วนใหญ่เกรงอิทธิพลของจีนแผ่นดินใหญ่ จึงให้การยอมรับจีนแผ่นดิน"
            "ใหญ่มากกว่า\n"
            "ในปี พ.ศ. 2514 (ค.ศ. 1971) ก่อนที่นายพล เจียง ไคเช็ก"
            "(ภาษาจีน: 蔣中正) จะถึงอสัญกรรมไม่กี่ปี สาธารณรัฐจีนซึ่งเป็น"
            "ประเทศที่ร่วมก่อตั้งองค์การสหประชาชาติได้สูญเสียสมาชิกภาพใน"
            "ฐานะตัวแทนชาวจีนให้กับสาธารณรัฐประชาชนจีน ในปี พ.ศ. 2521 (1978)"
            "สหประชาชาติประกาศรับรองจีนเดียวคือจีนแผ่นดินใหญ่และตัดสัมพันธ์"
            "ทางการเมืองกับสาธารณรัฐจีน ทั้งสหรัฐอเมริกาก็ได้ถอนการรับรองว่า"
            "สาธารณรัฐจีนมีฐานะเป็นรัฐ ไต้หวันจึงกลายเป็นเพียงดินแดนที่จีน"
            "อ้างว่าเป็นส่วนหนึ่งของสาธารณรัฐประชาชนจีนตั้งแต่นั้นเป็นต้นมา\n"
            "เมื่อเจียง ไคเช็ก ถึงแก่อสัญกรรมในปี พ.ศ. 2518 (1975) ลูกชาย"
            "ที่ชื่อ เจี่ยง จิงกั๋ว ได้เป็นผู้สืบทอดการปกครอง"
            "ไต้หวันต่อและเริ่มกระบวนการ วางรากฐานไปสู่ประชาธิปไตย\n"
            "หลังจากที่ประธานาธิบดี เจียง จิงกั๋ว เสียชีวิต ไต้หวันจึงได้เข้า"
            "สู่ระบอบประชาธิปไตยเต็มรูปแบบ ประธานาธิบดีคนใหม่ ซึ่งเกิดใน"
            "ไต้หวัน ชื่อ หลี่ เติงฮุย ขึ้นบริหารประเทศ โดยการสนับสนุนของ"
            "เจี่ยง จิงกั๋ว ทั้งที่ หลี่ เติงฮุย นั้นเคลื่อนไหว"
            "สนับสนุนเอกราชไต้หวัน นาย รัฐบาลจีนที่ปักกิ่งได้ตั้ง"
            'ฉายาประธานาธิบดีไต้หวันคนใหม่ว่า "จิ้งจกปากหวาน" '
            "ช่วงเวลาที่นายหลี่ เติงฮุย เป็นประธานาธิบดี การเมืองของไต้หวัน"
            "เกิดการแตกแยกออกเป็น 3 ฝ่ายคือ 1) พวกก๊กมินตั๋ง ที่ต้องการกลับ"
            "ไปรวมประเทศกับจีนแผ่นดินใหญ่ (รวมจีนแผ่นดินใหญ่ภายใต้การปกครอง"
            "ของสาธารณรัฐจีน) 2) พวกที่ต้องการให้ไต้หวันเป็นประเทศอิสระไม่"
            "เกี่ยวข้องกับจีนแผ่นดินใหญ่ และ 3) พวกที่ต้องการดำรงฐานะของ"
            "ประเทศไว้ดังเดิมต่อไป\n"
            "ไต้หวันกับจีนแผ่นดินใหญ่นัดเจรจาหาทางออกของข้อขัดแย้งทางการเมือง"
            "ครั้งแรกที่สิงคโปร์เมื่อปี พ.ศ. 2536 (ค.ศ. 1993) แต่ปรากฏว่าจีน"
            "แผ่นดินใหญ่ประวิงเวลาลงนามในสัญญาหลายฉบับที่เป็นข้อตกลงร่วมกัน "
            "ทำให้ผลการเจรจาคราวนั้นไม่ก้าวหน้าไปถึงไหน ความสัมพันธ์ระหว่าง"
            "สองจีนเลวร้ายลงทุกที เมื่อประธานาธิบดี หลี่ เติงฮุย เดินทางไป"
            "เยือนสหรัฐอเมริกาและได้รับการยอมรับอย่างเอิกเกริก ทำให้จีนแผ่น"
            "ดินใหญ่ไม่พอใจอย่างมาก จึงข่มขวัญไต้หวันกับประเทศที่ให้การสนับ"
            "สนุนไต้หวัน ด้วยการทำการซ้อมรบขึ้นใกล้ ๆ เกาะไต้หวัน สหรัฐ"
            "อเมริกาออกมาแสดงอาการปกป้องคุ้มครองไต้หวันด้วยการส่งกำลังกอง"
            "เรือรบของสหรัฐฯ มาป้วนเปี้ยนอยู่ในน่านน้ำที่จีนซ้อมรบ\n"
            "ขณะที่โลกกำลังล่อแหลมกับสถานการณ์ที่ตึงเครียดในน่านน้ำจีนมาก"
            "ขึ้นทุกทีนั้น ไต้หวันก็จัดให้มีการเลือกตั้งครั้งใหม่ และในการ"
            "เลือกตั้งครั้งใหม่นั้นเอง ไต้หวันก็ได้นายหลี่ เติงฮุย เป็น"
            "ประธานาธิบดีอีกครั้ง\n"
            "ไต้หวันเข้าสู่สภาวะวิกฤต เมื่อเกิดแผ่นดินไหวครั้งร้ายแรงที่สุดใน"
            "ประวัติศาสตร์ในเดือนกันยายน พ.ศ. 2542 (ค.ศ. 1999) ทำให้ประชากร"
            "ส่วนมากที่เป็นชาวพื้นเมืองเสียชีวิตไป 2,000 คน ทั้งเมืองมีแต่"
            "เศษซากปรักหักพังจากภัยธรรมชาติ และช่วงนี้ไต้หวันต้องเผชิญความ"
            "ยากลำบาก จีนแผ่นดินใหญ่ก็เพิ่มความกดดันไม่ให้นานาชาติ"
            "เข้ามายุ่งเกี่ยวกับไต้หวันแม้ในยามคับขันเช่นนี้ โดยประกาศว่า "
            "หากมีประเทศใดจะเข้าไปให้ความช่วยเหลือไต้หวัน จะต้องได้รับอนุญาต"
            "จากจีนก่อน ซึ่งคำประกาศของจีนแผ่นดินใหญ่สวนทางกับเมตตาธรรมของ"
            "ประเทศทั่วโลกที่ต้องการให้ความช่วยเหลือไต้หวัน\n"
            "เดือนมีนาคม พ.ศ. 2543 (ค.ศ. 2000) มีการเลือกตั้งใหม่ในไต้หวัน "
            "ชาวไต้หวันเลือกผู้แทนจากพรรคประชาธิปไตยก้าวหน้า คือ นายเฉิน สุย"
            "เปี่ยน เป็นประธานาธิบดีคนใหม่ของไต้หวัน ผู้ประกาศนโยบายการเมือง"
            "แข็งกร้าวว่าไต้หวันต้องการแยกตัวเป็นอิสระจากจีนแผ่นดินใหญ่ ยุติ"
            "ยุคของพรรคชาตินิยมที่ยังฝักใฝ่แผ่นดินใหญ่อยู่ จีนแผ่นดินใหญ่จึง"
            "ถือว่าเป็นกบฏต่อการปกครองของจีน เพราะแต่ไหนแต่ไร ไต้หวันไม่เคย"
            "ประกาศอย่างเป็นทางการว่าเป็นประเทศอิสระแยกจากจีน และจีนพูดอยู่"
            "เสมอว่าไต้หวันเป็นเด็กในปกครองที่ค่อนข้างจะหัวดื้อและเกเร หาก"
            "ไต้หวันประกาศว่าเป็นอิสระจากจีนเมื่อใด จีนก็จะยกกำลังจัดการ"
            "กับไต้หวันทันที\n"
            "ในขณะที่ความสัมพันธ์ทางการเมืองระหว่างสองจีนในสายตาชาวโลก"
            "เลวร้ายลง จีนทั้งสองกลับมีการติดต่อทางการค้ากันมากขึ้น มีการ"
            "ผ่อนปรนอนุญาตให้ชาวไต้หวันเดินทางไปจีนแผ่นดินใหญ่เพื่อเยี่ยม"
            "ญาติได้ เกิดปรากฏการณ์สำคัญคือนักธุรกิจไต้หวันหอบเงินทุนกว่า "
            "20,000 ล้านดอลลาร์สหรัฐ ไปลงทุนดำเนินธุรกิจทางตอนใต้ของจีน"
            "แผ่นดินใหญ่ จนกระทั่งขณะนี้ชาวไต้หวันกลายเป็นนักลงทุนรายใหญ่"
            "เป็นลำดับ 2 ของจีน\n"
            "วันที่ 24 พฤษภาคม 2560 ศาลรัฐธรรมนูญวินิจฉัยว่ากฎหมายสมรส"
            "ปัจจุบันในเวลานั้น ละเมิดรัฐธรรมนูญ โดยปฏิเสธสิทธิสมรสของคู่รัก"
            "เพศเดียวกันชาวไต้หวัน ศาลวินิจฉัยว่าหากสภานิติบัญญัติไม่ผ่าน"
            "การแก้ไขกฎหมายที่เพียงพอต่อกฎหมายสมรสของไต้หวันภายในสองปี "
            "การสมรสเพศเดียวกันจะชอบด้วยกฎหมายโดยอัตโนมัติในไต้หวัน[17] "
            "วันที่ 17 พฤษภาคม 2562 สภานิติบัญญัติไต้หวันอนุมัติ"
            "ร่างกฎหมายทำให้การสมรสเพศเดียวกันชอบด้วยกฎหมาย"
            " ทำให้เป็นประเทศแรกในทวีปเอเชียที่ผ่านกฎหมายดังกล่าว[18][19]"
        )

        self.danger_text1 = (
            "ชิชิชิชิชิชิชิชิชิชิชิชิชิชิชิชิชิชิชิชิชิชิชิชิชิชิชิชิชิชิ"
            "ชิชิชิชิชิชิชิชิชิชิชิชิชิชิชิชิชิชิชิชิชิชิชิชิชิชิชิชิชิชิ"
            "ชิชิชิชิชิชิชิชิชิ"
        )

        self.danger_text2 = (
            "ด้านหน้าด้านหน้าด้านหน้าด้านหน้าด้านหน้าด้านหน้าด้าน"
            "หน้าด้านหน้าด้านหน้าด้านหน้าด้านหน้าด้านหน้าด้านหน้าด้าน"
        )

        self.danger_text3 = (
            "ด้านหน้าด้านหน้าด้านหน้าด้านหน้าด้านหน้าด้านหน้าด้านหน้า"
            "ด้านหน้าด้านหน้าด้านหน้าด้านหน้าด้านหน้าด้านหน้าด้านหน้า"
            "ด้านหน้าด้านหน้าด้านหน้าด้านหน้าด้านหน้าด้านหน้าด้านหน้า"
            "ด้านหน้าด้านหน้าด้านกกกกกก"
            "กกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกก"
        )

    def test_clause_tokenize(self):
        self.assertIsNotNone(clause_tokenize(["ฉัน", "ทดสอบ"]))
        self.assertIsInstance(clause_tokenize(["ฉัน", "ทดสอบ"]), list)

    def test_Tokenizer(self):
        t_test = Tokenizer(DEFAULT_WORD_DICT_TRIE)
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
            ["หา", "เงิน", "เพื่", "อ", "เรีย", "น"],
        )
        self.assertEqual(etcc.segment("หนังสือ"), ["ห", "นัง", "สือ"])
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
        self.assertIsNotNone(word_tokenize(self.text_1, engine="newmm"))
        self.assertIsNotNone(word_tokenize(self.text_1, engine="mm"))
        self.assertIsNotNone(word_tokenize(self.text_1, engine="longest"))
        self.assertIsNotNone(word_tokenize(self.text_1, engine="icu"))
        self.assertIsNotNone(word_tokenize(self.text_1, engine="deepcut"))
        self.assertIsNotNone(word_tokenize(self.text_1, engine="attacut"))
        with self.assertRaises(ValueError):
            word_tokenize("หมอนทอง", engine="XX")  # engine does not exist

        self.assertTrue(
            "ไฟ" in word_tokenize("รถไฟฟ้า", custom_dict=dict_trie(["ไฟ"]))
        )

    def test_word_tokenize_deepcut(self):
        self.assertEqual(tokenize_deepcut.segment(None), [])
        self.assertEqual(tokenize_deepcut.segment(""), [])
        self.assertIsNotNone(
            tokenize_deepcut.segment("ทดสอบ", DEFAULT_WORD_DICT_TRIE)
        )
        self.assertIsNotNone(tokenize_deepcut.segment("ทดสอบ", ["ทด", "สอบ"]))
        self.assertIsNotNone(word_tokenize("ทดสอบ", engine="deepcut"))
        self.assertIsNotNone(
            word_tokenize(
                "ทดสอบ", engine="deepcut", custom_dict=DEFAULT_WORD_DICT_TRIE
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
            longest_tokenizer.word_tokenize("เฉียบพลัน"), ["เฉียบพลัน"],
        )

    def test_word_tokenize_mm(self):
        self.assertEqual(multi_cut.segment(None), [])
        self.assertEqual(multi_cut.segment(""), [])
        self.assertIsNotNone(multi_cut.segment("ตัด", dict_trie([""])))

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
        self.assertFalse(
            " " in word_tokenize("จุ๋มง่วง", keep_whitespace=False,)
        )

    def test_word_tokenize_newmm_longtext(self):
        self.assertIsInstance(
            word_tokenize(self.long_text, engine="newmm"), list
        )
        self.assertIsInstance(
            word_tokenize(self.long_text, engine="newmm-safe"), list
        )

    def test_word_tokenize_newmm_dangertext(self):
        self.assertIsInstance(
            word_tokenize(self.danger_text1, engine="newmm"), list
        )
        self.assertIsInstance(
            word_tokenize(self.danger_text2, engine="newmm"), list
        )
        self.assertIsInstance(
            word_tokenize(self.danger_text3, engine="newmm"), list
        )
        self.assertIsInstance(
            word_tokenize(self.danger_text1, engine="newmm-safe"), list
        )
        self.assertIsInstance(
            word_tokenize(self.danger_text2, engine="newmm-safe"), list
        )
        self.assertIsInstance(
            word_tokenize(self.danger_text3, engine="newmm-safe"), list
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

        sent_1 = "ฉันไปโรงเรียน เธอไปโรงพยาบาล"
        sent_1_toks = ["ฉันไปโรงเรียน ", "เธอไปโรงพยาบาล"]
        sent_2 = "วันนี้ฉันกินข้าว และโดดเรียน"
        sent_2_toks = ["วันนี้ฉันกินข้าว และโดดเรียน"]
        sent_3 = (
            "(1) บทความนี้ผู้เขียนสังเคราะห์ขึ้นมา"
            + "จากผลงานวิจัยที่เคยทำมาในอดีต"
            + " มิได้ทำการศึกษาค้นคว้าใหม่อย่างกว้างขวางแต่อย่างใด"
            + " จึงใคร่ขออภัยในความบกพร่องทั้งปวงมา ณ ที่นี้"
        )
        sent_3_toks = [
            "(1) บทความนี้ผู้เขียนสังเคราะห์ขึ้นมา"
            + "จากผลงานวิจัยที่เคยทำมาในอดีต ",
            "มิได้ทำการศึกษาค้นคว้าใหม่อย่างกว้างขวางแต่อย่างใด ",
            "จึงใคร่ขออภัยในความบกพร่องทั้งปวงมา ณ ที่นี้",
        ]

        self.assertEqual(
            sent_tokenize(sent_1, engine="crfcut"), sent_1_toks,
        )
        self.assertEqual(
            sent_tokenize(sent_2, engine="crfcut"), sent_2_toks,
        )
        self.assertEqual(
            sent_tokenize(sent_3, engine="crfcut"), sent_3_toks,
        )
        self.assertEqual(
            sent_tokenize(sent_1), sent_1_toks,
        )
        self.assertEqual(
            sent_tokenize(sent_2), sent_2_toks,
        )
        self.assertEqual(
            sent_tokenize(sent_3), sent_3_toks,
        )
        self.assertIsNotNone(
            sent_tokenize(sent_1, keep_whitespace=False, engine="whitespace",),
        )
        self.assertFalse(
            " "
            in sent_tokenize(
                sent_1, engine="whitespace", keep_whitespace=False,
            )
        )
        with self.assertRaises(ValueError):
            sent_tokenize("ฉันไป กิน", engine="XX")  # engine does not exist

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
        self.assertIsInstance(subword_tokenize("โควิด19", engine="etcc"), list)
        self.assertFalse(
            " " in subword_tokenize("พันธมิตร ชา นม", keep_whitespace=False)
        )
        with self.assertRaises(ValueError):
            subword_tokenize("นกแก้ว", engine="XX")  # engine does not exist

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
        self.assertFalse(
            " " in syllable_tokenize("พันธมิตร ชา นม", keep_whitespace=False)
        )
        with self.assertRaises(ValueError):
            syllable_tokenize("กรอเทป", engine="XX")  # engine does not exist

    def test_tcc(self):
        self.assertEqual(tcc.segment(None), [])
        self.assertEqual(tcc.segment(""), [])
        self.assertEqual(
            tcc.segment("ประเทศไทย"), ["ป", "ระ", "เท", "ศ", "ไท", "ย"]
        )
        self.assertEqual(list(tcc.tcc("")), [])
        self.assertEqual(tcc.tcc_pos(""), set())
