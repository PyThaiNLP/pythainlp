# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""
Characterization tests for pythainlp.transliterate.wiktionary.

Expected values were recorded from the implementation before refactoring.
"""

import unittest

from pythainlp.transliterate.wiktionary import (
    _apply_ho_rule,
    transliterate_wiktionary,
)

# (text, mode, expected output) recorded from the original code
CASES: tuple[tuple[str, str, str], ...] = (
    ("ถ๊ว-แมีย…กรรม", "royin", "thว-mแีย…kam"),
    ("หว๊วฑล–หฺณัวะ", "paiboon", "hwúuatl–หฺณัวะ"),
    ("แส็ ใขำ่ศ่ือบฒ๙", "ipa", "sแ็˨˩.ใขำ่ศ่ือบฒ9"),
    ("แกล(เฆฺว̄ัว", "ipa", "kɛːl˧(เฆฺว̄ัว"),
    ("แถรร–วฺรึย)เธาฏ", "royin", "thrแร–wruei)thaot"),
    ("", "xx", ""),
    ("ถ๊ว-แมีย…กรรม", "ipa", "tʰว˦˥.mแีย˦˥…kam˧"),
    ("ถ๊ว-แมีย…กรรม", "paiboon", "tว-mแีย…gam"),
    ("หว๊วฑล–หฺณัวะ", "ipa", "hwua̯t̚l˦˥.หฺณัวะ"),
    ("หว๊วฑล–หฺณัวะ", "royin", "hwuatl–หฺณัวะ"),
    ("แส็ ใขำ่ศ่ือบฒ๙", "royin", "sแ็ ใขำ่ศ่ือบฒ9"),
    ("แส็ ใขำ่ศ่ือบฒ๙", "paiboon", "sแ็ ใขำ่ศ่ือบฒ9"),
    ("แกล(เฆฺว̄ัว", "royin", "kael(เฆฺว̄ัว"),
    ("แกล(เฆฺว̄ัว", "paiboon", "gɛɛl(เฆฺว̄ัว"),
    ("แถรร–วฺรึย)เธาฏ", "ipa", "tʰrแร˨˩.wrɯj˦˥)tʰawt̚˧"),
    ("แถรร–วฺรึย)เธาฏ", "paiboon", "trแร–wrʉi)taot"),
    ("", "ipa", ""),
    ("", "royin", ""),
    ("", "paiboon", ""),
    ("ไศฺลอยฏบบอะๆ", "ipa", "ไศฺลอยฏบบอะๆ"),
    ("ไศาว่", "royin", "ไศาว่"),
    ("ตูย้พษฯแมวๆใว๊ัวตค", "ipa", "ตูย้พษฯแมวๆใว๊ัวตค"),
    ("หฺพ่อฌ", "royin", "หฺพ่อฌ"),
    ("ใฎฺวียะษฎ๊ เหฺธฺรู̄ก็", "ipa", "ใฎฺวียะษฎ๊.เหฺธฺรู̄ก็"),
    ("ครับ เนวพ.", "ipa", "kʰrap̚˦˥.nweːp̚˥˩."),
    ("แษาวๅหญี้ท$ngหฺฉือะ$ng", "paiboon", "แษาวๅหญี้ท$ngหฺฉือะ$ng"),
    ("แมวฯแฅฺลิว", "royin", "แมวฯแฅฺลิว"),
    ("ไป̄ะ\nหฺหร็อย๊ณ", "ipa", "pไะ˧\nหฺหร็อย๊ณ"),
    ("ฆ็รaเถุย̄ใญีว่ๅ", "royin", "kh็รaเถุย̄ใญีว่ๅ"),
    ("แจัว่ฯลฯ", "royin", "แจัว่ฯลฯ"),
    ("เผลีย้๒ไหฺฒล๊ยคโปะ้ส๑", "ipa", "เผลีย้2ไหฺฒล๊ยคโปะ้ส1"),
    ("ดวย้…หฺหี๊สล๒", "paiboon", "ดวย้…หฺหี๊สล2"),
    ("ไหล็อ", "royin", "hlไ็อ"),
    ("แค่", "ipa", "kʰɛː˥˩"),
    ("หฺควยฯลฯโธีว๋ฑฦหฺบ็ส๒", "paiboon", "หฺควยฯลฯโธีว๋ฑฦหฺบ็ส2"),
    ("แหฺข๋เทธหญฺวู๋ยฌ๊ภ(", "royin", "แหฺข๋เทธหญฺวู๋ยฌ๊ภ("),
    ("หฺฝุ๋ยฐ$ng", "ipa", "หฺฝุ๋ยฐ$ng"),
    ("โหฺธ็̄๑", "ipa", "โหฺธ็̄1"),
    ("น้ำ)ฐรอ๙ใหยัยช๙", "ipa", "nam˦˥)ฐรอ9ใหยัยช9"),
    ("ชอฐaขย̄", "ipa", "t͡ɕʰɔːt̚˥˩aขย̄"),
    ("ใหฺลอะรร๑โฎำ่", "royin", "ใหฺลอะรร1โฎำ่"),
    ("ลฺวฬ๙เบุยมประชา", "paiboon", "ลฺวฬ9เบุยมประชา"),
    ("ไขา๙หรือ่ฆข๙หวฺรีล", "paiboon", "ไขา9หรือ่ฆข9หวฺรีล"),
    ("สึ̄", "paiboon", "sʉ"),
    ("หน้ิ็ฯลฯเหวัวะ๙ครับ-", "paiboon", "หน้ิ็ฯลฯเหวัวะ9ครับ-"),
    ("ใต๋ัวะหวว̄ิaเอฺล็อยส", "ipa", "ใต๋ัวะหวว̄ิaʔlเ็อยs˨˩"),
    ("ห้าวหญฺล้ร๑ใหฺฎวฃ", "ipa", "ห้าวหญฺล้ร1ใหฺฎวฃ"),
    ("ไหฺกฺว๊เใขฺุให็ณฺ", "royin", "ไหฺกฺว๊เใขฺุให็ณฺ"),
    ("ครับ๒", "paiboon", "ครับ2"),
    ("โลเอ)ธายฆต กรรม.", "royin", "โลเอ)thายkt kam."),
    ("เชฺระด", "paiboon", "chrเะt"),
    ("โฒู๊ฯ", "ipa", "โฒู๊ฯ"),
    ("เฐียะ้ถฏ๙มฺล̄ย…แย็้ฏษ", "paiboon", "เฐียะ้ถฏ9มฺล̄ย…yɛ́tt"),
    ("เตัวaวฺวายภ๑โฅลำง", "paiboon", "dtเัวaวฺวายภ1โฅลำง"),
    ("ขิว̄ศ ไฒ็อย)เหงรูย๋พ", "paiboon", "ขิว̄ศ tไ็อย)เหงรูย๋พ"),
    ("โฮ̄@โหฺท๊็นฏ\n", "royin", "ho-โหฺท๊็นฏ\n"),
    ("ให๊อะฑ-สฺร๊ยใฝฺร้ำฯ", "paiboon", "hใอะt-สฺร๊ยใฝฺร้ำฯ"),
    ("ฒะ๊ศ๑", "ipa", "ฒะ๊ศ1"),
    ("แจุ้$ng", "royin", "chแุng"),
    ("หร๊วยร(พ̄ิ็ๆแซว๋ฤ", "ipa", "hrวยn˦˥(พ̄ิ็ๆแซว๋ฤ"),
    ("อรรแข่าฟฃ๑", "royin", "อรรแข่าฟฃ1"),
    ("แหร๊ษ", "royin", "hraet"),
    ("ไอ่าวญ", "royin", "ไาวn"),
    ("แพับโนรร.ธว่เอฐพ๙", "ipa", "แพับโนรร.ธว่เอฐพ9"),
    ("หล๋อยฏสวัสดี-", "ipa", "หล๋อยฏสวัสดี."),
    ("โฆ่อย)ปายล๒ฝ้ำ", "paiboon", "kโอย)ปายล2ฝ้ำ"),
    ("ฟ้็อย๒ใมิว̄จ", "paiboon", "ฟ้็อย2ใมิว̄จ"),
    ("ใหว๊ิวดฺรูย̄สนฤใหยลอ๊๒", "paiboon", "ใหว๊ิวดฺรูย̄สนฤใหยลอ๊2"),
    ("ครับ$ngแษียฑ", "ipa", "kʰrap̚˦˥$ngsแียt̚˨˩"),
    ("ฟ่ย", "ipa", "fย˥˩"),
    ("ไภู๋ยๅไหฺตอย)แฐ็อลๆ", "ipa", "ไภู๋ยๅไหฺตอย)แฐ็อลๆ"),
    ("ในรรตฺรือะ้ฤ๒", "royin", "ในรรตฺรือะ้ฤ2"),
    ("โว̄อะต\n", "paiboon", "wโอะt\n"),
    ("แช๋ิศ๙ธ๊าฑ๒", "paiboon", "แช๋ิศ9ธ๊าฑ2"),
    ("ไจัถโลุล-ด๋รฑ๑", "royin", "ไจัถโลุล-ด๋รฑ1"),
    ("พวสณ", "royin", "phuasn"),
    ("กรรม๙", "paiboon", "กรรม9"),
    ("แฬวียหะ๑โญัย้น", "royin", "แฬวียหะ1โญัย้น"),
    ("เฎเอ้๒", "royin", "เฎเอ้2"),
    ("หราช ", "ipa", "hraːt͡ɕʰ˨˩."),
    ("ไพู๋ฦใณัว(", "royin", "ไพู๋ฦใณัว("),
    ("ฅ้", "royin", "kha"),
    ("มฺวาวฟ๒", "ipa", "มฺวาวฟ2"),
    ("ฟฺร̄ยณ)โทเฺ", "royin", "frยn)โทเฺ"),
    ("แฟฺรุยฟศ@แพ๋าๆ", "paiboon", "frแุยft@แพ๋าๆ"),
    ("เญฺวูส๒", "paiboon", "เญฺวูส2"),
    ("ถะ่หนู๋", "royin", "ถะ่หนู๋"),
    ("หฺฟาก็ใฬำฎ๙", "paiboon", "หฺฟาก็ใฬำฎ9"),
    ("ไหยัฏฃ๒หมา", "royin", "ไหยัฏฃ2หมา"),
    ("โพล๊ายฤโลว็๊ดฒ๒ใฌุย่ฃๅ", "ipa", "โพล๊ายฤโลว็๊ดฒ2ใฌุย่ฃๅ"),
    ("หฺรำ่ ไฅุย่ธ๒", "paiboon", "หฺรำ่ ไฅุย่ธ2"),
    ("แหญ่ึตฬือะษ…เฐฺล̄ำฑ", "royin", "แหญ่ึตฬือะษ…thlเำt"),
    ("แศ๊ว(", "ipa", "sɛːw˦˥("),
    ("หลฺรึยฆ(โผู่@ครับ…", "paiboon", "หลฺรึยฆ(โผู่@kráp…"),
    ("กุ๋ย", "royin", "กุ๋ย"),
    ("โย๋ำ(", "paiboon", "yโำ("),
    ("โฟ้าว", "paiboon", "fโาว"),
    ("เหนูยฐป๒โง่ว๙", "ipa", "เหนูยฐป2โง่ว9"),
    ("ฆึชส\nหู๊บ)", "ipa", "kʰɯt͡ɕʰs˦˥\nหู๊บ)"),
    ("แตฺว็อ", "paiboon", "dtwแ็อ"),
    ("แขัวฑ", "paiboon", "kแัวt"),
    ("ครับ-เฐือะก็เฏ๊ิภฌ", "royin", "khrap-เฐือะก็เฏ๊ิภฌ"),
    ("ฮฺล̄วยคษ$ngหวอยธฎ\n", "paiboon", "hlวยkt$nghwอยtt\n"),
    ("เษ๊ือฏ…โง้ำ$ngญาว่", "ipa", "เษ๊ือฏ…ŋโำ˦˥$ngญาว่"),
    ("แมว", "royin", "maeo"),
    ("รรกรรม๑ดรีวฆ ", "paiboon", "รรกรรม1ดรีวฆ "),
    ("ฑ่ัฌท๒เฮย้ฯแฆ้ัล…", "royin", "ฑ่ัฌท2เฮย้ฯแฆ้ัล…"),
    ("เฃู๊…ฤโฎริ็คฯ", "royin", "khเู…ฤโฎริ็คฯ"),
    ("ใษุย", "royin", "sใุย"),
    ("ไฃฺวา้ญรร๑โฮฺรือๆ", "ipa", "ไฃฺวา้ญรร1โฮฺรือๆ"),
    ("ไตะฅ", "paiboon", "dtไะk"),
    ("ใกีย)ฆุ)ฝลึย̄", "royin", "kใีย)khu)ฝลึย̄"),
    ("ฑูย.โมาว–ซวยร–", "royin", "thui.mโาว–swยร–"),
    ("หม้รรฎรา$ngใหญฺลียะพ๑", "ipa", "หม้รรฎรา$ngใหญฺลียะพ1"),
    ("แษรีวท", "paiboon", "srแีวt"),
    ("ว้ฏ)ใหญาย๊รเหงลอยฌๆ", "paiboon", "wót)ใหญาย๊รเหงลอยฌๆ"),
    ("แธะ-", "ipa", "tʰɛʔ˦˥."),
    ("งือฆ$ng", "royin", "ngือkng"),
    ("โบวคด", "paiboon", "bwòokt"),
    ("โอ̄ัวศ๑โฉ̄ะฎเก็", "royin", "โอ̄ัวศ1โฉ̄ะฎเก็"),
    ("ฑลวคโฌี̄ชภใหะณ๑", "paiboon", "ฑลวคโฌี̄ชภใหะณ1"),
    ("แขัยตไภ่ึฎ๙แน่ยบ\n", "royin", "แขัยตไภ่ึฎ9แน่ยบ\n"),
    ("ฬย(เฮิวแธิพฯ", "ipa", "lย˦˥(เฮิวแธิพฯ"),
    ("ไป่อยร-คฺล็อธ", "royin", "pไอยn-khlot"),
    ("ไภือะฒ๒ใย่ิเษ็อย", "paiboon", "ไภือะฒ2ใย่ิเษ็อย"),
    ("เอิว", "ipa", "ʔเิว˨˩"),
    ("abc", "ipa", "abc"),
    ("abc", "royin", "abc"),
    ("abc", "paiboon", "abc"),
    ("@", "ipa", "@"),
    ("@", "royin", ""),
    ("@", "paiboon", "@"),
    ("$ng", "ipa", "$ng"),
    ("$ng", "royin", "ng"),
    ("$ng", "paiboon", "$ng"),
    ("ก@ข", "ipa", "ka˨˩@kʰaʔ˨˩"),
    ("ก@ข", "royin", "ka-kha"),
    ("ก@ข", "paiboon", "gà@kà"),
    ("ง$ng.", "ipa", "ŋa˦˥$ng."),
    ("ง$ng.", "royin", "nga-ng."),
    ("ง$ng.", "paiboon", "ngá$ng."),
    ("น$ngา", "ipa", "na˦˥$ngา"),
    ("น$ngา", "royin", "na-ngา"),
    ("น$ngา", "paiboon", "ná$ngา"),
    ("ก-ข", "ipa", "ka˨˩.kʰaʔ˨˩"),
    ("ก-ข", "royin", "ka-kha"),
    ("ก-ข", "paiboon", "gà-kà"),
    ("๑๒๓", "ipa", "123"),
    ("๑๒๓", "royin", "123"),
    ("๑๒๓", "paiboon", "123"),
    ("แมว๑", "ipa", "แมว1"),
    ("แมว๑", "royin", "แมว1"),
    ("แมว๑", "paiboon", "แมว1"),
    ("ก̄", "ipa", "kaʔ˧"),
    ("ก̄", "royin", "ka"),
    ("ก̄", "paiboon", "ga"),
    ("น้ำ ใจ", "ipa", "nam˦˥.t͡ɕaj˧"),
    ("น้ำ ใจ", "royin", "nam chai"),
    ("น้ำ ใจ", "paiboon", "nám jai"),
    ("ดาว ดาว", "ipa", "daːw˧.daːw˧"),
    ("ดาว ดาว", "royin", "dao dao"),
    ("ดาว ดาว", "paiboon", "daao daao"),
    ("แมว", "xx", "แมว"),
    ("ก", "", "ก"),
)


class WiktionaryCharacterizationTestCase(unittest.TestCase):
    def test_golden_cases(self):
        for text, mode, expected in CASES:
            with self.subTest(text=text, mode=mode):
                self.assertEqual(
                    transliterate_wiktionary(text, mode), expected
                )

    def test_default_mode_is_ipa(self):
        self.assertEqual(
            transliterate_wiktionary("แมว"),
            transliterate_wiktionary("แมว", mode="ipa"),
        )

    def test_unsupported_mode_returns_input(self):
        self.assertEqual(transliterate_wiktionary("แมว", "xx"), "แมว")

    def test_wrong_type_text(self):
        with self.assertRaises(TypeError):
            transliterate_wiktionary(None)  # type: ignore[arg-type]

    # BUG-LEDGER: wiktionary-ho-rule-unreachable
    def test_ho_rule_is_never_reached(self):
        # The syllable patterns capture the initial as one character or as
        # three (หฺ plus a consonant), so the two-character HO HIP rule
        # never applies. The helper itself works when called directly.
        for args, expected in (
            (("หย", "", "", "น"), ("ห", "", "ย", "น")),
            (("หร", "", "", "ม"), ("หร", "", "", "ม")),
            (("หร", "", "ย", ""), ("ห", "ร", "ย", "")),
            (("หก", "", "า", ""), ("หก", "", "า", "")),
            (("ก", "ร", "า", "ง"), ("ก", "ร", "า", "ง")),
        ):
            with self.subTest(args=args):
                self.assertEqual(_apply_ho_rule(*args), expected)


if __name__ == "__main__":
    unittest.main()
