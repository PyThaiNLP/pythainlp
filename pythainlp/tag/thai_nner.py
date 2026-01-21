# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Thai Nested Named Entity Recognition wrapper.

This module provides a wrapper for the Thai-NNER library which implements
Nested Named Entity Recognition for Thai text.
"""
from __future__ import annotations

from pythainlp.corpus import get_corpus_path


def get_top_level_entities(entities: list[dict]) -> list[dict]:
    """Extract only top-level (outermost) entities from nested NER results.

    In nested NER, entities can contain other entities. This function filters
    the results to return only the outermost entities that are not contained
    within any other entity.

    :param list[dict] entities: List of entity dictionaries with 'span',
                                'text', and 'entity_type' keys
    :return: List of top-level entities only
    :rtype: list[dict]

    :Example:
    ::

        from pythainlp.tag.thai_nner import get_top_level_entities

        # Input: nested entities where 'time' contains 'cardinal' and 'unit'
        entities = [
            {'text': ['ห้า'], 'span': [7, 9], 'entity_type': 'cardinal'},
            {'text': ['ห้า', 'โมง'], 'span': [7, 11], 'entity_type': 'time'},
            {'text': ['โมง'], 'span': [9, 11], 'entity_type': 'unit'}
        ]

        # Output: only 'time' entity (the outermost one)
        top_entities = get_top_level_entities(entities)
        # [{'text': ['ห้า', 'โมง'], 'span': [7, 11], 'entity_type': 'time'}]
    """
    top_level = []
    for ent in entities:
        is_contained = False
        for other in entities:
            if ent != other:
                # Check if ent is strictly contained in other
                if (other['span'][0] <= ent['span'][0] and
                    other['span'][1] >= ent['span'][1] and
                    not (other['span'][0] == ent['span'][0] and
                         other['span'][1] == ent['span'][1])):
                    is_contained = True
                    break
        if not is_contained:
            top_level.append(ent)
    return top_level


class Thai_NNER:
    """Thai Nested Named Entity Recognition.

    This class provides access to Thai Nested NER using the Thai-NNER model
    from https://github.com/vistec-AI/Thai-NNER

    The model recognizes nested named entities in Thai text, supporting
    104 entity types across multiple levels of nesting.

    :param str path_model: Path to the Thai-NNER model file.
                           If not specified, downloads from PyThaiNLP corpus.

    :Example:
    ::

        from pythainlp.tag.thai_nner import Thai_NNER

        nner = Thai_NNER()
        tokens, entities = nner.tag("วันนี้วันที่ 5 เมษายน 2565")
        print(f"Tokens: {tokens}")
        print(f"Entities: {entities}")
    """

    def __init__(self, path_model=get_corpus_path("thai_nner", "1.0")) -> None:
        """Initialize Thai_NNER with model path."""
        try:
            from thai_nner import NNER
        except ImportError:
            raise ImportError(
                "Not found thai_nner! Please install thai_nner by pip install thai-nner"
            )
        self.model = NNER(path_model=path_model)

    def tag(self, text: str, top_level_only: bool = False) -> tuple[list[str], list[dict]]:
        """Tag Thai text with nested named entities.

        :param str text: Thai text to tag
        :param bool top_level_only: If True, return only top-level (outermost)
                                    entities. If False, return all nested entities.
                                    Default is False.
        :return: Tuple of (tokens, entities) where tokens is a list of
                 tokenized strings and entities is a list of dictionaries
                 containing 'text', 'span', and 'entity_type' keys.
        :rtype: tuple[list[str], list[dict]]

        :Example:
        ::

            from pythainlp.tag.thai_nner import Thai_NNER

            nner = Thai_NNER()

            # Get all nested entities
            tokens, entities = nner.tag("วันที่ 5 เมษายน 2565")

            # Get only top-level entities
            tokens, top_entities = nner.tag("วันที่ 5 เมษายน 2565", top_level_only=True)
        """
        tokens, entities = self.model.get_tag(text)
        if top_level_only:
            entities = get_top_level_entities(entities)
        return tokens, entities
