# -*- coding: utf-8 -*-
import os
from functools import partial

from pythainlp.tools import get_full_data_path, get_pythainlp_data_path
from fairseq.models.transformer import TransformerModel
from sacremoses import MosesDetokenizer
from pythainlp.tokenize import word_tokenize as th_word_tokenize

en_word_detokenize = MosesDetokenizer("en")
th_word_tokenize = partial(th_word_tokenize, keep_whitespace=False)

def get_path(model, path1, path2, file=None):
    path = os.path.join(os.path.join(get_full_data_path(model), path1), path2)
    if file is not None:
        return os.path.join(path, file)
    return os.path.join(path, "")

th2en_bpe_model = TransformerModel.from_pretrained(
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

def _translate(text):
    hypothesis = th2en_bpe_model.translate(text, beam=24)
    return hypothesis