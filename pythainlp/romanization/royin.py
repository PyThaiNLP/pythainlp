# -*- coding: utf-8 -*-

import re

# สระ
_vowel_patterns = """เ*ียว,\\1iao
แ*็ว,\\1aeo
เ*ือย,\\1ueai
แ*ว,\\1aeo
เ*็ว,\\1eo
เ*ว,\\1eo
*ิว,\\1io
*วย,\\1uai
เ*ย,\\1oei
*อย,\\1oi
โ*ย,\\1oi
*ุย,\\1ui
*าย,\\1ai
ไ*ย,\\1ai
*ัย,\\1ai
ไ*,\\1ai
ใ*,\\1ai
*ว*,\\1ua\\2
*ัวะ,\\1ua
*ัว,\\1ua
เ*ือะ,\\1uea
เ*ือ,\\1uea
เ*ียะ,\\1ia
เ*ีย,\\1ia
เ*อะ,\\1oe
เ*อ,\\1oe
เ*ิ,\\1oe
*อ,\\1o
เ*าะ,\\1o
เ*็,\\1e
โ*ะ,\\1o
โ*,\\1o
แ*ะ,\\1ae
แ*,\\1ae
เ*าะ,\\1e
*าว,\\1ao
เ*า,\\1ao
เ*,\\1e
*ู,\\1u
*ุ,\\1u
*ื,\\1ue
*ึ,\\1ue
*ี,\\1i
*ิ,\\1i
*ำ,\\1am
*า,\\1a
*ั,\\1a
*ะ,\\1a
#ฤ,\\1rue
$ฤ,\\1ri"""
_vowel_patterns = _vowel_patterns.replace("*", "([ก-ฮ])")
_vowel_patterns = _vowel_patterns.replace("#", "([คนพมห])")
_vowel_patterns = _vowel_patterns.replace("$", "([กตทปศส])")

_VOWELS = [x.split(",") for x in _vowel_patterns.split("\n")]

# พยัญชนะ ต้น สะกด
_CONSONANTS = {
    "ก": ["k", "k"],
    "ข": ["kh", "k"],
    "ฃ": ["kh", "k"],
    "ค": ["kh", "k"],
    "ฅ": ["kh", "k"],
    "ฆ": ["kh", "k"],
    "ง": ["ng", "ng"],
    "จ": ["ch", "t"],
    "ฉ": ["ch", "t"],
    "ช": ["ch", "t"],
    "ซ": ["s", "t"],
    "ฌ": ["ch", "t"],
    "ญ": ["y", "n"],
    "ฎ": ["d", "t"],
    "ฏ": ["t", "t"],
    "ฐ": ["th", "t"],
    # ฑ พยัญชนะต้น เป็น d ได้
    "ฑ": ["th", "t"],
    "ฒ": ["th", "t"],
    "ณ": ["n", "n"],
    "ด": ["d", "t"],
    "ต": ["t", "t"],
    "ถ": ["th", "t"],
    "ท": ["th", "t"],
    "ธ": ["th", "t"],
    "น": ["n", "n"],
    "บ": ["b", "p"],
    "ป": ["p", "p"],
    "ผ": ["ph", "p"],
    "ฝ": ["f", "p"],
    "พ": ["ph", "p"],
    "ฟ": ["f", "p"],
    "ภ": ["ph", "p"],
    "ม": ["m", "m"],
    "ย": ["y", ""],
    "ร": ["r", "n"],
    "ฤ": ["rue", ""],
    "ล": ["l", "n"],
    "ว": ["w", ""],
    "ศ": ["s", "t"],
    "ษ": ["s", "t"],
    "ส": ["s", "t"],
    "ห": ["h", ""],
    "ฬ": ["l", "n"],
    "อ": ["", ""],
    "ฮ": ["h", ""],
}

_RE_CONSONANT = re.compile(r"[ก-ฮ]")
_RE_KARAN = re.compile(r"จน์|มณ์|ณฑ์|ทร์|ตร์|[ก-ฮ]์|[ก-ฮ][ะ-ู]์")
_RE_KARAN2 = re.compile(r"\w" + r"์")
_RE_YAMOK_PAIYANNOI = re.compile(r"[ๆฯ]")
_RE_TONE = re.compile(r"[่-๋]")


def _normalize(text):
    """ตัดอักษรที่ไม่ออกเสียง (การันต์ ไปยาลน้อย ไม้ยมก*) และวรรณยุกต์ทิ้ง"""
    text = _RE_KARAN.sub("", text)
    text = _RE_YAMOK_PAIYANNOI.sub("", text)
    text = _RE_TONE.sub("", text)
    if re.search(_RE_KARAN2, text):
        karans = re.findall(_RE_KARAN2, text)
        for karan in karans:
            text = re.sub(karan, "", text)
    return text


def _replace_vowels(word):
    for vowel in _VOWELS:
        word = re.sub(vowel[0], vowel[1], word)

    return word


def _replace_consonants(word, res):
    if res is None:
        pass
    elif len(res) == 1:
        word = word.replace(res[0], _CONSONANTS[res[0]][0])
    else:
        i = 0
        lenword = len(res)
        while i < lenword:
            if i == 0 and res[0] == "ห":
                word = word.replace(res[0], _CONSONANTS[res[0]][0])
                i += 1
            elif i == 0 and res[0] != "ห":
                word = word.replace(res[0], _CONSONANTS[res[0]][0])
                i += 1
            elif res[i] == "ร" and (word[i] == "ร" and len(word) == i + 1):
                word = word.replace(res[i], _CONSONANTS[res[i]][1])
            elif res[i] == "ร" and (word[i] == "ร" and word[i + 1] == "ร"):
                word = list(word)
                del word[i + 1]
                if i + 2 == lenword:
                    word[i] = "an"
                else:
                    word[i] = "a"
                word = "".join(word)
                i += 1
            else:
                word = word.replace(res[i], _CONSONANTS[res[i]][1])
                i += 1
    return word


def romanize(word):
    word2 = _replace_vowels(_normalize(word))
    res = re.findall(_RE_CONSONANT, word2)
    # 2-character word, all consonants
    if len(word2) == 2 and len(res) == 2:
        word2 = list(word2)
        word2.insert(1, "o")
        word2 = "".join(word2)
    word2 = _replace_consonants(word2, res)
    return word2


if __name__ == "__main__":
    print(romanize("กร") == romanize("กอน"))
