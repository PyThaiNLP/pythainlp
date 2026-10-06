# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""
Thai Nested Named Entity Recognition wrapper.

This module provides a wrapper for the Thai-NNER library which implements
Nested Named Entity Recognition for Thai text.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Union

from pythainlp.corpus import get_corpus_path

# Runtime import keeps typing.get_type_hints() working on this module.
from pythainlp.tag.named_entity import EntitySpan  # noqa: TC001

if TYPE_CHECKING:
    from thai_nner import NNER  # noqa: F401


__all__: list[str] = ["ThaiNNER"]


def _is_contained_in(entity: EntitySpan, container: EntitySpan) -> bool:
    """
    Check if an entity is strictly contained within a container entity.

    :param EntitySpan entity: entity to check
    :param EntitySpan container: potential container entity
    :return: ``True`` if the entity is strictly contained in the container
    :rtype: bool
    """
    ent_start, ent_end = entity["span"]
    cont_start, cont_end = container["span"]

    # Entity is contained if its span is within or equal to container's span,
    # but they're not exactly the same entity
    return (
        cont_start <= ent_start
        and cont_end >= ent_end
        and not (cont_start == ent_start and cont_end == ent_end)
    )


def get_top_level_entities(
    entities: list[EntitySpan],
) -> list[EntitySpan]:
    """
    Extract only top-level (outermost) entities from nested NER results.

    In nested NER, entities can contain other entities. This function filters
    the results to return only the outermost entities, which are not
    contained within other entities.

    :param list[EntitySpan] entities: list of entity dicts with ``span``,
        ``text``, and ``entity_type`` keys
    :return: list of top-level entities only
    :rtype: list[EntitySpan]

    :Example:

        >>> from pythainlp.tag.thai_nner import (
        ...     get_top_level_entities,
        ... )  # doctest: +SKIP

        >>> # Input: nested entities where 'time' contains 'cardinal' and 'unit'
        >>> entities = [  # doctest: +SKIP
        ...     {"text": ["ห้า"], "span": [7, 9], "entity_type": "cardinal"},
        ...     {
        ...         "text": ["ห้า", "โมง"],
        ...         "span": [7, 11],
        ...         "entity_type": "time",
        ...     },
        ...     {"text": ["โมง"], "span": [9, 11], "entity_type": "unit"},
        ... ]

        >>> # Output: only 'time' entity (the outermost one)
        >>> top_entities = get_top_level_entities(entities)  # doctest: +SKIP
        >>> # [{'text': ['ห้า', 'โมง'], 'span': [7, 11], 'entity_type': 'time'}]
    """
    if not entities:
        return []

    # Sort entities by span start, then by span end (descending)
    # This helps us process larger spans first
    sorted_entities = sorted(
        entities, key=lambda x: (x["span"][0], -x["span"][1])
    )

    top_level: list[EntitySpan] = []
    for ent in sorted_entities:
        is_contained = False
        # Only check against entities already in top_level
        for top_ent in top_level:
            if _is_contained_in(ent, top_ent):
                is_contained = True
                break
        if not is_contained:
            top_level.append(ent)
    return top_level


