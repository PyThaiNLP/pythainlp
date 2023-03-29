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
"""
Phonemes util
"""
import unicodedata
from pythainlp.util.trie import Trie
from pythainlp.tokenize import Tokenizer

consonants_ipa_nectec = [
    ("k","k","k^"),
    ("kʰ","kh"),
    ("ŋ","ng","ng^"),
    ("tɕ","c"),
    ("tɕʰ","ch"),
    ("s","s"),
    ("j","j","j^"),
    ("d","d"),
    ("t","y","t^"),
    ("tʰ","th"),
    ("n","n","n^"),
    ("b","b"),
    ("p","p","p^"),
    ("pʰ","ph"),
    ("f","f"),
    ("m","m","m^"),
    ("r","r"),
    ("l","l"),
    ("w","w","w^"),
    ("h","h"),
    ("?","z","z^")
]
# ipa, initial, final

monophthong_ipa_nectec = [
    ("i","i"),
    ("e","e"),
    ("ɛ","x"),
    ("ɤ","q"),
    ("a","a"),
    ("am","am^"),
    ("aj","aj^"),
    ("aw","aw^"),
    ("u","u"),
    ("o","o"),
    ("ɔ","@"),
    ("ii","ii"),
    ("ee","ee"),
    ("ɛɛ","xx"),
    ("ɯɯ","vv"),
    ("ɤɤ","qq"),
    ("aa","aa"),
    ("uu","uu"),
    ("oo","oo"),
    ("","@@"), #-อ long
]

diphthong_ipa_nectec = [
    ("ia","ia"),
    ("ɯa","va"),
    ("ua","ua"),
    ("iia","iia"),
    ("ɯɯa","vva"),
    ("uua","uua"),
]

tones_ipa_nectec = [
    ("˧","0"),
    ("˨˩","1"),
    ("˥˩","2"),
    ("˦˥","3"),
    ("˩˩˦","4"),
]

dict_nectec_to_ipa = {i[1]:i[0] for i in consonants_ipa_nectec+monophthong_ipa_nectec+diphthong_ipa_nectec+tones_ipa_nectec}
dict_nectec_to_ipa.update({i[2]:i[0] for i in consonants_ipa_nectec if len(i)>2})


def nectec_to_ipa(pronunciation: str) -> str:
    """
    Converter NECTEC system to IPA system

    :param str pronunciation: NECTEC phoneme
    :return: IPA that be convert
    :rtype: str

    :Example:
    ::

        from pythainlp.util import nectec_to_ipa
 
        print(nectec_to_ipa("kl-uua-j^-2"))
        # output : 'kl uua j ˥˩'


    References
    ----------

    Pornpimon Palingoon, Sumonmas Thatphithakkul. Chapter 4 Speech processing and Speech corpus. In: Handbook of Thai Electronic Corpus. 1st ed. p. 122–56.
    """
    pronunciation = pronunciation.split("-")
    _temp = []
    for i in pronunciation:
        if i in dict_nectec_to_ipa.keys():
            _temp.append(dict_nectec_to_ipa[i])
        else:
            _temp.append(i)
    return ' '.join(_temp)


dict_ipa_rtgs = {
    "b":"b",
    "d":"d",
    "f":"f",
    "h":"h",
    "j":"y",
    "k":"k",
    "kʰ":"kh",
    "l":"l",
    "m":"m",
    "n":"n",
    "ŋ":"ng",
    "p":"p",
    "pʰ":"ph",
    "r":"r",
    "s":"s",
    "t":"t",
    "tʰ":"th",
    "tɕ":"ch",
    "tɕʰ":"ch",
    "w":"w",
    "ʔ":"",
    "j":"i",
    "a":"a",
    "e":"e",
    "ɛ":"ae",
    "i":"i",
    "o":"o",
    "ɔ":"o",
    "u":"u",
    "ɯ":"ue",
    "ɤ":"oe",
    "aː":"a",
    "eː":"e",
    "ɛː":"ae",
    "iː":"i",
    "oː":"o",
    "ɔː":"o",
    "uː":"u",
    "ɯː":"ue",
    "ɤː":"oe",
    "ia":"ia",
    "ua":"ua",
    "ɯa":"uea",
    "aj":"ai",
    "aw":"ao",
    "ew":"eo",
    "ɛw":"aeo",
    "iw":"io",
    "ɔj":"io",
    "uj":"ui",
    "aːj":"ai",
    "aːw":"ao",
    "eːw":"eo",
    "ɛːw":"aeo",
    "oːj":"oi",
    "ɔːj":"oi",
    "ɤːj":"oei",
    "iaw":"iao",
    "uaj":"uai",
    "ɯaj":"ueai",
    ".":".",
}

dict_ipa_rtgs_final = {
    "w":"o"
}
trie = Trie(list(dict_ipa_rtgs.keys())+list(dict_ipa_rtgs_final.keys()))
ipa_cut = Tokenizer(custom_dict=trie, engine="newmm")


def ipa_to_rtgs(ipa: str) -> str:
    """
    Converter IPA system to The Royal Thai General System of Transcription (RTGS)

    Docs: https://en.wikipedia.org/wiki/Help:IPA/Thai

    :param str ipa: IPA phoneme
    :return: The RTGS that be convert
    :rtype: str

    :Example:
    ::

        from pythainlp.util import ipa_to_rtgs
 
        print(ipa_to_rtgs("kluaj"))
        # output : 'kluai'

    """
    _temp = []
    _list_ipa = ipa_cut.word_tokenize(ipa)
    for i,p in enumerate(_list_ipa):
        if i == len(_list_ipa) -1 and p in list(dict_ipa_rtgs_final.keys()):
            _temp.append(dict_ipa_rtgs_final[p])
        elif p in list(dict_ipa_rtgs.keys()):
            _temp.append(dict_ipa_rtgs[p])
        else:
            _temp.append(p)
    _text = ''.join(_temp)
    _text = unicodedata.normalize('NFKD', _text).encode('ascii', 'ignore')
    return _text.decode("utf-8")


def remove_tone_ipa(ipa: str) -> str:
    """
    Remove Thai Tone from IPA system

    :param str ipa: IPA phoneme
    :return: IPA phoneme that deleted tone
    :rtype: str

    :Example:
    ::

        from pythainlp.util import remove_tone_ipa
 
        print(remove_tone_ipa("laː˦˥.sa˨˩.maj˩˩˦"))
        # output : laː.sa.maj

    """
    _list_tone = ["˩˩˦", "˥˩", "˨˩", "˦˥", "˧"]
    for tone in _list_tone:
        ipa = ipa.replace(tone, "")
    return ipa
