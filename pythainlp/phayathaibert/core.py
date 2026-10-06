# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

import random
import re
import warnings
from typing import TYPE_CHECKING, Optional, Union, cast

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
    _model_name  # nosec B615
)


class ThaiTextProcessor:
    def __init__(self) -> None:
        (
            self._TK_UNK,
            self._TK_REP,
            self._TK_WREP,
            self._TK_URL,
            self._TK_END,
        ) = ["<unk>", "<rep>", "<wrep>", "<url>", "</s>"]
        self.SPACE_SPECIAL_TOKEN: str = "<_>"  # noqa: S105

    def replace_url(self, text: str) -> str:
        """
        Replace URLs in text with the URL token.

        See https://stackoverflow.com/a/6041965

        :param str text: text to be processed
        :return: text with URLs replaced
        :rtype: str

        :Example:

            >>> replace_url("go to https://github.com")
            'go to <url>'
        """
        return re.sub(_PAT_URL, self._TK_URL, text)

    def rm_brackets(self, text: str) -> str:
        """
        Remove empty brackets and artifacts within brackets from text.

        :param str text: text to be processed
        :return: text with useless brackets removed
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
        """
        Replace newlines in text with spaces.

        :param str text: text to be processed
        :return: text with newlines replaced with spaces
        :rtype: str

        :Example:

            >>> rm_useless_spaces("hey whats\n\nup")
            hey whats  up
        """
        return re.sub(r"[\n]", " ", text.strip())

    def rm_useless_spaces(self, text: str) -> str:
        """
        Collapse repeated spaces in text (code from `fastai`).

        :param str text: text to be processed
        :return: text with repeated spaces reduced to one
        :rtype: str

        :Example:

            >>> rm_useless_spaces("oh         no")
            oh no
        """
        return re.sub(" {2,}", " ", text)

    def replace_spaces(self, text: str, space_token: str = "<_>") -> str:  # noqa: S107  # nosec B107
        """
        Replace spaces in text with a space token.

        :param str text: text to be processed
        :param str space_token: token to replace spaces with
        :return: text with spaces replaced with the space token
        :rtype: str

        :Example:

            >>> replace_spaces("oh no")
            oh_no
        """
        return re.sub(" ", space_token, text)

    def replace_rep_after(self, text: str) -> str:
        """
        Remove character repetitions in text.

        :param str text: text to be processed
        :return: text with repeated characters removed
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
        """
        Remove repeated words after tokenization.

        The `replace_wrep` function of `fastai` does not work well
        with Thai.

        :param list[str] toks: list of words
        :return: list of words with repeated words removed
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
        """
        Remove spaces from a list of words, for bag-of-words models.

        :param list[str] toks: list of words
        :return: list of words with space tokens (" ") filtered out
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
        pre_rules: Optional[list[Callable[..., str]]] = None,
        tok_func: Callable[..., list[str]] = word_tokenize,
    ) -> str:
        """
        Preprocess text: apply the rules, then tokenize and join.

        :param str text: text to be preprocessed
        :param Optional[list[Callable[..., str]]] pre_rules: rules to
            apply in order after lowercasing. If None, use the text
            cleaning methods of this class.
        :param Callable[..., list[str]] tok_func: function to tokenize
            text
        :return: preprocessed text
        :rtype: str
        """
        if pre_rules is None:
            pre_rules = [
                self.rm_brackets,
                self.replace_newlines,
                self.rm_useless_spaces,
                self.replace_spaces,
                self.replace_rep_after,
            ]
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
            AutoTokenizer.from_pretrained(_model_name)  # nosec B615
        )
        self.model_for_masked_lm: "AutoModelForMaskedLM" = (
            AutoModelForMaskedLM.from_pretrained(_model_name)  # nosec B615
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
        """
        Generate text from PhayaThaiBERT.

        :param str sample_text: text to continue from
        :param int word_rank: rank of the predicted word to select
        :param int max_length: number of words to generate
        :param bool sample: whether to select a random word among the
            top five predictions
        :return: generated text
        :rtype: str
        """
        sample_txt = sample_text
        final_text = ""
        for _ in range(max_length):
            input_text = self.processor.preprocess(sample_txt)
            if sample:
                # Non-cryptographic use, pseudo-random generator is acceptable here
                random_word_idx = random.randint(0, 4)  # noqa: S311  # nosec B311  # NOSONAR
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
        """
        Augment text with PhayaThaiBERT.

        :param str text: Thai text to be augmented
        :param int num_augs: number of augmented texts to return
        :param bool sample: whether to sample words randomly, for more
            word diversity
        :return: list of augmented texts
        :rtype: list[str]
        :raises ValueError: if **num_augs** exceeds the limit of five

        :Example:

            >>> from pythainlp.augment.lm import (
            ...     ThaiTextAugmenter,
            ... )  # doctest: +SKIP

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
    def __init__(
        self,
        model: str = "lunarlist/pos_thai_phayathai",
        revision: Optional[str] = None,
    ) -> None:
        # Load model directly
        from transformers import (
            AutoModelForTokenClassification,
            AutoTokenizer,
        )

        self.tokenizer: "PreTrainedTokenizerBase" = (
            AutoTokenizer.from_pretrained(model, revision=revision)
        )
        self.model: "AutoModelForTokenClassification" = (
            AutoModelForTokenClassification.from_pretrained(
                model, revision=revision
            )
        )

    def get_tag(
        self, sentence: str, strategy: str = "simple"
    ) -> list[list[tuple[str, str]]]:
        """
        Tag text with part-of-speech (POS) tags.

        :param str sentence: text to be tagged
        :param str strategy: aggregation strategy of the token
            classification pipeline
        :return: list of lists of tuples (word, POS tag)
        :rtype: list[list[tuple[str, str]]]

        :Example:

        Label POS for the given text:

            >>> from pythainlp.phayathaibert.core import (
            ...     PartOfSpeechTagger,
            ... )  # doctest: +SKIP

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
    def __init__(
        self,
        model: str = "Pavarissy/phayathaibert-thainer",
        revision: Optional[str] = None,
    ) -> None:
        from transformers import (
            AutoModelForTokenClassification,
            AutoTokenizer,
        )

        self.tokenizer: "PreTrainedTokenizerBase" = (
            AutoTokenizer.from_pretrained(model, revision=revision)
        )
        self.model: "AutoModelForTokenClassification" = (
            AutoModelForTokenClassification.from_pretrained(
                model, revision=revision
            )
        )

    def get_ner(
        self,
        text: str,
        tag: bool = False,
        pos: bool = False,
        strategy: str = "simple",
    ) -> Union[list[tuple[str, str]], list[tuple[str, str, str]], str]:
        """
        Tag named entities in text.

        :param str text: Thai text to be tagged
        :param bool tag: return HTML-like tags in a string instead of a
            list of tuples
        :param bool pos: output part-of-speech tags. This model does not
            support them (use :class:`PartOfSpeechTagger` instead), so
            a warning is raised.
        :param str strategy: aggregation strategy of the token
            classification pipeline
        :return: list of tuples (word, named entity tag), or a string with
            HTML-like tags if **tag** is True
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
            'ทดสอบ<PERSON>นายปวริศ เรืองจุติโพธิ์พาน</PERSON><LOCATION>จาก</LOCATION><LOCATION>ประเทศไทย</LOCATION>'
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
    """
    Tokenize text into subwords with the PhayaThaiBERT tokenizer.

    The tokenizer is the sentencepiece model of WangchanBERTa, with
    vocabulary expansion.

    :param str sentence: text to be tokenized
    :return: list of subwords
    :rtype: list[str]
    """
    if not sentence or not isinstance(sentence, str):
        return []

    return cast("list[str]", _tokenizer.tokenize(sentence))
