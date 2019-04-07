# -*- coding: utf-8 -*-
"""
Named-entity recognizer
"""

__all__ = ["ThaiNameTagger"]

from typing import List, Tuple, Union

import sklearn_crfsuite
from pythainlp.corpus import download, get_corpus_path, thai_stopwords
from pythainlp.tag import pos_tag
from pythainlp.tokenize import word_tokenize
from pythainlp.util import isthai

_WORD_TOKENIZER = "newmm"  # ตัวตัดคำ


def _is_stopword(word: str) -> bool:  # เช็คว่าเป็นคำฟุ่มเฟือย
    return word in thai_stopwords()


def _doc2features(doc, i) -> dict:
    word = doc[i][0]
    postag = doc[i][1]

    # Features from current word
    features = {
        "word.word": word,
        "word.stopword": _is_stopword(word),
        "word.isthai": isthai(word),
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
        prev_features = {
            "word.prevword": prevword,
            "word.previsspace": prevword.isspace(),
            "word.previsthai": isthai(prevword),
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
        next_features = {
            "word.nextword": nextword,
            "word.nextisspace": nextword.isspace(),
            "word.nextpostag": nextpostag,
            "word.nextisthai": isthai(nextword),
            "word.nextstopword": _is_stopword(nextword),
            "word.nextwordisdigit": nextword.isdigit(),
        }
        features.update(next_features)
    else:
        features["EOS"] = True  # Special "End of Sequence" tag

    return features


class ThaiNameTagger:
    def __init__(self):
        """
        Thai named-entity recognizer
        """
        self.__data_path = get_corpus_path("thainer")
        if not self.__data_path:
            download("thainer")
            self.__data_path = get_corpus_path("thainer")
        self.crf = sklearn_crfsuite.CRF(
            algorithm="lbfgs",
            c1=0.1,
            c2=0.1,
            max_iterations=500,
            all_possible_transitions=True,
            model_filename=self.__data_path,
        )

    def get_ner(
        self, text: str, pos: bool = True
    ) -> Union[List[Tuple[str, str]], List[Tuple[str, str, str]]]:
        """
        Get named-entities in text

        :param string text: Thai text
        :param boolean pos: get Part-Of-Speech tag (True) or get not (False)

        :return: list of strings with name labels (and part-of-speech tags)

        **Example**::
            >>> from pythainlp.tag.named_entity import ThaiNameTagger
            >>> ner = ThaiNameTagger()
            >>> ner.get_ner("วันที่ 15 ก.ย. 61 ทดสอบระบบเวลา 14:49 น.")
            [('วันที่', 'NOUN', 'O'), (' ', 'PUNCT', 'O'), ('15', 'NUM', 'B-DATE'),
            (' ', 'PUNCT', 'I-DATE'), ('ก.ย.', 'NOUN', 'I-DATE'),
            (' ', 'PUNCT', 'I-DATE'), ('61', 'NUM', 'I-DATE'),
            (' ', 'PUNCT', 'O'), ('ทดสอบ', 'VERB', 'O'),
            ('ระบบ', 'NOUN', 'O'), ('เวลา', 'NOUN', 'O'), (' ', 'PUNCT', 'O'),
            ('14', 'NOUN', 'B-TIME'), (':', 'PUNCT', 'I-TIME'), ('49', 'NUM', 'I-TIME'),
            (' ', 'PUNCT', 'I-TIME'), ('น.', 'NOUN', 'I-TIME')]
            >>> ner.get_ner("วันที่ 15 ก.ย. 61 ทดสอบระบบเวลา 14:49 น.", pos=False)
            [('วันที่', 'O'), (' ', 'O'), ('15', 'B-DATE'), (' ', 'I-DATE'),
            ('ก.ย.', 'I-DATE'), (' ', 'I-DATE'), ('61', 'I-DATE'), (' ', 'O'),
            ('ทดสอบ', 'O'), ('ระบบ', 'O'), ('เวลา', 'O'), (' ', 'O'), ('14', 'B-TIME'),
            (':', 'I-TIME'), ('49', 'I-TIME'), (' ', 'I-TIME'), ('น.', 'I-TIME')]
        """
        self.__tokens = word_tokenize(text, engine=_WORD_TOKENIZER)
        self.__pos_tags = pos_tag(
            self.__tokens, engine="perceptron", corpus="orchid_ud"
        )
        self.__x_test = self.__extract_features(self.__pos_tags)
        self.__y = self.crf.predict_single(self.__x_test)

        if pos:
            return [
                (self.__pos_tags[i][0], self.__pos_tags[i][1], data)
                for i, data in enumerate(self.__y)
            ]

        return [(self.__pos_tags[i][0], data) for i, data in enumerate(self.__y)]

    def __extract_features(self, doc):
        return [_doc2features(doc, i) for i in range(len(doc))]
