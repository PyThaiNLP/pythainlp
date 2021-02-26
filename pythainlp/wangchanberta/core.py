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


class ThaiNameTagger:
    def __init__(self,
                dataset_name: str = "thainer",
                grouped_entities: bool = True):
        self.dataset_name = dataset_name
        self.grouped_entities = grouped_entities
        self.classify_tokens = pipeline(
            task='ner',
            tokenizer=_tokenizer,
            model = f'airesearch/{_model_name}',
            revision = f'finetuned@{self.dataset_name}-ner',
            ignore_labels=[], 
            grouped_entities=self.grouped_entities
        )
    
    def IOB(self, tag):
        if tag != "O":
            return "B-"+tag
        return "O"

    def get_ner(
        self, text: str, tag: bool = False
    ) -> List[Tuple[str, str]]:
        """
        This function tags named-entitiy from text in IOB format.

        Powered by wangchanberta from VISTEC-depa AI Research Institute of Thailand
        :param str text: text in Thai to be tagged
        :param bool tag: output like html tag.
        :return: a list of tuple associated with tokenized word group, NER tag,
                 and output like html tag (if the parameter `tag` is
                 specified as `True`).
                 Otherwise, return a list of tuple associated with tokenized
                 word and NER tag
        :rtype: Union[list[tuple[str, str]]], str
        """
        text = re.sub(" ", "<_>", text)
        self.json_ner = self.classify_tokens(text)
        self.output = ""
        if self.grouped_entities and self.dataset_name == "thainer":
            self.sent_ner = [(i['word'].replace("<_>", " "), self.IOB(i['entity_group'])) for i in self.json_ner]
        elif self.dataset_name == "thainer":
            self.sent_ner = [(i['word'].replace("<_>", " "), i['entity']) for i in self.json_ner if i['word'] != '▁']
        elif self.grouped_entities and self.dataset_name == "lst20":
            self.sent_ner = [(i['word'].replace("<_>", " "), self.IOB(i['entity_group'].replace('_','-').replace('E-','I-'))) for i in self.json_ner]
        else:
            self.sent_ner = [(i['word'].replace("<_>", " "), i['entity_group'].replace('_','-').replace('E-','I-')) for i in self.json_ner]

        if tag:
            temp = ""
            sent = ""
            for idx, (word, ner) in enumerate(self.sent_ner):
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

                if idx == len(self.sent_ner) - 1 and temp != "":
                    sent += "</" + temp + ">"

            return sent
        
        return self.sent_ner


class PosTagTransformers:
    def __init__(self,
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
            model = f'airesearch/{_model_name}',
            revision = f'finetuned@{self.corpus}-pos',
            ignore_labels=[], 
            grouped_entities=self.grouped_word
        )

    def tag(
        self, text: str, corpus: str = False, grouped_word: bool = False
    ) -> List[Tuple[str, str]]:
        if (corpus != self.corpus and corpus in ['lst20']) or grouped_word != self.grouped_word:
            self.grouped_word = grouped_word
            self.corpus = corpus
            self.load()
        text = re.sub(" ", "<_>", text)
        self.json_pos = self.classify_tokens(text)
        self.output = ""
        if grouped_word:
            self.sent_pos = [(i['word'].replace("<_>", " "),i['entity_group']) for i in self.json_pos]
        else:
            self.sent_pos = [(i['word'].replace("<_>", " ").replace('▁',''), i['entity']) for i in self.json_pos if i['word'] != '▁']
        return self.sent_pos

def segment(text):
    return _tokenizer.tokenize(text)
