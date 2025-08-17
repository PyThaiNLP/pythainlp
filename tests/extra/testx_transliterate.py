# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2025 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

import unittest

import torch

from pythainlp.corpus import remove
from pythainlp.transliterate import pronunciate, puan, romanize, transliterate
from pythainlp.transliterate.ipa import trans_list, xsampa_list
from pythainlp.transliterate.thai2rom import ThaiTransliterator
from pythainlp.transliterate.thai2rom_onnx import ThaiTransliterator_ONNX
from pythainlp.transliterate.wunsen import WunsenTransliterate


class TransliterateTestCaseX(unittest.TestCase):
    def test_romanize(self):
        self.assertEqual(romanize("แมว", engine="tltk"), "maeo")

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
        self.assertEqual(romanize("ชารินทร์", engine="thai2rom_onnx"), "charin")

    def test_romanize_lookup(self):
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
        self.assertEqual(transliterate("แมว", "pyicu"), "mæw")
        self.assertEqual(transliterate("คน", engine="ipa"), "kʰon")
        self.assertIsNotNone(transliterate("คน", engine="thaig2p"))
        self.assertIsNotNone(transliterate("แมว", engine="thaig2p"))
        self.assertIsNotNone(transliterate("คน", engine="thaig2p_v2"))
        self.assertIsNotNone(transliterate("แมว", engine="thaig2p_v2"))
        self.assertIsNotNone(transliterate("คน", engine="umt5_thaig2p"))
        self.assertIsNotNone(transliterate("แมว", engine="umt5_thaig2p"))
        self.assertIsNotNone(transliterate("คน", engine="tltk_g2p"))
        self.assertIsNotNone(transliterate("แมว", engine="tltk_g2p"))
        self.assertIsNotNone(transliterate("คน", engine="tltk_ipa"))
        self.assertIsNotNone(transliterate("แมว", engine="tltk_ipa"))

        self.assertIsNotNone(trans_list("คน"))
        self.assertIsNotNone(xsampa_list("คน"))

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
