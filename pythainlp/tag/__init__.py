# -*- coding: utf-8 -*-
"""
Tagging each token in a sentence with supplementary information,
such as its Part-of-Speech (POS) tag, and Named Entity Recognition (NER) tag.


"""

from typing import List, Tuple

__all__ = ["pos_tag", "pos_tag_sents", "tag_provinces"]
from .locations import tag_provinces

# tag map for orchid to Universal Dependencies
# from Korakot Chaovavanich
_TAG_MAP_UD = {
    # NOUN
    "NOUN": "NOUN",
    "NCMN": "NOUN",
    "NTTL": "NOUN",
    "CNIT": "NOUN",
    "CLTV": "NOUN",
    "CMTR": "NOUN",
    "CFQC": "NOUN",
    "CVBL": "NOUN",
    # VERB
    "VACT": "VERB",
    "VSTA": "VERB",
    # PROPN
    "PROPN": "PROPN",
    "NPRP": "PROPN",
    # ADJ
    "ADJ": "ADJ",
    "NONM": "ADJ",
    "VATT": "ADJ",
    "DONM": "ADJ",
    # ADV
    "ADV": "ADV",
    "ADVN": "ADV",
    "ADVI": "ADV",
    "ADVP": "ADV",
    "ADVS": "ADV",
    # INT
    "INT": "INTJ",
    # PRON
    "PRON": "PRON",
    "PPRS": "PRON",
    "PDMN": "PRON",
    "PNTR": "PRON",
    # DET
    "DET": "DET",
    "DDAN": "DET",
    "DDAC": "DET",
    "DDBQ": "DET",
    "DDAQ": "DET",
    "DIAC": "DET",
    "DIBQ": "DET",
    "DIAQ": "DET",
    # NUM
    "NUM": "NUM",
    "NCNM": "NUM",
    "NLBL": "NUM",
    "DCNM": "NUM",
    # AUX
    "AUX": "AUX",
    "XVBM": "AUX",
    "XVAM": "AUX",
    "XVMM": "AUX",
    "XVBB": "AUX",
    "XVAE": "AUX",
    # ADP
    "ADP": "ADP",
    "RPRE": "ADP",
    # CCONJ
    "CCONJ": "CCONJ",
    "JCRG": "CCONJ",
    # SCONJ
    "SCONJ": "SCONJ",
    "PREL": "SCONJ",
    "JSBR": "SCONJ",
    "JCMP": "SCONJ",
    # PART
    "PART": "PART",
    "FIXN": "PART",
    "FIXV": "PART",
    "EAFF": "PART",
    "EITT": "PART",
    "AITT": "PART",
    "NEG": "PART",
    # PUNCT
    "PUNCT": "PUNCT",
    "PUNC": "PUNCT",
}


def _UD_Exception(w: str, tag: str) -> str:
    if w == "การ" or w == "ความ":
        return "NOUN"

    return tag


def _orchid_to_ud(tag) -> List[Tuple[str, str]]:
    _i = 0
    temp = []
    while _i < len(tag):
        temp.append((tag[_i][0], _UD_Exception(tag[_i][0], _TAG_MAP_UD[tag[_i][1]])))
        _i += 1

    return temp


def _artagger_tag(words: List[str], corpus: str = None) -> List[Tuple[str, str]]:
    if not words:
        return []

    from artagger import Tagger

    words_ = Tagger().tag(" ".join(words))

    return [(word.word, word.tag) for word in words_]


