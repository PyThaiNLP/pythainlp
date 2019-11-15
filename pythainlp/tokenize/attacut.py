"""
Wrapper for AttaCut - Fast and Reasonably Accurate Word Tokenizer for Thai
:See Also:
    * `GitHub repository <https://github.com/PyThaiNLP/attacut>`_
"""
from typing import List

from attacut import tokenize


def segment(text: str) -> List[str]:
    if not text or not isinstance(text, str):
        return []

    return tokenize(text)
