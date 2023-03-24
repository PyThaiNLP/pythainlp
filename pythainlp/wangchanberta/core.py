# -*- coding: utf-8 -*-
# Copyright (C) 2016-2023 PyThaiNLP Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from typing import List, Tuple, Union
import re
from transformers import (
    CamembertTokenizer,
    pipeline,
)
import warnings
from pythainlp.tokenize import word_tokenize

_model_name = "wangchanberta-base-att-spm-uncased"
_tokenizer = CamembertTokenizer.from_pretrained(
    f"airesearch/{_model_name}", revision="main"
)
if _model_name == "wangchanberta-base-att-spm-uncased":
    _tokenizer.additional_special_tokens = ["<s>NOTUSED", "</s>NOTUSED", "<_>"]


class ThaiNameTagger:
    def __init__(
        self, dataset_name: str = "thainer", grouped_entities: bool = True
    ):
        """
        This function tags named-entitiy from text in IOB format.

        Powered by wangchanberta from VISTEC-depa\
             AI Research Institute of Thailand

        :param str dataset_name:
            * *thainer* - ThaiNER dataset
        :param bool grouped_entities: grouped entities
        """
        self.dataset_name = dataset_name
        self.grouped_entities = grouped_entities
        self.classify_tokens = pipeline(
            task="ner",
            tokenizer=_tokenizer,
            model=f"airesearch/{_model_name}",
            revision=f"finetuned@{self.dataset_name}-ner",
            ignore_labels=[],
            grouped_entities=self.grouped_entities,
        )

    def _IOB(self, tag):
        if tag != "O":
            return "B-" + tag
        return "O"

    def _clear_tag(self, tag):
        return tag.replace("B-", "").replace("I-", "")

    def get_ner(
        self, text: str, pos: bool= False,tag: bool = False
    ) -> Union[List[Tuple[str, str]], str]:
        """
        This function tags named-entitiy from text in IOB format.
        Powered by wangchanberta from VISTEC-depa\
             AI Research Institute of Thailand

        :param str text: text in Thai to be tagged
        :param bool tag: output like html tag.
        :return: a list of tuple associated with tokenized word group, NER tag, \
                 and output like html tag (if the parameter `tag` is \
                 specified as `True`). \
                 Otherwise, return a list of tuple associated with tokenized \
                 word and NER tag
        :rtype: Union[list[tuple[str, str]]], str
        """
        if pos:
            warnings.warn("This model doesn't support output postag and It doesn't output the postag.")
        text = re.sub(" ", "<_>", text)
        self.json_ner = self.classify_tokens(text)
        self.output = ""
        if self.grouped_entities and self.dataset_name == "thainer":
            self.sent_ner = [
                (
                    i["word"].replace("<_>", " ").replace("▁", ""),
                    self._IOB(i["entity_group"]),
                )
                for i in self.json_ner
            ]
        elif self.dataset_name == "thainer":
            self.sent_ner = [
                (i["word"].replace("<_>", " ").replace("▁", ""), i["entity"])
                for i in self.json_ner
                if i["word"] != "▁"
            ]
        else:
            self.sent_ner = [
                (
                    i["word"].replace("<_>", " ").replace("▁", ""),
                    i["entity"].replace("_", "-").replace("E-", "I-"),
                )
                for i in self.json_ner
            ]
        if self.sent_ner[0][0] == "" and len(self.sent_ner) > 1:
            self.sent_ner = self.sent_ner[1:]
        for idx, (word, ner) in enumerate(self.sent_ner):
            if idx > 0 and ner.startswith("B-"):
                if self._clear_tag(ner) == self._clear_tag(
                    self.sent_ner[idx - 1][1]
                ):
                    self.sent_ner[idx] = (word, ner.replace("B-", "I-"))
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
        else:
            return self.sent_ner


class NamedEntityRecognition:
    def __init__(self, model: str ="pythainlp/thainer-corpus-v2-base-model") -> None:
        """
        This function tags named-entitiy from text in IOB format.

        Powered by wangchanberta from VISTEC-depa\
             AI Research Institute of Thailand
        :param str model: The model that use wangchanberta pretrained.
        """
        from transformers import AutoTokenizer
        from transformers import AutoModelForTokenClassification
        self.tokenizer = AutoTokenizer.from_pretrained(model)
        self.model = AutoModelForTokenClassification.from_pretrained(model)
    def _fix_span_error(self, words, ner):
        _ner = []
        _ner=ner
        _new_tag=[]
        for i,j in zip(words,_ner):
            i=self.tokenizer.decode(i)
            if i.isspace() and j.startswith("B-"):
                j="O"
            if i=='' or i=='<s>' or i=='</s>':
                continue
            if i=="<_>":
                i=" "
            _new_tag.append((i,j))
        return _new_tag
    def get_ner(
        self, text: str, pos: bool= False,tag: bool = False
    ) -> Union[List[Tuple[str, str]], str]:
        """
        This function tags named-entitiy from text in IOB format.
        Powered by wangchanberta from VISTEC-depa\
             AI Research Institute of Thailand

        :param str text: text in Thai to be tagged
        :param bool tag: output like html tag.
        :return: a list of tuple associated with tokenized word group, NER tag, \
                 and output like html tag (if the parameter `tag` is \
                 specified as `True`). \
                 Otherwise, return a list of tuple associated with tokenized \
                 word and NER tag
        :rtype: Union[list[tuple[str, str]]], str
        """
        import torch
        if pos:
            warnings.warn("This model doesn't support output postag and It doesn't output the postag.")
        words_token = word_tokenize(text.replace(" ", "<_>"))
        inputs=self.tokenizer(words_token,is_split_into_words=True,return_tensors="pt")
        ids = inputs["input_ids"]
        mask = inputs["attention_mask"]
        # forward pass
        outputs = self.model(ids, attention_mask=mask)
        logits = outputs[0]
        predictions = torch.argmax(logits, dim=2)
        predicted_token_class = [self.model.config.id2label[t.item()] for t in predictions[0]]
        ner_tag=self._fix_span_error(inputs['input_ids'][0],predicted_token_class)
        if tag:
            temp = ""
            sent = ""
            for idx, (word, ner) in enumerate(ner_tag):
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

                if idx == len(ner_tag) - 1 and temp != "":
                    sent += "</" + temp + ">"

            return sent
        return ner_tag


def segment(text: str) -> List[str]:
    """
    Subword tokenize. SentencePiece from wangchanberta model.

    :param str text: text to be tokenized
    :return: list of subwords
    :rtype: list[str]
    """
    if not text or not isinstance(text, str):
        return []

    return _tokenizer.tokenize(text)
