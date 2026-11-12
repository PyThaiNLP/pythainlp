# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""
TLTK G2P and pronunciation conversion engine re-implemented in pure Python.

Derived from TLTK (Thai Language Toolkit) by Attapol Thamrongrattanarit.
Distributed under the BSD 3-Clause License.
"""

from __future__ import annotations

import gzip
import json
import math
import re
from collections import defaultdict
from copy import deepcopy

from pythainlp.corpus import corpus_path
from pythainlp.tools.path import safe_path_join

SegSep: str = chr(31)
SSegSep: str = chr(30)
WordSep: str = chr(124)
SylSep: str = chr(126)

_LOADED: bool = False

PRON: dict[str, list[str]] = defaultdict(list)
PRONUN: dict[str, list[str]] = defaultdict(list)
stable: dict[str, dict[str, str]] = defaultdict(defaultdict)
AK: dict[str, str] = defaultdict(str)
MKaran: dict[tuple[str, str], int] = defaultdict(int)
EngAbbr: list[str] = []

PhSTrigram: dict[tuple[str, str, str, str], float] = defaultdict(float)
FrmSTrigram: dict[tuple[str, str, str], float] = defaultdict(float)
PhSBigram: dict[tuple[str, str, str], float] = defaultdict(float)
FrmSBigram: dict[tuple[str, str], float] = defaultdict(float)
PhSUnigram: dict[tuple[str, str], float] = defaultdict(float)
FrmSUnigram: dict[str, float] = defaultdict(float)
AbsUnigram: dict[tuple[str, str], float] = defaultdict(float)
AbsFrmSUnigram: dict[str, float] = defaultdict(float)

TriCount: dict[tuple[str, str, str], int] = defaultdict(int)
BiCount: dict[tuple[str, str], int] = defaultdict(int)
BiType: dict[tuple[str, str], int] = defaultdict(int)
Count: dict[str, int] = defaultdict(int)
Type: dict[str, int] = defaultdict(int)
TotalWord: int = 0
TotalLex: int = 0

chart: dict[int, dict[int, list[str]]] = defaultdict(dict)
EndOfSent: int = 0
CollocSt: dict[tuple[int, int], float] = defaultdict(float)
TDICT: set[str] = set()

_CHAR_MAP: dict[str, list[tuple[re.Pattern[str], str, list[str]]]] = (
    defaultdict(list)
)
_WILDCARDS: list[tuple[re.Pattern[str], str, list[str]]] = []

_ENG_ABBR_LIST: list[str] = [
    "เอ",
    "บี",
    "ซี",
    "ดี",
    "อี",
    "เอฟ",
    "จี",
    "เจ",
    "เอช",
    "ไอ",
    "เค",
    "แอล",
    "เอ็ม",
    "เอ็น",
    "โอ",
    "พี",
    "คิว",
    "อาร์",
    "เอส",
    "ที",
    "ยู",
    "วี",
    "เอ็กซ์",
    "เอ็ก",
    "วาย",
    "แซด",
]


def read_sylpattern(Filename: str) -> None:
    global PRON
    global stable
    global AK
    global MKaran
    global EngAbbr

    stable = defaultdict(defaultdict)
    AK = defaultdict(str)
    MKaran = defaultdict(int)
    #    PRON = defaultdict(list)
    #    PRON = defaultdict(str)

    tmp = []
    with open(Filename, encoding="utf-8") as file1:
        for raw_line in file1:
            if re.match(r"#", raw_line):
                continue
            line = raw_line.rstrip()
            tmp = line.split(",")
            tmp[0] = re.sub(r"X", "([ก-ฮ])", tmp[0])
            tmp[0] = re.sub(r"C", "([กขคจดตทบปผพฟสศซ])", tmp[0])
            tmp[0] = re.sub(r"Y", "([ก-ฬฮ])", tmp[0])
            tmp[0] = re.sub(r"R", "([รลว])", tmp[0])
            tmp[0] = re.sub(r"K", "([ก-ฮ])", tmp[0])
            tmp[0] = re.sub(
                r"A", "([กจฆดตบปอขฉฐถผฝศษสหคชพภทธมยรลวนณซญฑฏฌ])", tmp[0]
            )
            tmp[0] = re.sub(r"Z", "([กงดนมบรลฎฏจตณถพศทสชคภปญ])", tmp[0])
            tmp[0] = re.sub(r"D", "([กงดนมบวยต])", tmp[0])
            tmp[0] = re.sub(r"W", "[ก-ฮ]", tmp[0])
            tmp[0] = re.sub(r"\\.", r"[\\.]", tmp[0])
            #        re.sub('Q',u"[\(\)\-\:\'\xCF\xE6]",tmp[0])
            if tmp[2] == "T":
                tmp[0] = re.sub(r"T", "[่้๊๋]", tmp[0])
            else:
                tmp[0] = re.sub(r"T", "[่้๊๋]*", tmp[0])

            #       print tmp[0]
            #        PRON[tmp[0]] = tmp[1]
            PRON[tmp[0]].append(tmp[1])

        #    for f in PRON:
        #        for x in PRON[f]:
        #            print(f,x)
        stable["X"] = {
            "ก": "k",
            "ข": "kh",
            "ฃ": "kh",
            "ค": "kh",
            "ฅ": "kh",
            "ฆ": "kh",
            "ง": "N",
            "จ": "c",
            "ฉ": "ch",
            "ช": "ch",
            "ซ": "s",
            "ฌ": "ch",
            "ญ": "j",
            "ฎ": "d",
            "ฏ": "t",
            "ฐ": "th",
            "ฑ": "th",
            "ฒ": "th",
            "ณ": "n",
            "ด": "d",
            "ต": "t",
            "ถ": "th",
            "ท": "th",
            "ธ": "th",
            "น": "n",
            "บ": "b",
            "ป": "p",
            "ผ": "ph",
            "ฝ": "f",
            "พ": "ph",
            "ฟ": "f",
            "ภ": "ph",
            "ม": "m",
            "ย": "j",
            "ร": "r",
            "ฤ": "r",
            "ล": "l",
            "ฦ": "l",
            "ว": "w",
            "ศ": "s",
            "ษ": "s",
            "ส": "s",
            "ห": "h",
            "ฬ": "l",
            "อ": "?",
            "ฮ": "h",
        }
        stable["Y"] = {
            "ก": "k",
            "ข": "k",
            "ค": "k",
            "ฆ": "k",
            "ง": "N",
            "จ": "t",
            "ฉ": "-",
            "ช": "t",
            "ซ": "t",
            "ฌ": "-",
            "ญ": "n",
            "ฎ": "t",
            "ฏ": "t",
            "ฐ": "t",
            "ฑ": "t",
            "ฒ": "t",
            "ณ": "n",
            "ด": "t",
            "ต": "t",
            "ถ": "t",
            "ท": "t",
            "ธ": "t",
            "น": "n",
            "บ": "p",
            "ป": "p",
            "ผ": "-",
            "ฝ": "-",
            "พ": "p",
            "ฟ": "p",
            "ภ": "p",
            "ม": "m",
            "ย": "j",
            "ร": "n",
            "ฤ": "-",
            "ล": "n",
            "ฦ": "-",
            "ว": "w",
            "ศ": "t",
            "ษ": "t",
            "ส": "t",
            "ห": "-",
            "ฬ": "n",
            "อ": "-",
            "ฮ": "-",
        }

    stable["A"] = stable["X"]
    stable["K"] = stable["X"]
    stable["C"] = stable["X"]
    stable["R"] = stable["X"]
    stable["G"] = stable["X"]
    stable["E"] = stable["X"]

    stable["D"] = stable["Y"]
    stable["Z"] = stable["Y"]
    stable["H"] = stable["Y"]
    stable["F"] = stable["Y"]

    AK["ก"] = "นฎฐณตถบปมรลวษสพหฬ"
    AK["ข"] = "จนณบมยรลฬดตทษภส"
    AK["ค"] = "กชดตนณปมทฑหบ"
    AK["ฆ"] = "กบรสช"
    AK["จ"] = "ณตนมรลทยกด"
    AK["ฉ"] = "กงนบพรลวทม"
    AK["ช"] = "กญนยรลวฎคทบมอ"
    AK["ซ"] = "ล"
    AK["ญ"] = "กภลญ"
    AK["ณ"] = "กร"
    AK["ด"] = "นรมวบ"
    AK["ต"] = "กตนภยรลฆงถบมวฤท"
    AK["ถ"] = "กนลวศพงมร"
    AK["ท"] = "กชนบมยรลวสหงศ"
    AK["ธ"] = "นภมยรวกพช"
    AK["น"] = "กทธฎภมยรวคขปลวห"
    AK["บ"] = "ดรทพม"
    AK["ป"] = "กฐฏณทนภรวศถฎตปยสหด"
    AK["ผ"] = "งจชดนลสวกคณทยรอ"
    AK["ฝ"] = "ร"
    AK["พ"] = "กญนมยลวสหณจธ"
    AK["ภ"] = "ยรคณมฤวน"
    AK["ม"] = "กณตนยรลหศดธมสฆว"
    AK["ย"] = "กดธภวสบศตมนถช"
    AK["ร"] = "กจณดพภมยวสหชตถนบ"
    AK["ล"] = "กคฆดตอบปพมลวห"
    AK["ว"] = "ชณดนพภรลสมยกจฏตทธปฤศหคธ"
    AK["ศ"] = "จณนบรลวศพดธกตมยส"
    AK["ษ"] = "ณฎบภรนคธม"
    AK["ส"] = "กคงดตถนบปพภมยรลวหอจฟสขทธฤ"
    AK["ห"] = "กงพทนรภญนมยรลวบต"
    AK["อ"] = "กงชณดตธนพภมยรลวสศคบฆจทปห"
    AK["ฑ"] = "มสรนค"
    AK["ฐ"] = "กจ"
    AK["ฏ"] = "ก"
    AK["ฌ"] = "ก"

    EngAbbr = [
        "เอ",
        "บี",
        "ซี",
        "ดี",
        "อี",
        "เอฟ",
        "จี",
        "เจ",
        "เอช",
        "ไอ",
        "เค",
        "แอล",
        "เอ็ม",
        "เอ็น",
        "โอ",
        "พี",
        "คิว",
        "อาร์",
        "เอส",
        "ที",
        "ยู",
        "วี",
        "เอ็กซ์",
        "เอ็ก",
        "วาย",
        "แซด",
    ]
    ## cannot add 'ดับบลิว' because it has two syllables


def read_syldict(filename: str) -> None:
    global PRON
    with open(filename, encoding="utf-8") as f:
        for raw_line in f:
            if raw_line.startswith("#"):
                continue
            line = raw_line.rstrip()
            tmp = line.split("\t")
            PRON[tmp[0]].append(tmp[1])


def read_PhSTrigram(filename: str) -> None:
    global \
        PhSTrigram, \
        FrmSTrigram, \
        PhSBigram, \
        FrmSBigram, \
        PhSUnigram, \
        FrmSUnigram, \
        AbsUnigram, \
        AbsFrmSUnigram
    open_fn = gzip.open if filename.endswith(".gz") else open
    with open_fn(filename, "rt", encoding="utf-8") as file_handle:
        for raw_line in file_handle:
            line = raw_line.rstrip().replace("<w>", "|")
            tmp = line.split("\t")
            if len(tmp) < 2:
                continue
            x, ct = tmp[0], tmp[1]
            if "/" not in x:
                continue
            fs, p = x.split("/")
            parts = fs.split("-")
            if len(parts) != 3:
                continue
            x1, x2, x3 = parts
            ct_f = float(ct)
            PhSTrigram[(x1, x2, x3, p)] += ct_f
            FrmSTrigram[(x1, x2, x3)] += ct_f
            PhSBigram[(x1, x2, p)] += ct_f
            FrmSBigram[(x1, x2)] += ct_f
            PhSBigram[(x2, x3, p)] += ct_f
            FrmSBigram[(x2, x3)] += ct_f
            PhSUnigram[(x2, p)] += ct_f
            FrmSUnigram[x2] += ct_f
            abs_x2 = re.sub(r"[่้๊๋]", "", x2)
            abs_x2 = re.sub(r"[ก-ฮ]", "C", abs_x2)
            abs_p = re.sub(r"[0-9]", "", p)
            abs_p = re.sub(r"[^aeio@OuxU]", "C", abs_p)
            AbsUnigram[(abs_x2, abs_p)] += ct_f
            AbsFrmSUnigram[abs_x2] += ct_f


def read_stat_json(filename: str) -> None:
    global TriCount, BiCount, BiType, Count, Type, TotalWord, TotalLex
    with gzip.open(filename, "rt", encoding="utf-8") as f:
        data = json.load(f)
    TriCount = defaultdict(int, {tuple(k): v for k, v in data})
    for (x, y, _z), freq in TriCount.items():
        BiType[(x, y)] += 1
        BiCount[(x, y)] += freq
        Count[y] += freq
    for x, _y in BiCount:
        Type[x] += 1
    for x in Count:
        TotalLex += 1
        TotalWord += Count[x]


def mergekaran1(Lst: list[str]) -> list[str]:
    ####  reconnect karan part to the previous syllable for SylSegment
    #### include merhing pronunciation
    rs = []
    global MKaran
    MKaran.clear()
    Found = "n"
    Lst.reverse()
    for s in Lst:
        if (re.search(r"(.+)[ิุ]์", s) or re.search(r"(.+)์", s)) and len(s) < 4:
            Found = "y"
            x = s
            continue
        if Found == "y":
            for ph in PRONUN[s]:
                if (s + x, ph) not in MKaran:
                    PRONUN[s + x].append(ph)
                    MKaran[(s + x, ph)] = 1
            merged_s = s + x
            rs.append(merged_s)
            Found = "n"
        else:
            rs.append(s)
    rs.reverse()
    return rs


########################################
# calculate proability of each possible output
#  Version 1.6>  expect input = list of forms
########################################


def prob_trisyl(SylLst: list[str]) -> float:
    global TriCount
    global BiCount
    global Count
    global BiType
    global Type
    global TotalWord
    global TotalLex
    global SegSep
    Prob: dict[tuple[str, str, str], float] = defaultdict(float)

    #    SegSep = chr(127)

    pw2 = SegSep
    pw1 = SegSep
    Probx = 1.0

    for w in SylLst:
        if (w, pw1, pw2) in Prob:
            Proba = Prob[(w, pw1, pw2)]
        else:
            Prob[(w, pw1, pw2)] = prob_wb(w, pw1, pw2)
            Proba = Prob[(w, pw1, pw2)]
        #        Probx *= Proba
        Probx += Proba  ## prob is changed to log
        pw2 = pw1
        pw1 = w
    #    print("prob ",SylLst,Probx)

    return Probx


########################################
# p(w | pw2 pw1)   Smoothing trigram prob  Witten-Bell
#######################################


def prob_wb(w: str, pw1: str, pw2: str) -> float:
    global TriCount
    global BiCount
    global Count
    global BiType
    global Type
    global TotalWord
    global TotalLex

    p3 = 0.0
    p2 = 0.0
    p1 = 0.0
    p = 0.0

    #    print("trigram ", '|',pw2,'|',pw1,'|',w)
    #    print("count ",TriCount[(pw2,pw1,w)],BiCount[(pw1,w)],Count[w])
    if TriCount[(pw2, pw1, w)] > 0:
        p3 = float(TriCount[(pw2, pw1, w)]) / float(
            BiCount[(pw2, pw1)] + BiType[(pw2, pw1)]
        )
    if BiCount[(pw1, w)] > 0:
        p2 = float(BiCount[(pw1, w)]) / float((Count[pw1] + Type[pw1]))
    if Count[w] > 0:
        p1 = float(Count[w]) / float(TotalWord + TotalLex)
    #    p = 0.8 * p3 + 0.15 * p2 + 0.04 * p1 + 1.0 / float((TotalWord + TotalLex)**2)
    p = 0.8 * p3 + 0.15 * p2 + 0.1 * p1 + 1.0 / float((TotalWord + TotalLex))
    ### change to log to prevent underflow value which can cause incorrect syllable segmentation
    p = math.log(p)
    #    print('prob',p)

    return p


def preprocess(text: str) -> str:
    global SegSep
    global SSegSep

    text = re.sub(r" +ๆ", r"ๆ", text)
    text = re.sub(
        r"ๆ([^ ])", r"ๆ" + SegSep + r"\1", text
    )  ## add space after ๆ
    #    print('adjust',text,'xxx')

    #    text = re.sub(u"เเ",u"แ",text)
    ####### codes suggested by Arthit Suriyawongkul #####
    NORMALIZE_DICT = [
        ("\u0e40\u0e40", "\u0e41"),  # Sara E + Sara E -> Sara AE
        ("\u0e4d\u0e32", "\u0e33"),  # Nikhahit + Sara AA -> Sara AM
        ("\u0e24\u0e32", "\u0e24\u0e45"),  # Ru + Sara AA -> Ru + Lakkhangyao
        ("\u0e26\u0e32", "\u0e26\u0e45"),  # Lu + Sara AA -> Lu + Lakkhangyao
    ]
    for k, v in NORMALIZE_DICT:
        text = text.replace(k, v)
    ########################################################
    #    print text.encode('raw_unicode_escape')

    ###  handle Thai writing one character one space by deleting each space
    #    pattern = re.compile(r'([ก-ฮเแาำะไใโฯๆ][\ุ\ู\ึ\ั\ี\๊\้\็\่\๋\ิ\ื\์]*) +([ก-ฮเแาำะไใโฯๆ\ุ\ู\ึ\ั\ี\๊\้\็\่\๋\ิ\ื\์]{,2}) +|([ก-ฮเแาำะไใโฯๆ][\ุ\ู\ึ\ั\ี\๊\้\็\่\๋\ิ\ื\์]*) +([ก-ฮเแาำะไใโฯๆ\ุ\ู\ึ\ั\ี\๊\้\็\่\๋\ิ\ื\์]{,2})$')
    pattern = re.compile(
        r"([ก-ฮเแาำะไใโฯๆ][\ุ\ู\ึ\ั\ี\๊\้\็\่\๋\ิ\ื\์]*) +([ก-ฮเแาำะไใโฯๆ][\ุ\ู\ึ\ั\ี\๊\้\็\่\๋\ิ\ื\์]*) +|([ก-ฮเแาำะไใโฯๆ][\ุ\ู\ึ\ั\ี\๊\้\็\่\๋\ิ\ื\์]*) +([ก-ฮเแาำะไใโฯๆ][\ุ\ู\ึ\ั\ี\๊\้\็\่\๋\ิ\ื\์]*)$"
    )
    #    while re.search(pattern, text):
    #       text = re.sub(pattern, r"\1\2", text,count=1)
    text = re.sub(pattern, r"\1\2", text)

    ##### change space\tab between [ET][ET] and [ET]  to be SegSep
    #    text = re.sub(r"([^\s\t\u00A0][\ุ\ู\ึ\ั\ี\๊\้\็\่\๋\ิ\ื\์]*[^\s\t\u00A0][\ุ\ู\ึ\ั\ี\๊\้\็\่\๋\ิ\ื\์]*)[\s\t\u00A0]+([^\s\t\u00A0])",r"\1"+SegSep+r"\2",text)
    text = re.sub(
        r"([^\s\t\u00A0]{3,})[\s\t\u00A0]+([^\s\t\u00A0]+?)",
        r"\1" + SegSep + r"\2",
        text,
    )
    #    print('1. ',text)

    ##### change space\tab between [ET] and [ET][ET]  to be SegSep
    #    text = re.sub(r"([^\s\t\u00A0][\ุ\ู\ึ\ั\ี\๊\้\็\่\๋\ิ\ื\์]*)[\s\t\u00A0]+([^\s\t\u00A0][\ุ\ู\ึ\ั\ี\๊\้\็\่\๋\ิ\ื\์]*[^\s\t\u00A0][\ุ\ู\ึ\ั\ี\๊\้\็\่\๋\ิ\ื\์]*)",r"\1"+SegSep+r"\2",text)
    text = re.sub(
        r"([^\s\t\u00A0]+)[\s\t\u00A0]+([0-9]+)", r"\1" + SegSep + r"\2", text
    )
    text = re.sub(
        r"([^\s\t\u00A0]+?)[\s\t\u00A0]+([^\s\t\u00A0]{3,})",
        r"\1" + SegSep + r"\2",
        text,
    )

    ### handle English and Thai mixed without a space inside $s by adding SSegSep (softSegSep)
    text = re.sub(r"([ก-์][ฯๆ])", r"\1" + SSegSep, text)
    text = re.sub(
        r"([\u0E01-\u0E5B]+\.?)([^\.\u0E01-\u0E5B\u001F]+)",
        r"\1" + SSegSep + r"\2",
        text,
    )
    text = re.sub(
        r"([^\.\u0E01-\u0E5B\u001F]+)([\u0E01-\u0E5B]+)",
        r"\1" + SSegSep + r"\2",
        text,
    )
    text = re.sub(r"(<.+?>)", SSegSep + r"\1", text)
    text = re.sub(
        r"([0-9a-zA-Z\.\-]{2,})([\u0E01-\u0E5B]+)",
        r"\1" + SSegSep + r"\2",
        text,
    )
    text = re.sub(
        r"(\.\.\.+)", r"" + SSegSep + r"\1" + SSegSep, text
    )  #  ....  add SSegSep after that
    #    print("3. ",text)

    return text


#############################################################################################################
### initialization by read syllable patterns, syllable trigrams, and satndard dictionary


def sylparse(Input: str) -> str:  # noqa: C901, CCR001  # phase2-todo
    global SylSep
    global PRON
    global PRONUN

    PRONUN = defaultdict(list)
    schart: dict[int, dict[int, list[str]]] = defaultdict(dict)
    probEnd: dict[tuple[int, int], float] = defaultdict(float)
    schartx: dict[int, dict[int, list[str]]] = {}
    schart.clear()
    probEnd.clear()
    tmp = []

    EndOfInput = len(Input)
    for i in range(EndOfInput):
        Inx = Input[i:]
        first_char = Inx[0]
        candidates = _CHAR_MAP.get(first_char, []) + _WILDCARDS
        for match_regex, f, _ in candidates:
            matchObj = match_regex.match(Inx)
            if matchObj:
                keymatch = matchObj.group()
                try:
                    matchObj.group(3)
                    charmatch = (
                        matchObj.group(1)
                        + " "
                        + matchObj.group(2)
                        + " "
                        + matchObj.group(3)
                    )
                except IndexError:
                    try:
                        matchObj.group(2)
                        charmatch = matchObj.group(1) + " " + matchObj.group(2)
                    except IndexError:
                        try:
                            matchObj.group(1)
                            charmatch = matchObj.group(1)
                        except IndexError:
                            #                            PRONUN[matchObj.group()].append(PRON[f])
                            #                            print("ADD",PRON[f])
                            PRONUN[matchObj.group()].extend(PRON[f])
                k = i + len(matchObj.group())
                schart[i][k] = [matchObj.group()]
                #                print("Match PRON",schart[i][k],i,k)
                #### expand all pronunciations
                for PronF in PRON[f]:
                    #                    print(f,PronF) #....
                    codematch = re.sub(r"[^AKYDZCRX]", "", PronF)
                    if codematch:
                        #                        print("code char",codematch,charmatch)
                        phone = ReplaceSnd(PronF, codematch, charmatch)
                        #                        print("phone",phone)
                        if NotExceptionSyl(
                            codematch, charmatch, keymatch, phone
                        ):
                            (phone, tone) = ToneAssign(
                                keymatch, phone, codematch, charmatch
                            )
                            #                            print('assign tone',tone,' to',keymatch,phone)
                            #                            if (tone < '5'): phone = re.sub(r'8',tone,phone)
                            (keymatch, phone) = TransformSyl(keymatch, phone)
                            if tone < "5":
                                phone = re.sub(r"8", tone, phone)
                                PRONUN["".join(schart[i][k])].append(phone)
                        #                                print("Add",PronF,''.join(schart[i][k]), phone)
                        if re.match(r"ทร", keymatch) and re.match(
                            r"thr", phone
                        ):  #### gen more syllable  ทร   thr => s
                            phone = re.sub(r"thr", "s", phone)
                            PRONUN["".join(schart[i][k])].append(phone)
                    #                            print("Add2",PronF,''.join(schart[i][k]), phone)
                    else:
                        PRONUN["".join(schart[i][k])].append(PronF)
                    #                        print('add',PronF)
                    probEnd[(i, k)] = prob_trisyl(schart[i][k])

    #                codematch = PRON[f]
    #                codematch = re.sub(r"[^AKYDZCRX]","",codematch)
    #                if codematch:
    #                    print("code char",codematch,charmatch)
    #                    phone = ReplaceSnd(PRON[f],codematch,charmatch)
    #                    if  NotExceptionSyl(codematch,charmatch,keymatch,phone):
    #                        (phone,tone) = ToneAssign(keymatch,phone,codematch,charmatch)
    #                        print('assign tone',tone,' to',keymatch)
    #                        if (tone < '5'): phone = re.sub(r'8',tone,phone)
    #                        (keymatch,phone) = TransformSyl(keymatch,phone)
    #                    PRONUN[''.join(schart[i][k])].append(phone)
    #                    print("Add",PRON[f],''.join(schart[i][k]), phone)
    #                    if  re.match(r'ทร',keymatch)  and  re.match(r"thr",phone):            #### gen more syllable  ทร   thr => s
    #                        phone=re.sub(r"thr","s",phone)
    #                        PRONUN[''.join(schart[i][k])].append(phone)
    #                        print("Add2",PRON[f],''.join(schart[i][k]), phone)
    #                    probEnd[(i,k)] = prob_trisyl(schart[i][k])

    for j in range(EndOfInput):
        schartx = deepcopy(schart)
        if j in schart[0]:
            s1 = schart[0][j]
            for k in schart[j]:
                s2 = schart[j][k]
                tmp = mergekaran1(s1 + s2)
                if k not in schart[0]:
                    schartx[0][k] = tmp
                    probEnd[(0, k)] = prob_trisyl(tmp)
                #                        print("Not Found K",tmp,probEnd[(0,k)])
                else:
                    p = prob_trisyl(tmp)
                    #                        print(p,"<>",probEnd[(0,k)])
                    #                        if p >= probEnd[(0,k)]:
                    if p > probEnd[(0, k)]:
                        schartx[0][k] = tmp
                        probEnd[(0, k)] = p
        #                            print("Found K new",tmp,probEnd[(0,k)])
        schart = deepcopy(schartx)
    if EndOfInput in schart[0]:
        return SylSep.join(schart[0][EndOfInput])
    return "<Fail>" + Input + "</Fail>"


def ReplaceSnd(phone: str, codematch: str, charmatch: str) -> str:
    global stable
    snd = phone
    tmp1Lst = charmatch.split(" ")  # get character
    for i, x in enumerate(codematch):
        s = stable[x][tmp1Lst[i]]
        snd = re.sub(x, s, snd)
    snd += "8"
    #     print('Sound',snd)
    return snd


def NotExceptionSyl(
    codematch: str, charmatch: str, form: str, phone: str
) -> bool:
    if re.search(r"\.", form):
        return True
        ##  check pronunciation marked in syllable dict, if it exists and it is different from the current phone, disregard current phone.
    if "CR" in codematch and re.match(
        r"ผ ร|ด ล|ต ล|ท ล|ด ว|ต ว|ท ว|บ ว|ป ว|พ ว|ฟ ว|ผ ว|ส ล|ส ว|ร ร|ศ ล|ศ ว",
        charmatch,
    ):
        return False
    # exception for AK = กย กง ขง คง คม จง จน จก ฉย ชง ดย ดง ดน ดม ถย บย บง บน บม ปง ผม พง ฟย ฟง ฟน ฟม ซย ซง ซน ซม  ถร บล บว ปว พร พว นน ยด คว
    if "AK" in codematch:  # check for leadnng and following consonant
        clst = charmatch.split(" ")
        if clst[1] not in AK[clst[0]]:
            return False

    # Case 1 xัว with sound like "..aw"
    if re.search(r"\u0E31[\0E48-\u0E4B]?ว]", form) and "aw" in phone:
        return False
        # Case 5 check for speller ข Only 3 vowel forms can be used  ัุ   เ
    return not (
        re.search(r"[ก-ฮ] ข", charmatch)
        and not re.search(r"[\u0E38\u0E31\u0E40]", form)
    )


# Case  xร - xon   except  Xรน (กรน ปรน)
"""    if re.search(r'[ก-ฮ] ร$',charmatch) and re.search(r'.an',phone):
        print(codematch,charmatch,form,phone)
        sys.exit()
        return(False)
    return(True)
