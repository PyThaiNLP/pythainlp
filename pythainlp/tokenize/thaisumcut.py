# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-FileCopyrightText: Copyright 2020 Nakhun Chumpolsathien
# SPDX-License-Identifier: Apache-2.0
"""
The implementation of sentence segmentator from Nakhun Chumpolsathien, 2020
original codes are from: https://github.com/nakhunchumpolsathien/ThaiSum

Cite:

@mastersthesis{chumpolsathien_2020,
    title={Using Knowledge Distillation from Keyword Extraction to Improve the Informativeness of Neural Cross-lingual Summarization},
    author={Chumpolsathien, Nakhun},
    year={2020},
    school={Beijing Institute of Technology}
"""

import re
import operator
import math
from typing import List
from pythainlp.tokenize import word_tokenize


def list_to_string(list: List[str]) -> str:
    string = "".join(list)
    string = " ".join(string.split())
    return string


def middle_cut(sentences: List[str]) -> List[str]:
    new_text = ""
    for sentence in sentences:
        sentence_size = len(word_tokenize(sentence, keep_whitespace=False))

        for k in range(0, len(sentence)):
            if k == 0 or k + 1 >= len(sentence):
                continue
            if sentence[k].isdigit() and sentence[k - 1] == " ":
                sentence = sentence[: k - 1] + sentence[k:]
            if k + 2 <= len(sentence):
                if sentence[k].isdigit() and sentence[k + 1] == " ":
                    sentence = sentence[: k + 1] + sentence[k + 2 :]

        fixed_text_lenth = 20

        if sentence_size > fixed_text_lenth:
            partition = math.floor(sentence_size / fixed_text_lenth)
            tokens = word_tokenize(sentence, keep_whitespace=True)
            for i in range(0, partition):
                middle_space = sentence_size / (partition + 1) * (i + 1)
                white_space_index = []
                white_space_diff = {}

                for j in range(len(tokens)):
                    if tokens[j] == " ":
                        white_space_index.append(j)

                for white_space in white_space_index:
                    white_space_diff.update(
                        {white_space: abs(white_space - middle_space)}
                    )

                if len(white_space_diff) > 0:
                    min_diff = min(
                        white_space_diff.items(), key=operator.itemgetter(1)
                    )
                    tokens.pop(min_diff[0])
                    tokens.insert(min_diff[0], "<stop>")
            new_text = new_text + list_to_string(tokens) + "<stop>"
        else:
            new_text = new_text + sentence + "<stop>"

    sentences = new_text.split("<stop>")
    sentences = [s.strip() for s in sentences]
    if "" in sentences:
        sentences.remove("")
    if "nan" in sentences:
        sentences.remove("nan")

    sentences = list(filter(None, sentences))
    return sentences


