# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Phonemes util"""

from __future__ import annotations

import unicodedata
from functools import lru_cache

from pythainlp.tokenize import Tokenizer
from pythainlp.util.trie import Trie

consonants_ipa_nectec: list[tuple[str, ...]] = [
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

monophthong_ipa_nectec: list[tuple[str, str]] = [
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

diphthong_ipa_nectec: list[tuple[str, str]] = [
    ("ia", "ia"),
    ("ɯa", "va"),
    ("ua", "ua"),
    ("iia", "iia"),
    ("ɯɯa", "vva"),
    ("uua", "uua"),
]

tones_ipa_nectec: list[tuple[str, str]] = [
    ("˧", "0"),
    ("˨˩", "1"),
    ("˥˩", "2"),
    ("˦˥", "3"),
    ("˩˩˦", "4"),
]

dict_nectec_to_ipa: dict[str, str] = {
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
    """Convert NECTEC system to IPA system

    :param str pronunciation: NECTEC phoneme
    :return: IPA that is converted
    :rtype: str

    :Example:

        >>> from pythainlp.util import nectec_to_ipa  # doctest: +SKIP

        >>> print(nectec_to_ipa("kl-uua-j^-2"))  # doctest: +SKIP
        'kl uua j ˥˩'

    References
    ----------
    Pornpimon Palingoon, Sumonmas Thatphithakkul. Chapter 4 Speech
    processing and Speech corpus. In: Handbook of Thai Electronic
    Corpus. 1st ed. p. 122–56.

    """
    parts = pronunciation.split("-")
    ipa = []
    for part in parts:
        if part in dict_nectec_to_ipa.keys():
            ipa.append(dict_nectec_to_ipa[part])
        else:
            ipa.append(part)
    return " ".join(ipa)


dict_ipa_rtgs: dict[str, str] = {
    "b": "b",
    "d": "d",
    "f": "f",
    "h": "h",
    # The conversion of j depends on its position in the syllable.
    # The current implementation cannot handle both cases.
    # The first mapping ("j": "y") is commented out because it is
    # overridden by the second one ("j": "i") and never takes effect.
    # See issue #846:
    # https://github.com/PyThaiNLP/pythainlp/issues/846
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

dict_ipa_rtgs_final: dict[str, str] = {"w": "o"}


@lru_cache
def _ipa_cut() -> Tokenizer:
    """Lazy load IPA tokenizer with cache"""
    trie = Trie(list(dict_ipa_rtgs.keys()) + list(dict_ipa_rtgs_final.keys()))
    return Tokenizer(custom_dict=trie, engine="newmm")


def ipa_to_rtgs(ipa: str) -> str:
    """Convert IPA system to The Royal Thai General System of Transcription (RTGS)

    Docs: https://en.wikipedia.org/wiki/Help:IPA/Thai

    :param str ipa: IPA phoneme
    :return: The RTGS that is converted, according to rules listed in the Wikipedia page
    :rtype: str

    :Example:

        >>> from pythainlp.util import ipa_to_rtgs  # doctest: +SKIP

        >>> print(ipa_to_rtgs("kluaj"))  # doctest: +SKIP
        'kluai'

    """
    rtgs_parts = []
    ipa_cut = _ipa_cut()

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
    """Remove Thai Tones from IPA system

    :param str ipa: IPA phoneme
    :return: IPA phoneme with tones removed
    :rtype: str

    :Example:

        >>> from pythainlp.util import remove_tone_ipa  # doctest: +SKIP

        >>> print(remove_tone_ipa("laː˦˥.sa˨˩.maj˩˩˦"))  # doctest: +SKIP
        laː.sa.maj

    """
    _list_tone = ["˩˩˦", "˥˩", "˨˩", "˦˥", "˧"]
    for tone in _list_tone:
        ipa = ipa.replace(tone, "")
    return ipa
