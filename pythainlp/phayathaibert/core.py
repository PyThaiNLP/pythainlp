# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

import random
import re
import warnings
from typing import TYPE_CHECKING, Union, cast

if TYPE_CHECKING:
    from collections.abc import Callable

    from transformers import (  # noqa: F401
        AutoModelForMaskedLM,
        AutoModelForTokenClassification,
        CamembertTokenizer,
        Pipeline,
        PreTrainedTokenizerBase,
    )

from transformers import (
    CamembertTokenizer,
)

from pythainlp.tokenize import word_tokenize

_PAT_URL: str = r"(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?"

_model_name: str = "clicknext/phayathaibert"
_tokenizer: "CamembertTokenizer" = CamembertTokenizer.from_pretrained(
    _model_name
)


class ThaiTextProcessor:
    def __init__(self) -> None:
        (
            self._TK_UNK,
            self._TK_REP,
            self._TK_WREP,
            self._TK_URL,
            self._TK_END,
        ) = "<unk> <rep> <wrep> <url> </s>".split()
        self.SPACE_SPECIAL_TOKEN: str = "<_>"  # noqa: S105

    def replace_url(self, text: str) -> str:
        """Replace url in `text` with TK_URL (https://stackoverflow.com/a/6041965)
        :param str text: text to replace url
        :return: text where urls are replaced
        :rtype: str
        :Example:

            >>> replace_url("go to https://github.com")
            'go to <url>'
        """
        return re.sub(_PAT_URL, self._TK_URL, text)

    def rm_brackets(self, text: str) -> str:
        """Remove all empty brackets and artifacts within brackets from `text`.
        :param str text: text to remove useless brackets
        :return: text where all useless brackets are removed
        :rtype: str
        :Example:

            >>> rm_brackets("hey() whats[;] up{*&} man(hey)")
            'hey whats up man(hey)'
        """
        # remove empty brackets
        new_line = re.sub(r"\(\)", "", text)
        new_line = re.sub(r"\{\}", "", new_line)
        new_line = re.sub(r"\[\]", "", new_line)
        # brackets with only punctuations
        new_line = re.sub(r"\([^a-zA-Z0-9ก-๙]+\)", "", new_line)
        new_line = re.sub(r"\{[^a-zA-Z0-9ก-๙]+\}", "", new_line)
        new_line = re.sub(r"\[[^a-zA-Z0-9ก-๙]+\]", "", new_line)
        # artifiacts after (
        new_line = re.sub(
            r"(?<=\()[^a-zA-Z0-9ก-๙]+(?=[a-zA-Z0-9ก-๙])", "", new_line
        )
        new_line = re.sub(
            r"(?<=\{)[^a-zA-Z0-9ก-๙]+(?=[a-zA-Z0-9ก-๙])", "", new_line
        )
        new_line = re.sub(
            r"(?<=\[)[^a-zA-Z0-9ก-๙]+(?=[a-zA-Z0-9ก-๙])", "", new_line
        )
        # artifacts before )
        new_line = re.sub(
            r"(?<=[a-zA-Z0-9ก-๙])[^a-zA-Z0-9ก-๙]+(?=\))", "", new_line
        )
        new_line = re.sub(
            r"(?<=[a-zA-Z0-9ก-๙])[^a-zA-Z0-9ก-๙]+(?=\})", "", new_line
        )
        new_line = re.sub(
            r"(?<=[a-zA-Z0-9ก-๙])[^a-zA-Z0-9ก-๙]+(?=\])", "", new_line
        )
        return new_line

    def replace_newlines(self, text: str) -> str:
        """Replace newlines in `text` with spaces.
        :param str text: text to replace all newlines with spaces
        :return: text where all newlines are replaced with spaces
        :rtype: str
        :Example:

            >>> rm_useless_spaces("hey whats\n\nup")
            hey whats  up
        """
        return re.sub(r"[\n]", " ", text.strip())

    def rm_useless_spaces(self, text: str) -> str:
        """Remove multiple spaces in `text`. (code from `fastai`)
        :param str text: text to replace useless spaces
        :return: text where all spaces are reduced to one
        :rtype: str
        :Example:

            >>> rm_useless_spaces("oh         no")
            oh no
        """
        return re.sub(" {2,}", " ", text)

    def replace_spaces(self, text: str, space_token: str = "<_>") -> str:  # noqa: S107
        """Replace spaces with _
        :param str text: text to replace spaces
        :return: text where all spaces replaced with _
        :rtype: str
        :Example:

            >>> replace_spaces("oh no")
            oh_no
        """
        return re.sub(" ", space_token, text)

    def replace_rep_after(self, text: str) -> str:
        """Replace repetitions at the character level in `text`
        :param str text: input text to replace character repetition
        :return: text with repetitive tokens removed.
        :rtype: str
        :Example:

            >>> text = "กาาาาาาา"
            >>> replace_rep_after(text)
            'กา'
        """

        def _replace_rep(m: re.Match[str]) -> str:
            c, cc = m.groups()
            return f"{c}"

        re_rep = re.compile(r"(\S)(\1{3,})")
        return re_rep.sub(_replace_rep, text)

    def replace_wrep_post(self, toks: list[str]) -> list[str]:
        """Replace repetitive words post tokenization;
        fastai `replace_wrep` does not work well with Thai.
        :param list[str] toks: list of tokens
        :return: list of tokens where repetitive words are removed.
        :rtype: list[str]
        :Example:

            >>> toks = ["กา", "น้ำ", "น้ำ", "น้ำ", "น้ำ"]
            >>> replace_wrep_post(toks)
            ['กา', 'น้ำ']
        """
        previous_word = ""
        rep_count = 0
        res = []
        for current_word in toks + [self._TK_END]:
            if current_word == previous_word:
                rep_count += 1
            elif (current_word != previous_word) & (rep_count > 0):
                res += [previous_word]
                rep_count = 0
            else:
                res.append(previous_word)
            previous_word = current_word

        return res[1:]

    def remove_space(self, toks: list[str]) -> list[str]:
        """Do not include space for bag-of-word models.
        :param list[str] toks: list of tokens
        :return: List of tokens where space tokens (" ") are filtered out
        :rtype: list[str]
        :Example:

            >>> toks = ["ฉัน", "เดิน", " ", "กลับ", "บ้าน"]
            >>> remove_space(toks)
            ['ฉัน', 'เดิน', 'กลับ', 'บ้าน']
        """
        res = []
        for t in toks:
            t = t.strip()
            if t:
                res.append(t)

        return res

    # combine them together
    def preprocess(
        self,
        text: str,
        pre_rules: list[Callable[..., str]] = [
            rm_brackets,
            replace_newlines,
            rm_useless_spaces,
            replace_spaces,
            replace_rep_after,
        ],
        tok_func: Callable[..., list[str]] = word_tokenize,
    ) -> str:
        text = text.lower()
        for rule in pre_rules:
            text = rule(text)
        toks = tok_func(text)

        return "".join(toks)


