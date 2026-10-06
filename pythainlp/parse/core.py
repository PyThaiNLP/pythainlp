# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Dependency parsing for Thai text."""

from __future__ import annotations

from typing import Any, List, Optional, Union

_tagger: Optional[Any] = None
_tagger_name: str = ""


def dependency_parsing(
    text: str,
    model: Optional[str] = None,
    tag: str = "str",
    engine: str = "esupar",
) -> Union[List[List[str]], str]:
    """
    Parse the dependency structure of a text.

    :param str text: text to be parsed
    :param Optional[str] model: model to use with the engine
        (for esupar, transformers_ud, and ud_goeswith)
    :param str tag: output type, ``"str"`` (CoNLL-U text, default)
        or ``"list"``
    :param str engine: engine to use for parsing. Options are:

        * *esupar* (default) - tokenizer, POS tagger, and dependency
          parser using BERT/RoBERTa/DeBERTa models.
          `GitHub <https://github.com/KoichiYasuoka/esupar>`_
        * *spacy_thai* - tokenizer, POS tagger, and dependency parser
          for the Thai language, using Universal Dependencies.
          `GitHub <https://github.com/KoichiYasuoka/spacy-thai>`_
        * *transformers_ud* - TransformersUD.
          `GitHub <https://github.com/KoichiYasuoka/>`_
        * *ud_goeswith* - POS tagger and dependency parser
          using ``goeswith`` for subwords
        * *attaparse* - Thai dependency parser using Stanza and
          PhayaThaiBERT.
          `GitHub <https://github.com/nlp-chula/attaparse>`_
    :return: CoNLL-U text if ``tag`` is ``"str"``, otherwise a list of
        lists of fields
    :rtype: Union[List[List[str]], str]
    :raises NotImplementedError: if the engine is not supported

    Options for ``model`` with the esupar engine:

    * *th* (default) - KoichiYasuoka/roberta-base-thai-spm-upos model.
      `Hugging Face
      <https://huggingface.co/KoichiYasuoka/roberta-base-thai-spm-upos>`_
    * *KoichiYasuoka/deberta-base-thai-upos* - DeBERTa(V2) model
      pre-trained on Thai Wikipedia texts for POS tagging and
      dependency parsing.
      `Hugging Face
      <https://huggingface.co/KoichiYasuoka/deberta-base-thai-upos>`_
    * *KoichiYasuoka/roberta-base-thai-syllable-upos* - RoBERTa model
      pre-trained on Thai Wikipedia texts for POS tagging and
      dependency parsing (syllable level).
      `Hugging Face
      <https://huggingface.co/KoichiYasuoka/roberta-base-thai-syllable-upos>`_
    * *KoichiYasuoka/roberta-base-thai-char-upos* - RoBERTa model
      pre-trained on Thai Wikipedia texts for POS tagging and
      dependency parsing (character level).
      `Hugging Face
      <https://huggingface.co/KoichiYasuoka/roberta-base-thai-char-upos>`_

    To train models for esupar, see the
    `esupar GitHub repository <https://github.com/KoichiYasuoka/esupar>`_.

    Options for ``model`` with the transformers_ud engine:

    * *KoichiYasuoka/deberta-base-thai-ud-head* (default) - DeBERTa(V2)
      model pre-trained on Thai Wikipedia texts for dependency parsing
      (head detection using Universal Dependencies) and question
      answering, derived from deberta-base-thai and trained on
      th_blackboard.conll.
      `Hugging Face
      <https://huggingface.co/KoichiYasuoka/deberta-base-thai-ud-head>`_
    * *KoichiYasuoka/roberta-base-thai-spm-ud-head* - RoBERTa model
      pre-trained on Thai Wikipedia texts for dependency parsing.
      `Hugging Face
      <https://huggingface.co/KoichiYasuoka/roberta-base-thai-spm-ud-head>`_

    Options for ``model`` with the ud_goeswith engine:

    * *KoichiYasuoka/deberta-base-thai-ud-goeswith* (default) -
      DeBERTa(V2) model pre-trained on Thai Wikipedia texts for POS
      tagging and dependency parsing (using ``goeswith`` for subwords).
      `Hugging Face
      <https://huggingface.co/KoichiYasuoka/deberta-base-thai-ud-goeswith>`_

    :Example:

        >>> from pythainlp.parse import dependency_parsing  # doctest: +SKIP

        >>> print(
        ...     dependency_parsing("ผมเป็นคนดี", engine="esupar")
        ... )  # doctest: +SKIP
        1       ผม      _       PRON    _       _       3       nsubj   _       SpaceAfter=No
        2       เป็น     _       VERB    _       _       3       cop     _       SpaceAfter=No
        3       คน      _       NOUN    _       _       0       root    _       SpaceAfter=No
        4       ดี       _       VERB    _       _       3       acl     _       SpaceAfter=No

        >>> print(
        ...     dependency_parsing("ผมเป็นคนดี", engine="spacy_thai")
        ... )  # doctest: +SKIP
        1       ผม              PRON    PPRS    _       2       nsubj   _       SpaceAfter=No
        2       เป็น             VERB    VSTA    _       0       ROOT    _       SpaceAfter=No
        3       คนดี             NOUN    NCMN    _       2       obj     _       SpaceAfter=No
    """
    global _tagger, _tagger_name

    if _tagger_name != engine:
        if engine == "esupar":
            from pythainlp.parse.esupar_engine import Parse

            _tagger = Parse(model=model or "th")
        elif engine == "transformers_ud":
            from pythainlp.parse.transformers_ud import Parse  # type: ignore[assignment]  # noqa: I001

            _tagger = Parse(
                model=model or "KoichiYasuoka/deberta-base-thai-ud-head"
            )
        elif engine == "spacy_thai":
            from pythainlp.parse.spacy_thai_engine import Parse  # type: ignore[assignment]  # noqa: I001

            _tagger = Parse()
        elif engine == "ud_goeswith":
            from pythainlp.parse.ud_goeswith import Parse  # type: ignore[assignment]  # noqa: I001

            _tagger = Parse(
                model=model or "KoichiYasuoka/deberta-base-thai-ud-goeswith"
            )
        elif engine == "attaparse":
            from pythainlp.parse.attaparse_engine import Parse  # type: ignore[assignment]  # noqa: I001

            _tagger = Parse()
        else:
            raise NotImplementedError("The engine doesn't support.")

    _tagger_name = engine

    return _tagger(text, tag=tag)  # type: ignore[misc,no-any-return]
