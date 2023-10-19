# -*- coding: utf-8 -*-

import unittest

import torch
from pythainlp.transliterate import romanize, transliterate, pronunciate, puan
from pythainlp.transliterate.ipa import trans_list, xsampa_list
from pythainlp.transliterate.thai2rom import ThaiTransliterator
from pythainlp.transliterate.thai2rom_onnx import ThaiTransliterator_ONNX
from pythainlp.transliterate.wunsen import WunsenTransliterate
from pythainlp.corpus import remove

_BASIC_TESTS = {
    None: "",
    "": "",
    "abc": "abc",
    "หมอก": "mok",
    "หาย": "hai",
    "แมว": "maeo",
    "เดือน": "duean",
    "ดำ": "dam",
    "ดู": "du",
    "บัว": "bua",
    "กก": "kok",
    "พร": "phon",
    "กร": "kon",
    "กรร": "kan",
    "กรรม": "kam",
    # "กรม": "krom",  # failed
    "ฝ้าย": "fai",
    "นพพร": "nopphon",
    "อัก": "ak",
    # "ทีปกร": "thipakon",  # failed
    # "ธรรพ์": "than",  # failed
    # "ธรรม": "tham",  # failed
    # "มหา": "maha",  # failed
    # "หยาก": "yak",  # failed
    # "อยาก": "yak",  # failed
    # "ยมก": "yamok",  # failed
    # "กลัว": "klua",  # failed
    # "บ้านไร่": "banrai",  # failed
    # "ชารินทร์": "charin",  # failed
}

# these are set of two-syllable words,
# to test if the transliteration/romanization is consistent, say
# romanize(1+2) = romanize(1) + romanize(2)
_CONSISTENCY_TESTS = [
    # ("กระจก", "กระ", "จก"),  # failed
    # ("ระเบิด", "ระ", "เบิด"),  # failed
    # ("หยากไย่", "หยาก", "ไย่"),  # failed
    ("ตากใบ", "ตาก", "ใบ"),
    # ("จัดสรร", "จัด", "สรร"),  # failed
]