class ThaiTextAugmenter:
    def __init__(self) -> None:
        from transformers import (
            AutoModelForMaskedLM,
            AutoTokenizer,
            pipeline,
        )

        self.tokenizer: "PreTrainedTokenizerBase" = (
            AutoTokenizer.from_pretrained(_model_name)
        )
        self.model_for_masked_lm: "AutoModelForMaskedLM" = (
            AutoModelForMaskedLM.from_pretrained(_model_name)
        )
        self.model: "Pipeline" = pipeline(  # transformers.Pipeline
            "fill-mask",
            tokenizer=self.tokenizer,
            model=self.model_for_masked_lm,
        )
        self.processor: ThaiTextProcessor = ThaiTextProcessor()

    def generate(
        self,
        sample_text: str,
        word_rank: int,
        max_length: int = 3,
        sample: bool = False,
    ) -> str:
        """Generate text from PhayaThaiBERT"""
        sample_txt = sample_text
        final_text = ""
        for _ in range(max_length):
            input_text = self.processor.preprocess(sample_txt)
            if sample:
                # Non-cryptographic use, pseudo-random generator is acceptable here
                random_word_idx = random.randint(0, 4)  # noqa: S311
                output = self.model(input_text)[random_word_idx]["sequence"]
            else:
                output = self.model(input_text)[word_rank]["sequence"]
            sample_txt = output + "<mask>"
            final_text = sample_txt

        gen_txt = re.sub("<mask>", "", final_text)

        return gen_txt

    def augment(
        self,
        text: str,
        num_augs: int = 3,
        sample: bool = False,
    ) -> list[str]:
        """Text augmentation from PhayaThaiBERT

        :param str text: Thai text
        :param int num_augs: an amount of augmentation text needed as an output
        :param bool sample: whether to sample the text as an output or not,\
              true if more word diversity is needed

        :return: list of text augment
        :rtype: list[str]

        :Example:

            >>> from pythainlp.augment.lm import ThaiTextAugmenter  # doctest: +SKIP

            >>> aug = ThaiTextAugmenter()  # doctest: +SKIP
            >>> aug.augment("ช้างมีทั้งหมด 50 ตัว บน", num_args=5)  # doctest: +SKIP

            ['ช้างมีทั้งหมด 50 ตัว บนโลกใบนี้ครับ.',
                'ช้างมีทั้งหมด 50 ตัว บนพื้นดินครับ...',
                'ช้างมีทั้งหมด 50 ตัว บนท้องฟ้าครับ...',
                'ช้างมีทั้งหมด 50 ตัว บนดวงจันทร์.‼',
                'ช้างมีทั้งหมด 50 ตัว บนเขาค่ะ😁']
        """
        MAX_NUM_AUGS = 5
        augment_list = []

        if num_augs <= MAX_NUM_AUGS:
            for rank in range(num_augs):
                gen_text = self.generate(
                    text,
                    rank,
                    sample=sample,
                )
                processed_text = re.sub(
                    "<_>", " ", self.processor.preprocess(gen_text)
                )
                augment_list.append(processed_text)
        else:
            raise ValueError(
                f"augmentation of more than {num_augs} is exceeded \
                    the default limit: {MAX_NUM_AUGS}"
            )

        return augment_list


