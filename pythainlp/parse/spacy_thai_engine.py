"""
spacy_thai: tokenizer, POS tagger, and dependency parser for Thai.

The parser uses Universal Dependencies.

GitHub: https://github.com/KoichiYasuoka/spacy-thai
"""

from __future__ import annotations

from typing import TYPE_CHECKING, List, Union

import spacy_thai

if TYPE_CHECKING:
    from spacy_thai import Language


class Parse:
    """Dependency parser using spacy_thai."""

    def __init__(self, model: str = "th") -> None:
        """
        Initialize the spacy_thai model.

        :param str model: model name; not used, the default model is loaded
        """
        self.nlp: Language = spacy_thai.load()

    def __call__(
        self, text: str, tag: str = "str"
    ) -> Union[List[List[str]], str]:
        """
        Parse the dependency structure of a text.

        :param str text: text to be parsed
        :param str tag: output type, ``"str"`` (CoNLL-U text, default)
            or ``"list"``
        :return: CoNLL-U text if ``tag`` is ``"str"``, otherwise a list of
            lists of fields
        :rtype: Union[List[List[str]], str]
        """
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
