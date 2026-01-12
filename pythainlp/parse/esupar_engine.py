"""esupar: Tokenizer, POS tagger and dependency parser with BERT/RoBERTa/DeBERTa models for Japanese and other languages

GitHub: https://github.com/KoichiYasuoka/esupar
"""

from __future__ import annotations

try:
    import esupar
except ImportError:
    raise ImportError("Import Error; Install esupar by pip install esupar")


class Parse:
    def __init__(self, model: str = "th") -> None:
        if model is None:
            model = "th"
        self.nlp = esupar.load(model)

    def __call__(self, text: str, tag: str = "str") -> list[list[str]] | str:
        _data = str(self.nlp(text))
        if tag == "list":
            _temp = _data.splitlines()
            _tag_data = []
            for i in _temp:
                _tag_data.append(i.split())
            return _tag_data
        return _data