"""

#######################################
# Tone assign :  ม้าน, maan, codematch XY,  charmatch  ม น,  => return 3
# ToneAssign($keymatch,$phone,$codematch,$charmatch);
#######################################


def ToneAssign(  # noqa: C901, CCR001  # phase2-todo
    keymatch: str, phone: str, codematch: str, charmatch: str
) -> tuple[str, str]:
    #    print("ToneAssign:",keymatch,phone,codematch,charmatch)
    if phone == "":
        return ("", "9")
    lead = ""
    init = ""
    if re.search(r"[0-4]8", phone):  # tone is already assigned
        phone = re.sub(r"([0-4])8", r"\1", phone)
        return (phone, "")
    if "X" in codematch or codematch == "GH" or codematch == "EF":
        lx = charmatch.split(" ")
        lead = ""
        init = lx[0]
    elif re.search(r"AK", codematch) or re.search(r"CR", codematch):
        #        (lead, init, final) = charmatch.split(' ')
        lx = charmatch.split(" ")
        lead = lx[0]
        if len(lx) > 1:
            init = lx[1]

    deadsyll = DeadSyl(phone)
    #    print('dead syallble',phone,deadsyll,lead,init,final)

    ### change + for leading syllable
    if "+'" in phone:
        #        print('found leading',phone,lead)
        if lead in "ผฝถขสหฉศษ" or lead in "กจดตบปอ":
            phone = re.sub(r"\+", "1", phone)
        else:
            phone = re.sub(r"\+", "3", phone)

    #### normal syllable
    if init in "กจดตฎฏบปอ":  # middle consonant
        if deadsyll == "L":
            if re.search(r"\u0E48", keymatch):
                return (phone, "1")  # Maiaek
            if re.search(r"\u0E49", keymatch):
                return (phone, "2")  # Maitoo
            if re.search(r"\u0E4A", keymatch):
                return (phone, "3")  # Maitri
            if re.search(r"\u0E4B", keymatch):
                return (phone, "4")  # Maijatawa
            return (phone, "0")
        if re.search(r"\u0E48", keymatch):
            return (phone, "9")  # Maiaek
        if re.search(r"\u0E49", keymatch):
            return (phone, "2")  # Maitoo
        if re.search(r"\u0E4A", keymatch):
            return (phone, "3")  # Maitri
        if re.search(r"\u0E4B", keymatch):
            return (phone, "4")  # Maijatawa
        return (phone, "1")
    if init in "ขฃฉฐถผฝสศษห":  # high consonant
        if deadsyll == "L":
            if re.search(r"\u0E48", keymatch):
                return (phone, "1")  # Maiaek
            if re.search(r"\u0E49", keymatch):
                return (phone, "2")  # Maitoo
            if re.search(r"\u0E4A", keymatch):
                return (phone, "9")  # Maitri
            if re.search(r"\u0E4B", keymatch):
                return (phone, "9")  # Maijatawa
            return (phone, "4")
        if re.search(r"\u0E48", keymatch):
            return (phone, "9")  # Maiaek
        if re.search(r"\u0E49", keymatch):
            return (phone, "2")  # Maitoo
        if re.search(r"\u0E4A", keymatch):
            return (phone, "9")  # Maitri
        if re.search(r"\u0E4B", keymatch):
            return (phone, "9")  # Maijatawa
        return (phone, "1")
    if (
        init in "งญณนมยรลวฬ" and lead != "" and lead in "ขฃฉฐถผฝสศษห"
    ):  # low consonant single
        #        if lead in 'ขฃฉฐถผฝสศษห':   # lead by high consonant
        if deadsyll == "L":
            if re.search(r"\u0E48", keymatch):
                return (phone, "1")  # Maiaek
            if re.search(r"\u0E49", keymatch):
                return (phone, "2")  # Maitoo
            if re.search(r"\u0E4A", keymatch):
                return (phone, "9")  # Maitri
            if re.search(r"\u0E4B", keymatch):
                return (phone, "9")  # Maijatawa
            return (phone, "4")
        if re.search(r"\u0E48", keymatch):
            return (phone, "9")  # Maiaek
        if re.search(r"\u0E49", keymatch):
            return (phone, "2")  # Maitoo
        if re.search(r"\u0E4A", keymatch):
            return (phone, "9")  # Maitri
        if re.search(r"\u0E4B", keymatch):
            return (phone, "9")  # Maijatawa
        return (phone, "1")
    if (
        init in "งญณนมยรลวฬ" and lead != "" and lead in "กจดตฎฏบปอ"
    ):  # low consonant single
        #        elif lead in 'กจดตฎฏบปอ':  #lead by middle consonant
        if deadsyll == "L":
            if re.search(r"\u0E48", keymatch):
                return (phone, "1")  # Maiaek
            if re.search(r"\u0E49", keymatch):
                return (phone, "2")  # Maitoo
            if re.search(r"\u0E4A", keymatch):
                return (phone, "3")  # Maitri
            if re.search(r"\u0E4B", keymatch):
                return (phone, "4")  # Maijatawa
            return (phone, "0")
        if re.search(r"\u0E48", keymatch):
            return (phone, "9")  # Maiaek
        if re.search(r"\u0E49", keymatch):
            return (phone, "2")  # Maitoo
        if re.search(r"\u0E4A", keymatch):
            return (phone, "3")  # Maitri
        if re.search(r"\u0E4B", keymatch):
            return (phone, "4")  # Maijatawa
        return (phone, "1")
    if init in "คฅฆชฌซฑฒทธพภฟฮงญณนมยรลวฬฤฦ":  # low consonant
        if deadsyll == "L":
            if re.search(r"\u0E48", keymatch):
                return (phone, "2")  # Maiaek
            if re.search(r"\u0E49", keymatch):
                return (phone, "3")  # Maitoo
            if re.search(r"\u0E4A", keymatch):
                return (phone, "9")  # Maitri
            if re.search(r"\u0E4B", keymatch):
                return (phone, "9")  # Maijatawa
            return (phone, "0")
        if re.search(r"[aeiouxOU@][aeiouxOU@]+", phone):  # long vowel
            if re.search(r"\u0E48", keymatch):
                return (phone, "9")  # Maiaek
            if re.search(r"\u0E49", keymatch):
                return (phone, "3")  # Maitoo
            if re.search(r"\u0E4A", keymatch):
                return (phone, "9")  # Maitri
            if re.search(r"\u0E4B", keymatch):
                return (phone, "4")  # Maijatawa
            return (phone, "2")
        # short vowel
        if re.search(r"\u0E48", keymatch):
            return (phone, "2")  # Maiaek
        if re.search(r"\u0E49", keymatch):
            return (phone, "9")  # Maitoo
        if re.search(r"\u0E4A", keymatch):
            return (phone, "9")  # Maitri
        if re.search(r"\u0E4B", keymatch):
            return (phone, "4")  # Maijatawa
        return (phone, "3")
    return (phone, "9")


#########################################
# Check whether it's a dead syllable : input is a pronunciation, return 'D' or 'L'
##########################################


def DeadSyl(phone: str) -> str:
    inx = phone
    inx = re.sub("ch", "C", inx)
    inx = re.sub(r"[0-4]", "", inx)
    if re.search(r"[mnwjlN]8?$", inx):
        return "L"
    if re.search(r"[pktfscC]8?$", inx):
        return "D"
    if re.search(r"([aeiouxOU\@])\1", inx):  # vowel length > 1
        return "L"
    return "D"


def TransformSyl(form: str, phone: str) -> tuple[str, str]:
    # xxY[12]  eeY[12] @@Y[12]  => ลดสระสั้น  ใน Y = [nmN]
    if re.search(r"xx[nmN][12]", phone):
        phone = re.sub(r"xx", "x", phone)
    elif re.search(r"ee[nmN][12]", phone):
        phone = re.sub(r"ee", "e", phone)
    elif re.search(r"@@[nmN][12]", phone):
        phone = re.sub(r"@@", "@", phone)
    # Case 1 อยxxx change sound "?a1'jxxx" to "jxxx"
    if (
        re.search(r"^อย่า$|^อยู่$|^อย่าง$|^อยาก$", form)
        and "'" in phone
        or "ห" in form
        and "ha1" in phone
        and not re.search(r"หนุ$|หก|หท|หพ|หฤ|หโ", form)
    ):
        x = phone.split("'")
        phone = x[-1]
    # Case 3 arti-cluster sound, sound "r" is deleted
    elif (
        re.search(r"[จซศส]ร", form)
        and re.search(r"[cs]r", phone)
        and re.search(r"[^']", phone)
    ):
        phone = re.sub("r", "", phone)
    return (form, phone)


#### word segment and select the most likely pronunciation in a word


def wordparse(Input: str) -> str:  # noqa: CCR001  # phase2-todo
    global TDICT
    global EndOfSent
    global chart
    global SegSep
    global WordSep
    global CollocSt

    maiyamok_find = r"(<tr/>|\|)" + r"([?a-zENOU0-9~'@^]+?)" + r"[|~]ๆ"
    maiyamok_rep = r"\1\2" + WordSep + r"\2"

    part = []
    chart = defaultdict(dict)
    SylSep = "~"
    outx = ""
    chart.clear()
    CollocSt = defaultdict(float)

    part = Input.split(SegSep)
    #    print('part',part,'xxx')
    for inx in part:
        SylLst = inx.split(SylSep)
        EndOfSent = len(SylLst)
        ######### Gen unknown word by set each syllable as a potential word
        #        gen_unknown_thaiw(SylLst)
        for i in range(EndOfSent):
            chart[i][i + 1] = [SylLst[i]]
        #            print("sylchart",i,chart[i][i+1])
        ############################################################
        for i in range(EndOfSent):
            for j in range(i, EndOfSent + 1):
                wrd = "".join(SylLst[i:j])
                if wrd in TDICT:
                    chart[i][j] = ["~".join(SylLst[i:j])]
                    if j > i + 1:  ### more than one syllable, compute St
                        St = 0.0
                        for ii in range(i, j - 1):
                            St += compute_colloc(
                                "mi", SylLst[ii], SylLst[ii + 1]
                            )
                        CollocSt[(i, j)] = (
                            St  #### Compute STrength of the word
                        )
                    else:  ### one sylable word St = 0
                        CollocSt[(i, j)] = 0.0
        if chart_parse():
            outx += WordSep.join(chart[0][EndOfSent])
            outx = outx.replace("~ๆ", "|ๆ")
            outx += "<tr/>"
            outp = []
            for wx in chart[0][EndOfSent]:
                tmp = wx.split(SylSep)
                op = SelectPhones(tmp)
                outp.append(op)
            outx += WordSep.join(outp)
            ### replace duplicate word for ๆ
            outx = re.sub(maiyamok_find, maiyamok_rep, outx)
            return outx
        return "<Fail>" + Input + "</Fail>"
    return ""


## input = list of syllables
## output = syl/pron-syl/pron-syl/pron


def SelectPhones(slst: list[str]) -> str:
    global PRONUN
    p = ""
    out = []
    prmax = 0.0

    slst = ["|", *slst, "|"]
    #   print('slist',slst)
    for i in range(1, len(slst) - 1):
        outp = ""
        prmax = 0.0
        #        if slst[i] == '|': continue
        if len(PRONUN[slst[i]]) == 1:
            out.append(PRONUN[slst[i]][0])
            continue
        for p in PRONUN[slst[i]]:
            pr = ProbPhone(p, slst[i - 1], slst[i], slst[i + 1])
            #                print(slst[i],' pronounce ',p,pr,prmax)
            if (
                pr > prmax
                or pr == prmax
                and re.search(r"'", p)
                and len(p) > len(outp)
            ):
                prmax = pr
                outp = p
        out.append(outp)
        #        print('out',slst[i],out)
    #   print('Select Phone',out)
    return "~".join(out)


####################


def ProbPhone(p: str, pw: str, w: str, nw: str) -> float:
    global PhSTrigram
    global FrmSTrigram
    global PhSBigram
    global FrmSBigram
    global PhSUnigram
    global FrmSUnigram
    global AbsUnigram
    global AbsFrmSUnigram

    p3 = 0.0
    p2 = 0.0
    p1 = 0.0
    p0 = 0.0
    if PhSTrigram[(pw, w, nw, p)] > 0.0:
        p3 = (1.0 + math.log(PhSTrigram[(pw, w, nw, p)])) / (
            1.0 + math.log(FrmSTrigram[(pw, w, nw)])
        )
    #        print('Trigram',pw,w,nw,p,PhSTrigram[(pw,w,nw,p)],"=>",p3)
    if PhSBigram[(pw, w, p)] > 0.0:
        p2 = (
            (1.0 + math.log(PhSBigram[(pw, w, p)]))
            / (1.0 + math.log(FrmSBigram[(pw, w)]))
            * 0.25
        )
    #        print('Bigram1',pw,w,p,PhSBigram[(pw,w,p)],"=>",p2)
    ### check w and next w because following syllable is important to determine the linking sound  give it more weigth x 3/4
    if PhSBigram[(w, nw, p)] > 0.0:
        p2 = (
            p2
            + (1.0 + math.log(PhSBigram[(w, nw, p)]))
            / (1.0 + math.log(FrmSBigram[(w, nw)]))
            * 0.75
        )
    #        print('Bigram2',w,nw,p,PhSBigram[(w,nw,p)],"=>",p2)
    if PhSUnigram[(w, p)] > 0.0:
        p1 = (1 + math.log(PhSUnigram[(w, p)])) / (
            1.0 + math.log(FrmSUnigram[w])
        )
    #        print('Unigram',w,p,PhSUnigram[(w,p)],"=>",p1)

    #    prob =  0.8*p3 + 0.16*p2 + 0.03*p1 + 0.00000000001
    #    return(prob)
    ### get abstract form of sounds

    abs_w = re.sub(r"[่้๊๋]", "", w)
    abs_w = re.sub(r"[ก-ฮ]", "C", abs_w)
    abs_p = re.sub(r"[0-9]", "", p)
    abs_p = re.sub(r"[^aeio@OuxU]", "C", abs_p)
    if AbsUnigram[(abs_w, abs_p)] > 0.0:
        p0 = (1 + math.log(AbsUnigram[(abs_w, abs_p)])) / (
            1.0 + math.log(AbsFrmSUnigram[abs_w])
        )
    #        print('AbsUnigram',p0)
    prob = 0.8 * p3 + 0.16 * p2 + 0.03 * p1 + 0.00001 * p0 + 0.00000000001
    #    print(prob)
    return prob


#############


def g2p(Input: str) -> str:
    global SegSep
    global SSegSep
    output = ""
    out = ""

    Input = preprocess(Input)
    sentLst = Input.split(SegSep)
    for s in sentLst:
        inLst = s.split(SSegSep)
        for inp in inLst:
            if inp == "":
                continue
            objMatch = re.match(r"[^ก-์]+", inp)
            if objMatch:
                out = inp + "<tr/>" + inp
            else:
                y = sylparse(inp)
                out = wordparse(y)
            output = output + out + WordSep
        output = output + "<s/>"  ####write <s/> output for SegSep
    return output


## return all transcriptions based on syllable parse


def th2ipa(txt: str) -> str:
    out = ""
    NORMALIZE_IPA = [
        ("O", "\u1d10"),
        ("x", "\u025b"),
        ("@", "\u0264"),
        ("N", "\u014b"),
        ("?", "\u0294"),
        ("U", "\u026f"),
        ("|", " "),
        ("~", "."),
        ("^", "."),
        ("'", "."),
        ("4", "5"),
        ("3", "4"),
        ("2", "3"),
        ("1", "2"),
        ("0", "1"),
    ]
    inx = g2p(txt)
    for seg in inx.split("<s/>"):
        if seg == "":
            continue
        (th, tran) = seg.split("<tr/>")
        tran = re.sub(r"([aeiouUxO@])\1", r"\1ː", tran)
        tran = re.sub(r"([ptkc])h", r"\1ʰ", tran)
        for k, v in NORMALIZE_IPA:
            tran = tran.replace(k, v)
        out += tran + "<s/>"
    return out


def th2roman(txt: str) -> str:
    out = ""
    NORMALIZE_ROM = [
        ("O", "o"),
        ("x", "ae"),
        ("@", "oe"),
        ("N", "ng"),
        ("U", "ue"),
        ("aw", "ao"),
        ("iw", "io"),
        ("ew", "eo"),
        ("?", ""),
        ("|", " "),
        ("~", "-"),
        ("^", "-"),
        ("'", "-"),
    ]
    inx = g2p(txt)
    for seg in inx.split("<s/>"):
        if seg == "":
            continue
        (th, tran) = seg.split("<tr/>")
        tran = re.sub(r"([aeiouUxO@])\1", r"\1", tran)
        tran = re.sub(r"[0-9]", r"", tran)
        for k, v in NORMALIZE_ROM:
            tran = tran.replace(k, v)
        tran = re.sub(r"([aeiou])j", r"\1i", tran)
        tran = tran.replace("j", "y")
        tran = re.sub(r"c([^h])", r"ch\1", tran)
        tran = re.sub(r"\-([^aeiou])", r"\1", tran)
        out += tran + "<s/>"
    return out


### end of modules used in g2p  ###############
##############################################################################################################


####################################################################
##  spelling variant of the same pronunciation
####################################################################


def chart_parse() -> int:
    global chart
    global CollocSt

    for j in range(EndOfSent):
        chartx = deepcopy(chart)
        if j in chart[0]:
            s1 = chart[0][j]
            for k in chart[j]:
                s2 = chart[j][k]
                if k not in chart[0]:
                    chartx[0][k] = s1 + s2
                    #                        CollocSt[(0,k)] = (CollocSt[(0,j)] + CollocSt[(j,k)])/2.0
                    CollocSt[(0, k)] = CollocSt[(0, j)] + CollocSt[(j, k)]
                else:
                    if CollocSt[(0, j)] + CollocSt[(j, k)] > CollocSt[(0, k)]:
                        #                            CollocSt[(0,k)] = (CollocSt[(0,j)] + CollocSt[(j,k)])/2.0
                        CollocSt[(0, k)] = CollocSt[(0, j)] + CollocSt[(j, k)]
                        chartx[0][k] = s1 + s2
        chart = deepcopy(chartx)
    if EndOfSent in chart[0]:
        return 1
    return 0


#############################################################################################################
###  Syllable Segmentation for Thai texts
### Input = a paragraph of Thai texts


def compute_colloc(stat: str, w1: str, w2: str) -> float:
    global TriCount
    global BiCount
    global Count
    global BiType
    global Type
    global TotalWord
    global TotalLex

    if BiCount[(w1, w2)] < 1 or Count[w1] < 1 or Count[w2] < 1:
        BiCount[(w1, w2)] += 1
        Count[w1] += 1
        Count[w2] += 1
        TotalWord += 2
    #    print(w1,w2,Count[w1],Count[w2],BiCount[(w1,w2)],TotalWord)
    ###########################
    ##  Mutual Information
    ###########################
    if stat == "mi":
        mi = float(BiCount[(w1, w2)] * TotalWord) / float(
            (Count[w1] * Count[w2])
        )
        value = abs(math.log2(mi))
    #########################
    ### Compute Chisquare
    ##########################
    if stat == "chi2":
        value = 0
        O11 = BiCount[(w1, w2)]
        O21 = Count[w2] - BiCount[(w1, w2)]
        O12 = Count[w1] - BiCount[(w1, w2)]
        O22 = TotalWord - Count[w1] - Count[w2] + BiCount[(w1, w2)]
        value = float(TotalWord * (O11 * O22 - O12 * O21) ** 2) / float(
            (O11 + O12) * (O11 + O21) * (O12 + O22) * (O21 + O22)
        )

    return value


def _index_patterns() -> None:
    global _CHAR_MAP, _WILDCARDS
    _CHAR_MAP.clear()
    _WILDCARDS.clear()
    for p, pron_list in PRON.items():
        compiled = re.compile(p)
        first = p[0]
        if first not in ("(", "[", "^", ".", "\\"):
            _CHAR_MAP[first].append((compiled, p, pron_list))
        else:
            _WILDCARDS.append((compiled, p, pron_list))


def _ensure_loaded() -> None:
    global _LOADED, TDICT
    if _LOADED:
        return
    base = safe_path_join(corpus_path(), "tltk")
    read_sylpattern(safe_path_join(base, "sylrule.lts"))
    read_syldict(safe_path_join(base, "thaisyl.dict"))
    read_PhSTrigram(safe_path_join(base, "PhSTrigram.sts.gz"))
    read_stat_json(safe_path_join(base, "sylseg.3g.json.gz"))
    with gzip.open(
        safe_path_join(base, "thdict.txt.gz"), "rt", encoding="utf-8"
    ) as f:
        TDICT = set(f.read().splitlines())
    _index_patterns()
    _LOADED = True


def tltk_g2p_native(text: str) -> str:
    _ensure_loaded()
    return g2p(text)


def tltk_th2ipa_native(text: str) -> str:
    _ensure_loaded()
    return th2ipa(text)


def tltk_th2roman_native(text: str) -> str:
    _ensure_loaded()
    return th2roman(text)


def mergekaran(lst: list[str]) -> list[str]:
    rs: list[str] = []
    found = "n"
    lst_rev = list(reversed(lst))
    x = ""
    for s in lst_rev:
        if (re.search(r"(.+)[ิุ]์", s) or re.search(r"(.+)์", s)) and len(s) < 4:
            found = "y"
            x = s
            continue
        if found == "y":
            merged = s + x
            rs.append(merged)
            found = "n"
        else:
            rs.append(s)
    rs.reverse()
    return rs


def sylseg(input_text: str) -> str:  # noqa: CCR001  # phase2-todo
    schart: dict[int, dict[int, list[str]]] = defaultdict(dict)
    prob_end: dict[tuple[int, int], float] = defaultdict(float)

    end_of_input = len(input_text)
    for i in range(end_of_input):
        inx = input_text[i:]
        first_char = inx[0]
        candidates = _CHAR_MAP.get(first_char, []) + _WILDCARDS
        for match_regex, _f, _ in candidates:
            match_obj = match_regex.match(inx)
            if match_obj:
                k = i + len(match_obj.group())
                schart[i][k] = [match_obj.group()]
                prob_end[(i, k)] = prob_trisyl([match_obj.group()])

    for j in range(end_of_input):
        schartx = {idx: dict(row) for idx, row in schart.items()}
        if j in schart[0]:
            s1 = schart[0][j]
            for k in schart[j]:
                s2 = schart[j][k]
                tmp = mergekaran(s1 + s2)
                if k not in schart[0]:
                    schartx[0][k] = tmp
                    prob_end[(0, k)] = prob_trisyl(tmp)
                else:
                    p = prob_trisyl(tmp)
                    if p > prob_end[(0, k)]:
                        schartx[0][k] = tmp
                        prob_end[(0, k)] = p
        schart = defaultdict(dict, schartx)
    if end_of_input in schart[0]:
        return SylSep.join(schart[0][end_of_input])
    return "<Fail>" + input_text + "</Fail>"


def tltk_syl_segment_native(input_text: str) -> str:
    _ensure_loaded()
    output = ""
    input_text = preprocess(input_text)
    sent_lst = input_text.split(SegSep)
    for s in sent_lst:
        in_lst = s.split(SSegSep)
        for inp in in_lst:
            if inp == "":
                continue
            obj_match = re.match(r"[^ก-์]+", inp)
            if obj_match:
                out = inp
            else:
                out = sylseg(inp)
            output = output + out + SylSep
        output = output + "<s/>"
    return output


def _gen_unknown_w(
    syl_lst: list[str],
    cur_chart: dict[int, dict[int, list[str]]],
    end_idx: int,
) -> int:
    for i in range(end_idx):
        cur_chart[i][i + 1] = [syl_lst[i]]
        if syl_lst[i] not in TDICT:
            for j in range(i + 1, end_idx):
                if syl_lst[j] not in TDICT:
                    newwrd = "".join(syl_lst[i : j + 1])
                    cur_chart[i][j + 1] = [newwrd]
                else:
                    break
    return 1


def _eng_abbr(
    syl_lst: list[str],
    cur_chart: dict[int, dict[int, list[str]]],
    end_idx: int,
) -> int:
    i = 0
    while i < end_idx - 1:
        if syl_lst[i] in _ENG_ABBR_LIST:
            j = i + 1
            while j < end_idx and syl_lst[j] in _ENG_ABBR_LIST:
                j = j + 1
            if j > i + 1:
                cur_chart[i][j] = ["".join(syl_lst[i:j])]
                i = j + 1
            i = i + 1
        else:
            i = i + 1
    return 1


def wordseg_colloc(input_text: str) -> str:  # noqa: CCR001  # phase2-todo
    global EndOfSent, chart, CollocSt
    part = input_text.split(SegSep)
    outx = ""
    for inx in part:
        syl_lst = tltk_syl_segment_native(inx).split("~")
        if syl_lst[-1] == "<s/>":
            syl_lst.pop()
        end_of_sent = len(syl_lst)
        EndOfSent = end_of_sent
        chart = defaultdict(dict)
        CollocSt = defaultdict(float)
        _gen_unknown_w(syl_lst, chart, end_of_sent)
        _eng_abbr(syl_lst, chart, end_of_sent)
        for i in range(end_of_sent):
            for j in range(i, end_of_sent + 1):
                wrd = "".join(syl_lst[i:j])
                if wrd in TDICT:
                    chart[i][j] = [wrd]
                    if j > i + 1:
                        st = 0.0
                        for ii in range(i, j - 1):
                            st += compute_colloc(
                                "mi", syl_lst[ii], syl_lst[ii + 1]
                            )
                        CollocSt[(i, j)] = st
                    else:
                        CollocSt[(i, j)] = 0.0
        if chart_parse():
            outx += WordSep.join(chart[0][end_of_sent])
            return outx
        return "<Fail>" + input_text + "</Fail>"
    return outx


def tltk_word_segment_native(input_text: str) -> str:
    _ensure_loaded()
    output = ""
    out = ""
    input_text = preprocess(input_text)
    sent_lst = input_text.split(SegSep)
    for s in sent_lst:
        in_lst = s.split(SSegSep)
        for inp in in_lst:
            if inp == "":
                continue
            obj_match = re.match(r"[^ก-์]+", inp)
            if obj_match:
                out = inp
            else:
                out = wordseg_colloc(inp)
            output = output + out + WordSep
        output = output + "<s/>"
    return output