def pos_tag(
    words: List[str], engine: str = "perceptron", corpus: str = "orchid"
) -> List[Tuple[str, str]]:
    """
    The function tag a list of tokenized words into Part-of-Speech (POS) tags
    such as 'NOUN', 'VERB', 'ADJ', and 'DET'.

    :param list words: a list of tokenized words
    :param str engine:
        * *perceptron* - perceptron tagger (default)
        * *unigram* - unigram tagger
        * *artagger* - RDR POS tagger
    :param str corpus:
        * *orchid* - annotated Thai academic articles namedly
          `Orchid <https://www.academia.edu/9127599/Thai_Treebank>`_ (default)
        * *orchid_ud* - annotated Thai academic articles *Orchid* but the
          POS tags are mapped to comply with
          `Universal Dependencies <https://universaldependencies.org/u/pos>`_
          POS  Tags
        * *pud* - `Parallel Universal Dependencies (PUD)
          <https://github.com/UniversalDependencies/UD_Thai-PUD>`_ treebanks
    :return: returns a list of labels regarding which part of speech it is
    :rtype: list[tuple[str, str]]

    :Note:
        * *artagger*, only support one sentence and the sentence must
          be tokenized beforehand.

    :Example:

        Tag words with corpus `orchid` (default):

        >>> from pythainlp.tag import pos_tag
        >>>
        >>> words = ['ฉัน','มี','ชีวิต','รอด','ใน','อาคาร','หลบภัย','ของ', \\
            'นายก', 'เชอร์ชิล']
        >>> pos_tag(words)
        [('ฉัน', 'PPRS'), ('มี', 'VSTA'), ('ชีวิต', 'NCMN'), ('รอด', 'NCMN'),
        ('ใน', 'RPRE'), ('อาคาร', 'NCMN'), ('หลบภัย', 'NCMN'), ('ของ', 'RPRE'),
        ('นายก', 'NCMN'), ('เชอร์ชิล', 'NCMN')]

        Tag words with corpus `orchid_ud`:

        >>> from pythainlp.tag import pos_tag
        >>>
        >>> words = ['ฉัน','มี','ชีวิต','รอด','ใน','อาคาร','หลบภัย','ของ', \\
            'นายก', 'เชอร์ชิล']
        >>> pos_tag(words, corpus='orchid_ud')
        [('ฉัน', 'PROPN'), ('มี', 'VERB'), ('ชีวิต', 'NOUN'), ('รอด', 'NOUN'),
        ('ใน', 'ADP'),  ('อาคาร', 'NOUN'), ('หลบภัย', 'NOUN'), ('ของ', 'ADP'),
        ('นายก', 'NOUN'), ('เชอร์ชิล', 'NOUN')]

        Tag words with corpus `pud`:

        >>> from pythainlp.tag import pos_tag
        >>>
        >>> words = ['ฉัน','มี','ชีวิต','รอด','ใน','อาคาร','หลบภัย','ของ', \\
            'นายก', 'เชอร์ชิล']
        >>> pos_tag(words, corpus='pud')
        [('ฉัน', 'PRON'), ('มี', 'VERB'), ('ชีวิต', 'NOUN'), ('รอด', 'VERB'),
        ('ใน', 'ADP'), ('อาคาร', 'NOUN'), ('หลบภัย', 'NOUN'), ('ของ', 'ADP'),
        ('นายก', 'NOUN'), ('เชอร์ชิล', 'PROPN')]

        Tag words with different engines including *perceptron*, *unigram*,
        and *artagger*:

        >>> from pythainlp.tag import pos_tag
        >>>
        >>> words = ['เก้าอี้','มี','จำนวน','ขา', ' ', '=', '3']
        >>> pos_tag(words, engine='perceptron', corpus='orchid')
        [('เก้าอี้', 'NCMN'), ('มี', 'VSTA'), ('จำนวน', 'NCMN'),
         ('ขา', 'NCMN'), (' ', 'PUNC'),
         ('=', 'PUNC'), ('3', 'NCNM')]
        >>>
        >>> pos_tag(words, engine='unigram', corpus='pud')
        [('เก้าอี้', None), ('มี', 'VERB'), ('จำนวน', 'NOUN'), ('ขา', None),
        ('<space>', None), ('<equal>', None), ('3', 'NUM')]
        >>>
        >>> pos_tag(words, engine='artagger', corpus='orchid')
        [('เก้าอี้', 'NCMN'), ('มี', 'VSTA'), ('จำนวน', 'NCMN'),
         ('ขา', 'NCMN'), ('<space>', 'PUNC'),
         ('<equal>', 'PUNC'), ('3', 'NCNM')]
    """

    # NOTE:
    _corpus = corpus
    _tag = []
    if corpus == "orchid_ud":
        corpus = "orchid"
    if not words:
        return []

    if engine == "perceptron":
        from .perceptron import tag as tag_
    elif engine == "artagger":
        tag_ = _artagger_tag
    else:  # default, use "unigram" ("old") engine
        from .unigram import tag as tag_
    _tag = tag_(words, corpus=corpus)

    if _corpus == "orchid_ud":
        _tag = _orchid_to_ud(_tag)

    return _tag


def pos_tag_sents(
    sentences: List[List[str]], engine: str = "perceptron", corpus: str = "orchid"
) -> List[List[Tuple[str, str]]]:
    """
    The function tag multiple list of tokenized words into Part-of-Speech
    (POS) tags.

    :param list sentences: a list of lists of tokenized words
    :param str engine:
        * *perceptron* - perceptron tagger (default)
        * *unigram* - unigram tagger
        * *artagger* - RDR POS tagger
    :param str corpus:
        * *orchid* - annotated Thai academic articles namedly\
            `Orchid <https://www.academia.edu/9127599/Thai_Treebank>`_\
            (default)
        * *orchid_ud* - annotated Thai academic articles using\
            `Universal Dependencies <https://universaldependencies.org/>`_ Tags
        * *pud* - `Parallel Universal Dependencies (PUD)\
            <https://github.com/UniversalDependencies/UD_Thai-PUD>`_ treebanks
    :return: returns a list of labels regarding which part of speech it is
             for each sentence given.
    :rtype: list[list[tuple[str, str]]]

    :Example:

        Labels POS for two sentences:

        >>> from pythainlp.tag import pos_tag_sents
        >>>
        >>> sentences = [['เก้าอี้','มี','3','ขา'], \\
                         ['นก', 'บิน', 'กลับ', 'รัง']]
        >>> pos_tag_sents(sentences, corpus='pud)
        [[('เก้าอี้', 'PROPN'), ('มี', 'VERB'), ('3', 'NUM'), ('ขา', 'NOUN')],
        [('นก', 'NOUN'), ('บิน', 'VERB'), ('กลับ', 'VERB'), ('รัง', 'NOUN')]]
    """
    if not sentences:
        return []

    return [pos_tag(sent, engine=engine, corpus=corpus) for sent in sentences]
