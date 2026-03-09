# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Where's the Point? Self-Supervised Multilingual Punctuation-Agnostic Sentence Segmentation

GitHub: https://github.com/bminixhofer/wtpsplit
"""

from __future__ import annotations

import threading
from typing import Optional, cast

from wtpsplit import WtP

_MODEL: Optional[WtP] = None
_MODEL_NAME: Optional[str] = None
_model_lock: threading.Lock = threading.Lock()


def _tokenize(
    text: str,
    lang_code: str = "th",
    model: str = "wtp-bert-mini",
    tokenize: str = "sentence",
    paragraph_threshold: float = 0.5,
    style: str = "newline",
) -> list[str]:
    """Internal tokenization function with model loading protection.

    The wrapper uses a lock to protect model loading when switching models.
    However, thread-safety of the underlying WtP library itself is not
    guaranteed. Please refer to the WtP library documentation for its
    thread-safety guarantees.
    """
    # Thread-safe model loading
    global _MODEL, _MODEL_NAME
    with _model_lock:
        if _MODEL_NAME != model:
            _MODEL = WtP(model_name_or_model=model)
            _MODEL_NAME = model
        model_instance = _MODEL

    # Ensure model is loaded
    if model_instance is None:
        raise RuntimeError("Model failed to load")

    if tokenize == "sentence":
        return cast(
            "list[str]", model_instance.split(text, lang_code=lang_code)
        )
    else:  # Paragraph
        if style == "newline":
            return cast(
                "list[str]",
                model_instance.split(
                    text,
                    lang_code=lang_code,
                    do_paragraph_segmentation=True,
                    paragraph_threshold=paragraph_threshold,
                ),
            )
        elif style == "opus100":
            return cast(
                "list[str]",
                model_instance.split(
                    text,
                    lang_code=lang_code,
                    do_paragraph_segmentation=True,
                    threshold=paragraph_threshold,
                    style=style,
                ),
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
