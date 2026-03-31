# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Thank https://dev.to/ton_ami/text-data-augmentation-synonym-replacement-4h8l"""

from __future__ import annotations

__all__: list[str] = [
    "WordNetAug",
    "postype2wordnet",
]

import itertools
from collections import OrderedDict
from typing import TYPE_CHECKING, Callable, Optional

from nltk.corpus import wordnet as wn

if TYPE_CHECKING:
    from nltk.corpus.reader.wordnet import Synset

from pythainlp.corpus import wordnet
from pythainlp.tag import pos_tag
from pythainlp.tokenize import word_tokenize

orchid: dict[str, str] = {
    "": "",
    # NOUN
    "NOUN": wn.NOUN,
    "NCMN": wn.NOUN,
    "NTTL": wn.NOUN,
    "CNIT": wn.NOUN,
    "CLTV": wn.NOUN,
    "CMTR": wn.NOUN,
    "CFQC": wn.NOUN,
    "CVBL": wn.NOUN,
    # VERB
    "VACT": wn.VERB,
    "VSTA": wn.VERB,
    # PROPN
    "PROPN": "",
    "NPRP": "",
    # ADJ
    "ADJ": wn.ADJ,
    "NONM": wn.ADJ,
    "VATT": wn.ADJ,
    "DONM": wn.ADJ,
    # ADV
    "ADV": wn.ADV,
    "ADVN": wn.ADV,
    "ADVI": wn.ADV,
    "ADVP": wn.ADV,
    "ADVS": wn.ADV,
    # INT
    "INT": "",
    # PRON
    "PRON": "",
    "PPRS": "",
    "PDMN": "",
    "PNTR": "",
    # DET
    "DET": "",
    "DDAN": "",
    "DDAC": "",
    "DDBQ": "",
    "DDAQ": "",
    "DIAC": "",
    "DIBQ": "",
    "DIAQ": "",
    # NUM
    "NUM": "",
    "NCNM": "",
    "NLBL": "",
    "DCNM": "",
    # AUX
    "AUX": "",
    "XVBM": "",
    "XVAM": "",
    "XVMM": "",
    "XVBB": "",
    "XVAE": "",
    # ADP
    "ADP": "",
    "RPRE": "",
    # CCONJ
    "CCONJ": "",
    "JCRG": "",
    # SCONJ
    "SCONJ": "",
    "PREL": "",
    "JSBR": "",
    "JCMP": "",
    # PART
    "PART": "",
    "FIXN": "",
    "FIXV": "",
    "EAFF": "",
    "EITT": "",
    "AITT": "",
    "NEG": "",
    # PUNCT
    "PUNCT": "",
    "PUNC": "",
}


def postype2wordnet(pos: str, corpus: str) -> Optional[str]:
    """Convert part-of-speech type to wordnet type

    :param str pos: POS type
    :param str corpus: part-of-speech corpus

    **Options for corpus**
        * *orchid* - Orchid Corpus
    """
    if corpus not in ["orchid"]:
        return None
    return orchid[pos]


class WordNetAug:
    """Text Augment using wordnet"""

    synonyms: list[str]
    list_synsets: list[Synset]
    p2w_pos: Optional[str]
    synset: Synset
    syn: str
    synonyms_without_duplicates: list[str]
    list_words: list[str]
    list_synonym: list[list[str]]
    p_all: int
    list_pos: list[tuple[str, str]]
    temp: list[str]

    def __init__(self) -> None:
        pass

    def find_synonyms(
        self,
        word: str,
        pos: Optional[str] = None,
        postag_corpus: str = "orchid",
    ) -> list[str]:
        """Find synonyms using wordnet

        :param str word: word
        :param Optional[str] pos: part-of-speech type. Default is None.
        :param str postag_corpus: name of POS tag corpus
        :return: list of synonyms
        :rtype: list[str]
        """
        self.synonyms: list[str] = []
        if pos is None:
            self.list_synsets: list[Synset] = wordnet.synsets(word)
        else:
            self.p2w_pos: Optional[str] = postype2wordnet(pos, postag_corpus)
            if self.p2w_pos != "":
                self.list_synsets: list[Synset] = wordnet.synsets(
                    word, pos=self.p2w_pos
                )
            else:
                self.list_synsets: list[Synset] = wordnet.synsets(word)

        for self.synset in wordnet.synsets(word):
            for self.syn in self.synset.lemma_names(lang="tha"):
                self.synonyms.append(self.syn)

        self.synonyms_without_duplicates: list[str] = list(
            OrderedDict.fromkeys(self.synonyms)
        )
        return self.synonyms_without_duplicates

    def augment(
        self,
        sentence: str,
        tokenize: Callable[[str], list[str]] = word_tokenize,
        max_syn_sent: int = 6,
        postag: bool = True,
        postag_corpus: str = "orchid",
    ) -> list[list[str]]:
        """Text Augment using wordnet

        :param str sentence: Thai sentence
        :param object tokenize: function for tokenizing words
        :param int max_syn_sent: maximum number of synonymous sentences
        :param bool postag: use part-of-speech
        :param str postag_corpus: name of POS tag corpus

        :return: list of synonyms
        :rtype: list[list[str]]

        :Example:

            >>> from pythainlp.augment import WordNetAug  # doctest: +SKIP

            >>> aug = WordNetAug()  # doctest: +SKIP
            >>> aug.augment("เราชอบไปโรงเรียน")  # doctest: +SKIP
            [('เรา', 'ชอบ', 'ไป', 'ร.ร.'),
             ('เรา', 'ชอบ', 'ไป', 'รร.'),
             ('เรา', 'ชอบ', 'ไป', 'โรงเรียน'),
             ('เรา', 'ชอบ', 'ไป', 'อาคารเรียน'),
             ('เรา', 'ชอบ', 'ไปยัง', 'ร.ร.'),
             ('เรา', 'ชอบ', 'ไปยัง', 'รร.')]
        """
        new_sentences = []
        self.list_words: list[str] = tokenize(sentence)
        self.list_synonym: list[list[str]] = []
        self.p_all: int = 1
        if postag:
            self.list_pos: list[tuple[str, str]] = pos_tag(
                self.list_words, corpus=postag_corpus
            )
            for word, pos in self.list_pos:
                self.temp: list[str] = self.find_synonyms(
                    word, pos, postag_corpus
                )
                if not self.temp:
                    self.list_synonym.append([word])
                else:
                    self.list_synonym.append(self.temp)
                    self.p_all *= len(self.temp)
        else:
            for word in self.list_words:
                self.temp: list[str] = self.find_synonyms(word)
                if not self.temp:
                    self.list_synonym.append([word])
                else:
                    self.list_synonym.append(self.temp)
                    self.p_all *= len(self.temp)
        if max_syn_sent > self.p_all:
            max_syn_sent = self.p_all
        for x in list(itertools.product(*self.list_synonym))[0:max_syn_sent]:
            new_sentences.append(list(x))
        return new_sentences