class ThaiNNER:
    """
    Thai nested named entity recognizer.

    This class provides access to Thai nested NER using the Thai-NNER model
    from https://github.com/vistec-AI/Thai-NNER

    The model recognizes nested named entities in Thai text, supporting
    104 entity types across multiple levels of nesting.

    :param Optional[str] path_model: path to the Thai-NNER model file;
        use the default PyThaiNLP corpus path if not specified

    :Example:

        >>> from pythainlp.tag.thai_nner import ThaiNNER  # doctest: +SKIP

        >>> nner = ThaiNNER()  # doctest: +SKIP
        >>> tokens, entities = nner.tag(
        ...     "วันนี้วันที่ 5 เมษายน 2565"
        ... )  # doctest: +SKIP
        >>> print(f"Tokens: {tokens}")  # doctest: +SKIP
        >>> print(f"Entities: {entities}")  # doctest: +SKIP
    """

    def __init__(self, path_model: Optional[str] = None) -> None:
        """
        Initialize the Thai nested named entity recognizer.

        :param Optional[str] path_model: path to the model file;
            use the default corpus path if ``None``
        """
        # Resolve path_model at runtime to avoid freezing the value at module import time
        if path_model is None:
            path_model = get_corpus_path("thai_nner", "1.0")
        if not path_model:
            raise FileNotFoundError(
                "corpus-not-found name='thai_nner'\n"
                "  Corpus 'thai_nner' not found.\n"
                "    Python: pythainlp.corpus.download('thai_nner')\n"
                "    CLI:    thainlp data get thai_nner"
            )

        # Import inside __init__ (not at module level) to allow:
        # 1. Helper functions (get_top_level_entities, _entities_to_iob, etc.) to work
        #    without requiring the thai-nner library
        # 2. Module to be imported for documentation generation
        # 3. Clear error message only when ThaiNNER class is actually instantiated
        try:
            from thai_nner import NNER
        except ImportError as e:
            raise ImportError(
                "thai-nner library not found. Please install it with 'pip install thai-nner'."
            ) from e
        self.model: NNER = NNER(path_model=path_model)

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

        :Example:

            >>> from pythainlp.tag.thai_nner import ThaiNNER  # doctest: +SKIP

            >>> nner = ThaiNNER()  # doctest: +SKIP

            >>> # Get all nested entities
            >>> tokens, entities = nner.tag(
            ...     "วันที่ 5 เมษายน 2565"
            ... )  # doctest: +SKIP

            >>> # Get only top-level entities
            >>> tokens, top_entities = nner.tag(  # doctest: +SKIP
            ...     "วันที่ 5 เมษายน 2565", top_level_only=True
            ... )
        """
        tokens, entities = self.model.get_tag(text)
        if top_level_only:
            entities = get_top_level_entities(entities)
        return tokens, entities

    def get_ner(
        self, text: str, pos: bool = False, tag: bool = False
    ) -> Union[list[tuple[str, str]], str]:
        """
        Tag named entities in text in IOB format.

        This method provides compatibility with the NER class interface by
        converting the nested entity format of Thai-NNER to IOB format.

        :param str text: Thai text to be tagged
        :param bool pos: include part-of-speech (POS) tags in the results
            (not supported; ignored)
        :param bool tag: return the text with HTML-like tags
            instead of a list of tuples
        :return: list of tuples (word, IOB tag), or the text with
            HTML-like tags if ``tag`` is ``True``
        :rtype: Union[list[tuple[str, str]], str]

        .. note::
            When converting to IOB format, only top-level entities are used to
            avoid overlapping tags. POS tagging is not supported and the pos
            parameter is ignored.

        :Example:

            >>> from pythainlp.tag.thai_nner import ThaiNNER  # doctest: +SKIP

            >>> nner = ThaiNNER()  # doctest: +SKIP

            >>> # Get IOB format
            >>> result = nner.get_ner("วันที่ 5 เมษายน 2565")  # doctest: +SKIP
            >>> # [('วัน', 'O'), ('ที่', 'O'), (' ', 'O'), ('5', 'B-DATE'), ...]

            >>> # Get HTML-like tags
            >>> result = nner.get_ner(
            ...     "วันที่ 5 เมษายน 2565", tag=True
            ... )  # doctest: +SKIP
            >>> # 'วันที่ <DATE>5 เมษายน 2565</DATE>'
        """
        # Get tokens and entities, using only top-level to avoid overlaps in IOB
        tokens, entities = self.tag(text, top_level_only=True)

        if tag:
            # Convert to HTML-like tags format
            return _entities_to_html(tokens, entities)
        # Convert to IOB format
        return _entities_to_iob(tokens, entities)


def _entities_to_iob(
    tokens: list[str], entities: list[EntitySpan]
) -> list[tuple[str, str]]:
    """
    Convert the Thai-NNER entity format to IOB format.

    This function assumes entities do not overlap. When converting nested
    entities to IOB format, use only top-level entities to avoid
    overlapping tags. If overlapping entities are given, later entities
    overwrite the IOB tags of earlier entities.

    :param list[str] tokens: list of words
    :param list[EntitySpan] entities: list of entity dicts
        (should not overlap)
    :return: list of (word, IOB tag) tuples
    :rtype: list[tuple[str, str]]
    """
    # Initialize all tokens as 'O' (outside)
    iob_tags = ["O"] * len(tokens)

    # Process each entity
    for entity in entities:
        start, end = entity["span"]
        entity_type = entity["entity_type"].upper()

        # Tag the first token as B- (beginning)
        if start < len(iob_tags):
            iob_tags[start] = f"B-{entity_type}"

        # Tag subsequent tokens as I- (inside)
        for i in range(start + 1, min(end, len(iob_tags))):
            iob_tags[i] = f"I-{entity_type}"

    # Combine tokens with their tags
    result = [(token, tag) for token, tag in zip(tokens, iob_tags)]
    return result


def _entities_to_html(tokens: list[str], entities: list[EntitySpan]) -> str:
    """
    Convert the Thai-NNER entity format to HTML-like tags.

    This function assumes entities do not overlap. If entities overlap,
    words between overlapping entities may be skipped. For best results,
    use only top-level entities (filter with ``get_top_level_entities()``).

    :param list[str] tokens: list of words
    :param list[EntitySpan] entities: list of entity dicts
    :return: text with HTML-like entity tags
    :rtype: str
    """
    # Sort entities by start position to process in order
    sorted_entities = sorted(entities, key=lambda x: x["span"][0])

    # Build the result string
    result_parts = []
    last_pos = 0

    for entity in sorted_entities:
        start, end = entity["span"]
        entity_type = entity["entity_type"].upper()

        # Add tokens before this entity
        result_parts.extend(tokens[last_pos:start])

        # Add entity with tags
        entity_text = "".join(tokens[start:end])
        result_parts.append(f"<{entity_type}>{entity_text}</{entity_type}>")

        last_pos = end

    # Add remaining tokens
    result_parts.extend(tokens[last_pos:])

    return "".join(result_parts)
