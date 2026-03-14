# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

import os
import unittest
import warnings
from unittest.mock import patch

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
        # Test for character ฅ (issue: Transliterator cannot handle ฅ)
        self.assertIsNotNone(romanize("ภาษาไวคาลีฅ", engine="tltk"))

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
        # Test for character ฅ (issue: Transliterator cannot handle ฅ)
        self.assertIsNotNone(transliterate("ภาษาไวคาลีฅ", engine="tltk_g2p"))
        self.assertIsNotNone(transliterate("ภาษาไวคาลีฅ", engine="tltk_ipa"))

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
        with patch.dict(os.environ, {"PYTHAINLP_ALLOW_UNSAFE_PICKLE": "1"}):
            with warnings.catch_warnings(record=True):
                warnings.simplefilter("always")
                self.assertIsNotNone(pronunciate("คน", engine="w2p"))
                self.assertIsNotNone(pronunciate("แมว", engine="w2p"))
                self.assertIsNotNone(pronunciate("มข.", engine="w2p"))
                self.assertIsNotNone(pronunciate("มช.", engine="w2p"))
                self.assertIsNotNone(pronunciate("jks", engine="w2p"))

    def test_pronunciate_w2p_pickle_blocked_by_default(self):
        """Thai_W2P._load_variables must raise RuntimeError for a legacy .npy
        corpus when PYTHAINLP_ALLOW_UNSAFE_PICKLE is not set.
        """
        try:
            from pythainlp.transliterate.w2p import Thai_W2P
        except (FileNotFoundError, RuntimeError):
            self.skipTest("w2p module not ready (corpus missing or pickle blocked)")

        instance = object.__new__(Thai_W2P)
        instance.checkpoint = "/fake/model.npy"
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("PYTHAINLP_ALLOW_UNSAFE_PICKLE", None)
            with self.assertRaises(RuntimeError) as ctx:
                instance._load_variables()
            self.assertIn("PYTHAINLP_ALLOW_UNSAFE_PICKLE", str(ctx.exception))

    def test_pronunciate_w2p_pickle_warning_when_allowed(self):
        """Thai_W2P._load_variables must emit a UserWarning when loading a
        legacy .npy corpus with PYTHAINLP_ALLOW_UNSAFE_PICKLE set.
        """
        import numpy as np

        try:
            from pythainlp.transliterate.w2p import Thai_W2P
        except (FileNotFoundError, RuntimeError):
            self.skipTest("w2p module not ready (corpus missing or pickle blocked)")

        keys = [
            "encoder.emb.weight",
            "encoder.rnn.weight_ih_l0",
            "encoder.rnn.weight_hh_l0",
            "encoder.rnn.bias_ih_l0",
            "encoder.rnn.bias_hh_l0",
            "decoder.emb.weight",
            "decoder.rnn.weight_ih_l0",
            "decoder.rnn.weight_hh_l0",
            "decoder.rnn.bias_ih_l0",
            "decoder.rnn.bias_hh_l0",
            "decoder.fc.weight",
            "decoder.fc.bias",
        ]
        fake_weights = {k: np.zeros(1) for k in keys}
        fake_array = np.empty((), dtype=object)
        fake_array[()] = fake_weights

        instance = object.__new__(Thai_W2P)
        instance.checkpoint = "/fake/model.npy"
        with patch.dict(os.environ, {"PYTHAINLP_ALLOW_UNSAFE_PICKLE": "1"}):
            with patch("numpy.load", return_value=fake_array):
                with warnings.catch_warnings(record=True) as w:
                    warnings.simplefilter("always")
                    instance._load_variables()
                user_warnings = [
                    x for x in w if issubclass(x.category, UserWarning)
                ]
                self.assertTrue(
                    any(
                        "PYTHAINLP_ALLOW_UNSAFE_PICKLE" in str(x.message)
                        for x in user_warnings
                    ),
                    "Expected a UserWarning mentioning PYTHAINLP_ALLOW_UNSAFE_PICKLE",
                )

    def test_puan(self):
        self.assertEqual(puan("แมว"), "แมว")
        self.assertEqual(puan("นาริน"), "นิน-รา")
        self.assertEqual(puan("นาริน", show_pronunciation=False), "นินรา")
        self.assertEqual(
            puan("การทำความดี", show_pronunciation=False), "ดานทำความกี"
        )
