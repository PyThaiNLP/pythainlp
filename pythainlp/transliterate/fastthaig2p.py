# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""
FastThaiG2P grapheme-to-phoneme engine.

FastThaiG2P is a fast Thai grapheme-to-phoneme (G2P) conversion engine
optimized for low latency speech pipelines. It combines comprehensive text
normalization, dictionary-based tokenization, 62k IPA dictionary lookup,
and rule-based fallback phonemization for out-of-vocabulary words.

References:
    - FastThaiG2P: https://github.com/awslabs/FastThaiG2P

## License

Copyright 2026 Charin Polpanumas and Amazon Web Services

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from __future__ import annotations

import json
import re
from importlib.resources import files
from typing import Dict, Final, List, Optional, Pattern, Set, Tuple

from pythainlp.tokenize import Tokenizer
from pythainlp.util import expand_maiyamok as _expand_maiyamok_pythainlp

__all__: Final[List[str]] = [
    "FastThaiG2P",
    "fallback_g2p",
    "normalize",
    "transliterate",
]

THAI_DIGITS: Final[Dict[str, str]] = {
    "0": "ศูนย์",
    "1": "หนึ่ง",
    "2": "สอง",
    "3": "สาม",
    "4": "สี่",
    "5": "ห้า",
    "6": "หก",
    "7": "เจ็ด",
    "8": "แปด",
    "9": "เก้า",
}

THAI_NUMERAL_MAP: Final[Dict[str, str]] = {
    "๐": "0",
    "๑": "1",
    "๒": "2",
    "๓": "3",
    "๔": "4",
    "๕": "5",
    "๖": "6",
    "๗": "7",
    "๘": "8",
    "๙": "9",
}

LETTER_TO_THAI: Final[Dict[str, str]] = {
    "A": "เอ",
    "B": "บี",
    "C": "ซี",
    "D": "ดี",
    "E": "อี",
    "F": "เอฟ",
    "G": "จี",
    "H": "เอช",
    "I": "ไอ",
    "J": "เจ",
    "K": "เค",
    "L": "แอล",
    "M": "เอ็ม",
    "N": "เอ็น",
    "O": "โอ",
    "P": "พี",
    "Q": "คิว",
    "R": "อาร์",
    "S": "เอส",
    "T": "ที",
    "U": "ยู",
    "V": "วี",
    "W": "ดับเบิลยู",
    "X": "เอ็กซ์",
    "Y": "วาย",
    "Z": "แซด",
}

