# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Recognize named entities and tokenize subwords with WangchanBERTa."""

from __future__ import annotations

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
    """Get the tokenizer, initializing it if necessary."""
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


def _format_ner_tags(entities: list[tuple[str, str]]) -> str:
    """Wrap named entities in HTML-like tags."""
    tagged_text = []
    active_entity = ""
    for word, ner in entities:
        if ner.startswith("B-"):
            if active_entity:
                tagged_text.append(f"</{active_entity}>")
            active_entity = ner[2:]
            tagged_text.append(f"<{active_entity}>")
        elif ner == "O" and active_entity:
            tagged_text.append(f"</{active_entity}>")
            active_entity = ""
        tagged_text.append(word)
    if active_entity:
        tagged_text.append(f"</{active_entity}>")
    return "".join(tagged_text)


class ThaiNameTagger:
    """Tag named entities with the WangchanBERTa pipeline."""

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

        Use WangchanBERTa from the VISTEC-depa AI Research Institute
        of Thailand.

        :param str dataset_name: dataset the model is fine-tuned on
            * *thainer* - ThaiNER dataset (default)
        :param bool grouped_entities: whether to group word pieces of the
            same entity
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

    def _prepare_ner(
        self, entities: list[dict[str, str]]
    ) -> list[tuple[str, str]]:
        if self.grouped_entities and self.dataset_name == "thainer":
            return [
                (
                    item["word"].replace("<_>", " ").replace("▁", ""),
                    self._IOB(item["entity_group"]),
                )
                for item in entities
            ]
        if self.dataset_name == "thainer":
            return [
                (
                    item["word"].replace("<_>", " ").replace("▁", ""),
                    item["entity"],
                )
                for item in entities
                if item["word"] != "▁"
            ]
        return [
            (
                item["word"].replace("<_>", " ").replace("▁", ""),
                item["entity"].replace("_", "-").replace("E-", "I-"),
            )
            for item in entities
        ]

    def _fix_consecutive_begin_tags(self) -> None:
        for idx in range(1, len(self.sent_ner)):
            word, ner = self.sent_ner[idx]
            previous_ner = self.sent_ner[idx - 1][1]
            if ner.startswith("B-") and self._clear_tag(
                ner
            ) == self._clear_tag(previous_ner):
                self.sent_ner[idx] = (word, ner.replace("B-", "I-"))

    def get_ner(
        self, text: str, pos: bool = False, tag: bool = False
    ) -> Union[list[tuple[str, str]], str]:
        """
        Tag named entities in Thai text.

        Use WangchanBERTa from the VISTEC-depa AI Research Institute
        of Thailand.

        :param str text: Thai text to be tagged
        :param bool pos: whether to request part-of-speech output; the
            model does not support it, so a warning is raised
        :param bool tag: whether to return HTML-like tags instead of tuples
        :return: tagged words, or an HTML-like tagged string if *tag* is True
        :rtype: Union[list[tuple[str, str]], str]
        """
        if pos:
            warnings.warn(
                "This model does not support POS tag output.",
                UserWarning,
                stacklevel=2,
            )
        text = text.replace(" ", "<_>")
        self.json_ner: list[dict[str, str]] = self.classify_tokens(text)
        self.output: str = ""
        self.sent_ner = self._prepare_ner(self.json_ner)
        if (
            self.sent_ner
            and self.sent_ner[0][0] == ""
            and len(self.sent_ner) > 1
        ):
            self.sent_ner = self.sent_ner[1:]
        self._fix_consecutive_begin_tags()
        if tag:
            return _format_ner_tags(self.sent_ner)
        return self.sent_ner


class NamedEntityRecognition:
    """Recognize Thai named entities with a WangchanBERTa model."""

    tokenizer: PreTrainedTokenizerBase
    model: PreTrainedModel

    def __init__(
        self,
        model: str = "pythainlp/thainer-corpus-v2-base-model",
        revision: Optional[str] = None,
    ) -> None:
        """
        Initialize a named entity recognizer.

        Use a model pretrained with WangchanBERTa.

        :param str model: pretrained model name
        :param Optional[str] revision: git revision ID (branch, tag, or
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
            tag = "O" if i_decoded.isspace() and j.startswith("B-") else j
            if i_decoded in ("", "<s>", "</s>"):
                continue
            if i_decoded == "<_>":
                i_decoded = " "
            _new_tag.append((i_decoded, tag))
        return _new_tag

    def get_ner(
        self, text: str, pos: bool = False, tag: bool = False
    ) -> Union[list[tuple[str, str]], str]:
        """
        Tag named entities in Thai text.

        :param str text: Thai text to be tagged
        :param bool pos: whether to request part-of-speech output; the
            model does not support it, so a warning is raised
        :param bool tag: whether to return HTML-like tags instead of tuples
        :return: tagged words, or an HTML-like tagged string if *tag* is True
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
            return _format_ner_tags(ner_tag)
        return ner_tag


def segment(text: str) -> list[str]:
    """
    Tokenize text into subwords with the WangchanBERTa tokenizer.

    :param str text: text to be tokenized
    :return: list of subwords
    :rtype: list[str]
    """
    if not text or not isinstance(text, str):
        return []

    return cast("list[str]", _get_tokenizer().tokenize(text))
