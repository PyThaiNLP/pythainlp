# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Named-entity recognizer"""

from __future__ import annotations

__all__: list[str] = ["ThaiNameTagger"]


from typing import TYPE_CHECKING, Union

from pythainlp.corpus import get_corpus_path, thai_stopwords
from pythainlp.tag.pos_tag import pos_tag
from pythainlp.tokenize import word_tokenize
from pythainlp.util import is_thai

if TYPE_CHECKING:
    from pycrfsuite import (
        Tagger as CRFTagger,  # pyright: ignore[reportAttributeAccessIssue]  # pyrefly: ignore[missing-module-attribute]
    )

_TOKENIZER_ENGINE: str = "mm"


def _is_stopword(word: str) -> bool:  # เช็คว่าเป็นคำฟุ่มเฟือย
    return word in thai_stopwords()


def _doc2features(
    doc: list[tuple[str, str]], i: int
) -> dict[str, Union[str, bool]]:
    features: dict[str, Union[str, bool]]
    word = doc[i][0]
    postag = doc[i][1]

    # Features from current word
    features = {
        "word.word": word,
        "word.stopword": _is_stopword(word),
        "word.isthai": is_thai(word),
        "word.isspace": word.isspace(),
        "postag": postag,
        "word.isdigit": word.isdigit(),
    }
    if word.isdigit() and len(word) == 5:
        features["word.islen5"] = True

    # Features from previous word
    if i > 0:
        prevword = doc[i - 1][0]
        prevpostag = doc[i - 1][1]
        prev_features: dict[str, Union[str, bool]] = {
            "word.prevword": prevword,
            "word.previsspace": prevword.isspace(),
            "word.previsthai": is_thai(prevword),
            "word.prevstopword": _is_stopword(prevword),
            "word.prevpostag": prevpostag,
            "word.prevwordisdigit": prevword.isdigit(),
        }
        features.update(prev_features)
    else:
        features["BOS"] = True  # Special "Beginning of Sequence" tag

    # Features from next word
    if i < len(doc) - 1:
        nextword = doc[i + 1][0]
        nextpostag = doc[i + 1][1]
        next_features: dict[str, Union[str, bool]] = {
            "word.nextword": nextword,
            "word.nextisspace": nextword.isspace(),
            "word.nextpostag": nextpostag,
            "word.nextisthai": is_thai(nextword),
            "word.nextstopword": _is_stopword(nextword),
            "word.nextwordisdigit": nextword.isdigit(),
        }
        features.update(next_features)
    else:
        features["EOS"] = True  # Special "End of Sequence" tag

    return features