ABBREVIATIONS: Final[Dict[str, str]] = {
    # Months
    "ม.ค.": "มกราคม",
    "ก.พ.": "กุมภาพันธ์",
    "มี.ค.": "มีนาคม",
    "เม.ย.": "เมษายน",
    "พ.ค.": "พฤษภาคม",
    "มิ.ย.": "มิถุนายน",
    "ก.ค.": "กรกฎาคม",
    "ส.ค.": "สิงหาคม",
    "ก.ย.": "กันยายน",
    "ต.ค.": "ตุลาคม",
    "พ.ย.": "พฤศจิกายน",
    "ธ.ค.": "ธันวาคม",
    # Eras
    "พ.ศ.": "พุทธศักราช",
    "ค.ศ.": "คริสต์ศักราช",
    # Titles
    "น.ส.": "นางสาว",
    "นส.": "นางสาว",
    "ดร.": "ด็อกเตอร์",
    "ผศ.": "ผู้ช่วยศาสตราจารย์",
    "รศ.": "รองศาสตราจารย์",
    # Medical & Professional
    "นพ.": "นายแพทย์",
    "พญ.": "แพทย์หญิง",
    "ทพ.": "ทันตแพทย์",
    "ทพญ.": "ทันตแพทย์หญิง",
    "น.สพ.": "นายสัตวแพทย์",
    "สพ.ญ.": "สัตวแพทย์หญิง",
    "ภก.": "เภสัชกร",
    "ภญ.": "เภสัชกรหญิง",
    "ทนพ.": "เทคนิคการแพทย์",
    "กภ.": "กายภาพบำบัด",
    # Army (Officers)
    "พล.อ.": "พลเอก",
    "พล.ท.": "พลโท",
    "พล.ต.": "พลตรี",
    "พ.อ.": "พันเอก",
    "พ.ท.": "พันโท",
    "พ.ต.": "พันตรี",
    "ร.อ.": "ร้อยเอก",
    "ร.ท.": "ร้อยโท",
    "ร.ต.": "ร้อยตรี",
    # Army (NCOs)
    "จ.ส.อ.": "จ่าสิบเอก",
    "จ.ส.ท.": "จ่าสิบโท",
    "จ.ส.ต.": "จ่าสิบตรี",
    "ส.อ.": "สิบเอก",
    "ส.ท.": "สิบโท",
    "ส.ต.": "สิบตรี",
    # Police
    "พล.ต.อ.": "พลตำรวจเอก",
    "พล.ต.ท.": "พลตำรวจโท",
    "พล.ต.ต.": "พลตำรวจตรี",
    "พ.ต.อ.": "พันตำรวจเอก",
    "พ.ต.ท.": "พันตำรวจโท",
    "พ.ต.ต.": "พันตำรวจตรี",
    "ร.ต.อ.": "ร้อยตำรวจเอก",
    "ร.ต.ท.": "ร้อยตำรวจโท",
    "ร.ต.ต.": "ร้อยตำรวจตรี",
    "ด.ต.": "ดาบตำรวจ",
    # Navy
    "พล.ร.อ.": "พลเรือเอก",
    "พล.ร.ท.": "พลเรือโท",
    "พล.ร.ต.": "พลเรือตรี",
    "น.อ.": "นาวาเอก",
    "น.ท.": "นาวาโท",
    "น.ต.": "นาวาตรี",
    "พ.จ.อ.": "พันจ่าเอก",
    "พ.จ.ท.": "พันจ่าโท",
    "พ.จ.ต.": "พันจ่าตรี",
    "จ.อ.": "จ่าเอก",
    "จ.ท.": "จ่าโท",
    "จ.ต.": "จ่าตรี",
    # Air Force
    "พล.อ.อ.": "พลอากาศเอก",
    "พล.อ.ท.": "พลอากาศโท",
    "พล.อ.ต.": "พลอากาศตรี",
    "พ.อ.อ.": "พันจ่าอากาศเอก",
    "พ.อ.ท.": "พันจ่าอากาศโท",
    "พ.อ.ต.": "พันจ่าอากาศตรี",
    # Royal & Noble
    "ม.จ.": "หม่อมเจ้า",
    "ม.ร.ว.": "หม่อมราชวงศ์",
    "ม.ล.": "หม่อมหลวง",
    # Common
    "กทม.": "กรุงเทพมหานคร",
    "รร.": "โรงเรียน",
    "ร.ร.": "โรงเรียน",
    "รพ.": "โรงพยาบาล",
    "ร.พ.": "โรงพยาบาล",
    "บจก.": "บริษัทจำกัด",
    "ฯลฯ": "เป็นต้น",
}

SYMBOLS: Final[Dict[str, str]] = {
    "%": "เปอร์เซ็นต์",
    "°C": "องศาเซลเซียส",
    "°F": "องศาฟาเรนไฮต์",
    "°": "องศา",
    "@": " แอท ",
    "/": " ทับ ",
}

ENGLISH_ABBREVS: Final[Dict[str, str]] = {
    # Finance
    "thb": "บาท",
    "usd": "ดอลลาร์",
    "eur": "ยูโร",
    "vat": "แวต",
    "pin": "พิน",
    # Tech
    "ram": "แรม",
    "wifi": "ไวไฟ",
    "otp": "โอทีพี",
    # Health
    "covid": "โควิด",
    # Orgs
    "fifa": "ฟีฟ่า",
    # Brands / internet words
    "line": "ไลน์",
    "facebook": "เฟซบุ๊ก",
    "instagram": "อินสตาแกรม",
    "amazon": "อมาซอน",
    "twitter": "ทวิตเตอร์",
    "google": "กูเกิล",
    "youtube": "ยูทูบ",
    "tiktok": "ติ๊กต็อก",
    "gmail": "จีเมล",
    "hotmail": "ฮอตเมล",
    "email": "อีเมล",
    "com": "คอม",
    "net": "เน็ต",
    "app": "แอป",
    "lazada": "ลาซาด้า",
    "shopee": "ช้อปปี้",
    "grab": "แกร็บ",
    "uber": "อูเบอร์",
    "whatsapp": "วอทส์แอป",
    "paypal": "เพย์พาล",
    "promptpay": "พร้อมเพย์",
    "truemoney": "ทรูมันนี่",
}

