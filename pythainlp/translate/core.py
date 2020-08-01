# -*- coding: utf-8 -*-
import os
import tarfile
from collections import defaultdict
from functools import partial

from pythainlp.corpus import download, get_corpus_path
from pythainlp.tools import get_full_data_path, get_pythainlp_data_path
from fairseq.models.transformer import TransformerModel
from sacremoses import MosesTokenizer, MosesDetokenizer
from pythainlp.tools import get_full_data_path, get_pythainlp_data_path
from pythainlp.tokenize import word_tokenize as th_word_tokenize

en_word_detokenize = MosesDetokenizer("en")
en_word_tokenize = MosesTokenizer("en")
th_word_tokenize = partial(th_word_tokenize, keep_whitespace=False)


def download_model() -> None:
    """
    Download Model
    """
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
model = None
model_name = None

def get_path(model, path1, path2, file= None) -> str:
    path = os.path.join(os.path.join(get_full_data_path(model), path1), path2)
    if file is not None:
        return os.path.join(path, file)
    return os.path.join(path, "")


def en2th_word2bpe_model():
    global model,model_name
    if model_name != "en2th_word2bpe":
        del model
        model = TransformerModel.from_pretrained(
            model_name_or_path=get_path(
                "scb_1m_en-th_moses",
                "SCB_1M+TBASE_en-th_moses-spm_130000-16000_v1.0",
                "models",
            ),
            checkpoint_file="checkpoint.pt",
            data_name_or_path=get_path(
                "scb_1m_en-th_moses",
                "SCB_1M+TBASE_en-th_moses-spm_130000-16000_v1.0",
                "vocab",
                ),
        )
        model_name = "en2th_word2bpe"


def _en2th_word2bpe_translate(text: str) -> str:
    global model,model_name
    en2th_word2bpe_model()
    tokenized_sentence = " ".join(
        en_word_tokenize.tokenize(text)
    )
    hypothesis = model.translate(tokenized_sentence)
    hypothesis = hypothesis.replace(" ", "").replace("▁", " ")
    return hypothesis

def th2en_word2word_model():
    global model,model_name
    if model_name != "th2en_word2word":
        del model
        model = TransformerModel.from_pretrained(
            model_name_or_path=get_path(
                "scb_1m_th-en_newmm",
                "SCB_1M+TBASE_th-en_newmm-moses_130000-130000_v1.0",
                "models",
            ),
            checkpoint_file="checkpoint.pt",
            data_name_or_path=get_path(
                "scb_1m_th-en_newmm",
                "SCB_1M+TBASE_th-en_newmm-moses_130000-130000_v1.0",
                "vocab",
            ),
        )
        model_name = "th2en_word2word"


def _th2en_word2word_translate(text: str) -> str:
    global model,model_name
    th2en_word2word_model()
    tokenized_sentence = " ".join(th_word_tokenize(text))
    _hypothesis = model.translate(tokenized_sentence)
    hypothesis = en_word_detokenize.detokenize([_hypothesis])
    return hypothesis


def th2en_bpe_model():
    global model,model_name
    if model_name != "th2en_bpe":
        del model
        model = TransformerModel.from_pretrained(
            model_name_or_path=get_path(
                "scb_1m_th-en_spm",
                "SCB_1M+TBASE_th-en_spm-spm_32000-joined_v1.0",
                "models",
            ),
            checkpoint_file="checkpoint.pt",
            data_name_or_path=get_path(
                "scb_1m_th-en_spm",
                "SCB_1M+TBASE_th-en_spm-spm_32000-joined_v1.0",
                "vocab",
            ),
            bpe="sentencepiece",
            sentencepiece_vocab=get_path(
                "scb_1m_th-en_spm",
                "SCB_1M+TBASE_th-en_spm-spm_32000-joined_v1.0",
                "bpe",
                "spm.th.model",
            ),
        )
        model_name = "th2en_bpe"


def _th2en_bpe_translate(text: str) -> str:
    global model,model_name
    th2en_bpe_model()
    hypothesis = model.translate(text, beam=24)
    return hypothesis


def translate(
    text: str,
    source: str = "en",
    target: str = "th",
    tokenizer: str = "bpe",
) -> str:
    """
    Translate Language

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
            hypothesis = _th2en_word2word_translate(text)
        else:
            hypothesis = _th2en_bpe_translate(text)
    elif source == "en" and target == "th" and tokenizer == "bpe":
        hypothesis = _en2th_word2bpe_translate(text)
    else:
        return ValueError("the combination of the arguments isn't allowed.")

    return hypothesis
