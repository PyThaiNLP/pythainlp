# -*- coding: utf-8 -*-
"""
Named-entity recognizer
"""
import warnings
from typing import List, Tuple, Union

from pythainlp.util.messages import deprecation_message


class NER:
    """
    Named-entity recognizer class

    :param str engine: Named-entity recognizer engine
    :param str corpus: corpus

    **Options for engine**
        * *thainer* - Thai NER engine
        * *wangchanberta* - wangchanberta model
        * *lst20_onnx* - LST20 NER model by wangchanberta with ONNX runtime
        * *tltk* - wrapper for `TLTK <https://pypi.org/project/tltk/>`_.

    **Options for corpus**
        * *thaimer* - Thai NER corpus
        * *lst20* - lst20 corpus (wangchanberta only). \
            `LST20 <https://aiforthai.in.th/corpus.php>`_ corpus \
            by National Electronics and Computer Technology Center, Thailand \
            It is free for **non-commercial uses and research only**. \
            You can read at \
            `Facebook <https://www.facebook.com/dancearmy/posts/10157641945708284>`_.

    **Note**: for tltk engine, It's support ner model from tltk only.
    """

    def __init__(self, engine: str, corpus: str = "thainer") -> None:
        if any([arg.startswith("lst20") for arg in (engine, corpus)]):
            dep_msg = deprecation_message(
                [("engine", "lst20_onnx"), ("corpus", "lst20")],
                "`named_entity.NER`",
                "4.0.0",
            )
            warnings.warn(dep_msg, DeprecationWarning, stacklevel=2)
        self.load_engine(engine=engine, corpus=corpus)

    def load_engine(self, engine: str, corpus: str) -> None:
        self.name_engine = engine
        self.engine = None
        if engine == "thainer" and corpus == "thainer":
            from pythainlp.tag.thainer import ThaiNameTagger

            self.engine = ThaiNameTagger()
        elif engine == "lst20_onnx":
            from pythainlp.tag.lst20_ner_onnx import LST20_NER_ONNX

            self.engine = LST20_NER_ONNX()
        elif engine == "wangchanberta":
            from pythainlp.wangchanberta import ThaiNameTagger

            if corpus == "lst20":
                warnings.warn(
                    """
                LST20 corpus are free for research and open source only.\n
                If you want to use in Commercial use, please contract NECTEC.\n
                https://www.facebook.com/dancearmy/posts/10157641945708284
                """
                )
            self.engine = ThaiNameTagger(dataset_name=corpus)
        elif engine == "tltk":
            from pythainlp.tag import tltk

            self.engine = tltk
        else:
            raise ValueError(
                "NER class not support {0} engine or {1} corpus.".format(
                    engine, corpus
                )
            )

    def tag(
        self, text, pos=True, tag=False
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
        if (
            self.name_engine == "wangchanberta"
            or self.name_engine == "lst20_onnx"
        ):
            return self.engine.get_ner(text, tag=tag)
        else:
            return self.engine.get_ner(text, tag=tag, pos=pos)


class NNER:
    """
    Nested Named Entity Recognition

    :param str engine: Nested Named entity recognizer engine
    :param str corpus: corpus

    **Options for engine**
        * *thai_nner* - Thai NER engine
    """

    def __init__(self, engine: str = "thai_nner") -> None:
        self.load_engine(engine)

    def load_engine(self, engine: str = "thai_nner") -> None:
        from pythainlp.tag.thai_nner import Thai_NNER

        self.engine = Thai_NNER()

    def tag(self, text) -> Tuple[List[str], List[dict]]:
        """
        This function tags nested named-entitiy.

        :param str text: text in Thai to be tagged

        :return: a list of tuple associated with tokenized word, NNER tag.
        :rtype: Tuple[List[str], List[dict]]

        :Example:

            >>> from pythainlp.tag.named_entity import NNER
            >>> nner = NNER()
            >>> nner.tag("แมวทำอะไรตอนห้าโมงเช้า")
            ([
                '<s>',
                '',
                'แมว',
                'ทํา',
                '',
                'อะไร',
                'ตอน',
                '',
                'ห้า',
                '',
                'โมง',
                '',
                'เช้า',
                '</s>'
            ],
            [
                {
                    'text': ['', 'ห้า'],
                    'span': [7, 9],
                    'entity_type': 'cardinal'
                },
                {
                    'text': ['', 'ห้า', '', 'โมง'],
                    'span': [7, 11],
                    'entity_type': 'time'
                },
                {
                    'text': ['', 'โมง'],
                    'span': [9, 11],
                    'entity_type': 'unit'
                }
            ])
        """
        return self.engine.tag(text)
