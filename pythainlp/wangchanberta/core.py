# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Named entity recognition using WangchanBERTa."""

from __future__ import annotations

import re
import warnings
from typing import TYPE_CHECKING, Optional, Union, cast

if TYPE_CHECKING:
    from transformers import (
        CamembertTokenizer,
        PreTrainedModel,
        PreTrainedTokenizerBase,
    )
    from transformers.pipelines import TokenClassificationPipeline

from pythainlp.tokenize import word_tokenize

_model_name: str = "wangchanberta-base-att-spm-uncased"
_tokenizer: Optional[CamembertTokenizer] = None


def _get_tokenizer() -> CamembertTokenizer:
    """Return the tokenizer, initializing it if necessary."""
    global _tokenizer
    if _tokenizer is None:
        from transformers import CamembertTokenizer

        _tokenizer = CamembertTokenizer.from_pretrained(
            f"airesearch/{_model_name}",
            revision="main",  # nosec B615
        )
        if _model_name == "wangchanberta-base-att-spm-uncased":
            _tokenizer.additional_special_tokens = [
                "<s>NOTUSED",
                "</s>NOTUSED",
                "<_>",
            ]
    return _tokenizer


class ThaiNameTagger:
    """Tag named entities in Thai text using WangchanBERTa."""

    dataset_name: str
    grouped_entities: bool
    classify_tokens: TokenClassificationPipeline
    json_ner: list[dict[str, str]]
    output: str
    sent_ner: list[tuple[str, str]]

    def __init__(
        self, dataset_name: str = "thainer", grouped_entities: bool = True
    ) -> None:
        """
        Initialize a named entity tagger in IOB format.

        Powered by WangchanBERTa from the VISTEC-depa AI Research
        Institute of Thailand.

        :param str dataset_name: dataset the model is fine-tuned on

            * *thainer* - ThaiNER dataset (default)

        :param bool grouped_entities: whether to group word pieces of
            the same entity
        """
        from transformers import pipeline

        self.dataset_name = dataset_name
        self.grouped_entities = grouped_entities
        self.classify_tokens = pipeline(
            task="ner",
            tokenizer=_get_tokenizer(),
            model=f"airesearch/{_model_name}",
            revision=f"finetuned@{self.dataset_name}-ner",
            ignore_labels=[],
            grouped_entities=self.grouped_entities,
        )

    def _IOB(self, tag: str) -> str:
        if tag != "O":
            return "B-" + tag
        return "O"

    def _clear_tag(self, tag: str) -> str:
        return tag.replace("B-", "").replace("I-", "")

    def get_ner(  # noqa: C901, CCR001  # phase2-todo
        self, text: str, pos: bool = False, tag: bool = False
    ) -> Union[list[tuple[str, str]], str]:
        """
        Tag named entities in text in IOB format.

        Powered by WangchanBERTa from the VISTEC-depa AI Research
        Institute of Thailand.

        :param str text: Thai text to be tagged
        :param bool pos: output part-of-speech tags. This model does not
            support them, so a warning is raised.
        :param bool tag: return HTML-like tags in a string instead of a
            list of tuples
        :return: list of tuples (word group, named entity tag), or a string
            with HTML-like tags if **tag** is True
        :rtype: Union[list[tuple[str, str]], str]
        """
        if pos:
            warnings.warn(
                "This model does not support POS tag output.",
                UserWarning,
                stacklevel=2,
            )
        text = re.sub(" ", "<_>", text)
        self.json_ner: list[dict[str, str]] = self.classify_tokens(text)
        self.output: str = ""
        if self.grouped_entities and self.dataset_name == "thainer":
            self.sent_ner: list[tuple[str, str]] = [
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
            if (
                idx > 0
                and ner.startswith("B-")
                and self._clear_tag(ner)
                == self._clear_tag(self.sent_ner[idx - 1][1])
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
        return self.sent_ner


class NamedEntityRecognition:
    """Recognize named entities in Thai text using WangchanBERTa."""

    tokenizer: PreTrainedTokenizerBase
    model: PreTrainedModel

    def __init__(
        self,
        model: str = "pythainlp/thainer-corpus-v2-base-model",
        revision: Optional[str] = None,
    ) -> None:
        """
        Initialize a named entity tagger in IOB format.

        Powered by WangchanBERTa from the VISTEC-depa AI Research
        Institute of Thailand.

        :param str model: name of a model pretrained from WangchanBERTa
        :param Optional[str] revision: git revision id (branch, tag, or
            commit hash). Pin to a full commit hash for secure downloads.
        """
        from transformers import AutoModelForTokenClassification, AutoTokenizer

        self.tokenizer: PreTrainedTokenizerBase = (
            AutoTokenizer.from_pretrained(model, revision=revision)
        )
        self.model: PreTrainedModel = (
            AutoModelForTokenClassification.from_pretrained(
                model, revision=revision
            )
        )

    def _fix_span_error(
        self, words: list[int], ner: list[str]
    ) -> list[tuple[str, str]]:
        _ner = []
        _ner = ner
        _new_tag = []
        for i, j in zip(words, _ner):
            i_decoded = self.tokenizer.decode(i)
            if i_decoded.isspace() and j.startswith("B-"):
                j = "O"
            if i_decoded in ("", "<s>", "</s>"):
                continue
            if i_decoded == "<_>":
                i_decoded = " "
            _new_tag.append((i_decoded, j))
        return _new_tag

    def get_ner(  # noqa: CCR001  # phase2-todo
        self, text: str, pos: bool = False, tag: bool = False
    ) -> Union[list[tuple[str, str]], str]:
        """
        Tag named entities in text in IOB format.

        Powered by WangchanBERTa from the VISTEC-depa AI Research
        Institute of Thailand.

        :param str text: Thai text to be tagged
        :param bool pos: output part-of-speech tags. This model does not
            support them, so a warning is raised.
        :param bool tag: return HTML-like tags in a string instead of a
            list of tuples
        :return: list of tuples (word group, named entity tag), or a string
            with HTML-like tags if **tag** is True
        :rtype: Union[list[tuple[str, str]], str]
        """
        import torch

        if pos:
            warnings.warn(
                "This model does not support POS tag output.",
                UserWarning,
                stacklevel=2,
            )
        words_token = word_tokenize(text.replace(" ", "<_>"))
        inputs = self.tokenizer(
            words_token, is_split_into_words=True, return_tensors="pt"
        )
        ids = inputs["input_ids"]
        mask = inputs["attention_mask"]
        # forward pass
        outputs = self.model(ids, attention_mask=mask)
        logits = outputs[0]
        predictions = torch.argmax(logits, dim=2)
        predicted_token_class = [
            self.model.config.id2label[t.item()] for t in predictions[0]
        ]
        ner_tag = self._fix_span_error(
            inputs["input_ids"][0], predicted_token_class
        )
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


def segment(text: str) -> list[str]:
    """
    Tokenize text into subwords with the WangchanBERTa tokenizer.

    The tokenizer is a SentencePiece model.

    :param str text: text to be tokenized
    :return: list of subwords
    :rtype: list[str]
    """
    if not text or not isinstance(text, str):
        return []

    return cast("list[str]", _get_tokenizer().tokenize(text))
