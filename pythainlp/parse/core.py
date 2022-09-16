# -*- coding: utf-8 -*-
_tagger = None
_tagger_name = ""

def dependency_parsing(text: str, engine: str="esupar")->str:
    """
    Dependency Parsing

    :param str text: text to do dependency parsing
    :param str engine: the name dependency parser
    :return: str (conllu)

    **Options for engine**
        * *esupar* (default) - Tokenizer POS-tagger and Dependency-parser \
            with BERT/RoBERTa/DeBERTa model. `GitHub \
                <https://github.com/KoichiYasuoka/esupar>`_
        * *spacy_thai* - Tokenizer, POS-tagger, and dependency-parser \
            for Thai language, working on Universal Dependencies. \
            `GitHub <https://github.com/KoichiYasuoka/spacy-thai>`_

    :Example:
    ::

        from pythainlp.parse import dependency_parsing

        print(dependency_parsing("ผมเป็นคนดี", engine="esupar"))
        # output:
        # 1       ผม      _       PRON    _       _       3       nsubj   _       SpaceAfter=No
        # 2       เป็น     _       VERB    _       _       3       cop     _       SpaceAfter=No
        # 3       คน      _       NOUN    _       _       0       root    _       SpaceAfter=No
        # 4       ดี       _       VERB    _       _       3       acl     _       SpaceAfter=No

        print(dependency_parsing("ผมเป็นคนดี", engine="spacy_thai"))
        # output:
        # 1       ผม              PRON    PPRS    _       2       nsubj   _       SpaceAfter=No
        # 2       เป็น             VERB    VSTA    _       0       ROOT    _       SpaceAfter=No
        # 3       คนดี             NOUN    NCMN    _       2       obj     _       SpaceAfter=No
    """
    global _tagger, _tagger_name
    if _tagger_name != engine:
        if engine == "esupar":
            from pythainlp.parse.esupar_engine import Parse
            _tagger = Parse()
        elif engine == "spacy_thai":
            from pythainlp.parse.spacy_thai_engine import Parse
            _tagger = Parse()
    _tagger_name = engine
    return _tagger(text)
