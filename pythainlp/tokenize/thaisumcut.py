# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileCopyrightText: 2020 Nakhun Chumpolsathien
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""
Tokenize Thai text into sentences with the ThaiSum sentence segmentor.

This is an implementation of the sentence segmentor by
Nakhun Chumpolsathien, 2020. The original code is from
https://github.com/nakhunchumpolsathien/ThaiSum

Cite:

.. code-block:: bibtex

    @mastersthesis{chumpolsathien_2020,
        title={Using Knowledge Distillation from Keyword Extraction
            to Improve the Informativeness of Neural Cross-lingual
            Summarization},
        author={Chumpolsathien, Nakhun},
        year={2020},
        school={Beijing Institute of Technology}
    }
"""

from __future__ import annotations

import math
import re

from pythainlp.tokenize import word_tokenize

_TH_ALPHABETS: str = "([ก-๙])"
_TH_CONJUNCTION: str = "(ทำให้|โดย|เพราะ|นอกจากนี้|แต่|กรณีที่|หลังจากนี้|ต่อมา|ภายหลัง|นับตั้งแต่|หลังจาก|ซึ่งเหตุการณ์|ผู้สื่อข่าวรายงานอีก|ส่วนที่|ส่วนสาเหตุ|ฉะนั้น|เพราะฉะนั้น|เพื่อ|เนื่องจาก|จากการสอบสวนทราบว่า|จากกรณี|จากนี้|อย่างไรก็ดี)"
_TH_CITE: str = "(กล่าวว่า|เปิดเผยว่า|รายงานว่า|ให้การว่า|เผยว่า|บนทวิตเตอร์ว่า|แจ้งว่า|พลเมืองดีว่า|อ้างว่า)"
_TH_KA_KRUB: str = "(ครับ|ค่ะ)"
_TH_STOP_AFTER: str = "(หรือไม่|โดยเร็ว|แล้ว|อีกด้วย)"
_TH_STOP_BEFORE: str = "(ล่าสุด|เบื้องต้น|ซึ่ง|ทั้งนี้|แม้ว่า|เมื่อ|แถมยัง|ตอนนั้น|จนเป็นเหตุให้|จากนั้น|อย่างไรก็ตาม|และก็|อย่างใดก็ตาม|เวลานี้|เช่น|กระทั่ง)"
_DIGIT: str = "([0-9])"
_TH_TITLE: str = "(นาย|นาง|นางสาว|เด็กชาย|เด็กหญิง|น.ส.|ด.ช.|ด.ญ.)"

# Phrases that contain a splitting word.
# Replace them with a placeholder before splitting, and restore them after.
# The order matters: a replacement can change what later ones match.
_PROTECT: tuple[tuple[str, str], ...] = (
    ("โดยเร็ว", "<rth_Doeirew>"),
    ("เพื่อน", "<rth_friend>"),
    ("แต่ง", "<rth_but>"),
    ("โดยสาร", "<rth_passenger>"),
    ("แล้วแต่", "<rth_leawtea>"),
    ("หรือเปล่า", "<rth_repraw>"),
    ("หรือไม่", "<rth_remai>"),
    ("จึงรุ่งเรืองกิจ", "<rth_tanatorn_lastname>"),
    ("ตั้งแต่", "<rth_tangtea>"),
    ("แต่ละ", "<rth_teala>"),
    ("วิตแล้ว", "<rth_chiwitleaw>"),
    ("โดยประ", "<rth_doipra>"),
    ("แต่หลังจากนั้น", "<rth_tealangjaknan>"),
    ("พรรคเพื่อ", "<for_party>"),
    ("แต่เนื่อง", "<rth_teaneung>"),
    ("เพื่อทำให้", "เพื่อ<rth_tamhai>"),
    ("ทำเพื่อ", "ทำ<rth_for>"),
    ("จึงทำให้", "จึง<tamhai>"),
    ("มาโดยตลอด", "<madoitalod>"),
    ("แต่อย่างใด", "<teayangdaikptam>"),
    ("แต่หลังจาก", "แต่<langjak>"),
    ("คงทำให้", "<rth_kongtamhai>"),
    ("แต่ทั้งนี้", "แต่<tangni>"),
    ("มีแต่", "มี<tea>"),
    ("เหตุที่ทำให้", "<hedteetamhai>"),
    ("โดยหลังจาก", "โดย<langjak>"),
    ("ซึ่งหลังจาก", "ซึ่ง<langjak>"),
    ("ตั้งโดย", "<rth_tangdoi>"),
    ("โดยตรง", "<rth_doitong>"),
    ("นั้นหรือ", "<rth_nanhlor>"),
    ("ซึ่งต้องทำให้", "ซึ่งต้อง<tamhai>"),
    ("ชื่อต่อมา", "ชื่อ<tomar>"),
    ("โดยเร่งด่วน", "<doi>เร่งด่วน"),
    ("ไม่ได้ทำให้", "ไม่ได้<tamhai>"),
    ("จะทำให้", "จะ<tamhai>"),
    ("จนทำให้", "จน<tamhai>"),
    ("เว้นแต่", "เว้น<rth_tea>"),
    ("ก็ทำให้", "ก็<tamhai>"),
    (" ณ ตอนนั้น", " ณ <tonnan>"),
    ("บางส่วน", "บาง<rth_suan>"),
    ("หรือแม้แต่", "หรือ<rth_meatea>"),
    ("โดยทำให้", "โดย<tamhai>"),
    ("หรือเพราะ", "หรือ<rth_orbecause>"),
    ("มาแต่", "มา<rth_tea>"),
    ("แต่ไม่ทำให้", "แต่<maitamhai>"),
    ("ฉะนั้นเมื่อ", "ฉะนั้น<rth_moe>"),
    ("เพราะฉะนั้น", "เพราะ<rth_chanan>"),
    ("เพราะหลังจาก", "เพราะ<rth_langjak>"),
    ("สามารถทำให้", "สามารถ<rth_tamhai>"),
    ("อาจทำ", "อาจ<rth_tam>"),
    ("จะทำ", "จะ<rth_tam>"),
    ("และนอกจากนี้", "นอกจากนี้"),
    ("อีกทั้งเพื่อ", "อีกทั้ง<rth_for>"),
    ("ทั้งนี้เพื่อ", "ทั้งนี้<rth_for>"),
    ("เวลาต่อมา", "เวลา<rth_toma>"),
    ("อย่างไรก็ตาม", "อย่างไรก็ตาม"),
    ("อย่างไรก็ตามหลังจาก", "<stop>อย่างไรก็ตาม<rth_langjak>"),
    ("ซึ่งทำให้", "ซึ่ง<rth_tamhai>"),
    ("โดยประมาท", "<doi>ประมาท"),
    ("โดยธรรม", "<doi>ธรรม"),
    ("โดยสัจจริง", "<doi>สัจจริง"),
)

# Restore the placeholders; this is not the exact reverse of _PROTECT.
_RESTORE: tuple[tuple[str, str], ...] = (
    ("<rth_Doeirew>", "โดยเร็ว"),
    ("<rth_friend>", "เพื่อน"),
    ("<rth_but>", "แต่ง"),
    ("<rth_passenger>", "โดยสาร"),
    ("<rth_leawtea>", "แล้วแต่"),
    ("<rth_repraw>", "หรือเปล่า"),
    ("<rth_remai>", "หรือไม่"),
    ("<rth_tanatorn_lastname>", "จึงรุ่งเรืองกิจ"),
    ("<rth_tangtea>", "ตั้งแต่"),
    ("<rth_teala>", "แต่ละ"),
    ("<rth_chiwitleaw>", "วิตแล้ว"),
    ("<rth_doipra>", "โดยประ"),
    ("<rth_tealangjaknan>", "แต่หลังจากนั้น"),
    ("<for_party>", "พรรคเพื่อ"),
    ("<rth_teaneung>", "แต่เนื่อง"),
    ("เพื่อ<rth_tamhai>", "เพื่อทำให้"),
    ("ทำ<rth_for>", "ทำเพื่อ"),
    ("จึง<tamhai>", "จึงทำให้"),
    ("<madoitalod>", "มาโดยตลอด"),
    ("แต่<langjak>", "แต่หลังจาก"),
    ("แต่<tangni>", "แต่ทั้งนี้"),
    ("มี<tea>", "มีแต่"),
    ("<teayangdaikptam>", "แต่อย่างใด"),
    ("<rth_kongtamhai>", "คงทำให้"),
    ("<hedteetamhai>", "เหตุที่ทำให้"),
    ("โดย<langjak>", "โดยหลังจาก"),
    ("ซึ่ง<langjak>", "ซึ่งหลังจาก"),
    ("<rth_tangdoi>", "ตั้งโดย"),
    ("<rth_doitong>", "โดยตรง"),
    ("<rth_nanhlor>", "นั้นหรือ"),
    ("ซึ่งต้อง<tamhai>", "ซึ่งต้องทำให้"),
    ("ชื่อ<tomar>", "ชื่อต่อมา"),
    ("<doi>เร่งด่วน", "โดยเร่งด่วน"),
    ("ไม่ได้<tamhai>", "ไม่ได้ทำให้"),
    ("จะ<tamhai>", "จะทำให้"),
    ("จน<tamhai>", "จนทำให้"),
    ("เว้น<rth_tea>", "เว้นแต่"),
    ("ก็<tamhai>", "ก็ทำให้"),
    (" ณ <tonnan>", " ณ ตอนนั้น"),
    ("บาง<rth_suan>", "บางส่วน"),
    ("หรือ<rth_meatea>", "หรือแม้แต่"),
    ("โดย<tamhai>", "โดยทำให้"),
    ("หรือ<rth_orbecause>", "หรือเพราะ"),
    ("มา<rth_tea>", "มาแต่"),
    ("แต่<maitamhai>", "แต่ไม่ทำให้"),
    ("ฉะนั้น<rth_moe>", "ฉะนั้นเมื่อ"),
    ("เพราะ<rth_chanan>", "เพราะฉะนั้น"),
    ("เพราะ<rth_langjak>", "เพราะหลังจาก"),
    ("สามารถ<rth_tamhai>", "สามารถทำให้"),
    ("อาจ<rth_tam>", "อาจทำ"),
    ("จะ<rth_tam>", "จะทำ"),
    ("อีกทั้ง<rth_for>", "อีกทั้งเพื่อ"),
    ("ทั้งนี้<rth_for>", "ทั้งนี้เพื่อ"),
    ("เวลา<rth_toma>", "เวลาต่อมา"),
    ("อย่างไรก็ตาม<rth_langjak>", "อย่างไรก็ตามหลังจาก"),
    ("ซึ่ง<rth_tamhai>", "ซึ่งทำให้"),
    ("<doi>ประมาท", "โดยประมาท"),
    ("<doi>ธรรม", "โดยธรรม"),
    ("<doi>สัจจริง", "โดยสัจจริง"),
)

# Words that start a new sentence unless a space follows soon after them:
# (keyword, distance from the keyword to the end of the tokens,
# distance from the keyword to the space) in token positions.
_SPLIT_KEYWORDS: tuple[tuple[str, int, int], ...] = (
    ("และ", 3, 5),
    ("หรือ", 3, 4),
    ("จึง", 2, 3),
)

# (pattern, replacement) pairs that mark sentence boundaries with "<stop>".
_BOUNDARY_RULES: tuple[tuple[re.Pattern[str], str], ...] = tuple(
    (re.compile(pattern), repl)
    for pattern, repl in (
        (" " + _TH_STOP_BEFORE, "<stop>\\1"),
        (_TH_KA_KRUB, "\\1<stop>"),
        (_TH_CONJUNCTION, "<stop>\\1"),
        (_TH_CITE, "\\1<stop>"),
        (" " + _DIGIT + "[.]" + _TH_TITLE, "<stop>\\1.\\2"),
        (" " + _DIGIT + _DIGIT + "[.]" + _TH_TITLE, "<stop>\\1\\2.\\3"),
        (_TH_ALPHABETS + _TH_STOP_AFTER + " ", "\\1\\2<stop>"),
    )
)

# Number of words in a sentence above which middle_cut() cuts it.
_MIDDLE_CUT_WORDS = 20


def list_to_string(list: list[str]) -> str:
    """
    Join a list of strings and collapse the whitespace.

    :param list[str] list: list of strings
    :return: joined string
    :rtype: str
    """
    string = "".join(list)
    string = " ".join(string.split())
    return string


def _remove_digit_spaces(sentence: str) -> str:
    """Remove a space before or after a digit."""
    sentence_len = len(sentence)
    for k in range(sentence_len):
        if k == 0 or k + 1 >= sentence_len:
            continue
        if sentence[k].isdigit() and sentence[k - 1] == " ":
            sentence = sentence[: k - 1] + sentence[k:]
            sentence_len = len(sentence)
        if (
            k + 2 <= sentence_len
            and sentence[k].isdigit()
            and sentence[k + 1] == " "
        ):
            sentence = sentence[: k + 1] + sentence[k + 2 :]
            sentence_len = len(sentence)
    return sentence


def _mark_middle_cuts(sentence: str, sentence_size: int) -> str:
    """Replace the spaces nearest to the partition points with "<stop>"."""
    partition = math.floor(sentence_size / _MIDDLE_CUT_WORDS)
    tokens = word_tokenize(sentence, keep_whitespace=True)
    for i in range(partition):
        middle_space = sentence_size / (partition + 1) * (i + 1)
        spaces = [j for j, tok in enumerate(tokens) if tok == " "]
        if spaces:
            nearest = min(spaces, key=lambda j: abs(j - middle_space))
            tokens[nearest] = "<stop>"
    return list_to_string(tokens)


def middle_cut(sentences: list[str]) -> list[str]:
    """
    Split long sentences at the space nearest to the middle.

    :param list[str] sentences: list of sentences
    :return: list of sentences
    :rtype: list[str]
    """
    result_parts = []
    for sentence in sentences:
        sentence_size = len(word_tokenize(sentence, keep_whitespace=False))
        sentence = _remove_digit_spaces(sentence)
        if sentence_size > _MIDDLE_CUT_WORDS:
            result_parts.append(_mark_middle_cuts(sentence, sentence_size))
        else:
            result_parts.append(sentence)

    all_sentences = (
        s.strip() for part in result_parts for s in part.split("<stop>")
    )

    return list(filter(None, all_sentences))


def _find_split_positions(
    tokens: list[str], keyword: str, end_gap: int, near_gap: int
) -> tuple[list[int], list[int]]:
    """
    Find where to put "<stop>" around a keyword.

    :param list[str] tokens: list of words
    :param str keyword: keyword to look for
    :param int end_gap: distance from the keyword to the end of the words
    :param int near_gap: distance from the keyword to the next space
    :return: positions of the spaces to replace with "<stop>",
        and positions to insert "<stop>" before
    :rtype: tuple[list[int], list[int]]
    """
    last_position = len(tokens)
    keyword_position = -1
    space_position = -1
    replace_positions: list[int] = []
    insert_positions: list[int] = []
    for i, tok in enumerate(tokens):
        if tok == keyword:
            keyword_position = i

        if (
            keyword_position != -1
            and i > keyword_position
            and tok == " "
            and space_position == -1
            and i - keyword_position != 1
        ):
            space_position = i

        if (
            keyword_position != -1
            and last_position - keyword_position == end_gap
        ):
            insert_positions.append(last_position)
            keyword_position = -1
            space_position = -1

        if space_position != -1:
            if space_position - keyword_position < near_gap:
                replace_positions.append(space_position)
            else:
                insert_positions.append(keyword_position)
            keyword_position = -1
            space_position = -1
    return replace_positions, insert_positions


def _split_around_keyword(
    text: str, keyword: str, end_gap: int, near_gap: int
) -> str:
    tokens = word_tokenize(text.strip(), keep_whitespace=True)
    replace_positions, insert_positions = _find_split_positions(
        tokens, keyword, end_gap, near_gap
    )
    for position in replace_positions:
        tokens[position] = "<stop>"
    for position in insert_positions:
        tokens.insert(position, "<stop>")
    return list_to_string(tokens)


def _replace_all(text: str, pairs: tuple[tuple[str, str], ...]) -> str:
    for old, new in pairs:
        text = text.replace(old, new)
    return text


def _mark_boundaries(text: str) -> str:
    for pattern, repl in _BOUNDARY_RULES:
        text = pattern.sub(repl, text)
    # Move the closing quote before the final punctuation
    text = text.replace(".”", "”.")
    text = text.replace('."', '".')
    text = text.replace('!"', '"!')
    return text.replace('?"', '"?')


class ThaiSentenceSegmentor:
    """Tokenize Thai text into sentences."""

    def split_into_sentences(
        self, text: str, isMiddleCut: bool = False
    ) -> list[str]:
        """
        Split text into sentences.

        :param str text: text to be tokenized
        :param bool isMiddleCut: also cut long sentences at the middle
        :return: list of sentences
        :rtype: list[str]
        """
        text = f" {text} "
        text = text.replace("\n", " ")
        text = _replace_all(text, _PROTECT)

        for keyword, end_gap, near_gap in _SPLIT_KEYWORDS:
            if keyword in text:
                text = _split_around_keyword(text, keyword, end_gap, near_gap)

        text = _mark_boundaries(text)
        text = _replace_all(text, _RESTORE)
        text = text.replace("?", "?<stop>")
        text = text.replace("!", "!<stop>")
        text = text.replace("<prd>", ".")
        sentences = text.split("<stop>")
        sentences = [s for s in map(str.strip, sentences) if s and s != "nan"]

        if isMiddleCut:
            return middle_cut(sentences)
        return sentences
