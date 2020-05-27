# -*- coding: utf-8 -*-

import unittest

import torch
from pythainlp.transliterate import romanize, transliterate
from pythainlp.transliterate.ipa import trans_list, xsampa_list
from pythainlp.transliterate.thai2rom import ThaiTransliterator

_BASIC_TESTS = {
    None: "",
    "": "",
    "หมอก": "mok",
    "หาย": "hai",
    "แมว": "maeo",
    "เดือน": "duean",
    "ดำ": "dam",
    "ดู": "du",
    "บัว": "bua",
    "กก": "kok",
    "กร": "kon",
    "กรร": "kan",
    "กรรม": "kam",
    # "กรม": "krom",  # failed
    "ฝ้าย": "fai",
    "นพพร": "nopphon",
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

    def test_romanize_royin_basic(self):
        for word in _BASIC_TESTS:
            expect = _BASIC_TESTS[word]
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

    def test_transliterate(self):
        self.assertEqual(transliterate(""), "")
        self.assertEqual(transliterate("แมว", "pyicu"), "mæw")
        self.assertEqual(transliterate("คน", engine="ipa"), "kʰon")
        self.assertIsNotNone(transliterate("คน", engine="thaig2p"))
        self.assertIsNotNone(transliterate("แมว", engine="thaig2p"))
        self.assertIsNotNone(trans_list("คน"))
        self.assertIsNotNone(xsampa_list("คน"))