UNITS: Final[Dict[str, str]] = {
    "km": "กิโลเมตร",
    "cm": "เซนติเมตร",
    "mm": "มิลลิเมตร",
    "ml": "มิลลิลิตร",
    "kwh": "กิโลวัตต์ชั่วโมง",
    "kw": "กิโลวัตต์",
    "mb": "เมกะไบต์",
    "gb": "กิกะไบต์",
    "tb": "เทราไบต์",
    "kb": "กิโลไบต์",
    "mbps": "เมกะบิตต่อวินาที",
    "กม.": "กิโลเมตร",
    "ซม.": "เซนติเมตร",
    "มม.": "มิลลิเมตร",
    "ตร.กม.": "ตารางกิโลเมตร",
    "ตร.ม.": "ตารางเมตร",
    "ตร.ซม.": "ตารางเซนติเมตร",
    "ตร.มม.": "ตารางมิลลิเมตร",
    "ตร.ว.": "ตารางวา",
    "ลบ.ม.": "ลูกบาศก์เมตร",
    "ลบ.ซม.": "ลูกบาศก์เซนติเมตร",
    "มล.": "มิลลิลิตร",
    "กล.": "กิโลลิตร",
    "กก.": "กิโลกรัม",
    "มก.": "มิลลิกรัม",
    "kg": "กิโลกรัม",
    "mg": "มิลลิกรัม",
}

_EMAIL_SEPARATORS: Final[Dict[str, str]] = {
    "@": " แอท ",
    ".": " ดอท ",
    "-": " ขีด ",
    "_": " ขีดล่าง ",
}

_EMAIL_WORDS: Final[Dict[str, str]] = {
    "gmail": "จีเมล",
    "hotmail": "ฮอตเมล",
    "yahoo": "ยาฮู",
    "outlook": "เอาต์ลุก",
    "com": "คอม",
    "net": "เน็ต",
    "org": "ออร์ก",
    "mail": "เมล",
    "email": "อีเมล",
}

_PLACE_UNITS: Final[Dict[int, str]] = {
    100000: "แสน",
    10000: "หมื่น",
    1000: "พัน",
    100: "ร้อย",
}

_SYMBOL_PATTERN: Final[Pattern[str]] = re.compile(
    "|".join(
        re.escape(k) for k in sorted(SYMBOLS.keys(), key=len, reverse=True)
    )
)
_ENGLISH_ABBREV_PATTERN: Final[Pattern[str]] = re.compile(
    r"\b("
    + "|".join(
        re.escape(k)
        for k in sorted(ENGLISH_ABBREVS.keys(), key=len, reverse=True)
    )
    + r")",
    re.IGNORECASE,
)
_UNIT_PATTERN: Final[Pattern[str]] = re.compile(
    r"(?<=\d)\s*("
    + "|".join(
        re.escape(k) for k in sorted(UNITS.keys(), key=len, reverse=True)
    )
    + r")"
)
_TIME_PATTERN: Final[Pattern[str]] = re.compile(
    r"\b(\d{1,2}):(\d{2})(?:\s*(?:นาฬิกา|น\.))?"
)
_EMAIL_PATTERN: Final[Pattern[str]] = re.compile(
    r"[A-Za-z0-9._-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
)
_PHONE_PATTERN: Final[Pattern[str]] = re.compile(
    r"\d{2,4}[-\.]\d{3,4}[-\.]\d{3,4}"
)
_ALPHANUM_ID_PATTERN: Final[Pattern[str]] = re.compile(
    r"[A-Za-z]+[\-]?\d+[\-\dA-Za-z]*|\d+[\-]?[A-Za-z]+[\-\dA-Za-z]*"
)
_COMMA_NUMBER_PATTERN: Final[Pattern[str]] = re.compile(
    r"-?\d{1,3}(?:,\d{3})+(?:\.\d+)?"
)
_NUMBER_PATTERN: Final[Pattern[str]] = re.compile(r"-?\d+(?:\.\d+)?")
_ABBREV_PATTERN: Final[Pattern[str]] = re.compile(
    "|".join(
        re.escape(k)
        for k in sorted(ABBREVIATIONS.keys(), key=len, reverse=True)
    )
)
_LATIN_RESIDUE_PATTERN: Final[Pattern[str]] = re.compile(r"[A-Za-z]+")

_TLTK_PHON_RE: Final[Pattern[str]] = re.compile(r"<tr/>(.+?)\|<s/>")