class ThaiSentenceSegmentor:
    def split_into_sentences(
        self, text: str, isMiddleCut: bool = False
    ) -> List[str]:
        # Declare Variables
        th_alphabets = "([ก-๙])"
        th_conjunction = "(ทำให้|โดย|เพราะ|นอกจากนี้|แต่|กรณีที่|หลังจากนี้|ต่อมา|ภายหลัง|นับตั้งแต่|หลังจาก|ซึ่งเหตุการณ์|ผู้สื่อข่าวรายงานอีก|ส่วนที่|ส่วนสาเหตุ|ฉะนั้น|เพราะฉะนั้น|เพื่อ|เนื่องจาก|จากการสอบสวนทราบว่า|จากกรณี|จากนี้|อย่างไรก็ดี)"
        th_cite = "(กล่าวว่า|เปิดเผยว่า|รายงานว่า|ให้การว่า|เผยว่า|บนทวิตเตอร์ว่า|แจ้งว่า|พลเมืองดีว่า|อ้างว่า)"
        th_ka_krub = "(ครับ|ค่ะ)"
        th_stop_after = "(หรือไม่|โดยเร็ว|แล้ว|อีกด้วย)"
        th_stop_before = "(ล่าสุด|เบื้องต้น|ซึ่ง|ทั้งนี้|แม้ว่า|เมื่อ|แถมยัง|ตอนนั้น|จนเป็นเหตุให้|จากนั้น|อย่างไรก็ตาม|และก็|อย่างใดก็ตาม|เวลานี้|เช่น|กระทั่ง)"
        degit = "([0-9])"
        th_title = "(นาย|นาง|นางสาว|เด็กชาย|เด็กหญิง|น.ส.|ด.ช.|ด.ญ.)"

        text = f" {text} "
        text = text.replace("\n", " ")
        text = text.replace("", "")
        text = text.replace("โดยเร็ว", "<rth_Doeirew>")
        text = text.replace("เพื่อน", "<rth_friend>")
        text = text.replace("แต่ง", "<rth_but>")
        text = text.replace("โดยสาร", "<rth_passenger>")
        text = text.replace("แล้วแต่", "<rth_leawtea>")
        text = text.replace("หรือเปล่า", "<rth_repraw>")
        text = text.replace("หรือไม่", "<rth_remai>")
        text = text.replace("จึงรุ่งเรืองกิจ", "<rth_tanatorn_lastname>")
        text = text.replace("ตั้งแต่", "<rth_tangtea>")
        text = text.replace("แต่ละ", "<rth_teala>")
        text = text.replace("วิตแล้ว", "<rth_chiwitleaw>")
        text = text.replace("โดยประ", "<rth_doipra>")
        text = text.replace("แต่หลังจากนั้น", "<rth_tealangjaknan>")
        text = text.replace("พรรคเพื่อ", "<for_party>")
        text = text.replace("แต่เนื่อง", "<rth_teaneung>")
        text = text.replace("เพื่อทำให้", "เพื่อ<rth_tamhai>")
        text = text.replace("ทำเพื่อ", "ทำ<rth_for>")
        text = text.replace("จึงทำให้", "จึง<tamhai>")
        text = text.replace("มาโดยตลอด", "<madoitalod>")
        text = text.replace("แต่อย่างใด", "<teayangdaikptam>")
        text = text.replace("แต่หลังจาก", "แต่<langjak>")
        text = text.replace("คงทำให้", "<rth_kongtamhai>")
        text = text.replace("แต่ทั้งนี้", "แต่<tangni>")
        text = text.replace("มีแต่", "มี<tea>")
        text = text.replace("เหตุที่ทำให้", "<hedteetamhai>")
        text = text.replace("โดยหลังจาก", "โดย<langjak>")
        text = text.replace("ซึ่งหลังจาก", "ซึ่ง<langjak>")
        text = text.replace("ตั้งโดย", "<rth_tangdoi>")
        text = text.replace("โดยตรง", "<rth_doitong>")
        text = text.replace("นั้นหรือ", "<rth_nanhlor>")
        text = text.replace("ซึ่งต้องทำให้", "ซึ่งต้อง<tamhai>")
        text = text.replace("ชื่อต่อมา", "ชื่อ<tomar>")
        text = text.replace("โดยเร่งด่วน", "<doi>เร่งด่วน")
        text = text.replace("ไม่ได้ทำให้", "ไม่ได้<tamhai>")
        text = text.replace("จะทำให้", "จะ<tamhai>")
        text = text.replace("จนทำให้", "จน<tamhai>")
        text = text.replace("เว้นแต่", "เว้น<rth_tea>")
        text = text.replace("ก็ทำให้", "ก็<tamhai>")
        text = text.replace(" ณ ตอนนั้น", " ณ <tonnan>")
        text = text.replace("บางส่วน", "บาง<rth_suan>")
        text = text.replace("หรือแม้แต่", "หรือ<rth_meatea>")
        text = text.replace("โดยทำให้", "โดย<tamhai>")
        text = text.replace("หรือเพราะ", "หรือ<rth_orbecause>")
        text = text.replace("มาแต่", "มา<rth_tea>")
        text = text.replace("แต่ไม่ทำให้", "แต่<maitamhai>")
        text = text.replace("ฉะนั้นเมื่อ", "ฉะนั้น<rth_moe>")
        text = text.replace("เพราะฉะนั้น", "เพราะ<rth_chanan>")
        text = text.replace("เพราะหลังจาก", "เพราะ<rth_langjak>")
        text = text.replace("สามารถทำให้", "สามารถ<rth_tamhai>")
        text = text.replace("อาจทำ", "อาจ<rth_tam>")
        text = text.replace("จะทำ", "จะ<rth_tam>")
        text = text.replace("และนอกจากนี้", "นอกจากนี้")
        text = text.replace("อีกทั้งเพื่อ", "อีกทั้ง<rth_for>")
        text = text.replace("ทั้งนี้เพื่อ", "ทั้งนี้<rth_for>")
        text = text.replace("เวลาต่อมา", "เวลา<rth_toma>")
        text = text.replace("อย่างไรก็ตาม", "อย่างไรก็ตาม")
        text = text.replace(
            "อย่างไรก็ตามหลังจาก", "<stop>อย่างไรก็ตาม<rth_langjak>"
        )
        text = text.replace("ซึ่งทำให้", "ซึ่ง<rth_tamhai>")
        text = text.replace("โดยประมาท", "<doi>ประมาท")
        text = text.replace("โดยธรรม", "<doi>ธรรม")
        text = text.replace("โดยสัจจริง", "<doi>สัจจริง")

        if "และ" in text:
            tokens = word_tokenize(text.strip(), keep_whitespace=True)
            and_position = -1
            nearest_space_position = -1
            last_position = len(tokens)
            pop_split_position = []
            split_position = []
            for i in range(len(tokens)):
                if tokens[i] == "และ":
                    and_position = i

                if (
                    and_position != -1
                    and i > and_position
                    and tokens[i] == " "
                    and nearest_space_position == -1
                ):
                    if i - and_position != 1:
                        nearest_space_position = i

                if and_position != -1 and last_position - and_position == 3:
                    split_position.append(last_position)
                    and_position = -1
                    nearest_space_position = -1

                if nearest_space_position != -1:
                    if nearest_space_position - and_position < 5:
                        pop_split_position.append(nearest_space_position)
                    else:
                        split_position.append(and_position)
                    and_position = -1
                    nearest_space_position = -1
            for pop in pop_split_position:
                tokens.pop(pop)
                tokens.insert(pop, "<stop>")
            for split in split_position:
                tokens.insert(split, "<stop>")
            text = list_to_string(tokens)

        if "หรือ" in text:
            tokens = word_tokenize(text.strip(), keep_whitespace=True)
            or_position = -1
            nearest_space_position = -1
            last_position = len(tokens)
            pop_split_position = []
            split_position = []
            for i in range(len(tokens)):
                if tokens[i] == "หรือ":
                    or_position = i
                if (
                    or_position != -1
                    and i > or_position
                    and tokens[i] == " "
                    and nearest_space_position == -1
                ):
                    if i - or_position != 1:
                        nearest_space_position = i

                if or_position != -1 and last_position - or_position == 3:
                    split_position.append(last_position)
                    or_position = -1
                    nearest_space_position = -1

                if nearest_space_position != -1:
                    if nearest_space_position - or_position < 4:
                        pop_split_position.append(nearest_space_position)
                    else:
                        split_position.append(or_position)
                    or_position = -1
                    nearest_space_position = -1
            for pop in pop_split_position:
                tokens.pop(pop)
                tokens.insert(pop, "<stop>")
            for split in split_position:
                tokens.insert(split, "<stop>")
            text = list_to_string(tokens)

        if "จึง" in text:
            tokens = word_tokenize(text.strip(), keep_whitespace=True)
            cung_position = -1
            nearest_space_position = -1
            pop_split_position = []
            last_position = len(tokens)
            split_position = []
            for i in range(len(tokens)):
                if tokens[i] == "จึง":
                    cung_position = i

                if (
                    cung_position != -1
                    and tokens[i] == " "
                    and i > cung_position
                    and nearest_space_position == -1
                ):
                    if i - cung_position != 1:
                        nearest_space_position = i

                if cung_position != -1 and last_position - cung_position == 2:
                    split_position.append(last_position)
                    cung_position = -1
                    nearest_space_position = -1

                if nearest_space_position != -1:
                    if nearest_space_position - cung_position < 3:
                        pop_split_position.append(nearest_space_position)
                    else:
                        split_position.append(cung_position)
                    cung_position = -1
                    nearest_space_position = -1

            for pop in pop_split_position:
                tokens.pop(pop)
                tokens.insert(pop, "<stop>")
            for split in split_position:
                tokens.insert(split, "<stop>")

            text = list_to_string(tokens)

        text = re.sub(" " + th_stop_before, "<stop>\\1", text)
        text = re.sub(th_ka_krub, "\\1<stop>", text)
        text = re.sub(th_conjunction, "<stop>\\1", text)
        text = re.sub(th_cite, "\\1<stop>", text)
        text = re.sub(" " + degit + "[.]" + th_title, "<stop>\\1.\\2", text)
        text = re.sub(
            " " + degit + degit + "[.]" + th_title, "<stop>\\1\\2.\\3", text
        )
        text = re.sub(th_alphabets + th_stop_after + " ", "\\1\\2<stop>", text)
        if "”" in text:
            text = text.replace(".”", "”.")
        if '"' in text:
            text = text.replace('."', '".')
        if "!" in text:
            text = text.replace('!"', '"!')
        if "?" in text:
            text = text.replace('?"', '"?')
        text = text.replace("<rth_Doeirew>", "โดยเร็ว")
        text = text.replace("<rth_friend>", "เพื่อน")
        text = text.replace("<rth_but>", "แต่ง")
        text = text.replace("<rth_passenger>", "โดยสาร")
        text = text.replace("<rth_leawtea>", "แล้วแต่")
        text = text.replace("<rth_repraw>", "หรือเปล่า")
        text = text.replace("<rth_remai>", "หรือไม่")
        text = text.replace("<rth_tanatorn_lastname>", "จึงรุ่งเรืองกิจ")
        text = text.replace("<rth_tangtea>", "ตั้งแต่")
        text = text.replace("<rth_teala>", "แต่ละ")
        text = text.replace("<rth_chiwitleaw>", "วิตแล้ว")
        text = text.replace("<rth_doipra>", "โดยประ")
        text = text.replace("<rth_tealangjaknan>", "แต่หลังจากนั้น")
        text = text.replace("<for_party>", "พรรคเพื่อ")
        text = text.replace("<rth_teaneung>", "แต่เนื่อง")
        text = text.replace("เพื่อ<rth_tamhai>", "เพื่อทำให้")
        text = text.replace("ทำ<rth_for>", "ทำเพื่อ")
        text = text.replace("จึง<tamhai>", "จึงทำให้")
        text = text.replace("<madoitalod>", "มาโดยตลอด")
        text = text.replace("แต่<langjak>", "แต่หลังจาก")
        text = text.replace("แต่<tangni>", "แต่ทั้งนี้")
        text = text.replace("มี<tea>", "มีแต่")
        text = text.replace("<teayangdaikptam>", "แต่อย่างใด")
        text = text.replace("<rth_kongtamhai>", "คงทำให้")
        text = text.replace("<hedteetamhai>", "เหตุที่ทำให้")
        text = text.replace("โดย<langjak>", "โดยหลังจาก")
        text = text.replace("ซึ่ง<langjak>", "ซึ่งหลังจาก")
        text = text.replace("<rth_tangdoi>", "ตั้งโดย")
        text = text.replace("<rth_doitong>", "โดยตรง")
        text = text.replace("<rth_nanhlor>", "นั้นหรือ")
        text = text.replace("ซึ่งต้อง<tamhai>", "ซึ่งต้องทำให้")
        text = text.replace("ชื่อ<tomar>", "ชื่อต่อมา")
        text = text.replace("<doi>เร่งด่วน", "โดยเร่งด่วน")
        text = text.replace("ไม่ได้<tamhai>", "ไม่ได้ทำให้")
        text = text.replace("จะ<tamhai>", "จะทำให้")
        text = text.replace("จน<tamhai>", "จนทำให้")
        text = text.replace("เว้น<rth_tea>", "เว้นแต่")
        text = text.replace("ก็<tamhai>", "ก็ทำให้")
        text = text.replace(" ณ <tonnan>", " ณ ตอนนั้น")
        text = text.replace("บาง<rth_suan>", "บางส่วน")
        text = text.replace("หรือ<rth_meatea>", "หรือแม้แต่")
        text = text.replace("โดย<tamhai>", "โดยทำให้")
        text = text.replace("หรือ<rth_orbecause>", "หรือเพราะ")
        text = text.replace("มา<rth_tea>", "มาแต่")
        text = text.replace("แต่<maitamhai>", "แต่ไม่ทำให้")
        text = text.replace("ฉะนั้น<rth_moe>", "ฉะนั้นเมื่อ")
        text = text.replace("เพราะ<rth_chanan>", "เพราะฉะนั้น")
        text = text.replace("เพราะ<rth_langjak>", "เพราะหลังจาก")
        text = text.replace("สามารถ<rth_tamhai>", "สามารถทำให้")
        text = text.replace("อาจ<rth_tam>", "อาจทำ")
        text = text.replace("จะ<rth_tam>", "จะทำ")
        text = text.replace("อีกทั้ง<rth_for>", "อีกทั้งเพื่อ")
        text = text.replace("ทั้งนี้<rth_for>", "ทั้งนี้เพื่อ")
        text = text.replace("เวลา<rth_toma>", "เวลาต่อมา")
        text = text.replace(
            "อย่างไรก็ตาม<rth_langjak>",
            "อย่างไรก็ตามหลังจาก",
        )
        text = text.replace("ซึ่ง<rth_tamhai>", "ซึ่งทำให้")
        text = text.replace("<doi>ประมาท", "โดยประมาท")
        text = text.replace("<doi>ธรรม", "โดยธรรม")
        text = text.replace("<doi>สัจจริง", "โดยสัจจริง")
        text = text.replace("?", "?<stop>")
        text = text.replace("!", "!<stop>")
        text = text.replace("<prd>", ".")
        sentences = text.split("<stop>")
        sentences = [s.strip() for s in sentences]
        if "" in sentences:
            sentences.remove("")
        if "nan" in sentences:
            sentences.remove("nan")

        sentences = list(filter(None, sentences))

        if isMiddleCut:
            return middle_cut(sentences)
        else:
            return sentences