class TestTransliteratePackage(unittest.TestCase):
    def test_romanize(self):
        self.assertEqual(romanize(None), "")
        self.assertEqual(romanize(""), "")
        self.assertEqual(romanize("แมว"), "maeo")
        self.assertEqual(romanize("แมว", engine="tltk"), "maeo")

    def test_romanize_royin_basic(self):
        for word, expect in _BASIC_TESTS.items():
            self.assertEqual(romanize(word, engine="royin"), expect)

    def test_romanize_royin_consistency(self):
        for word, part1, part2 in _CONSISTENCY_TESTS:
            self.assertEqual(
                romanize(word, engine="royin"),
                (
                    romanize(part1, engine="royin")
                    + romanize(part2, engine="royin")
                ),
            )

    def test_romanize_thai2rom(self):
        self.assertEqual(romanize("แมว", engine="thai2rom"), "maeo")
        self.assertEqual(romanize("บ้านไร่", engine="thai2rom"), "banrai")
        self.assertEqual(romanize("สุนัข", engine="thai2rom"), "sunak")
        self.assertEqual(romanize("นก", engine="thai2rom"), "nok")
        self.assertEqual(romanize("ความอิ่ม", engine="thai2rom"), "khwam-im")
        self.assertEqual(
            romanize("กานต์ ณรงค์", engine="thai2rom"), "kan narong"
        )
        self.assertEqual(romanize("สกุนต์", engine="thai2rom"), "sakun")
        self.assertEqual(romanize("ชารินทร์", engine="thai2rom"), "charin")

    def test_romanize_thai2rom_onnx(self):
        self.assertEqual(romanize("แมว", engine="thai2rom_onnx"), "maeo")
        self.assertEqual(romanize("บ้านไร่", engine="thai2rom_onnx"), "banrai")
        self.assertEqual(romanize("สุนัข", engine="thai2rom_onnx"), "sunak")
        self.assertEqual(romanize("นก", engine="thai2rom_onnx"), "nok")
        self.assertEqual(
            romanize("ความอิ่ม", engine="thai2rom_onnx"), "khwam-im"
        )
        self.assertEqual(
            romanize("กานต์ ณรงค์", engine="thai2rom_onnx"), "kan narong"
        )
        self.assertEqual(romanize("สกุนต์", engine="thai2rom_onnx"), "sakun")
        self.assertEqual(
            romanize("ชารินทร์", engine="thai2rom_onnx"), "charin"
        )

    def test_romanize_lookup(self):
        # found in v1.4
        self.assertEqual(romanize("บอล", engine="lookup"), "ball")
        self.assertEqual(romanize("บอยแบนด์", engine="lookup"), "boyband")
        self.assertEqual(romanize("กาแล็กซี", engine="lookup"), "galaxy")
        self.assertEqual(romanize("กีย์เซอไรต์", engine="lookup"), "geyserite")
        self.assertEqual(romanize("พลีโอนาสต์", engine="lookup"), "pleonaste")
        self.assertEqual(
            romanize("คาราเมล คาปูชิโน่", engine="lookup"),
            "caramel cappuccino",
        )
        ## found individually, but needs tokenization
        self.assertEqual(
            romanize("คาราเมลคาปูชิโน่", engine="lookup"), "khanamenkhapuchino"
        )
        # not found in v1.4
        ## default fallback
        self.assertEqual(romanize("ภาพยนตร์", engine="lookup"), "phapn")
        self.assertEqual(romanize("แมว", engine="lookup"), "maeo")
        ## fallback = 'thai2rom'
        self.assertEqual(
            romanize("ความอิ่ม", engine="lookup", fallback_engine="thai2rom"),
            "khwam-im",
        )
        self.assertEqual(
            romanize("สามารถ", engine="lookup", fallback_engine="thai2rom"),
            "samat",
        )

    def test_thai2rom_prepare_sequence(self):
        transliterater = ThaiTransliterator()

        UNK_TOKEN = 1  # UNK_TOKEN or <UNK> is represented by 1
        END_TOKEN = 3  # END_TOKEN or <end> is represented by 3

        self.assertListEqual(
            transliterater._prepare_sequence_in("A")
            .cpu()
            .detach()
            .numpy()
            .tolist(),
            torch.tensor([UNK_TOKEN, END_TOKEN], dtype=torch.long)
            .cpu()
            .detach()
            .numpy()
            .tolist(),
        )

        self.assertListEqual(
            transliterater._prepare_sequence_in("♥")
            .cpu()
            .detach()
            .numpy()
            .tolist(),
            torch.tensor([UNK_TOKEN, END_TOKEN], dtype=torch.long)
            .cpu()
            .detach()
            .numpy()
            .tolist(),
        )

        self.assertNotEqual(
            transliterater._prepare_sequence_in("ก")
            .cpu()
            .detach()
            .numpy()
            .tolist(),
            torch.tensor([UNK_TOKEN, END_TOKEN], dtype=torch.long)
            .cpu()
            .detach()
            .numpy()
            .tolist(),
        )

    def test_thai2rom_onnx_prepare_sequence(self):
        transliterater = ThaiTransliterator_ONNX()

        UNK_TOKEN = 1  # UNK_TOKEN or <UNK> is represented by 1
        END_TOKEN = 3  # END_TOKEN or <end> is represented by 3

        self.assertListEqual(
            transliterater._prepare_sequence_in("A").tolist(),
            torch.tensor([UNK_TOKEN, END_TOKEN], dtype=torch.long)
            .cpu()
            .detach()
            .numpy()
            .tolist(),
        )

        self.assertListEqual(
            transliterater._prepare_sequence_in("♥").tolist(),
            torch.tensor([UNK_TOKEN, END_TOKEN], dtype=torch.long)
            .cpu()
            .detach()
            .numpy()
            .tolist(),
        )

        self.assertNotEqual(
            transliterater._prepare_sequence_in("ก").tolist(),
            torch.tensor([UNK_TOKEN, END_TOKEN], dtype=torch.long)
            .cpu()
            .detach()
            .numpy()
            .tolist(),
        )

    def test_transliterate(self):
        self.assertEqual(transliterate(""), "")
        self.assertEqual(transliterate("แมว", "pyicu"), "mæw")
        self.assertEqual(transliterate("คน", engine="ipa"), "kʰon")
        self.assertIsNotNone(transliterate("คน", engine="thaig2p"))
        self.assertIsNotNone(transliterate("แมว", engine="thaig2p"))
        self.assertIsNotNone(transliterate("คน", engine="tltk_g2p"))
        self.assertIsNotNone(transliterate("แมว", engine="tltk_g2p"))
        self.assertIsNotNone(transliterate("คน", engine="tltk_ipa"))
        self.assertIsNotNone(transliterate("แมว", engine="tltk_ipa"))
        self.assertIsNotNone(transliterate("คน", engine="iso_11940"))
        self.assertIsNotNone(transliterate("แมว", engine="iso_11940"))
        self.assertIsNotNone(trans_list("คน"))
        self.assertIsNotNone(xsampa_list("คน"))

    def test_transliterate_iso11940(self):
        self.assertEqual(
            transliterate("เชียงใหม่", engine="iso_11940"), "echīyngıh̄m̀"
        )
        self.assertEqual(
            transliterate("ภาษาไทย", engine="iso_11940"), "p̣hās̛̄āịthy"
        )

    def test_transliterate_wunsen(self):
        wt = WunsenTransliterate()
        self.assertEqual(wt.transliterate("ohayō", lang="jp"), "โอฮาโย")
        self.assertEqual(
            wt.transliterate(
                "ohayou", lang="jp", jp_input="Hepburn-no diacritic"
            ),
            "โอฮาโย",
        )
        self.assertEqual(
            wt.transliterate("ohayō", lang="jp", system="RI35"), "โอะฮะโย"
        )
        self.assertEqual(
            wt.transliterate("annyeonghaseyo", lang="ko"), "อันนย็องฮาเซโย"
        )
        self.assertEqual(wt.transliterate("xin chào", lang="vi"), "ซีน จ่าว")
        self.assertEqual(wt.transliterate("ni3 hao3", lang="zh"), "หนี เห่า")
        self.assertEqual(
            wt.transliterate("ni3 hao3", lang="zh", zh_sandhi=False),
            "หนี่ เห่า",
        )
        self.assertEqual(
            wt.transliterate("ni3 hao3", lang="zh", system="RI49"), "หนี ห่าว"
        )
        with self.assertRaises(NotImplementedError):
            wt.transliterate("xin chào", lang="vii")

    def test_pronunciate(self):
        self.assertEqual(pronunciate(""), "")
        remove("thai_w2p")
        self.assertIsNotNone(pronunciate("คน", engine="w2p"))
        self.assertIsNotNone(pronunciate("แมว", engine="w2p"))
        self.assertIsNotNone(pronunciate("มข.", engine="w2p"))
        self.assertIsNotNone(pronunciate("มช.", engine="w2p"))
        self.assertIsNotNone(pronunciate("jks", engine="w2p"))

    def test_puan(self):
        self.assertEqual(puan("แมว"), "แมว")
        self.assertEqual(puan("นาริน"), "นิน-รา")
        self.assertEqual(puan("นาริน", show_pronunciation=False), "นินรา")
        self.assertEqual(
            puan("การทำความดี", show_pronunciation=False), "ดานทำความกี"
        )