_TONE_MAP: Final[Dict[str, str]] = {
    "0": "˧",
    "1": "˨˩",
    "2": "˥˩",
    "3": "˦˥",
    "4": "˩˩˦",
}

_CONSONANT_MAP: Final[List[Tuple[str, str]]] = [
    ("kh", "kʰ"),
    ("ph", "pʰ"),
    ("th", "tʰ"),
    ("ch", "t͡ɕʰ"),
    ("c", "t͡ɕ"),
    ("N", "ŋ"),
    ("?", "ʔ"),
]

_VOWEL_MAP: Final[List[Tuple[str, str]]] = [
    ("UUa", "ɯa̯"),
    ("Ua", "ɯa̯"),
    ("iia", "ia̯"),
    ("ia", "ia̯"),
    ("uua", "ua̯"),
    ("ua", "ua̯"),
    ("aa", "aː"),
    ("ii", "iː"),
    ("uu", "uː"),
    ("xx", "ɛː"),
    ("ee", "eː"),
    ("oo", "oː"),
    ("OO", "ɔː"),
    ("@@", "ɤː"),
    ("UU", "ɯː"),
    ("a", "a"),
    ("i", "i"),
    ("u", "u"),
    ("x", "ɛ"),
    ("e", "e"),
    ("o", "o"),
    ("O", "ɔ"),
    ("@", "ɤ"),
    ("U", "ɯ"),
]

_VOWEL_CHARS: Final[Set[str]] = set("aeiouɔɛɯɤː̯")


def _number_group_to_thai(n: int) -> str:
    if n == 0:
        return ""
    parts: List[str] = []
    remaining = n
    for place in (100000, 10000, 1000, 100, 10, 1):
        digit = remaining // place
        remaining = remaining % place
        if digit == 0:
            continue
        if place in _PLACE_UNITS:
            parts.append(THAI_DIGITS[str(digit)] + _PLACE_UNITS[place])
        elif place == 10:
            if digit == 1:
                parts.append("สิบ")
            elif digit == 2:
                parts.append("ยี่สิบ")
            else:
                parts.append(THAI_DIGITS[str(digit)] + "สิบ")
        else:  # place == 1
            if n > 1 and digit == 1:
                parts.append("เอ็ด")
            else:
                parts.append(THAI_DIGITS[str(digit)])
    return "".join(parts)


def _integer_to_thai(n: int) -> str:
    if n == 0:
        return "ศูนย์"
    if n < 0:
        return "ลบ" + _integer_to_thai(-n)
    parts: List[str] = []
    million_count = 0
    while n > 0:
        group = n % 1000000
        n = n // 1000000
        if group > 0:
            group_text = _number_group_to_thai(group)
            suffix = "ล้าน" * million_count
            parts.append(group_text + suffix)
        million_count += 1
    return "".join(reversed(parts))


def _digits_to_thai(digits: str) -> str:
    return "".join(THAI_DIGITS[d] for d in digits if d in THAI_DIGITS)


def _decimal_to_thai(text: str) -> str:
    if "." in text:
        integer_part, decimal_part = text.split(".", 1)
        integer_part = integer_part or "0"
        int_thai = _integer_to_thai(int(integer_part))
        dec_thai = _digits_to_thai(decimal_part)
        return int_thai + "จุด" + dec_thai
    return _integer_to_thai(int(text))


def _email_token_to_thai(token: str) -> str:
    if not token:
        return ""
    word = _EMAIL_WORDS.get(token.lower())
    if word:
        return word
    return "".join(
        THAI_DIGITS[c] if c.isdigit() else LETTER_TO_THAI.get(c.upper(), c)
        for c in token
    )


def _email_to_thai(match: re.Match[str]) -> str:
    out: List[str] = []
    token = ""
    for char in match.group(0):
        if char in _EMAIL_SEPARATORS:
            if token:
                out.append(_email_token_to_thai(token))
                token = ""
            out.append(_EMAIL_SEPARATORS[char])
        else:
            token += char
    if token:
        out.append(_email_token_to_thai(token))
    return "".join(out)


def _time_to_thai(match: re.Match[str]) -> str:
    hours, minutes = int(match.group(1)), int(match.group(2))
    result = _integer_to_thai(hours) + "นาฬิกา"
    if minutes:
        result += _integer_to_thai(minutes) + "นาที"
    return result


