"""esupar: Tokenizer, POS tagger and dependency parser with BERT/RoBERTa/DeBERTa models for Japanese and other languages

GitHub: https://github.com/KoichiYasuoka/esupar
"""

from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, Union

try:
    import esupar
except ImportError as e:
    raise ImportError(
        "esupar is not installed. Install it with: pip install esupar"
    ) from e

if TYPE_CHECKING:
    from esupar import Model


class Parse:
    def __init__(self, model: Optional[str] = "th") -> None:
        if model is None:
            model = "th"
        self.nlp: Model = esupar.load(model)

    def __call__(
        self, text: str, tag: str = "str"
    ) -> Union[List[List[str]], str]:
        _data = str(self.nlp(text))
        if tag == "list":
            _temp = _data.splitlines()
            _tag_data = []
            for i in _temp:
                _tag_data.append(i.split())
            return _tag_data
        return _data
