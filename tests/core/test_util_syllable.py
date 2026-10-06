# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Characterization tests for pythainlp.util.syllable.

Golden values were recorded from the pre-refactor implementation.
Known bugs are pinned on purpose (see working-docs/ROADMAP.md).
"""

from __future__ import annotations

import hashlib
import unittest
from typing import TYPE_CHECKING, Callable

from pythainlp import thai_consonants
from pythainlp.util.syllable import (
    sound_syllable,
    syllable_length,
    syllable_open_close_detector,
    thai_consonants_all,
    tone_detector,
)

if TYPE_CHECKING:
    from collections.abc import Iterator

# (syllable, sound_syllable result, tone_detector result);
# "!Name" means that the exception type Name is raised.
GOLDEN: list[tuple[str, str, str]] = [
    ("", "dead", ""),
    ("ก", "dead", "l"),
    ("อ", "dead", "l"),
    ("ฤ", "dead", ""),
    ("ฤๅ", "!IndexError", "!IndexError"),
    ("เอะ", "live", "m"),
    ("เอ", "live", "m"),
    ("เอา", "live", "m"),
    ("อา", "live", "m"),
    ("ฦ", "dead", ""),
    ("ฦๅ", "!IndexError", "!IndexError"),
    ("เ", "dead", ""),
    ("ะ", "dead", ""),
    ("เะ", "!IndexError", "!IndexError"),
    ("กก", "dead", "l"),
    ("a", "dead", ""),
    ("มา ", "live", "m"),
    ("เมาะ", "dead", "h"),
    ("เกาะ", "dead", "l"),
    ("เพราะ", "dead", "h"),
    ("แอะ", "live", "m"),
    ("โอะ", "live", "m"),
    ("เอาะ", "live", "m"),
    ("เออะ", "live", "m"),
    ("ฤๅษี", "live", "r"),
    ("พฤ", "dead", "f"),
    ("หนู", "live", "r"),
    ("อย่า", "live", "l"),
    ("อยู่", "live", "l"),
    ("หมา", "live", "r"),
    ("ไหม", "live", "r"),
    ("ๆ", "dead", ""),
    ("😀", "dead", ""),
    ("\u200b", "dead", ""),
    ("อยผ", "dead", "l"),
    ("แอว๊ห", "live", "h"),
    (" ทยุฬ", "live", "m"),
    ("อ๋อ", "live", "r"),
    ("ฃณิฏดผ", "dead", "l"),
    ("ห่รฌญ", "live", "l"),
    ("เงะ้", "dead", "h"),
    ("ลษฬ่ิ", "dead", "f"),
    ("อะ้อ", "dead", "f"),
    ("ษแ้ิศฮ", "dead", "f"),
    ("ำอธ่ึฦ", "live", "l"),
    ("พลดษฏฏฅ", "dead", "f"),
    ("แาดะลปจ", "dead", "l"),
    ("หลึต", "dead", "l"),
    ("ห้น", "live", "f"),
    ("ห่ว", "live", "l"),
    ("เกะ่ก", "dead", "l"),
    ("ไถยด", "live", "r"),
    ("ใธำ๊ร", "live", "m"),
    ("สอ่ม", "live", "l"),
    ("แผฤๅ๋ม", "live", "r"),
    ("เฮา่ก", "dead", "f"),
    ("ไฑ๋", "live", "m"),
    ("โณี้บ", "dead", "h"),
    ("ฝฤๅ๋ฤ", "dead", "l"),
    ("โงาว", "live", "m"),
    ("เถื๋ว", "live", "r"),
    ("หาก", "dead", "l"),
    ("โบีบ", "dead", "l"),
    ("ธึบ", "dead", "h"),
    ("ไฮฤๅ๊น", "live", "m"),
    ("ธะ๋ก", "dead", "h"),
    ("รอ่บ", "dead", "f"),
    ("ไนึ้บ", "live", "h"),
    ("แมว๊ฤ", "live", "m"),
    ("เฏา้น", "live", "f"),
    ("ใสะ้น", "live", "f"),
    ("ไมื๊", "live", "m"),
    ("ฅอ่บ", "dead", "f"),
    ("โอี้ว", "live", "f"),
    ("ฝ้ด", "dead", "f"),
    ("ไญู๋ว", "live", "m"),
    ("โรู้ว", "live", "h"),
    ("แงว้ฤ", "live", "h"),
    ("ไงำ้บ", "live", "h"),
    ("ไฑือ", "live", "m"),
    ("ใบา้ว", "live", "f"),
    ("เละ่ก", "dead", "f"),
    ("เอุ่ฤ", "live", "l"),
    ("แณา๋ร", "live", "m"),
    ("เฉึ๋ม", "live", "r"),
    ("ไซา๋", "live", "m"),
    ("ฝื่อ", "live", "l"),
    ("เชอ๋ก", "dead", "f"),
    ("เบำ๊ฤ", "live", "h"),
    ("แฑุ๊อ", "live", "h"),
    ("เปา้ย", "live", "f"),
    ("เคว๋ด", "dead", "f"),
    ("ใศุ่ย", "live", "l"),
    ("แจั๊ง", "live", "h"),
    ("แชุ่น", "live", "f"),
    ("เฆัร", "live", "m"),
    ("ขุบ", "dead", "l"),
    ("โสฤๅ่ด", "dead", "l"),
    ("ผะ่ห", "dead", "l"),
    ("โฏอ้ด", "dead", "f"),
    ("เฌา๊ว", "live", "m"),
    ("ไฃุง", "live", "r"),
    ("แฝ่ม", "live", "l"),
    ("ไฌื่ย", "live", "f"),
    ("แป็่อ", "live", "l"),
    ("เปึ่ร", "live", "l"),
    ("โดย๊ร", "live", "h"),
    ("เฎิ้ง", "live", "f"),
    ("เทื้ย", "live", "h"),
    ("ฆี้ฤ", "live", "h"),
    ("เยิ๊ม", "live", "m"),
    ("เจฤ๊ด", "dead", "h"),
    ("เยา๊ร", "live", "m"),
    ("โธึ", "live", "h"),
    ("โภะ๊ร", "dead", "h"),
    ("โฮื๋บ", "dead", "f"),
    ("เซั๊ห", "dead", "h"),
    ("แธฤๅ๋", "live", "m"),
    ("ไฌึ๋ย", "live", "m"),
    ("เบึ่ย", "live", "l"),
    ("ใขี๊ฤ", "live", "r"),
    ("โลา้ฤ", "live", "h"),
    ("แศื้ย", "live", "f"),
    ("เบ็๊ด", "dead", "h"),
    ("โอิ้อ", "live", "f"),
    ("แฬั่ก", "dead", "f"),
    ("รฤๅ๊ง", "live", "m"),
    ("โลื่บ", "dead", "f"),
    ("ใฆะ้น", "live", "h"),
    ("ไฃำ๊ก", "live", "r"),
    ("ใถะ่อ", "live", "l"),
    ("พา๋อ", "live", "m"),
    ("ไกฤด", "live", "m"),
    ("ฉั๋ด", "dead", "l"),
    ("แจ็ด", "dead", "l"),
    ("แณะ๋ว", "dead", "h"),
    ("เกึ้ห", "dead", "f"),
    ("เอำ๊ง", "live", "h"),
    ("ฒู่ฤ", "live", "f"),
    ("เนูฤ", "live", "m"),
    ("ไผะ้ก", "live", "f"),
    ("ใฏำ่บ", "live", "l"),
    ("แหื๊น", "live", "r"),
    ("ใฑู๋", "live", "m"),
    ("โษย๊ห", "live", "r"),
    ("แดฤ่ก", "dead", "l"),
    ("ไฅา่ย", "live", "f"),
    ("ไฑำ่ด", "live", "f"),
    ("โฏว", "live", "m"),
    ("เฝิ้อ", "dead", "f"),
    ("เปื้ม", "live", "f"),
    ("ญะอ", "dead", "h"),
    ("โกืฤ", "live", "m"),
    ("แฝำ๊น", "live", "r"),
    ("ฑา๋", "live", "m"),
    ("ไพิ๋ย", "live", "m"),
    ("ไฌา๊ม", "live", "m"),
    ("บห", "dead", "l"),
    ("แฌื้น", "live", "h"),
    ("ฎอย", "live", "m"),
    ("โยฤ่", "live", "f"),
    ("โฮื๋ย", "live", "m"),
    ("กะ๋น", "live", "r"),
    ("แฬา๋อ", "live", "m"),
    ("โษฤ๊ด", "dead", "l"),
    ("ใฟุ๊ง", "live", "m"),
    ("ตะ่ย", "live", "l"),
    ("โงื่", "live", "f"),
    ("ฏา่ร", "live", "l"),
    ("ใตะอ", "live", "m"),
    ("ฎ็๊ง", "live", "h"),
    ("เพอ่ว", "live", "f"),
    ("ใฒี๊ง", "live", "m"),
    ("โยว๋อ", "live", "m"),
    ("ไฌั่ง", "live", "f"),
    ("แฅี่บ", "dead", "f"),
    ("ไตึบ", "live", "m"),
    ("โตฤ๋น", "live", "r"),
    ("พา๋ห", "live", "m"),
    ("เฌา๋ด", "dead", "f"),
    ("ใฃฤๅฤ", "live", "r"),
    ("โฟย๋ก", "dead", "f"),
    ("ใลำ๊ร", "live", "m"),
    ("ใรู้บ", "dead", "h"),
    ("แฮ็๋", "live", "m"),
    ("ไลา่ห", "live", "f"),
    ("ศี๊อ", "live", "r"),
    ("โที๋ว", "live", "m"),
    ("ไภื้ร", "live", "h"),
    ("แอ็่ว", "live", "l"),
    ("ไฆั๊ว", "live", "m"),
    ("ใซิ้ง", "live", "h"),
    ("โธะ๋ว", "dead", "h"),
    ("โปยน", "live", "m"),
    ("ฟาง", "live", "m"),
    ("ไณิ่ห", "live", "f"),
    ("โถี๋ก", "dead", "l"),
    ("ไฒฤ้ร", "live", "h"),
    ("เฒย่อ", "live", "f"),
    ("ตะ๋อ", "dead", "r"),
    ("เฏา้ด", "dead", "f"),
    ("ใฌ่ม", "live", "f"),
    ("ไพึ๊ห", "live", "m"),
    ("เขืว", "live", "r"),
    ("ใติ้ร", "live", "f"),
    ("โฉ็๋ด", "dead", "l"),
    ("ไสี๋", "live", "r"),
    ("เถูง", "live", "r"),
    ("ใฎา๊ย", "live", "h"),
    ("แฐั้ด", "dead", "f"),
    ("เพะ่ด", "dead", "f"),
    ("ใปวก", "live", "m"),
    ("แบีด", "dead", "l"),
    ("ใศ", "live", "r"),
    ("ไฌา่อ", "live", "f"),
    ("ผั๊ฤ", "dead", "l"),
    ("งุ๊อ", "dead", "h"),
    ("ไงั้น", "live", "h"),
    ("ไวึ๊ร", "live", "m"),
    ("แฬืด", "dead", "f"),
    ("ใอี๋ก", "dead", "r"),
    ("ใฌะ๋ม", "live", "m"),
    ("แหึ่น", "live", "l"),
    ("คฤ้ม", "live", "h"),
    ("สว่ว", "live", "l"),
    ("ใดุ๊ด", "live", "h"),
    ("ไปุ่ร", "live", "l"),
    ("ใกำ้ก", "live", "f"),
    ("ฑฤ้ย", "live", "h"),
    ("โซย่อ", "live", "f"),
    ("ณา้ย", "live", "h"),
    ("เภว๊ห", "dead", "f"),
    ("ดะฤ", "dead", "l"),
    ("ใอา้ย", "live", "f"),
    ("ใอฤ้ย", "live", "f"),
    ("แบืบ", "dead", "l"),
    ("ใพอ๋อ", "live", "m"),
    ("แฆฤๅ่ฤ", "live", "f"),
    ("ไหูร", "live", "r"),
    ("เตี๊ฤ", "live", "h"),
    ("คฤ๋ม", "live", "m"),
    ("เพำ๋ง", "live", "m"),
    ("โวีบ", "dead", "f"),
    ("ใฉั๊น", "live", "r"),
    ("โหั้ด", "dead", "f"),
    ("ใดี๊ก", "dead", "h"),
    ("ใศะ่ด", "live", "l"),
    ("ใศา้", "live", "f"),
    ("ถา้ว", "live", "f"),
    ("แญา๊ห", "live", "m"),
    ("ใมั่น", "live", "f"),
    ("แฑ็่ห", "live", "f"),
    ("แฌุ้อ", "live", "h"),
    ("ตำ๋ฤ", "live", "r"),
    ("โฒา่บ", "dead", "f"),
    ("ใค่ร", "live", "f"),
    ("ขั๋ง", "live", "r"),
    ("โบืด", "dead", "l"),
    ("โวำว", "live", "m"),
    ("ทอ๊ร", "live", "m"),
    ("ลา๋ร", "live", "m"),
    ("ไฃ็้น", "live", "f"),
    ("เฑ่อ", "dead", "f"),
    ("ไณั้ก", "live", "h"),
    ("ไฉง", "live", "r"),
    ("ไฌา๋บ", "dead", "f"),
    ("ใธำ๊", "live", "m"),
    ("แมา๊", "live", "m"),
    ("โอั้", "live", "f"),
    ("แสยม", "live", "r"),
    ("เวุ๊อ", "dead", "h"),
    ("แฎิ๊ว", "live", "h"),
    ("เชะน", "live", "m"),
    ("แฐา๊อ", "live", "r"),
    ("แซฤ้ว", "live", "h"),
    ("เชีย", "live", "m"),
    ("ผุบ", "dead", "l"),
    ("ไญอ้ด", "live", "h"),
    ("ไถิก", "live", "r"),
    ("โซฤย", "live", "m"),
    ("เสอ๊ย", "live", "r"),
    ("ไควอ", "live", "m"),
    ("ขิ๊ว", "live", "r"),
    ("ไผฤๅ๊", "live", "r"),
    ("มิ้", "dead", "h"),
    ("โฆึน", "live", "m"),
    ("ตา๋อ", "live", "r"),
    ("ในำย", "live", "m"),
    ("ใจะ่ง", "live", "l"),
    ("ไพิฤ", "live", "h"),
    ("ไดะ่ร", "live", "l"),
    ("แฎำ่ฤ", "live", "l"),
    ("แฬาว", "live", "m"),
    ("โฝื๋ก", "dead", "l"),
    ("ฉะ้ห", "dead", "f"),
    ("โนา", "live", "m"),
    ("โพ๋", "live", "m"),
    ("ใผิ่ห", "live", "l"),
    ("ไรำ๋ง", "live", "m"),
    ("แรื๋น", "live", "m"),
    ("ไผิ่ว", "live", "l"),
]

LEADS = ["", "เ", "แ", "โ", "ไ", "ใ"]
VOWELS = [
    "",
    "ะ",
    "ั",
    "า",
    "ิ",
    "ี",
    "ึ",
    "ื",
    "ุ",
    "ู",
    "ำ",
    "็",
    "อ",
    "า",
    "ว",
    "ย",
    "ฤ",
    "ฤๅ",
    "ะ",
]
FINALS = ["", "ก", "ด", "บ", "ง", "น", "ม", "ย", "ว", "อ", "ร", "ห", "ฤ"]
TONES = ["", "\u0e48", "\u0e49", "\u0e4a", "\u0e4b"]

# SHA-256 of every 13th generated syllable with its two results.
GRID_SIZE = 25080
GRID_DIGEST = (
    "7c5d516512e3cfc4b1f25ac33e44027403505743aad45979e9015f11b30f0daa"
)
# Every 125th syllable of that sequence, as (text, sound, tone).
# Shows the failing syllables if the digest differs.
GRID_SAMPLE: list[tuple[str, str, str]] = [
    ("ก", "dead", "l"),
    ("ขึ", "dead", "l"),
    ("ฃอ", "dead", "l"),
    ("คะ", "dead", "h"),
    ("ฆี", "live", "m"),
    ("ง็", "live", "m"),
    ("จฤๅ", "dead", "l"),
    ("ชิ", "dead", "h"),
    ("ซำ", "live", "m"),
    ("ฌฤ", "dead", "f"),
    ("ฎา", "live", "m"),
    ("ฏู", "live", "m"),
    ("ฐย", "live", "r"),
    ("ฒั", "dead", "h"),
    ("ณุ", "dead", "h"),
    ("ดว", "live", "m"),
    ("ถะ", "dead", "l"),
    ("ทื", "live", "m"),
    ("ธา", "live", "m"),
    ("บ", "dead", "l"),
    ("ปึ", "dead", "l"),
    ("ผอ", "dead", "l"),
    ("ฝะ", "dead", "l"),
    ("ฟี", "live", "m"),
    ("ภ็", "dead", "f"),
    ("มฤๅ", "live", "m"),
    ("ริ", "dead", "h"),
    ("ลำ", "live", "m"),
    ("วฤ", "live", "m"),
    ("ษา", "live", "r"),
    ("สู", "live", "r"),
    ("หย", "live", "r"),
    ("อั", "dead", "l"),
    ("ฮุ", "dead", "h"),
    ("เกว", "live", "m"),
    ("เฃะ", "dead", "l"),
    ("เคื", "live", "m"),
    ("เฅา", "live", "m"),
    ("เง", "live", "m"),
    ("เจึ", "dead", "l"),
    ("เฉอ", "dead", "l"),
    ("เชะ", "dead", "h"),
    ("เฌี", "live", "m"),
    ("เญ็", "live", "m"),
    ("เฎฤๅ", "dead", "l"),
    ("เฐิ", "dead", "l"),
    ("เฑำ", "live", "m"),
    ("เฒฤ", "dead", "f"),
    ("เดา", "live", "m"),
    ("เตู", "live", "m"),
    ("เถย", "live", "r"),
    ("เธั", "dead", "h"),
    ("เนุ", "dead", "h"),
    ("เบว", "live", "m"),
    ("เผะ", "dead", "l"),
    ("เฝื", "live", "r"),
    ("เพา", "live", "m"),
    ("เภ", "dead", "f"),
    ("เมึ", "dead", "h"),
    ("เยอ", "live", "m"),
    ("เระ", "dead", "h"),
    ("เวี", "live", "m"),
    ("เศ็", "dead", "l"),
    ("เษฤๅ", "dead", "l"),
    ("เหิ", "dead", "l"),
    ("เฬำ", "live", "m"),
    ("เอฤ", "live", "m"),
    ("แกา", "live", "m"),
    ("แขู", "live", "r"),
    ("แฃย", "live", "r"),
    ("แฅั", "live", "h"),
    ("แฆุ", "live", "h"),
    ("แงว", "live", "m"),
    ("แฉะ", "dead", "l"),
    ("แชื", "live", "m"),
    ("แซา", "live", "m"),
    ("แญ", "live", "m"),
    ("แฎึ", "live", "m"),
    ("แฏอ", "live", "m"),
    ("แฐะ", "dead", "l"),
    ("แฒี", "live", "m"),
    ("แณ็", "live", "m"),
    ("แดฤๅ", "live", "m"),
    ("แถิ", "live", "r"),
    ("แทำ", "live", "m"),
    ("แธฤ", "live", "m"),
    ("แบา", "live", "m"),
    ("แปู", "live", "m"),
    ("แผย", "live", "r"),
    ("แพั", "live", "h"),
    ("แฟุ", "live", "h"),
    ("แภว", "live", "m"),
    ("แยะ", "dead", "h"),
    ("แรื", "live", "m"),
    ("แลา", "live", "m"),
    ("แศ", "dead", "l"),
    ("แษึ", "live", "r"),
    ("แสอ", "live", "r"),
    ("แหะ", "dead", "l"),
    ("แอี", "live", "m"),
    ("แฮ็", "live", "m"),
    ("โกฤๅ", "live", "m"),
    ("โฃิ", "live", "r"),
    ("โคำ", "live", "m"),
    ("โฅฤ", "live", "m"),
    ("โงา", "live", "m"),
    ("โจู", "live", "m"),
    ("โฉย", "live", "r"),
    ("โซั", "live", "h"),
    ("โฌุ", "live", "h"),
    ("โญว", "live", "m"),
    ("โฏะ", "dead", "l"),
    ("โฐื", "live", "r"),
    ("โฑา", "live", "m"),
    ("โณ", "live", "m"),
    ("โดึ", "live", "m"),
    ("โตอ", "live", "m"),
    ("โถะ", "dead", "l"),
    ("โธี", "live", "m"),
    ("โน็", "live", "m"),
    ("โบฤๅ", "live", "m"),
    ("โผิ", "live", "r"),
    ("โฝำ", "live", "r"),
    ("โพฤ", "live", "m"),
    ("โภา", "live", "m"),
    ("โมู", "live", "m"),
    ("โยย", "live", "m"),
    ("โลั", "live", "h"),
    ("โวุ", "live", "h"),
    ("โศว", "live", "r"),
    ("โสะ", "dead", "l"),
    ("โหื", "live", "r"),
    ("โฬา", "live", "m"),
    ("โฮ", "live", "m"),
    ("ไกึ", "live", "m"),
    ("ไขอ", "live", "r"),
    ("ไฃะ", "live", "r"),
    ("ไฅี", "live", "m"),
    ("ไฆ็", "live", "m"),
    ("ไงฤๅ", "live", "m"),
    ("ไฉิ", "live", "r"),
    ("ไชำ", "live", "m"),
    ("ไซฤ", "live", "m"),
    ("ไญา", "live", "m"),
    ("ไฎู", "live", "m"),
    ("ไฏย", "live", "m"),
    ("ไฑั", "live", "h"),
    ("ไฒุ", "live", "h"),
    ("ไณว", "live", "m"),
    ("ไตะ", "live", "m"),
    ("ไถื", "live", "r"),
    ("ไทา", "live", "m"),
    ("ไน", "live", "m"),
    ("ไบึ", "live", "m"),
    ("ไปอ", "live", "m"),
    ("ไผะ", "live", "r"),
    ("ไพี", "live", "m"),
    ("ไฟ็", "live", "m"),
    ("ไภฤๅ", "live", "m"),
    ("ไยิ", "live", "h"),
    ("ไรำ", "live", "m"),
    ("ไลฤ", "live", "m"),
    ("ไศา", "live", "r"),
    ("ไษู", "live", "r"),
    ("ไสย", "live", "r"),
    ("ไฬั", "live", "h"),
    ("ไอุ", "live", "m"),
    ("ไฮว", "live", "m"),
    ("ใขะ", "live", "r"),
    ("ใฃื", "live", "r"),
    ("ใคา", "live", "m"),
    ("ใฆ", "live", "m"),
    ("ใงึ", "live", "h"),
    ("ใจอ", "live", "m"),
    ("ใฉะ", "live", "r"),
    ("ใซี", "live", "m"),
    ("ใฌ็", "live", "m"),
    ("ใญฤๅ", "live", "m"),
    ("ใฏิ", "live", "m"),
    ("ใฐำ", "live", "r"),
    ("ใฑฤ", "live", "m"),
    ("ใณา", "live", "m"),
    ("ใดู", "live", "m"),
    ("ใตย", "live", "m"),
    ("ใทั", "live", "h"),
    ("ใธุ", "live", "h"),
    ("ในว", "live", "m"),
    ("ใปะ", "live", "m"),
    ("ใผื", "live", "r"),
    ("ใฝา", "live", "r"),
    ("ใฟ", "live", "m"),
    ("ใภึ", "live", "h"),
    ("ใมอ", "live", "m"),
    ("ใยะ", "live", "h"),
    ("ใลี", "live", "m"),
    ("ใว็", "live", "m"),
    ("ใศฤๅ", "live", "r"),
    ("ใสิ", "live", "r"),
    ("ใหำ", "live", "r"),
    ("ใฬฤ", "live", "m"),
    ("ใฮา", "live", "m"),
]


def _grid() -> Iterator[str]:
    for lead in LEADS:
        for consonant in thai_consonants:
            for vowel in VOWELS:
                for final in FINALS:
                    for tone in TONES:
                        yield lead + consonant + vowel + tone + final


def _outcome(func: Callable[[str], str], text: str) -> str:
    try:
        return func(text)
    except Exception as err:
        return "!" + type(err).__name__


class SyllableCharacterizationTestCase(unittest.TestCase):
    def test_golden(self) -> None:
        for text, sound, tone in GOLDEN:
            with self.subTest(text=text):
                self.assertEqual(_outcome(sound_syllable, text), sound)
                self.assertEqual(_outcome(tone_detector, text), tone)

    def test_generated_grid(self) -> None:
        digest = hashlib.sha256()
        count = 0
        for text in list(_grid())[::13]:
            record = (
                text,
                _outcome(sound_syllable, text),
                _outcome(tone_detector, text),
            )
            digest.update(repr(record).encode())
            count += 1
        self.assertEqual(count, GRID_SIZE)
        if digest.hexdigest() != GRID_DIGEST:
            for text, sound, tone in GRID_SAMPLE:
                with self.subTest(text=text):
                    self.assertEqual(
                        (
                            _outcome(sound_syllable, text),
                            _outcome(tone_detector, text),
                        ),
                        (sound, tone),
                    )
            self.fail(
                "Digest differs, but GRID_SAMPLE rows match; "
                "regenerate GRID_DIGEST with the same loop."
            )

    def test_long_input(self) -> None:
        self.assertEqual(sound_syllable("ก" * 500), "dead")
        self.assertEqual(tone_detector("ก" * 500), "l")
        self.assertEqual(sound_syllable("มา" * 300), "live")
        self.assertEqual(tone_detector("มา" * 300), "m")
        self.assertEqual(sound_syllable("เ" + "ก" * 50 + "า"), "live")

    def test_wrong_type(self) -> None:
        for value in (None, 5, 1.5, b"abc"):
            with self.subTest(value=value):
                with self.assertRaises(TypeError):
                    sound_syllable(value)  # type: ignore[arg-type]
                with self.assertRaises(TypeError):
                    tone_detector(value)  # type: ignore[arg-type]

    def test_empty_and_short(self) -> None:
        self.assertEqual(sound_syllable(""), "dead")
        self.assertEqual(sound_syllable("ก"), "dead")
        self.assertEqual(tone_detector(""), "")
        self.assertEqual(tone_detector("ฤ"), "")


class SyllableKnownBugTestCase(unittest.TestCase):
    def test_tone_detector_ru_lue(self) -> None:
        # BUG-LEDGER: tone-detector-ru-lue
        # Expected: return a tone. Current: IndexError.
        with self.assertRaises(IndexError):
            tone_detector("ฤๅ")

    def test_sound_syllable_ru_lue(self) -> None:
        # BUG-LEDGER: sound-syllable-ru-lue
        # Expected: return "live" or "dead". Current: IndexError.
        with self.assertRaises(IndexError):
            sound_syllable("ฤๅ")

    def test_sound_syllable_e_a(self) -> None:
        # BUG-LEDGER: sound-syllable-e-a
        # Expected: "dead" (short vowel เ-อะ). Current: "live".
        self.assertEqual(sound_syllable("เอะ"), "live")

    def test_consonant_sets(self) -> None:
        # BUG-LEDGER: syllable-consonant-sets
        # sound_syllable excludes "อ"; other functions include it.
        self.assertIn("อ", thai_consonants)
        self.assertNotIn("อ", thai_consonants_all)
        self.assertEqual(syllable_open_close_detector("คอ"), "open")
        self.assertEqual(syllable_open_close_detector("คอก"), "close")
        self.assertEqual(syllable_length("คอ"), "long")
        self.assertEqual(sound_syllable("คอ"), "dead")
        self.assertEqual(tone_detector("เอ"), "m")


if __name__ == "__main__":
    unittest.main()
