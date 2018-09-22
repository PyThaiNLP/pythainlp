# -*- coding: utf-8 -*-
'''
Code by https://github.com/cstorm125/thai2vec/tree/master/notebook
'''
from __future__ import absolute_import,unicode_literals
import os
import sys
import re
import torch

#numpy and fastai
try:
    import numpy as np
    from fastai.text import *
    import dill as pickle
except ImportError:
    from pythainlp.tools import install_package
    install_package('fastai')
    install_package('numpy')
    try:
        import numpy as np
        from fastai.text import *
        import dill as pickle
    except ImportError:
        print("Error installing using 'pip install fastai numpy dill'")
        sys.exit(0)

#import torch
try:
    import torch
except ImportError:
    print('PyTorch required. See https://pytorch.org/.')

from pythainlp.tokenize import word_tokenize
from pythainlp.corpus import get_file
from pythainlp.corpus import download
MODEL_NAME = 'thwiki_model2'
ITOS_NAME = 'itos'

#paralellized thai tokenizer with some text cleaning
class ThaiTokenizer():
    def __init__(self, engine='newmm'):
        """
        :parameters for tokenization engine:
            * newmm - Maximum Matching algorithm + TCC
            * icu -  IBM ICU
            * longest-matching - Longest matching
            * mm - Maximum Matching algorithm
            * pylexto - LexTo
            * deepcut - Deep Neural Network
        """
        self.engine = engine
        self.re_br = re.compile(r'<\s*br\s*/?>', re.IGNORECASE)
        self.re_rep = re.compile(r'(\S)(\1{3,})')

    def sub_br(self,text): 
        """
        :meth:`sub_br` replace `<br>` tags with `\n`
        :param str text: text to process
        :return: procssed text
        """
        return self.re_br.sub("\n", text)

    def tokenize(self,text):
        """
        :meth: tokenize text with selected engine
        :param str text: text to tokenize
        :return: tokenized text
        """
        return [t for t in word_tokenize(self.sub_br(text),engine=self.engine)]
  
    @staticmethod
    def replace_rep(text):
        '''
        :meth:`replace_rep` replace 3 or above repetitive characters with `tkrep`
        :param str text: text to process
        :return: processed text where repetitions are replaced by `tkrep` followed by number of repetitions
        **Example**::
            >>> from pythainlp.ulmfit.utils import ThaiTokenizer
            >>> tt = ThaiTokenizer()
            >>> tt.replace_rep('คือดียยยยยย')
            คือดีtkrep6ย
        '''
        TK_REP = 'tkrep'
        c,cc = text.groups()
        return f'{TK_REP}{len(cc)+1}{c}'

    def proc_text(self, text):
        """
        :meth: `proc_text` procss and tokenize text removing repetitions, special characters, double spaces
        :param str text: text to process
        :return: processed and tokenized text
        """
        s = self.re_rep.sub(ThaiTokenizer.replace_rep, text)
        s = re.sub(r'([/#])', r' \1 ', s)
        #remvoe double space
        s = re.sub(' {2,}', ' ', s)
        return self.tokenize(s)

    @staticmethod
    def proc_all(ss):
        """
        :meth: `proc_all` runs `proc_text` for multiple sentences
        :param str text: text to process
        :return: processed and tokenized text
        """
        tok = ThaiTokenizer()
        return [tok.proc_text(s) for s in ss]

    @staticmethod
    def proc_all_mp(ss):
        """
        :meth: `proc_all` runs `proc_text` for multiple sentences using multiple cpus
        :param str text: text to process
        :return: processed and tokenized text
        """
        ncpus = num_cpus()//2
        with ProcessPoolExecutor(ncpus) as e:
            return sum(e.map(ThaiTokenizer.proc_all, ss), [])

#ulmfit helper functions
BOS = 'xbos'  # beginning-of-sentence tag
def get_texts(df):
    """
    :meth: `get_texts` get tuple of tokenized texts and labels
    :param pandas.DataFrame df: `pandas.DataFrame` with `label` as first column and `text` as second column
    :return:
        * tok - lists of tokenized texts with beginning-of-sentence tag `xbos` as first element of each list
        * labels - list of labels
    """
    labels = df.iloc[:,0].values.astype(np.int64)
    texts = BOS+df.iloc[:,1].astype(str).apply(lambda x: x.rstrip())
    tok = ThaiTokenizer().proc_all_mp(partition_by_cores(texts))
    return(tok, list(labels))

def get_all(df):
    """
    :meth: `get_all` iterate `get_texts` for all the entire `pandas.DataFrame`
    :param pandas.DataFrame df: `pandas.DataFrame` with `label` as first column and `text` as second column
    :return:
        * tok - lists of tokenized texts with beginning-of-sentence tag `xbos` as first element of each list
        * labels - list of labels
    """
    tok, labels = [], []
    for i, r in enumerate(df):
        tok_, labels_ = get_texts(r)
        tok += tok_;
        labels += labels_
    return(tok, labels)

