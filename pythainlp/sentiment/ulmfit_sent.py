# -*- coding: utf-8 -*-
"""
Sentiment analyzer based on thai2vec ("ulmfit" engine)
Code by https://github.com/cstorm125/thai2vec/tree/master/notebook
"""
from collections import defaultdict

import dill as pickle
import numpy as np
import torch
from pythainlp.corpus import download, get_file
from pythainlp.tokenize import word_tokenize
from torch import LongTensor
from torch.autograd import Variable

# from fastai.text import multiBatchRNN

MODEL_NAME = "sent_model"
ITOS_NAME = "itos_sent"


# download pretrained model
def get_path(fname):
    path = get_file(fname)
    if not path:
        download(fname)
        path = get_file(fname)
    return path


# load model
model = torch.load(get_path(MODEL_NAME))
model.eval()

# load itos and stoi
itos = pickle.load(open(get_path(ITOS_NAME), "rb"))
stoi = defaultdict(lambda: 0, {v: k for k, v in enumerate(itos)})

# get sentiment; 1 for positive and 0 for negative
# or score if specified return_score=True
softmax = lambda x: np.exp(x) / np.sum(np.exp(x))


def get_sentiment(text, return_score=False):
    words = word_tokenize(text)
    tensor = LongTensor([stoi[word] for word in words]).view(-1, 1).cpu()
    tensor = Variable(tensor, volatile=False)
    model.reset()
    pred, *_ = model(tensor)
    result = pred.data.cpu().numpy().reshape(-1)

    if return_score:
        return softmax(result)
    else:
        return np.argmax(result)


def about():
    return """
    Sentiment analyzer based on thai2vec
    Data is from various online reviews including but not limited to JagerV3 and Wongnai Challenge.
    89% accuracy based on 15% validation set compared to
    72% of fastText and 52% most-frequent-class baseline.

    Development: Charin Polpanumas
    GitHub: https://github.com/cstorm125/thai2vec
    """
