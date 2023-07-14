# -*- coding: utf-8 -*-
# Copyright (C) 2016-2023 PyThaiNLP Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import re
from typing import List
from pythainlp import (
    thai_letters,
    thai_consonants,
    thai_lead_vowels,
    thai_follow_vowels,
    thai_above_vowels,
    thai_below_vowels,
    thai_tonemarks
)
from pythainlp.tokenize import Tokenizer
from pythainlp.tokenize import subword_tokenize


_r1=["เ-ย","เ-ะ","แ-ะ","โ-ะ","เ-าะ","เ-อะ","เ-อ","เ-า"]
_r2=["–ั:วะ","เ–ี:ยะ","เ–ือะ","–ั:ว","เ–ี:ย","เ–ื:อ","–ื:อ"]
tonemarks={i:"ไม้"+j for i,j in zip(list(thai_tonemarks),["เอก","โท","ตรี","จัตวา"])}

rule1=[i.replace("-",f"([{thai_letters}](thai_tonemarks)?)") for i in _r1]
rule2=[i.replace("–",f"([{thai_letters}])").replace(":",f"") for i in _r2]
rule3=[i.replace("–",f"([{thai_letters}])").replace(":",f"([{thai_tonemarks}])") for i in _r2]
dict_vowel_ex={}
for i in _r1+_r2:
    dict_vowel_ex[i.replace("-","อ").replace("–","อ").replace(":","")]=i.replace("-","อ").replace(":","").replace("–","อ")
dict_vowel={}
for i in _r1+_r2:
    dict_vowel[i.replace("-","อ").replace("–","อ").replace(":","")]=i.replace("-","อ").replace(":","").replace("–","อ")
for i in thai_lead_vowels:
    dict_vowel[i]=i+"อ"
for i in thai_follow_vowels:
    dict_vowel[i]="อ"+i
for i in thai_above_vowels:
    dict_vowel[i]="อ"+i
for i in thai_below_vowels:
    dict_vowel[i]="อ"+i

_cut=Tokenizer(list(dict_vowel.keys())+list(thai_consonants),engine="mm")


def _clean(w):
    if bool(re.match('|'.join(rule3),w)):
        for r in rule3:
            if bool(re.match(r,w)):
                _w=re.sub(r,"\\1==\\2==",w)
                _temp=_w.split("==")
                w=_temp[0]+r.replace(f"([{thai_letters}])","อ").replace(f"([{thai_tonemarks}])","")+_temp[1]
    elif bool(re.match('|'.join(rule2),w)):
        for r in rule2:
            if bool(re.match(r,w)):
                w=re.sub(r,"\\1",w)+r.replace(f"([{thai_letters}])","อ")
    elif bool(re.match('|'.join(rule1),w)):
        for r in rule1:
            if bool(re.match(r,w)):
                w=re.sub(r,"\\1",w)+r.replace(f"([{thai_letters}](thai_tonemarks)?)","อ")
    return w


def spell_syllable(s: str)-> List[str]:
    """
    Spell syllable by Thai word distribution form.

    :param str s: Thai syllable only
    :return: List of spell syllable
    :rtype: List[str]

    :Example:
    ::

        from pythainlp.util.spell_words import spell_syllable

        print(spell_syllable("แมว"))
        # output: ['มอ', 'วอ', 'แอ', 'แมว']
    """
    _t=s
    s=_cut.word_tokenize(_clean(s))
    _c_only = [i+"อ" for i in s if i in set(thai_consonants)]
    _v_only = [dict_vowel[i] for i in s if i in set(dict_vowel.keys())]
    _t_only = [tonemarks[i] for i in s if i in set(tonemarks.keys())]
    _out=_c_only+_v_only+_t_only
    _out.append(_t)
    return _out


def spell_word(w: str)-> List[str]:
    """
    Spell word by Thai word distribution form.

    :param str w: Thai word only
    :return: List of spell word
    :rtype: List[str]

    :Example:
    ::

        from pythainlp.util.spell_words import spell_word

        print(spell_word("คนดี"))
        # output: ['คอ', 'นอ', 'คน', 'ดอ', 'อี', 'ดี', 'คนดี']
    """
    _r=[]
    _temp=subword_tokenize(w,engine="ssg")
    for i in _temp:
        _r.extend(spell_syllable(i))
    if len(_temp)>1:
        _r.append(w)
    return _r