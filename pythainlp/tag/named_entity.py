# -*- coding: utf-8 -*-
"""
Named-entity recognizer
"""
import warnings
from typing import List, Tuple, Union
from pythainlp.tag.thainer import ThaiNameTagger


class NER:
    """
    Named-entity recognizer class

    :param str engine: Named-entity recognizer engine
    :param str corpus: corpus

    **Options for engine**
        * *thainer* - Thai NER engine
        * *wangchanberta* - wangchanberta model
        * *tltk* - wrapper for `TLTK <https://pypi.org/project/tltk/>`_.

    **Options for corpus**
        * *thaimer* - Thai NER corpus
        * *lst20* - lst20 corpus (wangchanberta only)

    **Note**: for tltk engine, It's support ner model from tltk only.
    """
    def __init__(self, engine: str, corpus: str = "thainer") -> None:
        self.load_engine(engine=engine, corpus=corpus)

    def load_engine(self, engine: str, corpus: str) -> None:
        self.name_engine = engine
        self.engine = None
        if engine == "thainer" and corpus == "thainer":
            from pythainlp.tag.thainer import ThaiNameTagger
            self.engine = ThaiNameTagger()
        elif engine == "wangchanberta":
            from pythainlp.wangchanberta import ThaiNameTagger
            self.engine = ThaiNameTagger(dataset_name=corpus)
        elif engine == "tltk":
            from pythainlp.tag import tltk
            self.engine = tltk
        else:
            raise ValueError(
                "NER class not support {0} engine or {1} corpus.".format(
                    engine,
                    corpus
                )
            )

    def tag(
        self,
        text,
        pos=True,
        tag=False
    ) -> Union[List[Tuple[str, str]], List[Tuple[str, str, str]], str]:
        """
        This function tags named-entitiy from text in IOB format.

        :param str text: text in Thai to be tagged
        :param bool pos: output with part-of-speech tag.\
            (wangchanberta is not support)
        :param bool tag: output like html tag.
        :return: a list of tuple associated with tokenized word, NER tag,
                 POS tag (if the parameter `pos` is specified as `True`),
                 and output like html tag (if the parameter `tag` is
                 specified as `True`).
                 Otherwise, return a list of tuple associated with tokenized
                 word and NER tag
        :rtype: Union[List[Tuple[str, str]], List[Tuple[str, str, str]], str]
        :Example:

            >>> from pythainlp.tag import NER
            >>>
            >>> ner = NER("thainer")
            >>> ner.tag("ทดสอบนายวรรณพงษ์ ภัททิยไพบูลย์")
            [('ทดสอบ', 'VV', 'O'),
            ('นาย', 'NN', 'B-PERSON'),
            ('วรรณ', 'NN', 'I-PERSON'),
            ('พงษ์', 'NN', 'I-PERSON'),
            (' ', 'PU', 'I-PERSON'),
            ('ภัททิย', 'NN', 'I-PERSON'),
            ('ไพบูลย์', 'NN', 'I-PERSON')]
            >>> ner.tag("ทดสอบนายวรรณพงษ์ ภัททิยไพบูลย์", tag=True)
            'ทดสอบ<PERSON>นายวรรณพงษ์ ภัททิยไพบูลย์</PERSON>'
        """
        if pos and self.name_engine == "wangchanberta":
            warnings.warn(
                """wangchanberta is not support part-of-speech tag.
                It have not part-of-speech tag in output."""
            )
        if self.name_engine == "wangchanberta":
            return self.engine.get_ner(text, tag=tag)
        else:
            return self.engine.get_ner(text, tag=tag, pos=pos)
