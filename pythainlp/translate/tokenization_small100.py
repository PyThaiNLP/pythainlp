# SPDX-FileCopyrightText: 2022 Idiap Research Institute
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

# Copyright (c) 2022 Idiap Research Institute, https://www.idiap.ch/
# Written by Alireza Mohammadshahi <alireza.mohammadshahi@idiap.ch>
# This is a modified version of https://github.com/huggingface/transformers/blob/main/src/transformers/models/m2m_100/tokenization_m2m_100.py
# which owns by Fariseq Authors and The HuggingFace Inc. team.
#
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Tokenization classes for SMALL100."""

from __future__ import annotations

import json
import os
from pathlib import Path
from shutil import copyfile
from typing import TYPE_CHECKING, Any, Mapping, Optional, Union, cast

if TYPE_CHECKING:
    from sentencepiece import SentencePieceProcessor

from transformers.tokenization_utils import BatchEncoding, PreTrainedTokenizer

SPIECE_UNDERLINE: str = "▁"

VOCAB_FILES_NAMES: dict[str, str] = {
    "vocab_file": "vocab.json",
    "spm_file": "sentencepiece.bpe.model",
    "tokenizer_config_file": "tokenizer_config.json",
}

PRETRAINED_VOCAB_FILES_MAP: dict[str, dict[str, str]] = {
    "vocab_file": {
        "alirezamsh/small100": "https://huggingface.co/alirezamsh/small100/resolve/main/vocab.json",
    },
    "spm_file": {
        "alirezamsh/small100": "https://huggingface.co/alirezamsh/small100/resolve/main/sentencepiece.bpe.model",
    },
    "tokenizer_config_file": {
        "alirezamsh/small100": "https://huggingface.co/alirezamsh/small100/resolve/main/tokenizer_config.json",
    },
}

PRETRAINED_POSITIONAL_EMBEDDINGS_SIZES: dict[str, int] = {
    "alirezamsh/small100": 1024,
}

# fmt: off
FAIRSEQ_LANGUAGE_CODES: dict[str, list[str]] = {
    "m2m100": ["af", "am", "ar", "ast", "az", "ba", "be", "bg", "bn", "br", "bs", "ca", "ceb", "cs", "cy", "da", "de", "el", "en", "es", "et", "fa", "ff", "fi", "fr", "fy", "ga", "gd", "gl", "gu", "ha", "he", "hi", "hr", "ht", "hu", "hy", "id", "ig", "ilo", "is", "it", "ja", "jv", "ka", "kk", "km", "kn", "ko", "lb", "lg", "ln", "lo", "lt", "lv", "mg", "mk", "ml", "mn", "mr", "ms", "my", "ne", "nl", "no", "ns", "oc", "or", "pa", "pl", "ps", "pt", "ro", "ru", "sd", "si", "sk", "sl", "so", "sq", "sr", "ss", "su", "sv", "sw", "ta", "th", "tl", "tn", "tr", "uk", "ur", "uz", "vi", "wo", "xh", "yi", "yo", "zh", "zu"]
}
# fmt: on


class SMALL100Tokenizer(PreTrainedTokenizer):  # type: ignore[misc]
    """
    Tokenize text for the SMALL100 model.

    It is based on SentencePiece (https://github.com/google/sentencepiece).
    This tokenizer inherits from ``PreTrainedTokenizer``, which contains
    most of the main methods. See that superclass for more information
    about those methods.

    :param str vocab_file: path to the vocabulary file
    :param str spm_file: path to the SentencePiece file (generally has a
        .spm extension) that contains the vocabulary
    :param Optional[str] tgt_lang: target language
    :param str eos_token: end of sequence token (default is ``"</s>"``)
    :param str sep_token: separator token (default is ``"</s>"``). It is
        used when building a sequence from multiple sequences, for example
        two sequences for sequence classification, or a text and a question
        for question answering. It is also used as the last token of a
        sequence built with special tokens.
    :param str unk_token: unknown token (default is ``"<unk>"``). A token
        that is not in the vocabulary cannot be converted to an ID. It is
        set to this token instead.
    :param str pad_token: token used for padding (default is ``"<pad>"``),
        for example when batching sequences of different lengths
    :param Optional[str] language_codes: language codes to use. It must be
        ``"m2m100"``.
    :param Optional[dict] sp_model_kwargs: keyword arguments passed to
        ``SentencePieceProcessor.__init__()``. The Python wrapper for
        SentencePiece
        (https://github.com/google/sentencepiece/tree/master/python)
        can be used, among other things, to set:

        * *enable_sampling* - enable subword regularization
        * *nbest_size* - sampling parameter for unigram. Invalid for
          BPE-Dropout.

          * ``nbest_size = {0,1}`` - no sampling is performed
          * ``nbest_size > 1`` - sample from the nbest_size results
          * ``nbest_size < 0`` - assume that nbest_size is infinite and
            sample from all hypotheses (lattice) using the
            forward-filtering-and-backward-sampling algorithm

        * *alpha* - smoothing parameter for unigram sampling, and dropout
          probability of merge operations for BPE-dropout

    Examples:
    ```python
    >>> from tokenization_small100 import SMALL100Tokenizer
    >>> tokenizer = SMALL100Tokenizer.from_pretrained("alirezamsh/small100", tgt_lang="ro")
    >>> src_text = " UN Chief Says There Is No Military Solution in Syria"
    >>> tgt_text = "Şeful ONU declară că nu există o soluţie militară în Siria"
    >>> model_inputs = tokenizer(src_text, text_target=tgt_text, return_tensors="pt")
    >>> model(**model_inputs)  # should work
    ```

    """

    vocab_files_names: dict[str, str] = VOCAB_FILES_NAMES
    max_model_input_sizes: dict[str, int] = (
        PRETRAINED_POSITIONAL_EMBEDDINGS_SIZES
    )
    pretrained_vocab_files_map: dict[str, dict[str, str]] = (
        PRETRAINED_VOCAB_FILES_MAP
    )
    model_input_names: list[str] = ["input_ids", "attention_mask"]

    prefix_tokens: Optional[list[int]] = []
    suffix_tokens: list[int] = []

    sp_model_kwargs: dict[str, str]
    language_codes: str
    lang_code_to_token: dict[str, str]
    vocab_file: str
    encoder: dict[str, int]
    decoder: dict[int, str]
    spm_file: str
    sp_model: SentencePieceProcessor
    encoder_size: int
    lang_token_to_id: dict[str, int]
    lang_code_to_id: dict[str, int]
    id_to_lang_token: dict[int, str]
    _tgt_lang: str
    cur_lang_id: int
    num_madeup_words: int

    def __init__(
        self,
        vocab_file: str,
        spm_file: str,
        tgt_lang: Optional[str] = None,
        bos_token: str = "<s>",  # noqa: S107  # nosec B107
        eos_token: str = "</s>",  # noqa: S107  # nosec B107
        sep_token: str = "</s>",  # noqa: S107  # nosec B107
        pad_token: str = "<pad>",  # noqa: S107  # nosec B107
        unk_token: str = "<unk>",  # noqa: S107  # nosec B107
        language_codes: str = "m2m100",
        sp_model_kwargs: Optional[dict[str, str]] = None,
        num_madeup_words: int = 8,
        **kwargs: Any,
    ) -> None:
        """
        Initialize the tokenizer.

        :param str vocab_file: path to the vocabulary file
        :param str spm_file: path to the SentencePiece model file
        :param Optional[str] tgt_lang: target language code
        :param str language_codes: language code set (m2m100)
        :param Optional[dict[str, str]] sp_model_kwargs: keyword arguments for
            the SentencePiece processor
        :param int num_madeup_words: number of made-up words
        """
        self.sp_model_kwargs: dict[str, str] = (
            {} if sp_model_kwargs is None else sp_model_kwargs
        )

        self.language_codes: str = language_codes
        fairseq_language_code = FAIRSEQ_LANGUAGE_CODES[language_codes]
        self.lang_code_to_token: dict[str, str] = {
            lang_code: f"__{lang_code}__"
            for lang_code in fairseq_language_code
        }

        kwargs["additional_special_tokens"] = kwargs.get(
            "additional_special_tokens", []
        )
        kwargs["additional_special_tokens"] += [
            self.get_lang_token(lang_code)
            for lang_code in fairseq_language_code
            if self.get_lang_token(lang_code)
            not in kwargs["additional_special_tokens"]
        ]

        super().__init__(
            tgt_lang=tgt_lang,
            bos_token=bos_token,
            eos_token=eos_token,
            sep_token=sep_token,
            unk_token=unk_token,
            pad_token=pad_token,
            language_codes=language_codes,
            sp_model_kwargs=self.sp_model_kwargs,
            num_madeup_words=num_madeup_words,
            **kwargs,
        )

        self.vocab_file: str = vocab_file
        encoder_data = load_json(vocab_file)
        if not isinstance(encoder_data, dict):
            raise ValueError("encoder must be a dict")
        self.encoder: dict[str, int] = cast("dict[str, int]", encoder_data)
        self.decoder: dict[int, str] = {v: k for k, v in self.encoder.items()}
        self.spm_file: str = spm_file
        self.sp_model: SentencePieceProcessor = load_spm(
            spm_file, self.sp_model_kwargs
        )  # SentencePieceProcessor

        self.encoder_size: int = len(self.encoder)

        self.lang_token_to_id: dict[str, int] = {
            self.get_lang_token(lang_code): self.encoder_size + i
            for i, lang_code in enumerate(fairseq_language_code)
        }
        self.lang_code_to_id: dict[str, int] = {
            lang_code: self.encoder_size + i
            for i, lang_code in enumerate(fairseq_language_code)
        }
        self.id_to_lang_token: dict[int, str] = {
            v: k for k, v in self.lang_token_to_id.items()
        }

        self._tgt_lang: str = tgt_lang if tgt_lang is not None else "en"
        self.cur_lang_id: int = self.get_lang_id(self._tgt_lang)
        self.set_lang_special_tokens(self._tgt_lang)

        self.num_madeup_words: int = num_madeup_words

    @property
    def vocab_size(self) -> int:
        """Return the vocabulary size."""
        # Type ignore for external library dict operations
        return (
            len(self.encoder)
            + len(self.lang_token_to_id)
            + self.num_madeup_words
        )

    @property
    def tgt_lang(self) -> str:
        """Return the target language code."""
        return self._tgt_lang

    @tgt_lang.setter
    def tgt_lang(self, new_tgt_lang: str) -> None:
        self._tgt_lang: str = new_tgt_lang
        self.set_lang_special_tokens(self._tgt_lang)

    def _tokenize(self, text: str) -> list[str]:
        return cast("list[str]", self.sp_model.encode(text, out_type=str))

    def _convert_token_to_id(self, token: str) -> int:
        if token in self.lang_token_to_id:
            return self.lang_token_to_id[token]
        return self.encoder.get(token, self.encoder[self.unk_token])

    def _convert_id_to_token(self, index: int) -> str:
        """Convert an index (integer) to a token (str) using the decoder."""
        if index in self.id_to_lang_token:
            return self.id_to_lang_token[index]
        token = self.decoder.get(index, self.unk_token)
        if token is None:
            return cast("str", self.unk_token)
        return token

    def convert_tokens_to_string(self, tokens: list[str]) -> str:
        """Convert a sequence of tokens (sub-word strings) to a string."""
        return cast("str", self.sp_model.decode(tokens))

    def get_special_tokens_mask(
        self,
        token_ids_0: list[int],
        token_ids_1: Optional[list[int]] = None,
        already_has_special_tokens: bool = False,
    ) -> list[int]:
        """
        Retrieve sequence IDs from a token list that has no special tokens.

        This method is called when adding special tokens using the
        tokenizer ``prepare_for_model`` method.

        :param list[int] token_ids_0: list of IDs
        :param Optional[list[int]] token_ids_1: second list of IDs for
            sequence pairs
        :param bool already_has_special_tokens: whether the token list is
            already formatted with special tokens for the model
        :return: list of integers in the range [0, 1], 1 for a special
            token and 0 for a sequence token
        :rtype: list[int]
        """
        if already_has_special_tokens:
            # External library method
            return cast(
                "list[int]",
                super().get_special_tokens_mask(
                    token_ids_0=token_ids_0,
                    token_ids_1=token_ids_1,
                    already_has_special_tokens=True,
                ),
            )

        prefix_ones = (
            [1] * len(self.prefix_tokens) if self.prefix_tokens else []
        )
        suffix_ones = [1] * len(self.suffix_tokens)
        if token_ids_1 is None:
            return prefix_ones + ([0] * len(token_ids_0)) + suffix_ones
        return (
            prefix_ones
            + ([0] * len(token_ids_0))
            + ([0] * len(token_ids_1))
            + suffix_ones
        )

    def build_inputs_with_special_tokens(
        self, token_ids_0: list[int], token_ids_1: Optional[list[int]] = None
    ) -> list[int]:
        """
        Build model inputs by adding special tokens to one or two sequences.

        This is for sequence classification tasks. An MBART sequence has
        the following format, where ``X`` represents the sequence:

        * ``input_ids`` (for encoder): ``X [eos, src_lang_code]``
        * ``decoder_input_ids`` (for decoder): ``X [eos, tgt_lang_code]``

        BOS is never used. Pairs of sequences are not the expected use case,
        but they will be handled without a separator.

        :param list[int] token_ids_0: list of IDs to add special tokens to
        :param Optional[list[int]] token_ids_1: second list of IDs for
            sequence pairs
        :return: list of input IDs with the appropriate special tokens
        :rtype: list[int]
        """
        if token_ids_1 is None:
            if self.prefix_tokens is None:
                return token_ids_0 + self.suffix_tokens
            return self.prefix_tokens + token_ids_0 + self.suffix_tokens
        # We don't expect to process pairs,
        # but leave the pair logic for API consistency
        if self.prefix_tokens is None:
            return token_ids_0 + token_ids_1 + self.suffix_tokens
        return (
            self.prefix_tokens + token_ids_0 + token_ids_1 + self.suffix_tokens
        )

    def get_vocab(self) -> dict[str, int]:
        """Return the vocabulary as a token-to-id mapping."""
        vocab = {
            self.convert_ids_to_tokens(i): i for i in range(self.vocab_size)
        }
        vocab.update(self.added_tokens_encoder)
        return vocab

    def __getstate__(self) -> dict[str, Any]:
        """Return the state for pickling, without the SentencePiece model."""
        state = self.__dict__.copy()
        state["sp_model"] = None
        return state

    def __setstate__(self, d: dict[str, Any]) -> None:
        """Restore the state and reload the SentencePiece model."""
        self.__dict__: dict[str, Any] = d

        # for backward compatibility
        if not hasattr(self, "sp_model_kwargs"):
            self.sp_model_kwargs: dict[str, str] = {}

        self.sp_model: SentencePieceProcessor = load_spm(
            self.spm_file, self.sp_model_kwargs
        )

    def save_vocabulary(
        self, save_directory: str, filename_prefix: Optional[str] = None
    ) -> tuple[str, str]:
        """
        Save the vocabulary and the SentencePiece model files.

        :param str save_directory: directory to save the files to
        :param Optional[str] filename_prefix: prefix of the file names
        :return: paths of the vocabulary file and the SentencePiece model file
        :rtype: tuple[str, str]
        :raises OSError: if save_directory is not a directory
        """
        save_dir = Path(save_directory)
        if not save_dir.is_dir():
            raise OSError(f"{save_directory} should be a directory")
        vocab_save_path = save_dir / (
            (filename_prefix + "-" if filename_prefix else "")
            + self.vocab_files_names["vocab_file"]
        )
        spm_save_path = save_dir / (
            (filename_prefix + "-" if filename_prefix else "")
            + self.vocab_files_names["spm_file"]
        )

        save_json(self.encoder, str(vocab_save_path))

        if os.path.abspath(self.spm_file) != os.path.abspath(
            spm_save_path
        ) and os.path.isfile(self.spm_file):
            copyfile(self.spm_file, spm_save_path)
        elif not os.path.isfile(self.spm_file):
            with open(spm_save_path, "wb") as fi:
                content_spiece_model = self.sp_model.serialized_model_proto()
                fi.write(content_spiece_model)

        return (str(vocab_save_path), str(spm_save_path))

    def prepare_seq2seq_batch(
        self,
        src_texts: list[str],
        tgt_texts: Optional[list[str]] = None,
        tgt_lang: str = "ro",
        **kwargs: Any,
    ) -> BatchEncoding:
        """
        Prepare a batch of source and target texts for a seq2seq model.

        :param list[str] src_texts: list of source texts
        :param Optional[list[str]] tgt_texts: list of target texts
        :param str tgt_lang: target language code
        :return: encoded batch
        :rtype: transformers.BatchEncoding
        """
        self.tgt_lang: str = tgt_lang
        self.set_lang_special_tokens(self.tgt_lang)
        return super().prepare_seq2seq_batch(src_texts, tgt_texts, **kwargs)

    def _build_translation_inputs(
        self,
        raw_inputs: Union[str, list[str]],
        tgt_lang: Optional[str],
        **extra_kwargs: str,
    ) -> dict[str, Any]:
        """
        Prepare inputs for the generate function.

        The translation pipeline uses this method.
        """
        if tgt_lang is None:
            raise ValueError(
                "Translation requires a `tgt_lang` for this model"
            )
        self.tgt_lang: str = tgt_lang
        inputs = self(raw_inputs, add_special_tokens=True, **extra_kwargs)
        return cast("dict[str, Any]", inputs)

    def _switch_to_input_mode(self) -> None:
        self.set_lang_special_tokens(self.tgt_lang)

    def _switch_to_target_mode(self) -> None:
        self.prefix_tokens: Optional[list[int]] = None
        self.suffix_tokens: list[int] = [self.eos_token_id]

    def set_lang_special_tokens(self, src_lang: str) -> None:
        """
        Reset the special tokens to the target language setting.

        There is no prefix, and the suffix is ``[eos, tgt_lang_code]``.
        """
        lang_token = self.get_lang_token(src_lang)
        self.cur_lang_id: int = self.lang_token_to_id[lang_token]
        self.prefix_tokens: list[int] = [self.cur_lang_id]
        self.suffix_tokens: list[int] = [self.eos_token_id]

    def get_lang_token(self, lang: str) -> str:
        """
        Return the special token of a language.

        :param str lang: language code
        :return: language token
        :rtype: str
        """
        return self.lang_code_to_token[lang]

    def get_lang_id(self, lang: str) -> int:
        """
        Return the token id of a language.

        :param str lang: language code
        :return: language token id
        :rtype: int
        """
        lang_token = self.get_lang_token(lang)
        return self.lang_token_to_id[lang_token]


def load_spm(
    path: str, sp_model_kwargs: dict[str, str]
) -> SentencePieceProcessor:
    """
    Load a SentencePiece model from a file.

    :param str path: path to the model file
    :param dict[str, str] sp_model_kwargs: keyword arguments for the
        SentencePiece processor
    :return: SentencePiece processor
    :rtype: sentencepiece.SentencePieceProcessor
    """
    import sentencepiece

    spm = sentencepiece.SentencePieceProcessor(**sp_model_kwargs)
    spm.Load(str(path))
    return spm


def load_json(path: str) -> Union[dict[str, str], list[str]]:
    """
    Load JSON data from a file.

    :param str path: path to the JSON file
    :return: loaded data
    :rtype: Union[dict[str, str], list[str]]
    """
    with open(path) as f:
        return cast("Union[dict[str, str], list[str]]", json.load(f))


def save_json(
    data: Union[Mapping[str, Union[str, int]], list[str]], path: str
) -> None:
    """
    Save data to a JSON file.

    :param data: data to save
    :type data: Union[Mapping[str, Union[str, int]], list[str]]
    :param str path: path to the JSON file
    """
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
