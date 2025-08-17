# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2025 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""
umt5-thai-g2p-v2-0.5k 

huggingface: https://huggingface.co/B-K/umt5-thai-g2p-v2-0.5k
"""

# Use a pipeline as a high-level helper
from transformers import pipeline


class Umt5ThaiG2P:
    """
    Latin transliteration of Thai words, using International Phonetic Alphabet
    """

    def __init__(self, device: str = "cpu"):
        self.pipe = pipeline("text2text-generation", model="B-K/umt5-thai-g2p-v2-0.5k", device=device)

    def g2p(self, text: str) -> str:
        return self.pipe(text)[0]["generated_text"]


_THAI_G2P = None


def transliterate(text: str, device="cpu") -> str:
    global _THAI_G2P
    if _THAI_G2P is None:
        _THAI_G2P = Umt5ThaiG2P(device=device)
    return _THAI_G2P.g2p(text)
