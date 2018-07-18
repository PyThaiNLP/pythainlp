# -*- coding: utf-8 -*-
'''
Code by https://github.com/cstorm125/thai2vec/tree/master/notebook
'''
from __future__ import absolute_import,unicode_literals
import os
import sys
from collections import defaultdict

#numpy and dill
try:
    import numpy as np
    import dill as pickle
except ImportError:
    from pythainlp.tools import install_package
    install_package('numpy')
    install_package('dill')
    try:
        import numpy as np
        import dill as pickle
    except ImportError:
        print("Error installing using 'pip install numpy dill'")
        sys.exit(0)

#import torch
try:
    import torch
except ImportError:
    print('PyTorch required. See https://pytorch.org/.')
import torch
from torch.autograd import Variable
from torch import LongTensor

#import fastai for multiBatchRNN
try:
    from fastai.text import *
except ImportError:
    print(
    """
    fastai required for multiBatchRNN. 
    Run 'pip install https://github.com/fastai/fastai/archive/master.zip'
    """)

from pythainlp.tokenize import word_tokenize
from pythainlp.corpus import get_file
from pythainlp.corpus import download

MODEL_NAME = 'sent_model'
ITOS_NAME = 'itos_sent'

#download pretrained model
def get_path(fname):
	path = get_file(fname)
	if path==None:
		download(fname)
		path = get_file(fname)
	return(path)

#load model
m = torch.load(get_path(MODEL_NAME))
m.eval()
#load itos and stoi
itos = pickle.load(open(get_path(ITOS_NAME),'rb'))
stoi = defaultdict(lambda:0, {v:k for k,v in enumerate(itos)})


#get sentiment; 1 for positive and 0 for negative
#or score if specified return_score=True
softmax = lambda x : np.exp(x)/np.sum(np.exp(x))
def get_sentiment(ss,return_score=False):
    s = word_tokenize(ss)
    t = LongTensor([stoi[i] for i in s]).view(-1,1).cpu()
    t = Variable(t,volatile=False)
    m.reset()
    pred,*_ = m(t)
    result = pred.data.cpu().numpy().reshape(-1)
    if return_score:
        return(softmax(result))
    else:
        return(np.argmax(result))

def about():
	return '''
	Sentiment Analyzer based on thai2vec
	Data is from various online reviews including but not limited to JagerV3 and Wongnai Challenge.
    89% accuracy based on 15% validation set compared to 72% of fastText and 52% most-frequent-class baseline.
	
	Development : Charin Polpanumas
	GitHub : https://github.com/cstorm125/thai2vec
	'''