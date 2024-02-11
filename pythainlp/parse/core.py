# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0

from typing import List, Union


_tagger = None
_tagger_name = ""


def dependency_parsing(
    text: str,
    model: Union[str, None] = None,
    tag: str = "str",
    engine: str = "esupar",
) -> Union[List[List[str]], str]:
    """
    Dependency Parsing

    :param str text: text to apply dependency parsing to
    :param str model: model for using with engine \
        (for esupar and transformers_ud)
    :param str tag: output type (str or list)
    :param str engine: the name of dependency parser
    :return: str (conllu) or List
    :rtype: Union[List[List[str]], str]

    **Options for engine**
        * *esupar* (default) - Tokenizer, POS tagger and Dependency parser \
            using BERT/RoBERTa/DeBERTa models. `GitHub \
                <https://github.com/KoichiYasuoka/esupar>`_
        * *spacy_thai* - Tokenizer, POS tagger, and dependency parser \
            for the Thai language, using Universal Dependencies. \
            `GitHub <https://github.com/KoichiYasuoka/spacy-thai>`_
        * *transformers_ud* - TransformersUD \
            `GitHub <https://github.com/KoichiYasuoka/>`_
        * *ud_goeswith* - POS tagging and dependency parsing \
            using `goeswith` for subwords

    **Options for model (esupar engine)**
        * *th* (default) - KoichiYasuoka/roberta-base-thai-spm-upos model \
            `Huggingface \
            <https://huggingface.co/KoichiYasuoka/roberta-base-thai-spm-upos>`_
        * *KoichiYasuoka/deberta-base-thai-upos* - DeBERTa(V2) model \
            pre-trained on Thai Wikipedia texts for POS tagging and \
            dependency parsing `Huggingface \
            <https://huggingface.co/KoichiYasuoka/deberta-base-thai-upos>`_
        * *KoichiYasuoka/roberta-base-thai-syllable-upos* - RoBERTa model \
            pre-trained on Thai Wikipedia texts for POS tagging and \
            dependency parsing. (syllable level) `Huggingface \
            <https://huggingface.co/KoichiYasuoka/roberta-base-thai-syllable-upos>`_
        * *KoichiYasuoka/roberta-base-thai-char-upos* - RoBERTa model \
            pre-trained on Thai Wikipedia texts for POS tagging \
            and dependency parsing. (char level) `Huggingface \
            <https://huggingface.co/KoichiYasuoka/roberta-base-thai-char-upos>`_

    If you want to train models for esupar, you can read \
    `Huggingface <https://github.com/KoichiYasuoka/esupar>`_

    **Options for model (transformers_ud engine)**
        * *KoichiYasuoka/deberta-base-thai-ud-head* (default) - \
            DeBERTa(V2) model pretrained on Thai Wikipedia texts \
            for dependency parsing (head-detection using Universal \
            Dependencies) and question-answering, derived from \
            deberta-base-thai. \
            trained by th_blackboard.conll. `Huggingface \
            <https://huggingface.co/KoichiYasuoka/deberta-base-thai-ud-head>`_
        * *KoichiYasuoka/roberta-base-thai-spm-ud-head* - \
            roberta model pretrained on Thai Wikipedia texts \
            for dependency parsing. `Huggingface \
            <https://huggingface.co/KoichiYasuoka/roberta-base-thai-spm-ud-head>`_

    **Options for model (ud_goeswith engine)**
        * *KoichiYasuoka/deberta-base-thai-ud-goeswith* (default) - \
            This is a DeBERTa(V2) model pre-trained on Thai Wikipedia \
            texts for POS tagging and dependency parsing (using goeswith for subwords) \
            `Huggingface <https://huggingface.co/KoichiYasuoka/deberta-base-thai-ud-goeswith>`_

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

            _tagger = Parse(model=model)
        elif engine == "transformers_ud":
            from pythainlp.parse.transformers_ud import Parse

            _tagger = Parse(model=model)
        elif engine == "spacy_thai":
            from pythainlp.parse.spacy_thai_engine import Parse

            _tagger = Parse()
        elif engine == "ud_goeswith":
            from pythainlp.parse.ud_goeswith import Parse

            _tagger = Parse(model=model)
        else:
            raise NotImplementedError("The engine doesn't support.")

    _tagger_name = engine

    return _tagger(text, tag=tag)