def _phone_number_to_thai(match: re.Match[str]) -> str:
    phone = match.group(0)
    parts = re.split(r"[-.]", phone)
    return " ".join(_digits_to_thai(p) for p in parts)


def _alphanum_to_thai(match: re.Match[str]) -> str:
    token = match.group(0)
    result: List[str] = []
    for char in token:
        if char.isdigit():
            result.append(THAI_DIGITS[char])
        elif char.upper() in LETTER_TO_THAI:
            result.append(LETTER_TO_THAI[char.upper()])
        elif char == "-":
            result.append(" ")
        else:
            result.append(char)
    return "".join(result)


def _strip_commas_and_convert(match: re.Match[str]) -> str:
    return _decimal_to_thai(match.group(0).replace(",", ""))


def _number_or_id_to_thai(match: re.Match[str]) -> str:
    text = match.group(0)
    raw = text.lstrip("-")
    negative = text.startswith("-")

    if "." in raw:
        integer_part, _ = raw.split(".", 1)
    else:
        integer_part = raw

    if len(integer_part) >= 7:
        if "." in raw:
            int_p, dec_p = raw.split(".", 1)
            result = _digits_to_thai(int_p) + "จุด" + _digits_to_thai(dec_p)
        else:
            result = _digits_to_thai(integer_part)
        if negative:
            result = "ลบ" + result
        return result

    return _decimal_to_thai(text)


def _expand_abbreviations(text: str) -> str:
    return _ABBREV_PATTERN.sub(lambda m: ABBREVIATIONS[m.group(0)], text)


def _spell_latin_residue(text: str) -> str:
    return _LATIN_RESIDUE_PATTERN.sub(
        lambda m: "".join(LETTER_TO_THAI[c.upper()] for c in m.group(0)), text
    )


def _expand_symbols(text: str) -> str:
    return _SYMBOL_PATTERN.sub(lambda m: SYMBOLS[m.group(0)], text)


def _expand_english_abbrevs(text: str) -> str:
    return _ENGLISH_ABBREV_PATTERN.sub(
        lambda m: ENGLISH_ABBREVS[m.group(0).lower()], text
    )


def _expand_units(text: str) -> str:
    return _UNIT_PATTERN.sub(lambda m: UNITS[m.group(1)], text)


def _expand_maiyamok(text: str) -> str:
    if "ๆ" not in text:
        return text
    return "".join(_expand_maiyamok_pythainlp(text))


def _thai_numerals_to_arabic(text: str) -> str:
    for thai, arabic in THAI_NUMERAL_MAP.items():
        text = text.replace(thai, arabic)
    return text


def normalize(text: str) -> str:
    """Normalize text for Thai TTS/G2P: convert numbers, abbreviations, and
    special characters to speakable Thai words.

    :param str text: Thai text to normalize
    :return: Normalized speakable Thai text
    :rtype: str

    :Example:

        >>> from pythainlp.transliterate.fastthaig2p import normalize
        >>> normalize("มี 42 คน")
        'มี สี่สิบสอง คน'
        >>> normalize("ราคา 1,000 บาท")
        'ราคา หนึ่งพัน บาท'
        >>> normalize("เด็กๆ")
        'เด็กเด็ก'
    """
    if not text or not isinstance(text, str):
        return ""

    text = _expand_maiyamok(text)
    text = _thai_numerals_to_arabic(text)
    text = _EMAIL_PATTERN.sub(_email_to_thai, text)
    text = _expand_english_abbrevs(text)
    text = _expand_units(text)
    text = _expand_symbols(text)
    text = _TIME_PATTERN.sub(_time_to_thai, text)
    text = _PHONE_PATTERN.sub(_phone_number_to_thai, text)
    text = _ALPHANUM_ID_PATTERN.sub(_alphanum_to_thai, text)
    text = _COMMA_NUMBER_PATTERN.sub(_strip_commas_and_convert, text)
    text = _NUMBER_PATTERN.sub(_number_or_id_to_thai, text)
    text = _expand_abbreviations(text)
    text = _spell_latin_residue(text)
    text = text.replace("-", " ")
    return text


def _tltk_syllable_to_ipa(syl: str) -> str:
    """Convert a single tltk syllable to IPA."""
    tone_digit = syl[-1] if syl and syl[-1] in "01234" else "0"
    if syl and syl[-1] in "01234":
        syl = syl[:-1]
    tone = _TONE_MAP.get(tone_digit, "˧")

    result = syl
    for old, new in _CONSONANT_MAP:
        result = result.replace(old, new)
    for old, new in _VOWEL_MAP:
        result = result.replace(old, new)

    if result and result[-1] in "ktp":
        if any(c in _VOWEL_CHARS for c in result[:-1]):
            result = result[:-1] + result[-1] + "̚"

    return result + tone


