# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

import unittest

from pythainlp.transliterate import get_word_dict
from pythainlp.transliterate.wiktionary import transliterate_wiktionary


class TransliterateThPronTestCase(unittest.TestCase):
    def test_transliterate_wiktionary(self):
        self.assertEqual(
            transliterate_wiktionary("แมว", mode="royin"), "maeo"
        )
        self.assertEqual(
            transliterate_wiktionary("คน", mode="paiboon"), "kon"
        )
        self.assertEqual(
            transliterate_wiktionary("คน", mode="ipa"), "kʰon˧")

    def test_transliterate_wiktionary_returns_input_for_unknown_mode(self):
        self.assertEqual(transliterate_wiktionary("แมว", mode="unknown"), "แมว")

    def test_thai_digits_conversion(self):
        self.assertEqual(transliterate_wiktionary("๑๒๓", mode="royin"), "123")

    def test_get_word_dict(self):
        self.assertEqual(
            get_word_dict("ปฺระ-ชา"),
            {
                "word": "ปฺระ-ชา",
                "paiboon": "bprà-chaa",
                "royin": "pra-cha",
                "ipa": "pra˨˩.t͡ɕʰaː˧",
            },
        )

    def test_transliterate_wiktionary_paiboon_cases(self):
        # test cases from https://w.wiki/RifX
        test_cases = [
            ('เฮิ็้ย', 'hə́i'),
            ('เฉิ็ย', 'chə̌i'),
            ('เงิ็น', 'ngən'),
            ('เกดส', 'gèets'),  # เกตส์ (Gates)
            ('มันส', 'mans'),  # มันส์
            ('ไอ๊ส', 'áis'),  # ไอซ์ (ice)
            ('เซ็กส', 'séks'),  # เซ็กส์ (sex)
            ('เอ็๊กส', 'éks'),  # เอกซ์ & เอ็กซ์ & เอ๊กซ์ (ex)
            ('เฮ้าส', 'háos'),  # เฮาส์ & เฮ้าส์ (house)
            ('เม้าส', 'máos'),  # เมาส์ & เม้าส์ (mouse)
            ('ทฺรำ-เป็ด', 'tram-bpèt'),  # ทรัมเป็ต
            ('ห็อย', 'hɔ̌i'),
            ('หฺม็อย', 'mɔ̌i'),
            ('หฺมั่น-โถว', 'màn-tǒow'),
            ('เด๊ด-สะ-มอ-เร่', 'déet-sà-mɔɔ-rêe'),
            ('เห', 'hěe'),
            ('แคฺล', 'klɛɛ'),
            ('แคล', 'kɛɛl'),
            ('เพฺล', 'plee'),
            ('เพล', 'peel'),
            ('เปฺล', 'bplee'),
            ('เปล', 'bpeel'),
            ('เบล', 'beel'),
            ('เซล', 'seel'),
            ('โพล', 'pool'),
            ('รา-ชา-ทิ-ราด', 'raa-chaa-tí-râat'),
            ('ขฺวน-ขฺวาย', 'kwǒn-kwǎai'),  # ขวนขวาย Only the word ขวน read as kwǒn instead of kǔuan.
            ('ข่วน', 'kùuan'),
            ('หอน', 'hɔ̌ɔn'),
            ('โหน', 'hǒon'),  # ห้อยโหน homograph issue
            ('สะ-โหฺน', 'sà-nǒo'),  # โสน homograph issue
            ('แหน', 'hɛ̌ɛn'),  # หวงแหน homograph issue
            ('แหฺน', 'nɛ̌ɛ'),  # จอกแหน homograph issue
            ('แถ็ว', 'tɛ̌o'),  # แถว
            ('ซวง', 'suuang'),
            ('น้ำ', 'nám'),
            ('หฺมาย', 'mǎai'),
            ('แห็่ง', 'hɛ̀ng'),
            ('หน', 'hǒn'),
            ('เหด-สุด-วิ-ไส', 'hèet-sùt-wí-sǎi'),
            ('ไหฺย่', 'yài'),
            ('หก', 'hòk'),
            ('หอย', 'hɔ̌ɔi'),
            ('กับ', 'gàp'),
            ('ธรรม', 'tam'),
            ('ปฺระ-ชา', 'bprà-chaa'),
            ('นะ-คอน', 'ná-kɔɔn'),
            ('บาด', 'bàat'),
            ('บ้า', 'bâa'),
            ('แข็ง', 'kɛ̌ng'),
            ('แกะ', 'gɛ̀'),
            ('แดง', 'dɛɛng'),
            ('แปฺล', 'bplɛɛ'),
            ('ผฺล็อง', 'plɔ̌ng'),
            ('เกาะ', 'gɔ̀'),
            ('นอน', 'nɔɔn'),
            ('พ่อ', 'pɔ̂ɔ'),
            ('เห็ด', 'hèt'),
            ('เล็่น', 'lên'),
            ('เตะ', 'dtè'),
            ('เพฺลง', 'pleeng'),
            ('เท-วี', 'tee-wii'),
            ('เยอะ', 'yə́'),
            ('เดิน', 'dəən'),
            ('เผฺลอ', 'plə̌ə'),
            ('ตก', 'dtòk'),
            ('โต๊ะ', 'dtó'),
            ('โชค', 'chôok'),
            ('โม-โห', 'moo-hǒo'),
            ('คิด', 'kít'),
            ('มิ-ถุน', 'mí-tǔn'),
            ('หิ-มะ', 'hì-má'),
            ('อีก', 'ìik'),
            ('จี้', 'jîi'),
            ('ลึก', 'lʉ́k'),
            ('รึ', 'rʉ́'),
            ('กฺลืน', 'glʉʉn'),
            ('ชื่อ', 'chʉ̂ʉ'),
            ('คุก', 'kúk'),
            ('จุ-ฬา', 'jù-laa'),
            ('ลูก', 'lûuk'),
            ('ปู', 'bpuu'),
            ('เดี๊ยะ', 'día'),
            ('เปาะ-เปี๊ยะ', 'bpɔ̀-bpía'),
            ('ปอ-เปี๊ยะ', 'bpɔɔ-bpía'),
            ('เปฺรี๊ยะ', 'bpría'),
            ('เตียง', 'dtiiang'),
            ('เมีย', 'miia'),
            ('เอือะ', 'ʉ̀a'),
            ('เรื่อง', 'rʉ̂ʉang'),
            ('เรือ', 'rʉʉa'),
            ('ผฺลัวะ', 'plùa'),
            ('นวด', 'nûuat'),
            ('ตัว', 'dtuua'),
            ('ไม่', 'mâi'),
            ('ใส่', 'sài'),
            ('วัย', 'wai'),
            ('ไทย', 'tai'),
            ('ไม้', 'mái'),
            ('หาย', 'hǎai'),
            ('ผฺล็อย', 'plɔ̌i'),
            ('ซอย', 'sɔɔi'),
            ('เลย', 'ləəi'),
            ('โดย', 'dooi'),
            ('ทุย', 'tui'),
            ('เหฺนื่อย', 'nʉ̀ai'),
            ('สวย', 'sǔai'),
            ('เรา', 'rao'),
            ('ขาว', 'kǎao'),
            ('แมว', 'mɛɛo'),
            ('เกอว', 'gəəo'),
            ('เร็ว', 'reo'),
            ('เอว', 'eeo'),
            ('หิว', 'hǐu'),
            ('เขียว', 'kǐao'),
            ('ทำ', 'tam'),
        ]

        for thai_text, expected_translit in test_cases:
            with self.subTest(thai_text=thai_text):
                self.assertEqual(
                    transliterate_wiktionary(thai_text, mode="paiboon"),
                    expected_translit
                )

if __name__ == '__main__':
    unittest.main()
