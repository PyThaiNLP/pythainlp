# -*- coding: utf-8 -*-
import os
import tarfile
from collections import defaultdict
from functools import partial

from pythainlp.corpus import download, get_corpus_path
from pythainlp.tokenize import word_tokenize as th_word_tokenize
from pythainlp.tools import get_full_data_path, get_pythainlp_data_path

from fairseq.models.transformer import TransformerModel
from sacremoses import MosesDetokenizer, MosesTokenizer


def get_path(model, path1, path2, file=None):
    path = os.path.join(os.path.join(get_full_data_path(model), path1), path2)
    if file is not None:
        return os.path.join(path, file)
    return os.path.join(path, "")


def download_model():
    print("Download model ...")
    if get_corpus_path("scb_1m_th-en_newmm") is None:
        download("scb_1m_th-en_newmm", force=True, version="1.0")
        tar = tarfile.open(get_corpus_path("scb_1m_th-en_newmm"), "r:gz")
        tar.extractall()
        tar.close()
    if get_corpus_path("scb_1m_th-en_spm") is None:
        download("scb_1m_th-en_spm", force=True, version="1.0")
        tar = tarfile.open(get_corpus_path("scb_1m_th-en_spm"), "r:gz")
        tar.extractall()
        tar.close()
    if get_corpus_path("scb_1m_en-th_moses") is None:
        download("scb_1m_en-th_moses", force=True, version="1.0")
        tar = tarfile.open(get_corpus_path("scb_1m_en-th_moses"), "r:gz")
        tar.extractall()
        tar.close()

    print("Install model...")
    if not os.path.exists(get_full_data_path("scb_1m_th-en_newmm")):
        os.mkdir(get_full_data_path("scb_1m_th-en_newmm"))
        with tarfile.open(get_corpus_path("scb_1m_th-en_newmm")) as tar:
            tar.extractall(path=get_full_data_path("scb_1m_th-en_newmm"))
    if not os.path.exists(get_full_data_path("scb_1m_th-en_spm")):
        os.mkdir(get_full_data_path("scb_1m_th-en_spm"))
        with tarfile.open(get_corpus_path("scb_1m_th-en_spm")) as tar:
            tar.extractall(path=get_full_data_path("scb_1m_th-en_spm"))
    if not os.path.exists(get_full_data_path("scb_1m_en-th_moses")):
        os.mkdir(get_full_data_path("scb_1m_en-th_moses"))
        with tarfile.open(get_corpus_path("scb_1m_en-th_moses")) as tar:
            tar.extractall(path=get_full_data_path("scb_1m_en-th_moses"))


download_model()



def translate(
    text: str,
    source: str = "en",
    target: str = "th",
    tokenizer: str = "bpe",
) -> str:
    """
    :param str text: input text in source language
    :param str source: source language ("en" or "th")
    :param str target: target language ("en" or "th")
    :param str tokenizer: tokenizer (word,bpe)

    :return: translated text in target language
    :rtype: str
    """
    hypothesis = None

    if source == "th" and target == "en":
        if tokenizer == "word":
            from pythainlp.translate.th2en_word2word import _translate
            hypothesis = _translate(text)
        else:
            from pythainlp.translate.th2en_bpe2bpe import _translate
            hypothesis = _translate(text)
    elif source == "en" and target == "th" and tokenizer == "bpe":
        from pythainlp.translate.en2th_word2bpe import _translate
        hypothesis = _translate(text)

    return hypothesis
