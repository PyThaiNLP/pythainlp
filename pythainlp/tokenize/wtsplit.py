# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""
Where's the Point? Self-Supervised Multilingual Punctuation-Agnostic Sentence Segmentation

GitHub: https://github.com/bminixhofer/wtpsplit
"""

from __future__ import annotations

from wtpsplit import WtP

_MODEL = None
_MODEL_NAME = None


def _tokenize(
    text: str,
    lang_code: str = "th",
    model: str = "wtp-bert-mini",
    tokenize: str = "sentence",
    paragraph_threshold: float = 0.5,
    style: str = "newline",
) -> list[str]:
    global _MODEL_NAME, _MODEL

    if _MODEL_NAME != model:
        _MODEL = WtP(model_name_or_model=model)
        _MODEL_NAME = model

    if tokenize == "sentence":
        return _MODEL.split(text, lang_code=lang_code)
    else:  # Paragraph
        if style == "newline":
            return _MODEL.split(
                text,
                lang_code=lang_code,
                do_paragraph_segmentation=True,
                paragraph_threshold=paragraph_threshold,
            )
        elif style == "opus100":
            return _MODEL.split(
                text,
                lang_code=lang_code,
                do_paragraph_segmentation=True,
                threshold=paragraph_threshold,
                style=style,
            )
        else:
            raise ValueError(
                f"""Segmentation style \"{style}\" not found.
              It might be a typo; if not, please consult our document."""
            )


def tokenize(
    text: str,
    size: str = "mini",
    tokenize: str = "sentence",
    paragraph_threshold: float = 0.5,
    style: str = "newline",
) -> list[str]:
    _model_load = ""
    if size == "tiny":
        _model_load = "wtp-bert-tiny"
    elif size == "base":
        _model_load = "wtp-canine-s-1l"
    elif size == "large":
        _model_load = "wtp-canine-s-12l"
    else:  # mini
        _model_load = "wtp-bert-mini"

    return _tokenize(
        text,
        model=_model_load,
        tokenize=tokenize,
        paragraph_threshold=paragraph_threshold,
        style=style,
    )
