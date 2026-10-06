# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""
Translate between English and Thai using VISTEC-depa models.

The models are from the VISTEC-depa Thailand Artificial Intelligence
Research Institute.

Website: https://airesearch.in.th/releases/machine-translation-models/
"""

from __future__ import annotations

import warnings
from typing import Optional

try:
    from fairseq.models.transformer import TransformerModel
except ImportError as e:
    raise ImportError(
        "fairseq is not installed. Install it with: pip install fairseq"
    ) from e

try:
    from sacremoses import MosesTokenizer
except ImportError as e:
    raise ImportError(
        "sacremoses is not installed. Install it with: pip install sacremoses"
    ) from e

from pythainlp.corpus import download, get_corpus_path
from pythainlp.tools.path import safe_path_join

_EN_TH_MODEL_NAME: str = "scb_1m_en-th_moses"
# SCB_1M-MT_OPUS+TBASE_en-th_moses-spm_130000-16000_v1.0.tar.gz
_EN_TH_FILE_NAME: str = (
    "SCB_1M-MT_OPUS+TBASE_en-th_moses-spm_130000-16000_v1.0"
)

_TH_EN_MODEL_NAME: str = "scb_1m_th-en_spm"
# SCB_1M-MT_OPUS+TBASE_th-en_spm-spm_32000-joined_v1.0.tar.gz
_TH_EN_FILE_NAME: str = "SCB_1M-MT_OPUS+TBASE_th-en_spm-spm_32000-joined_v1.0"


def _get_translate_path(model: str, *path: str) -> str:
    corpus_path = get_corpus_path(model, version="1.0")
    if not corpus_path:
        return ""
    return safe_path_join(corpus_path, *path)


def _download_install(name: str) -> None:
    if not get_corpus_path(name):
        download(name, force=True, version="1.0")


def download_model_all() -> None:
    """Download all translation models in advance."""
    _download_install(_EN_TH_MODEL_NAME)
    _download_install(_TH_EN_MODEL_NAME)


class EnThTranslator:
    """
    Translate English to Thai.

    The model is from the VISTEC-depa Thailand Artificial Intelligence
    Research Institute.

    Website: https://airesearch.in.th/releases/machine-translation-models/

    :param bool use_gpu: load the model on a GPU (default: False)
    """

    def __init__(self, use_gpu: bool = False) -> None:
        """
        Initialize the English-to-Thai translator.

        :param bool use_gpu: load the model on a GPU
        """
        self._tokenizer: MosesTokenizer = MosesTokenizer("en")

        self._model_name: str = _EN_TH_MODEL_NAME

        _download_install(self._model_name)
        self._model: TransformerModel = TransformerModel.from_pretrained(
            model_name_or_path=_get_translate_path(
                self._model_name,
                _EN_TH_FILE_NAME,
                "models",
            ),
            checkpoint_file="checkpoint.pt",
            data_name_or_path=_get_translate_path(
                self._model_name,
                _EN_TH_FILE_NAME,
                "vocab",
            ),
        )
        if use_gpu:
            self._model = self._model.cuda()

    def translate(
        self, text: str, exclude_words: Optional[list[str]] = None
    ) -> str:
        """
        Translate text from English to Thai.

        :param str text: text to translate
        :param Optional[list[str]] exclude_words: words to exclude from
            translation
        :return: translated text
        :rtype: str

        :Example:

        Translate text from English to Thai:

            >>> from pythainlp.translate import (
            ...     EnThTranslator,
            ... )  # doctest: +SKIP

            >>> enth = EnThTranslator()  # doctest: +SKIP

            >>> enth.translate("I love cat.")  # doctest: +SKIP
            ฉันรักแมว

        Translate text from English to Thai with excluded words:

            >>> enth.translate(
            ...     "I love cat.", exclude_words=["cat"]
            ... )  # doctest: +SKIP
            ฉันรัก cat

        """
        from pythainlp.translate.core import (
            _prepare_text_with_exclusions,
            _restore_excluded_words,
        )

        prepared_text, placeholder_map = _prepare_text_with_exclusions(
            text, exclude_words
        )
        tokens = " ".join(self._tokenizer.tokenize(prepared_text))
        translated = self._model.translate(tokens)
        result = translated.replace(" ", "").replace("▁", " ").strip()
        return _restore_excluded_words(result, placeholder_map)


class ThEnTranslator:
    """
    Translate Thai to English.

    The model is from the VISTEC-depa Thailand Artificial Intelligence
    Research Institute.

    Website: https://airesearch.in.th/releases/machine-translation-models/

    :param bool use_gpu: load the model on a GPU (default: False)
    """

    def __init__(self, use_gpu: bool = False) -> None:
        """
        Initialize the Thai-to-English translator.

        :param bool use_gpu: load the model on a GPU
        """
        self._model_name: str = _TH_EN_MODEL_NAME

        _download_install(self._model_name)
        # Suppress model type mismatch warning from transformers
        # The pre-trained model has camembert config but works fine
        with warnings.catch_warnings():
            warnings.filterwarnings(
                "ignore",
                message="(?i).*using a model of type .* to instantiate a model of type.*",
            )
            self._model: TransformerModel = TransformerModel.from_pretrained(
                model_name_or_path=_get_translate_path(
                    self._model_name,
                    _TH_EN_FILE_NAME,
                    "models",
                ),
                checkpoint_file="checkpoint.pt",
                data_name_or_path=_get_translate_path(
                    self._model_name,
                    _TH_EN_FILE_NAME,
                    "vocab",
                ),
                bpe="sentencepiece",
                sentencepiece_model=_get_translate_path(
                    self._model_name,
                    _TH_EN_FILE_NAME,
                    "bpe",
                    "spm.th.model",
                ),
            )
        if use_gpu:
            self._model = self._model.cuda()

    def translate(
        self, text: str, exclude_words: Optional[list[str]] = None
    ) -> str:
        """
        Translate text from Thai to English.

        :param str text: text to translate
        :param Optional[list[str]] exclude_words: words to exclude from
            translation
        :return: translated text
        :rtype: str

        :Example:

        Translate text from Thai to English:

            >>> from pythainlp.translate import (
            ...     ThEnTranslator,
            ... )  # doctest: +SKIP

            >>> then = ThEnTranslator()  # doctest: +SKIP

            >>> then.translate("ฉันรักแมว")  # doctest: +SKIP
            I love cat.

        Translate text from Thai to English with excluded words:

            >>> then.translate(
            ...     "ฉันรักแมว", exclude_words=["แมว"]
            ... )  # doctest: +SKIP
            I love แมว.

        """
        from pythainlp.translate.core import (
            _prepare_text_with_exclusions,
            _restore_excluded_words,
        )

        prepared_text, placeholder_map = _prepare_text_with_exclusions(
            text, exclude_words
        )
        translated = self._model.translate(prepared_text)
        return _restore_excluded_words(translated, placeholder_map)
