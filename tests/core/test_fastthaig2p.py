# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

import tempfile
import unittest
from pathlib import Path

from pythainlp.transliterate import FastThaiG2P, transliterate
from pythainlp.transliterate.fastthaig2p import (
    fallback_g2p,
    normalize,
    transliterate as fastthaig2p_transliterate,
)


class FastThaiG2PTestCase(unittest.TestCase):
    def test_normalize_plain_thai(self):
        self.assertEqual(normalize("สวัสดีครับ"), "สวัสดีครับ")

    def test_normalize_quantity(self):
        self.assertEqual(normalize("มี 42 คน"), "มี สี่สิบสอง คน")

    def test_normalize_large_number(self):
        self.assertEqual(
            normalize("1234567890"),
            "หนึ่งสองสามสี่ห้าหกเจ็ดแปดเก้าศูนย์",
        )

    def test_normalize_comma_number(self):
        self.assertEqual(normalize("1,000,000"), "หนึ่งล้าน")

    def test_normalize_decimal(self):
        self.assertEqual(normalize("3.14"), "สามจุดหนึ่งสี่")

    def test_normalize_thai_numerals(self):
        self.assertIn("สองพันห้าร้อยหกสิบเก้า", normalize("๒๕๖๙"))

    def test_normalize_phone_number(self):
        result = normalize("081-234-5678")
        self.assertIn("ศูนย์แปดหนึ่ง", result)
        self.assertIn("ห้าหกเจ็ดแปด", result)

    def test_normalize_alphanum_id(self):
        result = normalize("ORD-001")
        self.assertIn("โอ", result)
        self.assertIn("ศูนย์ศูนย์หนึ่ง", result)

    def test_normalize_abbreviations(self):
        self.assertIn("มกราคม", normalize("ม.ค."))
        self.assertIn("พุทธศักราช", normalize("พ.ศ."))
        self.assertIn("ด็อกเตอร์", normalize("ดร."))

    def test_normalize_mai_yamok(self):
        self.assertEqual(normalize("เด็กๆ"), "เด็กเด็ก")

    def test_normalize_symbols_and_units(self):
        self.assertIn("เปอร์เซ็นต์", normalize("50%"))
        self.assertIn("องศาเซลเซียส", normalize("30°C"))
        self.assertIn("กิโลกรัม", normalize("5 kg"))

    def test_normalize_time(self):
        self.assertEqual(normalize("8:00 น."), "แปดนาฬิกา")

    def test_normalize_email(self):
        result = normalize("somchai@gmail.com")
        self.assertIn("จีเมล", result)
        self.assertIn("แอท", result)

    def test_normalize_empty_and_invalid(self):
        self.assertEqual(normalize(""), "")
        self.assertEqual(normalize(None), "")  # type: ignore[arg-type]
        self.assertEqual(normalize(123), "")  # type: ignore[arg-type]

    def test_g2p_known_word(self):
        g2p = FastThaiG2P()
        result = g2p.convert("กิน")
        self.assertIn("/kin˧/", result)

    def test_g2p_multi_word_sentence(self):
        g2p = FastThaiG2P()
        result = g2p.convert("ไปกินข้าว")
        self.assertIn("/paj˧/", result)
        self.assertIn("kʰaːw˥˩", result)

    def test_g2p_number_normalized(self):
        g2p = FastThaiG2P()
        result = g2p.convert("มี 3 คน")
        self.assertNotIn("3", result)

    def test_g2p_abbreviation_expanded(self):
        g2p = FastThaiG2P()
        result = g2p.convert("ม.ค.")
        self.assertNotIn("ม.ค.", result)

    def test_g2p_empty_string(self):
        g2p = FastThaiG2P()
        self.assertEqual(g2p.convert(""), "")
        self.assertEqual(g2p.convert(None), "")  # type: ignore[arg-type]

    def test_g2p_oov_fallback(self):
        g2p = FastThaiG2P()
        result = g2p.convert("สตาร์บัคส์")
        self.assertTrue("สตาร์บัคส์" in result or "/" in result)

    def test_fallback_g2p_function(self):
        self.assertEqual(fallback_g2p(""), "")
        self.assertEqual(fallback_g2p(None), "")  # type: ignore[arg-type]
        res = fallback_g2p("คริปโต")
        self.assertIsNotNone(res)

    def test_transliterate_integration(self):
        result = transliterate("สวัสดีครับ", engine="fastthaig2p")
        self.assertEqual(result, "/sa˨˩.wat̚˨˩.diː˧/ /kʰrap̚˦˥/")

    def test_module_transliterate(self):
        result = fastthaig2p_transliterate("สวัสดีครับ")
        self.assertEqual(result, "/sa˨˩.wat̚˨˩.diː˧/ /kʰrap̚˦˥/")

    def test_custom_ipa_dict(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        ) as f:
            f.write("{\"ทดสอบ\": \"/tʰot̚˦˥.sɔːp̚˨˩/\"}")
            tmp_path = f.name

        try:
            g2p = FastThaiG2P(ipa_dict_path=tmp_path)
            self.assertEqual(g2p.convert("ทดสอบ"), "/tʰot̚˦˥.sɔːp̚˨˩/")
        finally:
            Path(tmp_path).unlink(missing_ok=True)
