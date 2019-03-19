# -*- coding: utf-8 -*-

from pythainlp.tag import ThaiNameTagger
ner = ThaiNameTagger()
print(ner.get_ner("วันที่ 15 ก.ย. 61 ทดสอบระบบเวลา 14:49 น."))
