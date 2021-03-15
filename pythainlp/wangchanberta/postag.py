from typing import Dict, List, Tuple, Union
import re
from transformers import (
    CamembertTokenizer,
    AutoTokenizer,
    pipeline,
)

_model_name = "wangchanberta-base-att-spm-uncased"
_tokenizer = CamembertTokenizer.from_pretrained(
        f'airesearch/{_model_name}',
        revision='main')
if _model_name == "wangchanberta-base-att-spm-uncased":
    _tokenizer.additional_special_tokens = ['<s>NOTUSED', '</s>NOTUSED', '<_>']


class PosTagTransformers:
    def __init__(
        self,
        corpus: str = "lst20",
        grouped_word: bool = False
    ) -> None:
        self.corpus = corpus
        self.grouped_word = grouped_word
        self.load()

    def load(self):
        self.classify_tokens = pipeline(
            task='ner',
            tokenizer=_tokenizer,
            model=f'airesearch/{_model_name}',
            revision=f'finetuned@{self.corpus}-pos',
            ignore_labels=[],
            grouped_entities=self.grouped_word
        )

    def tag(
        self, text: str, corpus: str = "lst20", grouped_word: bool = False
    ) -> List[Tuple[str, str]]:
        if (
            corpus != self.corpus and corpus in ['lst20']
        ) or grouped_word != self.grouped_word:
            self.grouped_word = grouped_word
            self.corpus = corpus
            self.load()
        text = re.sub(" ", "<_>", text)
        self.json_pos = self.classify_tokens(text)
        self.output = ""
        if grouped_word:
            self.sent_pos = [
                (
                    i['word'].replace("<_>", " "), i['entity_group']
                ) for i in self.json_pos
            ]
        else:
            self.sent_pos = [
                (
                    i['word'].replace("<_>", " ").replace('▁', ''),
                    i['entity']
                )
                for i in self.json_pos if i['word'] != '▁'
            ]
        return self.sent_pos


_corpus = "lst20"
_grouped_word = False
_postag = PosTagTransformers(corpus=_corpus, grouped_word=_grouped_word)


def pos_tag(
    text: str, corpus: str = "lst20", grouped_word: bool = False
) -> List[Tuple[str, str]]:
    """
    Marks words with part-of-speech (POS) tags.

    :param str text: thai text
    :param str corpus:
        * *lst20* - a LST20 tagger (default)
    :param bool grouped_word: grouped word (default is False)
    :return: a list of tuples (word, POS tag)
    :rtype: list[tuple[str, str]]
    """
    global _grouped_word, _postag
    if isinstance(text, list):
        text = ''.join(text)
    elif not text or not isinstance(text, str):
        return []
    if corpus not in ["lst20"]:
        raise NotImplementedError()
    if _grouped_word != grouped_word:
        _postag = PosTagTransformers(
            corpus=corpus,
            grouped_word=grouped_word
        )
        _grouped_word = grouped_word
    return _postag.tag(
        text,
        corpus=corpus,
        grouped_word=grouped_word
    )
