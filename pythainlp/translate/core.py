# -*- coding: utf-8 -*-
from functools import partial
from collections import defaultdict

from fairseq.models.transformer import TransformerModel

from sacremoses import MosesTokenizer, MosesDetokenizer
from pythainlp.tokenize import word_tokenize as th_word_tokenize
from pythainlp.corpus import get_corpus_path, download
import tarfile
from pythainlp.tools import get_pythainlp_data_path, get_full_data_path
import os

en_word_tokenize = MosesTokenizer('en')
en_word_detokenize = MosesDetokenizer('en')
th_word_tokenize = partial(th_word_tokenize, keep_whitespace=False)
model = None
model_name = ""
def get_path(model,path1,path2,file=None):
    path = os.path.join(os.path.join(os.path.join(get_pythainlp_data_path(), model),path1),path2)
    if file != None:
        return os.path.join(path,file)
    return os.path.join(path, "")
def download_model():
    print("Download model ...")
    if get_corpus_path("scb_1m_th-en_newmm") == None:
        download("scb_1m_th-en_newmm",force=True,version="1.0")
        tar = tarfile.open(get_corpus_path("scb_1m_th-en_newmm"), "r:gz")
        tar.extractall()
        tar.close()
    if get_corpus_path("scb_1m_th-en_spm") == None:
        download("scb_1m_th-en_spm",force=True,version="1.0")
        tar = tarfile.open(get_corpus_path("scb_1m_th-en_spm"), "r:gz")
        tar.extractall()
        tar.close()
    if get_corpus_path("scb_1m_en-th_moses") == None:
        download("scb_1m_en-th_moses",force=True,version="1.0")
        tar = tarfile.open(get_corpus_path("scb_1m_en-th_moses"), "r:gz")
        tar.extractall()
        tar.close()
    print("Install model...")
    if os.path.isdir(get_full_data_path("scb_1m_th-en_newmm")) == False:
        os.mkdir(get_full_data_path("scb_1m_th-en_newmm"))
        with tarfile.open(get_corpus_path("scb_1m_th-en_newmm")) as tar:
            tar.extractall(path=get_full_data_path("scb_1m_th-en_newmm"))
    if os.path.isdir(get_full_data_path("scb_1m_th-en_spm")) == False:
        os.mkdir(get_full_data_path("scb_1m_th-en_spm"))
        with tarfile.open(get_corpus_path("scb_1m_th-en_spm")) as tar:
            tar.extractall(path=get_full_data_path("scb_1m_th-en_spm"))
    if os.path.isdir(get_full_data_path("scb_1m_en-th_moses")) == False:
        os.mkdir(get_full_data_path("scb_1m_en-th_moses"))
        with tarfile.open(get_corpus_path("scb_1m_en-th_moses")) as tar:
            tar.extractall(path=get_full_data_path("scb_1m_en-th_moses"))
download_model()

def load_th2en_word2word():
    global model,model_name
    if model_name != "th2en_word2word":
        model = TransformerModel.from_pretrained(
            model_name_or_path=get_path("scb_1m_th-en_newmm", "SCB_1M+TBASE_th-en_newmm-moses_130000-130000_v1.0", 'models'),
            checkpoint_file='checkpoint.pt',
            data_name_or_path=get_path("scb_1m_th-en_newmm", "SCB_1M+TBASE_th-en_newmm-moses_130000-130000_v1.0", 'vocab')
        )
        model_name = "th2en_word2word"
def load_th2en_bpe2bpe():
    global model,model_name
    if model_name != "th2en_bpe2bpe":
        model = TransformerModel.from_pretrained(
            model_name_or_path=get_path("scb_1m_th-en_spm", "SCB_1M+TBASE_th-en_spm-spm_32000-joined_v1.0", 'models'),
            checkpoint_file='checkpoint.pt',
            data_name_or_path=get_path("scb_1m_th-en_spm", "SCB_1M+TBASE_th-en_spm-spm_32000-joined_v1.0", 'vocab'),
            bpe='sentencepiece',
            sentencepiece_vocab=get_path("scb_1m_th-en_spm", "SCB_1M+TBASE_th-en_spm-spm_32000-joined_v1.0", 'bpe','spm.th.model')
            )
        model_name = "th2en_bpe2bpe"
def load_en2th_word2bpe():
    global model,model_name
    if model_name != "en2th_word2bpe":
        model = TransformerModel.from_pretrained(
            model_name_or_path=get_path("scb_1m_en-th_moses", "SCB_1M+TBASE_en-th_moses-spm_130000-16000_v1.0", 'models'),
            checkpoint_file='checkpoint.pt',
            data_name_or_path=get_path("scb_1m_en-th_moses", "SCB_1M+TBASE_en-th_moses-spm_130000-16000_v1.0", 'vocab')
        )
        model_name = "en2th_word2bpe"
def translate(input_sentence, source = "en", target = "tha", tokenizer = "bpe"):
    """
    :param str input_sentence: input sentence
    :param str source: source language (en, tha)
    :param str tokenizer: tokenizer (word,bpe)
    :param str target: target language (en, tha)

    :return: translate sentence
    :rtype: str
    """
    global model
    hypothesis = None
    if source == "tha" and target == "en":
        if tokenizer == "word":
            load_th2en_word2word()
            tokenized_sentence = ' '.join(th_word_tokenize(input_sentence))
            _hypothesis = model.translate(tokenized_sentence)
            hypothesis = en_word_detokenize.detokenize([_hypothesis])
        else:
            load_th2en_bpe2bpe()
            hypothesis = model.translate(input_sentence, beam=24)
    elif source == "en" and target == "tha" and tokenizer == "bpe":
        load_en2th_word2bpe()
        tokenized_sentence = ' '.join(en_word_tokenize.tokenize(input_sentence))
        hypothesis = model.translate(tokenized_sentence)
        hypothesis = hypothesis.replace(' ', '').replace('▁', ' ')
    return hypothesis
