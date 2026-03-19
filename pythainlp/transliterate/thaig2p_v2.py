# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Thai Grapheme-to-Phoneme (Thai G2P)

huggingface: https://huggingface.co/pythainlp/thaig2p-v2.0
"""

# Use a pipeline as a high-level helper
from __future__ import annotations

from typing import TYPE_CHECKING, Optional, cast

if TYPE_CHECKING:
    from transformers import Pipeline


class ThaiG2P:
    """
    Thai Grapheme-to-Phoneme using transformer-based model (v2).

    This version uses the Hugging Face transformers pipeline with the
    pythainlp/thaig2p-v2.0 model for converting Thai text to International
    Phonetic Alphabet (IPA) representation.

    For more information, see:
    https://huggingface.co/pythainlp/thaig2p-v2.0
    """

    pipe: Pipeline

    def __init__(self, device: str = "cpu") -> None:
        from transformers import pipeline

        self.pipe: "Pipeline" = pipeline(
            "text2text-generation",
            model="pythainlp/thaig2p-v2.0",
            device=device,
        )

    def g2p(self, text: str) -> str:
        outputs = cast(list[dict[str, str]], self.pipe(text))
        return outputs[0]["generated_text"]


_THAI_G2P: Optional[ThaiG2P] = None


def transliterate(text: str, device: str = "cpu") -> str:
    global _THAI_G2P
    if _THAI_G2P is None:
        _THAI_G2P = ThaiG2P(device=device)
    return _THAI_G2P.g2p(text)
