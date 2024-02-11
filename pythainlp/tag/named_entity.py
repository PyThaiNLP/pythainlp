# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
"""
Named-entity recognizer
"""
from typing import List, Tuple, Union


class NER:
    """
    Class of named-entity recognizer

    :param str engine: engine of named-entity recognizer
    :param str corpus: corpus

    **Options for engine**
        * *thainer-v2* - Thai NER engine v2.0 for Thai NER 2.0 (default)
        * *thainer* - Thai NER engine
        * *tltk* - wrapper for `TLTK <https://pypi.org/project/tltk/>`_.

    **Options for corpus**
        * *thainer* - Thai NER corpus (default)

    **Note**: The tltk engine supports NER models from tltk only.
    """

    def __init__(self, engine: str = "thainer-v2", corpus: str = "thainer") -> None:
        self.load_engine(engine=engine, corpus=corpus)

    def load_engine(self, engine: str, corpus: str) -> None:
        self.name_engine = engine
        self.engine = None
        if engine == "thainer" and corpus == "thainer":
            from pythainlp.tag.thainer import ThaiNameTagger

            self.engine = ThaiNameTagger()
        elif engine == "thainer-v2" and corpus == "thainer":
            from pythainlp.wangchanberta import NamedEntityRecognition
            self.engine = NamedEntityRecognition(model="pythainlp/thainer-corpus-v2-base-model")
        elif engine == "tltk":
            from pythainlp.tag import tltk

            self.engine = tltk
        elif engine == "wangchanberta" and corpus == "thainer":
            from pythainlp.wangchanberta import ThaiNameTagger

            self.engine = ThaiNameTagger(dataset_name=corpus)
        elif engine == "phayathaibert" and corpus == "thainer-v2":
            from pythainlp.phayathaibert.core import NamedEntityTagger

            self.engine = NamedEntityTagger()
        else:
            raise ValueError(
                "NER class not support {0} engine or {1} corpus.".format(
                    engine, corpus
                )
            )

    def tag(self,
            text,
            pos=False,
            tag=False
            ) -> Union[List[Tuple[str, str]], List[Tuple[str, str, str]], str]:
        """
        This function tags named entities in text in IOB format.

        :param str text: text in Thai to be tagged
        :param bool pos: output with part-of-speech tags.\
            (wangchanberta is not supported)
        :param bool tag: output HTML-like tags.
        :return: a list of tuples associated with tokenized words, NER tags,
                 POS tags (if the parameter `pos` is specified as `True`),
                 and output HTML-like tags (if the parameter `tag` is
                 specified as `True`).
                 Otherwise, return a list of tuples associated with tokenized
                 words and NER tags
        :rtype: Union[List[Tuple[str, str]], List[Tuple[str, str, str]], str]
        :Example:

            >>> from pythainlp.tag import NER
            >>>
            >>> ner = NER("thainer")
            >>> ner.tag("ทดสอบนายวรรณพงษ์ ภัททิยไพบูลย์")
            [('ทดสอบ', 'O'),
            ('นาย', 'B-PERSON'),
            ('วรรณ', 'I-PERSON'),
            ('พงษ์', 'I-PERSON'),
            (' ', 'I-PERSON'),
            ('ภัททิย', 'I-PERSON'),
            ('ไพบูลย์', 'I-PERSON')]
            >>> ner.tag("ทดสอบนายวรรณพงษ์ ภัททิยไพบูลย์", tag=True)
            'ทดสอบ<PERSON>นายวรรณพงษ์ ภัททิยไพบูลย์</PERSON>'
        """
        return self.engine.get_ner(text, tag=tag, pos=pos)


class NNER:
    """
    Nested Named Entity Recognition

    :param str engine: engine of nested named entity recognizer
    :param str corpus: corpus

    **Options for engine**
        * *thai_nner* - Thai NER engine
    """

    def __init__(self, engine: str = "thai_nner") -> None:
        self.load_engine(engine)

    def load_engine(self, engine: str = "thai_nner") -> None:
        from pythainlp.tag.thai_nner import Thai_NNER

        self.engine = Thai_NNER()

    def tag(self, text) -> Tuple[List[str], List[dict]]:
        """
        This function tags nested named entities.

        :param str text: text in Thai to be tagged

        :return: a list of tuples associated with tokenized words and NNER tags.
        :rtype: Tuple[List[str], List[dict]]

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
        """
        return self.engine.tag(text)
