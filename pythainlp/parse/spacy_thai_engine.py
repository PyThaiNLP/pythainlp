# -*- coding: utf-8 -*-
"""
spacy_thai: Tokenizer, POS tagger, and dependency parser for the Thai language using Universal Dependencies.

GitHub: https://github.com/KoichiYasuoka/spacy-thai

"""
from typing import List, Union

import spacy_thai


class Parse:
    def __init__(self, model: str = "th") -> None:
        self.nlp = spacy_thai.load()

    def __call__(
        self, text: str, tag: str = "str"
    ) -> Union[List[List[str]], str]:
        doc = self.nlp(text)
        _text = []
        if tag == "list":
            _tag_data = []
            for t in doc:
                _tag_data.append(
                    [
                        str(t.i + 1),
                        t.orth_,
                        t.lemma_,
                        t.pos_,
                        t.tag_,
                        "_",
                        str(0 if t.head == t else t.head.i + 1),
                        t.dep_,
                        "_",
                        "_" if t.whitespace_ else "SpaceAfter=No",
                    ]
                )
            return _tag_data
        for t in doc:
            _text.append(
                "\t".join(
                    [
                        str(t.i + 1),
                        t.orth_,
                        t.lemma_,
                        t.pos_,
                        t.tag_,
                        "_",
                        str(0 if t.head == t else t.head.i + 1),
                        t.dep_,
                        "_",
                        "_" if t.whitespace_ else "SpaceAfter=No",
                    ]
                )
            )
        return "\n".join(_text)
