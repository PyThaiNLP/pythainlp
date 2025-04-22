# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2025 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""
English-Thai Machine Translation

from VISTEC-depa Thailand Artificial Intelligence Research Institute

Website: https://airesearch.in.th/releases/machine-translation-models/
"""
import os

try:
    from fairseq.models.transformer import TransformerModel
except ImportError:
    raise ImportError("Not found fairseq! Please install fairseq by pip install fairseq")

try:
    from sacremoses import MosesTokenizer
except ImportError:
    raise ImportError("Not found sacremoses! Please install sacremoses by pip install sacremoses")

from pythainlp.corpus import download, get_corpus_path

_EN_TH_MODEL_NAME = "scb_1m_en-th_moses"
# SCB_1M-MT_OPUS+TBASE_en-th_moses-spm_130000-16000_v1.0.tar.gz
_EN_TH_FILE_NAME = "SCB_1M-MT_OPUS+TBASE_en-th_moses-spm_130000-16000_v1.0"

_TH_EN_MODEL_NAME = "scb_1m_th-en_spm"
# SCB_1M-MT_OPUS+TBASE_th-en_spm-spm_32000-joined_v1.0.tar.gz
_TH_EN_FILE_NAME = "SCB_1M-MT_OPUS+TBASE_th-en_spm-spm_32000-joined_v1.0"


def _get_translate_path(model: str, *path: str) -> str:
    return os.path.join(get_corpus_path(model, version="1.0"), *path)


def _download_install(name: str) -> None:
    if get_corpus_path(name) is None:
        download(name, force=True, version="1.0")


def download_model_all() -> None:
    """
    Download all translation models in advance
    """
    _download_install(_EN_TH_MODEL_NAME)
    _download_install(_TH_EN_MODEL_NAME)


class EnThTranslator:
    """
    English-Thai Machine Translation

    from VISTEC-depa Thailand Artificial Intelligence Research Institute

    Website: https://airesearch.in.th/releases/machine-translation-models/

    :param bool use_gpu : load model using GPU (Default is False)
    """

    def __init__(self, use_gpu: bool = False):
        self._tokenizer = MosesTokenizer("en")

        self._model_name = _EN_TH_MODEL_NAME

        _download_install(self._model_name)
        self._model = TransformerModel.from_pretrained(
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

    def translate(self, text: str) -> str:
        """
        Translate text from English to Thai

        :param str text: input text in source language
        :return: translated text in target language
        :rtype: str

        :Example:

        Translate text from English to Thai::

            from pythainlp.translate import EnThTranslator

            enth = EnThTranslator()

            enth.translate("I love cat.")
            # output: ฉันรักแมว

        """
        tokens = " ".join(self._tokenizer.tokenize(text))
        translated = self._model.translate(tokens)
        return translated.replace(" ", "").replace("▁", " ").strip()


class ThEnTranslator:
    """
    Thai-English Machine Translation

    from VISTEC-depa Thailand Artificial Intelligence Research Institute

    Website: https://airesearch.in.th/releases/machine-translation-models/

    :param bool use_gpu : load model using GPU (Default is False)
    """

    def __init__(self, use_gpu: bool = False):
        self._model_name = _TH_EN_MODEL_NAME

        _download_install(self._model_name)
        self._model = TransformerModel.from_pretrained(
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
            self._model.cuda()

    def translate(self, text: str) -> str:
        """
        Translate text from Thai to English

        :param str text: input text in source language
        :return: translated text in target language
        :rtype: str

        :Example:

        Translate text from Thai to English::

            from pythainlp.translate import ThEnTranslator

            then = ThEnTranslator()

            then.translate("ฉันรักแมว")
            # output: I love cat.

        """
        return self._model.translate(text)