def numericalizer(df, itos=None, max_vocab = 60000, min_freq = 2, pad_tok = '_pad_', unk_tok = '_unk_'):
    """
    :meth: `numericalize` numericalize tokenized texts for:
        * tokens with word frequency more than `min_freq`
        * at maximum vocab size of `max_vocab`
        * add unknown token `_unk_` and padding token `_pad_` in first and second position
        * use integer-to-string list `itos` if avaiable e.g. ['_unk_', '_pad_','first_word','second_word',...]
    :param pandas.DataFrame df: `pandas.DataFrame` with `label` as first column and `text` as second column
    :param list itos: integer-to-string list
    :param int max_vocab: maximum number of vocabulary (default 60000)
    :param int min_freq: minimum word frequency to be included (default 2)
    :param str pad_tok: padding token
    :param str unk_token: unknown token
    :return:
        * lm - `numpy.array` of numericalized texts
        * tok - lists of tokenized texts with beginning-of-sentence tag `xbos` as first element of each list
        * labels - list of labels
        * itos - integer-to-string list e.g. ['_unk_', '_pad_','first_word','second_word',...]
        * stoi - string-to-integer dict e.g. {'_unk_':0, '_pad_':1,'first_word':2,'second_word':3,...}
        * freq - `collections.Counter` for word frequency
    """
    tok, labels = get_all(df)
    freq = Counter(p for o in tok for p in o)
    if itos is None:
        itos = [o for o,c in freq.most_common(max_vocab) if c>min_freq]
        itos.insert(0, pad_tok)
        itos.insert(0, unk_tok)
    stoi = collections.defaultdict(lambda:0, {v:k for k,v in enumerate(itos)})
    lm = np.array([[stoi[o] for o in p] for p in tok])
    return(lm,tok,labels,itos,stoi,freq)

def merge_wgts(em_sz, wgts, itos_pre, itos_cls):
    """
    :param pandas.DataFrame df: `pandas.DataFrame` with `label` as first column and `text` as second column
    :param int em_sz: size of embedding vectors (pretrained model is at 300)
    :param wgts: saved pyTorch weights of pretrained model
    :param list itos_pre: integer-to-string list of pretrained model
    :param list itos_cls: integer-to-string list of current dataset
    :return: merged weights of the model for current dataset
    """
    vocab_size = len(itos_cls)
    enc_wgts = to_np(wgts['0.encoder.weight'])
    #average weight of encoding
    row_m = enc_wgts.mean(0)
    stoi_pre = collections.defaultdict(lambda:-1, {v:k for k,v in enumerate(itos_pre)})
    #new embedding based on classification dataset
    new_w = np.zeros((vocab_size, em_sz), dtype=np.float32)
    for i,w in enumerate(itos_cls):
        r = stoi_pre[w]
        #use pretrianed embedding if present; else use the average
        new_w[i] = enc_wgts[r] if r>=0 else row_m
    wgts['0.encoder.weight'] = T(new_w)
    wgts['0.encoder_with_dropout.embed.weight'] = T(np.copy(new_w))
    wgts['1.decoder.weight'] = T(np.copy(new_w))
    return(wgts)

#feature extractor
def document_vector(ss, m, stoi,tok_engine='newmm'):
    """
    :meth: `document_vector` get document vector using pretrained ULMFit model
    :param str ss: sentence to extract embeddings
    :param m: pyTorch model
    :param dict stoi: string-to-integer dict e.g. {'_unk_':0, '_pad_':1,'first_word':2,'second_word':3,...}
    :param str tok_engine: tokenization engine (recommend using `newmm` if you are using pretrained ULMFit model)
    :return: `numpy.array` of document vector sized 300
    """
    s = word_tokenize(ss)
    t = LongTensor([stoi[i] for i in s]).view(-1,1).cuda()
    t = Variable(t,volatile=False)
    m.reset()
    pred,*_ = m[0](t)
    #get average of last lstm layer along bptt
    res = to_np(torch.mean(pred[-1],0).view(-1))
    return(res)

class SaveFeatures():
    features=None
    def __init__(self, m): self.hook = m.register_forward_hook(self.hook_fn)
    def hook_fn(self, module, input, output): self.features = output
    def remove(self): self.hook.remove()

#Download pretrained models
def get_path(fname):
	path = get_file(fname)
	if path==None:
		download(fname)
		path = get_file(fname)
	return(path)

def load_pretrained_model():
    path = get_path(MODEL_NAME)
    wgts = torch.load(path, map_location=lambda storage, loc: storage)
    return(wgts)

def load_pretrained_itos():
    path = get_path(ITOS_NAME)
    itos = pickle.load(open(path,'rb'))
    return(itos)

def about():
	return '''
	thai2vec
	State-of-the-Art Language Modeling, Text Feature Extraction and Text Classification in Thai Language.
    Created as part of pyThaiNLP with ULMFit implementation from fast.ai
	
	Development : Charin Polpanumas
	GitHub : https://github.com/cstorm125/thai2vec
	'''