def fallback_g2p(word: str) -> str:
    """Generate IPA for a word using rule-based G2P fallback.

    Uses TLTK if installed to generate syllable phonemes and converts
    them to Wiktionary IPA format. When TLTK is not available, returns
    the word as-is.

    :param str word: Thai word
    :return: IPA phonemes or original word
    :rtype: str
    """
    if not word or not isinstance(word, str):
        return ""

    try:
        from tltk.nlp import g2p as tltk_g2p_func

        tltk_result = tltk_g2p_func(word.replace("ฅ", "ค"))
        match = _TLTK_PHON_RE.search(tltk_result)
        if not match:
            return word

        tltk_phon = match.group(1)
        syllables: List[str] = []
        for part in re.split(r"[|~^]", tltk_phon):
            for sp in part.split("'"):
                sp = sp.strip()
                if sp:
                    syllables.append(_tltk_syllable_to_ipa(sp))

        if syllables:
            return "/" + ".".join(syllables) + "/"
        return word
    except (ImportError, Exception):
        return word


class FastThaiG2P:
    """FastThaiG2P: Lightning-fast Thai grapheme-to-phoneme conversion.

    Uses a 4-stage pipeline:
    1. Text normalization: expands numbers, units, abbreviations, emails, etc.
    2. Tokenization: segments normalized text with PyThaiNLP's newmm dictionary engine.
    3. Dictionary lookup: retrieves IPA phonemes from the 62k-word dictionary.
    4. Fallback G2P: handles out-of-vocabulary words using rule-based fallback.
    """

    _ipa: Dict[str, str]
    _tokenizer: Tokenizer

    def __init__(self, ipa_dict_path: Optional[str] = None) -> None:
        """Initialize FastThaiG2P engine.

        :param Optional[str] ipa_dict_path: Optional path to custom IPA dictionary JSON.
            If None, loads the default dictionary from pythainlp.corpus.
        """
        if ipa_dict_path is None:
            corpus_files = files("pythainlp.corpus")
            corpus_file = corpus_files.joinpath("fastthaig2p_ipa.json")
            text = corpus_file.read_text(encoding="utf-8")
        else:
            with open(ipa_dict_path, "r", encoding="utf-8") as f:
                text = f.read()

        self._ipa = json.loads(text)
        self._tokenizer = Tokenizer(
            custom_dict=set(self._ipa.keys()), engine="newmm"
        )

    def convert(self, text: str) -> str:
        """Convert Thai text to IPA phonemes.

        :param str text: Thai text to convert.
        :return: String of IPA phonemes separated by spaces.
        :rtype: str

        :Example:

            >>> from pythainlp.transliterate.fastthaig2p import FastThaiG2P
            >>> g2p = FastThaiG2P()
            >>> g2p.convert("สวัสดีครับ")
            '/sa˨˩.wat̚˨˩.diː˧/ /kʰrap̚˦˥/'
        """
        if not text or not isinstance(text, str):
            return ""

        normalized = normalize(text)
        tokens = self._tokenizer.word_tokenize(normalized)
        phonemes: List[str] = []
        for token in tokens:
            cleaned = token.strip()
            if not cleaned:
                continue
            ipa = self._ipa.get(token)
            if ipa:
                phonemes.append(ipa)
            else:
                phonemes.append(fallback_g2p(token))
        return " ".join(phonemes)


_FAST_THAI_G2P: Optional[FastThaiG2P] = None


def transliterate(text: str) -> str:
    """Transliterate Thai text to IPA phonemes using FastThaiG2P.

    :param str text: Thai text to transliterate
    :return: IPA phonemes
    :rtype: str

    :Example:

        >>> from pythainlp.transliterate.fastthaig2p import transliterate
        >>> transliterate("สวัสดีครับ")
        '/sa˨˩.wat̚˨˩.diː˧/ /kʰrap̚˦˥/'
    """
    global _FAST_THAI_G2P
    if _FAST_THAI_G2P is None:
        _FAST_THAI_G2P = FastThaiG2P()
    return _FAST_THAI_G2P.convert(text)