class PartOfSpeechTagger:
    def __init__(self, model: str = "lunarlist/pos_thai_phayathai") -> None:
        # Load model directly
        from transformers import (
            AutoModelForTokenClassification,
            AutoTokenizer,
        )

        self.tokenizer: "PreTrainedTokenizerBase" = (
            AutoTokenizer.from_pretrained(model)
        )
        self.model: "AutoModelForTokenClassification" = (
            AutoModelForTokenClassification.from_pretrained(model)
        )

    def get_tag(
        self, sentence: str, strategy: str = "simple"
    ) -> list[list[tuple[str, str]]]:
        """Marks sentences with part-of-speech (POS) tags.

        :param str sentence: a list of lists of tokenized words
        :return: a list of lists of tuples (word, POS tag)
        :rtype: list[list[tuple[str, str]]]

        :Example:

        Labels POS for given sentence:

            >>> from pythainlp.phayathaibert.core import PartOfSpeechTagger  # doctest: +SKIP

            >>> tagger = PartOfSpeechTagger()  # doctest: +SKIP
            >>> tagger.get_tag("แมวทำอะไรตอนห้าโมงเช้า")  # doctest: +SKIP
            [[('แมว', 'NOUN'), ('ทําอะไร', 'VERB'), ('ตอนห้าโมงเช้า', 'NOUN')]]
        """
        from transformers import TokenClassificationPipeline

        pipeline = TokenClassificationPipeline(
            model=self.model,
            tokenizer=self.tokenizer,
            aggregation_strategy=strategy,
        )
        outputs = pipeline(sentence)
        word_tags = [[(tag["word"], tag["entity_group"]) for tag in outputs]]

        return word_tags


