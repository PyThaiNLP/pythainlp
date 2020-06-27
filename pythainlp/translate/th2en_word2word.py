# -*- coding: utf-8 -*-
import os
from pythainlp.tools import get_full_data_path, get_pythainlp_data_path
from fairseq.models.transformer import TransformerModel
from sacremoses import MosesDetokenizer
from pythainlp.tokenize import word_tokenize as th_word_tokenize

en_word_detokenize = MosesDetokenizer("en")


def get_path(model, path1, path2, file=None):
    path = os.path.join(os.path.join(get_full_data_path(model), path1), path2)
    if file is not None:
        return os.path.join(path, file)
    return os.path.join(path, "")


th2en_word2word_model = TransformerModel.from_pretrained(
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


def _translate(text):
    tokenized_sentence = " ".join(th_word_tokenize(text))
    _hypothesis = th2en_word2word_model.translate(tokenized_sentence)
    hypothesis = en_word_detokenize.detokenize([_hypothesis])
    return hypothesis