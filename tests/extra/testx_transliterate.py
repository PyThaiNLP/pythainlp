# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

import unittest

import torch

from pythainlp.corpus import remove
from pythainlp.transliterate import (
    lookup,
    pronunciate,
    puan,
    romanize,
    thai2rom,
    thaig2p,
    transliterate,
)
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
            romanize("กานต์ ณรงค์", engine="thai2rom_onnx"), "kan narang"
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

    def test_thai2rom_unsupported_attention_method_raises_value_error(self):
        attn = thai2rom.Attn(method="unsupported", hidden_size=4)
        hidden = torch.randn(1, 1, 4)
        encoder_outputs = torch.randn(1, 2, 4)
        mask = torch.ones(1, 2, dtype=torch.bool)

        with self.assertRaisesRegex(ValueError, "Unsupported attention method"):
            attn(hidden, encoder_outputs, mask)

    def test_thai2rom_seq2seq_hidden_mismatch_raises_value_error(self):
        encoder = thai2rom.Encoder(
            vocabulary_size=16,
            embedding_size=8,
            hidden_size=8,
            dropout=0.0,
        )
        decoder = thai2rom.AttentionDecoder(
            vocabulary_size=16,
            embedding_size=8,
            hidden_size=10,
            dropout=0.0,
        )

        with self.assertRaisesRegex(
            ValueError, "Encoder and decoder hidden sizes must match"
        ):
            thai2rom.Seq2Seq(encoder, decoder, 2, 3, 10)

    def test_thai2rom_seq2seq_inference_teacher_forcing_raises_value_error(self):
        encoder = thai2rom.Encoder(
            vocabulary_size=16,
            embedding_size=8,
            hidden_size=8,
            dropout=0.0,
        )
        decoder = thai2rom.AttentionDecoder(
            vocabulary_size=16,
            embedding_size=8,
            hidden_size=8,
            dropout=0.0,
        )
        network = thai2rom.Seq2Seq(encoder, decoder, 2, 3, 10)

        with self.assertRaisesRegex(
            ValueError, "teacher_forcing_ratio must be zero during inference"
        ):
            network(
                torch.tensor([[1, 2, 0]], dtype=torch.long),
                torch.tensor([2], dtype=torch.int),
                None,
                teacher_forcing_ratio=0.5,
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

    def test_thaig2p_unsupported_attention_method_raises_value_error(self):
        attn = thaig2p.Attn(method="unsupported", hidden_size=4)
        hidden = torch.randn(1, 1, 4)
        encoder_outputs = torch.randn(1, 2, 4)
        mask = torch.ones(1, 2, dtype=torch.bool)

        with self.assertRaisesRegex(ValueError, "Unsupported attention method"):
            attn(hidden, encoder_outputs, mask)

    def test_thaig2p_seq2seq_hidden_mismatch_raises_value_error(self):
        encoder = thaig2p.Encoder(
            vocabulary_size=16,
            embedding_size=8,
            hidden_size=8,
            dropout=0.0,
        )
        decoder = thaig2p.AttentionDecoder(
            vocabulary_size=16,
            embedding_size=8,
            hidden_size=10,
            dropout=0.0,
        )

        with self.assertRaisesRegex(
            ValueError, "Encoder and decoder hidden sizes must match"
        ):
            thaig2p.Seq2Seq(encoder, decoder, 2, 3, 10)

    def test_thaig2p_seq2seq_inference_teacher_forcing_raises_value_error(self):
        encoder = thaig2p.Encoder(
            vocabulary_size=16,
            embedding_size=8,
            hidden_size=8,
            dropout=0.0,
        )
        decoder = thaig2p.AttentionDecoder(
            vocabulary_size=16,
            embedding_size=8,
            hidden_size=8,
            dropout=0.0,
        )
        network = thaig2p.Seq2Seq(encoder, decoder, 2, 3, 10)

        with self.assertRaisesRegex(
            ValueError, "teacher_forcing_ratio must be zero during inference"
        ):
            network(
                torch.tensor([[1, 2, 0]], dtype=torch.long),
                [2],
                None,
                teacher_forcing_ratio=0.5,
            )

    def test_lookup_non_callable_fallback_raises_type_error(self):
        with self.assertRaisesRegex(
            TypeError, "`fallback_engine` is not callable"
        ):
            lookup.romanize("___", fallback_func="not-callable")  # type: ignore[arg-type]

    def test_transliterate(self):
        self.assertEqual(transliterate("แมว", "pyicu"), "mæw")
        self.assertEqual(transliterate("คน", engine="ipa"), "kʰon")
        self.assertIsNotNone(transliterate("คน", engine="thaig2p"))
        self.assertIsNotNone(transliterate("แมว", engine="thaig2p"))
        self.assertIsNotNone(transliterate("คน", engine="thaig2p_v2"))
        self.assertIsNotNone(transliterate("แมว", engine="thaig2p_v2"))
        self.assertIsNotNone(transliterate("คน", engine="thaig2p_v3"))
        self.assertIsNotNone(transliterate("แมว", engine="thaig2p_v3"))
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
