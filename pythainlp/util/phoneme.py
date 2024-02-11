# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
"""
Phonemes util
"""
import unicodedata
from pythainlp.util.trie import Trie
from pythainlp.tokenize import Tokenizer

consonants_ipa_nectec = [
    ("k", "k", "k^"),
    ("kʰ", "kh"),
    ("ŋ", "ng", "ng^"),
    ("tɕ", "c"),
    ("tɕʰ", "ch"),
    ("s", "s"),
    ("j", "j", "j^"),
    ("d", "d"),
    ("t", "y", "t^"),
    ("tʰ", "th"),
    ("n", "n", "n^"),
    ("b", "b"),
    ("p", "p", "p^"),
    ("pʰ", "ph"),
    ("f", "f"),
    ("m", "m", "m^"),
    ("r", "r"),
    ("l", "l"),
    ("w", "w", "w^"),
    ("h", "h"),
    ("?", "z", "z^"),
]
# ipa, initial, final

monophthong_ipa_nectec = [
    ("i", "i"),
    ("e", "e"),
    ("ɛ", "x"),
    ("ɤ", "q"),
    ("a", "a"),
    ("am", "am^"),
    ("aj", "aj^"),
    ("aw", "aw^"),
    ("u", "u"),
    ("o", "o"),
    ("ɔ", "@"),
    ("ii", "ii"),
    ("ee", "ee"),
    ("ɛɛ", "xx"),
    ("ɯɯ", "vv"),
    ("ɤɤ", "qq"),
    ("aa", "aa"),
    ("uu", "uu"),
    ("oo", "oo"),
    ("", "@@"),  # -อ long
]

diphthong_ipa_nectec = [
    ("ia", "ia"),
    ("ɯa", "va"),
    ("ua", "ua"),
    ("iia", "iia"),
    ("ɯɯa", "vva"),
    ("uua", "uua"),
]

tones_ipa_nectec = [
    ("˧", "0"),
    ("˨˩", "1"),
    ("˥˩", "2"),
    ("˦˥", "3"),
    ("˩˩˦", "4"),
]

dict_nectec_to_ipa = {
    i[1]: i[0]
    for i in consonants_ipa_nectec
    + monophthong_ipa_nectec
    + diphthong_ipa_nectec
    + tones_ipa_nectec
}
dict_nectec_to_ipa.update(
    {i[2]: i[0] for i in consonants_ipa_nectec if len(i) > 2}
)


def nectec_to_ipa(pronunciation: str) -> str:
    """
    Convert NECTEC system to IPA system

    :param str pronunciation: NECTEC phoneme
    :return: IPA that is converted
    :rtype: str

    :Example:
    ::

        from pythainlp.util import nectec_to_ipa

        print(nectec_to_ipa("kl-uua-j^-2"))
        # output : 'kl uua j ˥˩'


    References
    ----------

    Pornpimon Palingoon, Sumonmas Thatphithakkul. Chapter 4 Speech processing \
        and Speech corpus. In: Handbook of Thai Electronic Corpus. \
        1st ed. p. 122–56.
    """
    parts = pronunciation.split("-")
    ipa = []
    for part in parts:
        if part in dict_nectec_to_ipa.keys():
            ipa.append(dict_nectec_to_ipa[part])
        else:
            ipa.append(part)
    return " ".join(ipa)


dict_ipa_rtgs = {
    "b": "b",
    "d": "d",
    "f": "f",
    "h": "h",
    # The conversion of j depends on its position in the syllable.
    # But, unfortunately, the current implementation cannot handle both cases.
    # To remove confusions without changing the behavior and breaking existing codes,
    # it is suggested that the first key-value mapping of j be simply commented out,
    # as it would be overridden by the second one and thus never take effect from the beginning.
    # See #846 for a more detailed discussion: https://github.com/PyThaiNLP/pythainlp/issues/846
    # "j":"y",
    "k": "k",
    "kʰ": "kh",
    "l": "l",
    "m": "m",
    "n": "n",
    "ŋ": "ng",
    "p": "p",
    "pʰ": "ph",
    "r": "r",
    "s": "s",
    "t": "t",
    "tʰ": "th",
    "tɕ": "ch",
    "tɕʰ": "ch",
    "w": "w",
    "ʔ": "",
    "j": "i",
    "a": "a",
    "e": "e",
    "ɛ": "ae",
    "i": "i",
    "o": "o",
    "ɔ": "o",
    "u": "u",
    "ɯ": "ue",
    "ɤ": "oe",
    "aː": "a",
    "eː": "e",
    "ɛː": "ae",
    "iː": "i",
    "oː": "o",
    "ɔː": "o",
    "uː": "u",
    "ɯː": "ue",
    "ɤː": "oe",
    "ia": "ia",
    "ua": "ua",
    "ɯa": "uea",
    "aj": "ai",
    "aw": "ao",
    "ew": "eo",
    "ɛw": "aeo",
    "iw": "io",
    "ɔj": "io",
    "uj": "ui",
    "aːj": "ai",
    "aːw": "ao",
    "eːw": "eo",
    "ɛːw": "aeo",
    "oːj": "oi",
    "ɔːj": "oi",
    "ɤːj": "oei",
    "iaw": "iao",
    "uaj": "uai",
    "ɯaj": "ueai",
    ".": ".",
}

dict_ipa_rtgs_final = {"w": "o"}
trie = Trie(list(dict_ipa_rtgs.keys()) + list(dict_ipa_rtgs_final.keys()))
ipa_cut = Tokenizer(custom_dict=trie, engine="newmm")


def ipa_to_rtgs(ipa: str) -> str:
    """
    Convert IPA system to The Royal Thai General System of Transcription (RTGS)

    Docs: https://en.wikipedia.org/wiki/Help:IPA/Thai

    :param str ipa: IPA phoneme
    :return: The RTGS that is converted, according to rules listed in the Wikipedia page
    :rtype: str

    :Example:
    ::

        from pythainlp.util import ipa_to_rtgs

        print(ipa_to_rtgs("kluaj"))
        # output : 'kluai'

    """
    rtgs_parts = []

    ipa_parts = ipa_cut.word_tokenize(ipa)
    for i, ipa_part in enumerate(ipa_parts):
        if i == len(ipa_parts) - 1 and ipa_part in list(dict_ipa_rtgs_final):
            rtgs_parts.append(dict_ipa_rtgs_final[ipa_part])
        elif ipa_part in list(dict_ipa_rtgs):
            rtgs_parts.append(dict_ipa_rtgs[ipa_part])
        else:
            rtgs_parts.append(ipa_part)

    rtgs = "".join(rtgs_parts)
    rtgs = (
        unicodedata.normalize("NFKD", rtgs)
        .encode("ascii", "ignore")
        .decode("utf-8")
    )

    return rtgs


def remove_tone_ipa(ipa: str) -> str:
    """
    Remove Thai Tones from IPA system

    :param str ipa: IPA phoneme
    :return: IPA phoneme with tones removed
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
