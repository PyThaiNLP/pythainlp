# -*- coding: utf-8 -*-
"""
NLTK WordNet wrapper

API here is exactly the same as NLTK API,
except that lang (language) argument will be "tha" (Thai) by default.
"""
import nltk

try:
    nltk.data.find("corpora/omw")
except LookupError:
    nltk.download("omw")

try:
    nltk.data.find("corpora/wordnet")
except LookupError:
    nltk.download("wordnet")

from nltk.corpus import wordnet


def synsets(word: str, pos: str = None, lang: str = "tha"):
    """
        This function return the synonym sets for all lemmas given the word with an optional argument to constrain the part of speech of the word.

        :param str word: word to find its synsets
        :param str pos: the part of speech constraint (i.e. *n* for Noun, *v* for Verb, *a* for Adjective, *s* for Adjective satellites, and *r* for Adverb)
        :param str lang: abbreviation of language (i.e. *eng*, *tha*). By default, it is *tha* 
        
        :return: :class:`Synset` for all lemmas for the word constrained with the argument *pos* 
        :rtype: list[:class:`Synset`]

        :Example:

            >>> from pythainlp.corpus.wordnet import synsets
            >>>
            >>> synsets("ทำงาน")
            [Synset('function.v.01'), Synset('work.v.02'), Synset('work.v.01'), Synset('work.v.08')]
            >>>
            >>> synsets("บ้าน", lang="tha"))
            [Synset('duplex_house.n.01'), Synset('dwelling.n.01'), Synset('house.n.01'),
             Synset('family.n.01'), Synset('home.n.03'), Synset('base.n.14'), Synset('home.n.01'),
             Synset('houseful.n.01'), Synset('home.n.07')]

            When specifying the part of speech constrain. For example, the word "แรง" cound be interpreted as force (n.) or hard (adj.).

            >>> from pythainlp.corpus.wordnet import synsets
            >>> # By default, accept all part of speech
            >>> synsets("แรง", lang="tha")
            >>>
            >>> # only Noun 
            >>> synsets("แรง", pos="n", lang="tha")
            [Synset('force.n.03'), Synset('force.n.02')]
            >>>
            >>> # only Adjective
            >>> synsets("แรง", pos="a", lang="tha")
            [Synset('hard.s.10'), Synset('strong.s.02')]
    """
    return wordnet.synsets(lemma=word, pos=pos, lang=lang)


def synset(name_synsets):
    """
        This function return the synonym set (synset) given the name of synset (i.e. 'dog.n.01', 'chase.v.01').

        :param str name_synsets: name of the sysset
    
        :return: :class:`Synset` of the given name
        :rtype: :class:`Synset`

        :Example:

            >>> from pythainlp.corpus.wordnet import synset
            >>>
            >>> difficult = synset('difficult.a.01')
            >>> difficult
            Synset('difficult.a.01')
            >>>
            >>> difficult.definition()
            'not easy; requiring great physical or mental effort to accomplish or comprehend or endure'
    """
    return wordnet.synset(name_synsets)


def all_lemma_names(pos: str = None, lang: str = "tha"):
    """
        This function returns all lemma names for all synsets for the given part of speech tag and language.
        If part of speech tag is not specified, all synsets for all part of speech will be used.

        :param str pos: the part of speech constraint (i.e. *n* for Noun, *v* for Verb, *a* for Adjective, *s* for Adjective satellites, and *r* for Adverb). By default, *pos* is **None**.
        :param str lang: abbreviation of language (i.e. *eng*, *tha*). By default, it is *tha*.
        
        :return: :class:`Synset` of lemmas names given the pos and language
        :rtype: list[:class:`Synset`]

        :Example:

            >>> from pythainlp.corpus.wordnet import all_lemma_names
            >>>
            >>> all_lemma_names()
            ['อเมริโก_เวสปุชชี',
             'เมืองชีย์เอนเน',
             'การรับเลี้ยงบุตรบุญธรรม',
             'ผู้กัด',
             'ตกแต่งเรือด้วยธง',
             'จิโอวานนิ_เวอร์จินิโอ',...]
            >>>
            >>> len(all_lemma_names())
            80508
            >>>
            >>> all_lemma_names(pos="a")
            ['ซึ่งไม่มีแอลกอฮอล์',
             'ซึ่งตรงไปตรงมา',
             'ที่เส้นศูนย์สูตร',
             'ทางจิตใจ',...]
            >>>
            >>> len(all_lemma_names(pos="a"))
            5277
    """
    return wordnet.all_lemma_names(pos=pos, lang=lang)


def all_synsets(pos: str = None):
    """
        This function iterates over all synsets constrained by given part of speech tag.
        
        :param str pos: part of speech tag

        :return: list of synsets constrained by given part of speech tag.
        :rtype: Iterable[:class:`Synset`]

        :Example:
            
            >>> from pythainlp.corpus.wordnet import all_synsets
            >>>
            >>> generator = all_synsets(pos="n")
            >>> next(generator)
            Synset('entity.n.01')
            >>> next(generator)
            Synset('physical_entity.n.01')
            >>> next(generator)
            Synset('abstraction.n.06')
            >>>
            >>>  generator = all_synsets()
            >>> next(generator)
            Synset('able.a.01')
            >>> next(generator)
            Synset('unable.a.01')
    """
    return wordnet.all_synsets(pos=pos)


def langs():
    return wordnet.langs()


def lemmas(word: str, pos: str = None, lang: str = "tha"):
    return wordnet.lemmas(word, pos=pos, lang=lang)


def lemma(name_synsets):
    return wordnet.lemma(name_synsets)


def lemma_from_key(key):
    return wordnet.lemma_from_key(key)


def path_similarity(synsets1, synsets2):
    return wordnet.path_similarity(synsets1, synsets2)


def lch_similarity(synsets1, synsets2):
    return wordnet.lch_similarity(synsets1, synsets2)


def wup_similarity(synsets1, synsets2):
    return wordnet.wup_similarity(synsets1, synsets2)


def morphy(form, pos: str = None):
    return wordnet.morphy(form, pos=None)


def custom_lemmas(tab_file, lang: str):
    return wordnet.custom_lemmas(tab_file, lang)