class ThaiNameTagger:
    """Thai named-entity recognizer or Thai NER.
    This function supports Thai NER 1.4 and 1.5 only.
    :param str version: Thai NER version.
        It supports Thai NER 1.4 & 1.5.
        The default value is `1.4

    :Example:

        >>> from pythainlp.tag.thainer import ThaiNameTagger  # doctest: +SKIP

        >>> thainer14 = ThaiNameTagger(version="1.4")  # doctest: +SKIP
        >>> thainer14.get_ner("วันที่ 15 ก.ย. 61 ทดสอบระบบเวลา 14:49 น.")  # doctest: +SKIP
    """

    crf: CRFTagger
    pos_tag_name: str

    def __init__(self, version: str = "1.4") -> None:
        """Thai named-entity recognizer.

        :param str version: Thai NER version.
                            It's support Thai NER 1.4 & 1.5.
                            The default value is `1.4`
        """
        from pycrfsuite import (
            Tagger as CRFTagger,  # pyright: ignore[reportAttributeAccessIssue]  # pyrefly: ignore[missing-module-attribute]
        )

        self.crf: "CRFTagger" = CRFTagger()

        if version == "1.4":
            model_path = get_corpus_path("thainer-1.4", version="1.4")
            if not model_path:
                raise FileNotFoundError(
                    "corpus-not-found name='thainer-1.4'\n"
                    "  Corpus 'thainer-1.4' not found.\n"
                    "    Python: pythainlp.corpus.download('thainer-1.4')\n"
                    "    CLI:    thainlp data get thainer-1.4"
                )
            self.crf.open(model_path)
            self.pos_tag_name: str = "orchid_ud"
        elif version == "1.5":
            model_path = get_corpus_path("thainer", version="1.5")
            if not model_path:
                raise FileNotFoundError(
                    "corpus-not-found name='thainer'\n"
                    "  Corpus 'thainer' not found.\n"
                    "    Python: pythainlp.corpus.download('thainer')\n"
                    "    CLI:    thainlp data get thainer"
                )
            self.crf.open(model_path)
            self.pos_tag_name = "blackboard"

    def get_ner(
        self, text: str, pos: bool = True, tag: bool = False
    ) -> Union[list[tuple[str, str]], list[tuple[str, str, str]], str]:
        """This function tags named-entities in text in IOB format.

        :param str text: text in Thai to be tagged
        :param bool pos: To include POS tags in the results (`True`) or
                            exclude (`False`). The default value is `True`
        :param bool tag: output HTML-like tags.
        :return: a list of tuples associated with tokenized words, NER tags,
                 POS tags (if the parameter `pos` is specified as `True`),
                 and output HTML-like tags (if the parameter `tag` is
                 specified as `True`).
                 Otherwise, return a list of tuples associated with tokenized
                 words and NER tags
        :rtype: Union[list[tuple[str, str]], list[tuple[str, str, str]], str]

        :Note:
            * For the POS tags to be included in the results, this function
              uses :func:`pythainlp.tag.pos_tag` with engine `perceptron`
              and corpus `orchid_ud`.

        :Example:

            >>> from pythainlp.tag.thainer import ThaiNameTagger
            >>>
            >>> ner = ThaiNameTagger()
            >>> ner.get_ner("วันที่ 15 ก.ย. 61 ทดสอบระบบเวลา 14:49 น.")
            [('วันที่', 'NOUN', 'O'), (' ', 'PUNCT', 'O'),
            ('15', 'NUM', 'B-DATE'), (' ', 'PUNCT', 'I-DATE'),
            ('ก.ย.', 'NOUN', 'I-DATE'), (' ', 'PUNCT', 'I-DATE'),
            ('61', 'NUM', 'I-DATE'), (' ', 'PUNCT', 'O'),
            ('ทดสอบ', 'VERB', 'O'), ('ระบบ', 'NOUN', 'O'),
            ('เวลา', 'NOUN', 'O'), (' ', 'PUNCT', 'O'),
            ('14', 'NOUN', 'B-TIME'), (':', 'PUNCT', 'I-TIME'),
            ('49', 'NUM', 'I-TIME'), (' ', 'PUNCT', 'I-TIME'),
            ('น.', 'NOUN', 'I-TIME')]
            >>>
            >>> ner.get_ner("วันที่ 15 ก.ย. 61 ทดสอบระบบเวลา 14:49 น.",
                            pos=False)
            [('วันที่', 'O'), (' ', 'O'),
            ('15', 'B-DATE'), (' ', 'I-DATE'),
            ('ก.ย.', 'I-DATE'), (' ', 'I-DATE'),
            ('61', 'I-DATE'), (' ', 'O'),
            ('ทดสอบ', 'O'), ('ระบบ', 'O'),
            ('เวลา', 'O'), (' ', 'O'),
            ('14', 'B-TIME'), (':', 'I-TIME'),
            ('49', 'I-TIME'), (' ', 'I-TIME'),
            ('น.', 'I-TIME')]
            >>> ner.get_ner("วันที่ 15 ก.ย. 61 ทดสอบระบบเวลา 14:49 น.",
                            tag=True)
            'วันที่ <DATE>15 ก.ย. 61</DATE> ทดสอบระบบเวลา <TIME>14:49 น.</TIME>'
        """
        tokens = word_tokenize(text, engine=_TOKENIZER_ENGINE)
        pos_tags = pos_tag(
            tokens, engine="perceptron", corpus=self.pos_tag_name
        )
        x_test = ThaiNameTagger._extract_features(pos_tags)
        y = self.crf.tag(x_test)

        sent_ner = [(pos_tags[i][0], data) for i, data in enumerate(y)]

        if tag:
            temp = ""
            sent = ""
            for idx, (word, ner) in enumerate(sent_ner):
                if ner.startswith("B-") and temp != "":
                    sent += "</" + temp + ">"
                    temp = ner[2:]
                    sent += "<" + temp + ">"
                elif ner.startswith("B-"):
                    temp = ner[2:]
                    sent += "<" + temp + ">"
                elif ner == "O" and temp != "":
                    sent += "</" + temp + ">"
                    temp = ""
                sent += word

                if idx == len(sent_ner) - 1 and temp != "":
                    sent += "</" + temp + ">"

            return sent

        if pos:
            return [
                (pos_tags[i][0], pos_tags[i][1], data)
                for i, data in enumerate(y)
            ]

        return sent_ner

    @staticmethod
    def _extract_features(
        doc: list[tuple[str, str]],
    ) -> list[dict[str, Union[str, bool]]]:
        return [_doc2features(doc, i) for i in range(len(doc))]
