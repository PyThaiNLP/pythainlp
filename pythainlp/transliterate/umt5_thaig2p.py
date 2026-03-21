# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""umt5-thai-g2p-v2-0.5k

huggingface: https://huggingface.co/B-K/umt5-thai-g2p-v2-0.5k
"""

# Use a pipeline as a high-level helper
from __future__ import annotations

from typing import TYPE_CHECKING, Optional, cast

if TYPE_CHECKING:
    from transformers import Pipeline


class Umt5ThaiG2P:
    """
    Thai Grapheme-to-Phoneme using UMT5 model.

    This version uses the B-K/umt5-thai-g2p-v2-0.5k model based on UMT5
    (Unified Multilingual T5) for converting Thai text to International
    Phonetic Alphabet (IPA) representation.

    For more information, see:
    https://huggingface.co/B-K/umt5-thai-g2p-v2-0.5k
    """

    pipe: Pipeline

    def __init__(self, device: str = "cpu") -> None:
        from transformers import pipeline

        self.pipe: "Pipeline" = pipeline(
            "text2text-generation",
            model="B-K/umt5-thai-g2p-v2-0.5k",
            device=device,
        )

    def g2p(self, text: str) -> str:
        outputs = cast(list[dict[str, str]], self.pipe(text))
        return outputs[0]["generated_text"]


_THAI_G2P: Optional[Umt5ThaiG2P] = None


def transliterate(text: str, device: str = "cpu") -> str:
    global _THAI_G2P
    if _THAI_G2P is None:
        _THAI_G2P = Umt5ThaiG2P(device=device)
    return _THAI_G2P.g2p(text)