class NamedEntityTagger:
    def __init__(self, model: str = "Pavarissy/phayathaibert-thainer") -> None:
        from transformers import (
            AutoModelForTokenClassification,
            AutoTokenizer,
        )

        self.tokenizer: "PreTrainedTokenizerBase" = (
            AutoTokenizer.from_pretrained(model)
        )
        self.model: "AutoModelForTokenClassification" = (
            AutoModelForTokenClassification.from_pretrained(model)
        )

    def get_ner(
        self,
        text: str,
        tag: bool = False,
        pos: bool = False,
        strategy: str = "simple",
    ) -> Union[list[tuple[str, str]], list[tuple[str, str, str]], str]:
        """This function tags named entities in text in IOB format.

        :param str text: text in Thai to be tagged
        :param bool pos: output with part-of-speech tags.\
            (PhayaThaiBERT is supported in PartOfSpeechTagger)
        :return: a list of tuples associated with tokenized words, NER tags,
                 POS tags (if the parameter `pos` is specified as `True`),
                 and output HTML-like tags (if the parameter `tag` is
                 specified as `True`).
                 Otherwise, return a list of tuples associated with tokenized
                 words and NER tags
        :rtype: Union[list[tuple[str, str]], list[tuple[str, str, str]], str]
        :Example:

            >>> from pythainlp.phayathaibert.core import NamedEntityTagger
            >>>
            >>> tagger = NamedEntityTagger()
            >>> tagger.get_ner("ทดสอบนายปวริศ เรืองจุติโพธิ์พานจากประเทศไทย")
            [('นายปวริศ เรืองจุติโพธิ์พานจากประเทศไทย', 'PERSON'),
            ('จาก', 'LOCATION'),
            ('ประเทศไทย', 'LOCATION')]
            >>> ner.tag("ทดสอบนายปวริศ เรืองจุติโพธิ์พานจากประเทศไทย", tag=True)
            'ทดสอบ<PERSON>นายปวริศ เรืองจุติโพธิ์พาน</PERSON>\
                <LOCATION>จาก</LOCATION><LOCATION>ประเทศไทย</LOCATION>'
        """
        from transformers import TokenClassificationPipeline

        if pos:
            warnings.warn(
                "This model does not support POS tag output.",
                UserWarning,
                stacklevel=2,
            )

        sample_output = []
        tag_text_list = []
        current_pos = 0
        pipeline = TokenClassificationPipeline(
            model=self.model,
            tokenizer=self.tokenizer,
            aggregation_strategy=strategy,
        )
        outputs = pipeline(text)

        for token in outputs:
            ner_tag = token["entity_group"]
            begin_pos, end_pos = token["start"], token["end"]
            if current_pos == 0:
                text_tag = (
                    text[:begin_pos]
                    + f"<{ner_tag}>"
                    + text[begin_pos:end_pos]
                    + f"</{ner_tag}>"
                )
            else:
                text_tag = (
                    text[current_pos:begin_pos]
                    + f"<{ner_tag}>"
                    + text[begin_pos:end_pos]
                    + f"</{ner_tag}>"
                )
            tag_text_list.append(text_tag)
            sample_output.append((token["word"], token["entity_group"]))
            current_pos = end_pos

        if tag:
            return str("".join(tag_text_list))

        return sample_output


def segment(sentence: str) -> list[str]:
    """Subword tokenize of PhayaThaiBERT, \
    sentencepiece from WangchanBERTa model with vocabulary expansion.

    :param str sentence: text to be tokenized
    :return: list of subwords
    :rtype: list[str]
    """
    if not sentence or not isinstance(sentence, str):
        return []

    return cast(list[str], _tokenizer.tokenize(sentence))
