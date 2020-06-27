# -*- coding: utf-8 -*-
import os
from pythainlp.tools import get_full_data_path, get_pythainlp_data_path
from fairseq.models.transformer import TransformerModel
from sacremoses import MosesTokenizer

en_word_tokenize = MosesTokenizer("en")


def get_path(model, path1, path2, file=None):
    path = os.path.join(os.path.join(get_full_data_path(model), path1), path2)
    if file is not None:
        return os.path.join(path, file)
    return os.path.join(path, "")


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

def _translate(text):
    tokenized_sentence = " ".join(
        en_word_tokenize.tokenize(text)
    )
    hypothesis = model.translate(tokenized_sentence)
    hypothesis = hypothesis.replace(" ", "").replace("▁", " ")
    return hypothesis