# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Named entity recognizer."""

from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict, Union

if TYPE_CHECKING:
    from types import ModuleType

    from pythainlp.phayathaibert.core import NamedEntityTagger
    from pythainlp.tag.thai_nner import ThaiNNER
    from pythainlp.tag.thainer import ThaiNameTagger
    from pythainlp.wangchanberta.core import (
        NamedEntityRecognition,
    )
    from pythainlp.wangchanberta.core import (
        ThaiNameTagger as WangchanbertaThaiNameTagger,
    )


class EntitySpan(TypedDict):
    """Named entity span with its type, words, and position."""

    entity_type: str
    text: list[str]
    span: list[int]


# Type alias for NER engine types
NEREngineType = Union[
    "ThaiNNER",
    "ModuleType",
    "ThaiNameTagger",
    "NamedEntityRecognition",
    "WangchanbertaThaiNameTagger",
    "NamedEntityTagger",
    None,
]


class NER:
    """
    Named entity recognizer.

    :param str engine: engine to use for recognition. Options are:

        * *phayathaibert* - PhayaThaiBERT-based Thai NER engine
        * *thainer* - Thai NER engine
        * *thai-nner* - Thai nested NER engine
        * *thainer-v2* - Thai NER engine v2.0 for Thai NER 2.0 (default)
        * *tltk* - wrapper for `TLTK <https://pypi.org/project/tltk/>`_
        * *wangchanberta* - WangchanBERTa-based Thai NER engine
    :param str corpus: corpus used to train the engine model.
        Options are:

        * *thainer* - Thai NER corpus (default)
        * *thainer-v2* - Thai NER v2 corpus

    .. note::
        The tltk engine supports NER models from tltk only.
        The thai-nner engine supports nested NER and ignores the corpus
        parameter.
    """

    name_engine: str
    engine: NEREngineType

    def __init__(
        self, engine: str = "thainer-v2", corpus: str = "thainer"
    ) -> None:
        self.load_engine(engine=engine, corpus=corpus)

    def load_engine(self, engine: str, corpus: str) -> None:
        self.name_engine = engine
        self.engine = None

        # Engines that ignore corpus parameter
        if engine == "thai-nner":
            from pythainlp.tag.thai_nner import ThaiNNER

            self.engine = ThaiNNER()
        elif engine == "tltk":
            from pythainlp.tag import tltk

            self.engine = tltk
        # Corpus-specific engines
        elif corpus == "thainer":
            if engine == "thainer":
                from pythainlp.tag.thainer import ThaiNameTagger

                self.engine = ThaiNameTagger()
            elif engine == "thainer-v2":
                from pythainlp.wangchanberta import NamedEntityRecognition

                self.engine = NamedEntityRecognition(
                    model="pythainlp/thainer-corpus-v2-base-model"
                )
            elif engine == "wangchanberta":
                from pythainlp.wangchanberta import (
                    ThaiNameTagger as WangchanbertaThaiNameTagger,
                )  # noqa: I001,E501

                self.engine = WangchanbertaThaiNameTagger(dataset_name=corpus)
        elif corpus == "thainer-v2":
            if engine == "phayathaibert":
                from pythainlp.phayathaibert.core import NamedEntityTagger

                self.engine = NamedEntityTagger()

        if self.engine is None:
            raise ValueError(
                f"NER class not support {engine} engine or {corpus} corpus."
            )

    def tag(
        self, text: str, pos: bool = False, tag: bool = False
    ) -> Union[list[tuple[str, str]], list[tuple[str, str, str]], str]:
        """
        Tag named entities in text in IOB format.

        :param str text: Thai text to be tagged
        :param bool pos: include part-of-speech (POS) tags in the results
            (not supported by wangchanberta)
        :param bool tag: return the text with HTML-like tags
            instead of a list of tuples
        :return: list of tuples of word, POS tag (if ``pos`` is ``True``),
            and named entity tag; or the text with HTML-like tags
            (if ``tag`` is ``True``)
        :rtype: Union[list[tuple[str, str]], list[tuple[str, str, str]], str]

        :Example:

            >>> from pythainlp.tag import NER
            >>>
            >>> ner = NER("thainer")
            >>> ner.tag("ทดสอบ นายวรรณพงษ์ ภัททิยไพบูลย์")
            [('ทดสอบ', 'O'),
            (' ', 'O'),
            ('นาย', 'B-PERSON'),
            ('วรรณ', 'I-PERSON'),
            ('พงษ์', 'I-PERSON'),
            (' ', 'I-PERSON'),
            ('ภัททิย', 'I-PERSON'),
            ('ไพบูลย์', 'I-PERSON')]
            >>> ner.tag("ทดสอบ นายวรรณพงษ์ ภัททิยไพบูลย์", tag=True)
            'ทดสอบ <PERSON>นายวรรณพงษ์ ภัททิยไพบูลย์</PERSON>'
        """
        if self.engine is None:
            raise RuntimeError("Engine not initialized")
        return self.engine.get_ner(text, tag=tag, pos=pos)


class NNER:
    """
    Nested named entity recognizer.

    :param str engine: engine to use for recognition. Options are:

        * *thai_nner* - Thai nested NER engine (default)
    :param str corpus: corpus used to train the engine model
    """

    engine: "ThaiNNER"

    def __init__(self, engine: str = "thai_nner") -> None:
        self.load_engine(engine)

    def load_engine(self, engine: str = "thai_nner") -> None:
        from pythainlp.tag.thai_nner import ThaiNNER

        self.engine = ThaiNNER()

    def tag(
        self, text: str, top_level_only: bool = False
    ) -> tuple[list[str], list[EntitySpan]]:
        """
        Tag nested named entities in text.

        :param str text: Thai text to be tagged
        :param bool top_level_only: return only top-level (outermost)
            entities (``True``) or all nested entities (``False``, default)
        :return: tuple of (words, entities), where entities is a list of
            dicts with ``text``, ``span``, and ``entity_type`` keys
        :rtype: tuple[list[str], list[EntitySpan]]

        .. note::
            The list of words may include empty strings as part of the
            tokenization process of the underlying Thai-NNER model.

        :Example:

            >>> from pythainlp.tag.named_entity import NNER
            >>> nner = NNER()
            >>> nner.tag("แมวทำอะไรตอนห้าโมงเช้า")
            ([
                '<s>',
                '',
                'แมว',
                'ทํา',
                '',
                'อะไร',
                'ตอน',
                '',
                'ห้า',
                '',
                'โมง',
                '',
                'เช้า',
                '</s>'
            ],
            [
                {
                    'text': ['', 'ห้า'],
                    'span': [7, 9],
                    'entity_type': 'cardinal'
                },
                {
                    'text': ['', 'ห้า', '', 'โมง'],
                    'span': [7, 11],
                    'entity_type': 'time'
                },
                {
                    'text': ['', 'โมง'],
                    'span': [9, 11],
                    'entity_type': 'unit'
                }
            ])
            >>> # Get only top-level entities (outermost entities)
            >>> nner.tag("แมวทำอะไรตอนห้าโมงเช้า", top_level_only=True)
            ([...], [{'text': ['', 'ห้า', '', 'โมง'], 'span': [7, 11], 'entity_type': 'time'}])
        """
        return self.engine.tag(text, top_level_only=top_level_only)
