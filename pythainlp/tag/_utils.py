# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Helpers shared by the named entity taggers."""

from __future__ import annotations


def _iob_to_markup(tagged: list[tuple[str, str]]) -> str:
    """Join (word, IOB tag) pairs into text with XML-like entity tags.

    A ``B-X`` tag opens ``<X>`` and closes the previous entity, if any.
    An ``O`` tag closes the open entity. An ``I-X`` tag changes nothing,
    even if ``X`` differs from the open entity. An entity still open at the
    last word is closed.

    :param list[tuple[str, str]] tagged: words with their IOB tags
    :return: text with entities wrapped, such as ``<DATE>15 ก.ย.</DATE>``
    :rtype: str
    """
    open_entity = ""
    out: list[str] = []
    for word, tag in tagged:
        if tag.startswith("B-"):
            if open_entity:
                out.append(f"</{open_entity}>")
            open_entity = tag[2:]
            out.append(f"<{open_entity}>")
        elif tag == "O" and open_entity:
            out.append(f"</{open_entity}>")
            open_entity = ""
        out.append(word)
    if open_entity:
        out.append(f"</{open_entity}>")
    return "".join(out)
