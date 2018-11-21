# -*- coding: utf-8 -*-

"""
Code by https://github.com/cstorm125/thai2fit/
"""
import re
import numpy as np
import dill as pickle

#fastai
from fastai import *    
from fastai.text.transform import *

#pytorch
import torch
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

#pythainlp
from pythainlp.corpus import download, get_file
from pythainlp.tokenize import word_tokenize
from pythainlp.util import normalize as normalize_char_order

MODEL_NAME = "thai2fit_lm"
ITOS_NAME = "thai2fit_itos"

#custom fastai tokenizer
class ThaiTokenizer(BaseTokenizer):
    """
    Wrapper around a frozen newmm tokenizer to make it a fastai `BaseTokenizer`.
    """
    def __init__(self, lang:str = 'th'):
        self.lang = lang
    def tokenizer(self, t:str) -> List[str]:
        """
        :meth: tokenize text with a frozen newmm engine
        :param str t: text to tokenize
        :return: tokenized text
        """
        return(word_tokenize(t,engine='ulmfit'))
    def add_special_cases(self, toks:Collection[str]):
        pass

#special rules for thai
def replace_rep_after(t:str) -> str:
    "Replace repetitions at the character level in `t` after the repetition"
    def _replace_rep(m:Collection[str]) -> str:
        c,cc = m.groups()
        return f' {c} {TK_REP} {len(cc)+1} '
    re_rep = re.compile(r'(\S)(\1{3,})')
    return re_rep.sub(_replace_rep, t)

def rm_useless_newlines(t:str) -> str:
    "Remove multiple newlines in `t`."
    return re.sub('[\n]{2,}', ' ', t)

def rm_brackets(t:str) -> str:
    "Remove all empty brackets from `t`."
    new_line = re.sub('\(\)','',t)
    new_line = re.sub('\{\}','',new_line)
    new_line = re.sub('\[\]','',new_line)
    return(new_line)

#in case we want to add more specific rules for thai
thai_rules = [fix_html, deal_caps, replace_rep_after, normalize_char_order, 
              spec_add_spaces, rm_useless_spaces, rm_useless_newlines, rm_brackets]

# Download pretrained models
def get_path(fname):
    """
    :meth: download get path of file from pythainlp-corpus
    :param str fname: file name
    :return: path to downloaded file
    """
    path = get_file(fname)
    if not path:
        download(fname)
        path = get_file(fname)
    return(path)

#pretrained paths
THWIKI = [get_path(MODEL_NAME)[:-4], get_path(ITOS_NAME)[:-4]]
tt = Tokenizer(tok_func = ThaiTokenizer, lang = 'th', rules = thai_rules)

def document_vector(text, learn, data):
    """
    :meth: `document_vector` get document vector using fastai language model and data bunch
    :param str text: sentence to extract embeddings
    :param learn: fastai language model learner
    :param data: fastai data bunch
    :return: `numpy.array` of document vector sized 1200 containing last hidden layer as well as its average pooling and max pooling
    """
    s = tt.tokenizer(text)
    t = torch.tensor(data.vocab.numericalize(s), requires_grad=False)[:,None].to(device)
    m = learn.model[0]
    m.reset()
    pred,_ = m(t)
    #return concatenation of last, mean and max
    last = pred[-1][-1,:,:].squeeze()
    avg_pool = pred[-1].mean(0)[0].squeeze()
    max_pool = pred[-1].max(0)[0].squeeze()
    res = torch.cat((last,avg_pool,max_pool)).detach().cpu().numpy()
    return(res)

def predict_word(text,learn,data,topk=5):
    """
    :meth: `predict_word` predicts top-k most likely words based on given string, fastai language model and data bunch
    :param str text: seed text
    :param learn: fastai language model learner
    :param data: fastai data bunch
    :param int topk: how many top-k words to generate
    :return: list of top-k words
    """    
    s = tt.tokenizer(text)
    t = torch.LongTensor(data.train_ds.vocab.numericalize(s)).view(-1,1).to(device)
    t.requires_grad = False
    m = learn.model
    m.reset()
    pred,*_ = m(t)
    pred_i = pred[-1].topk(topk)[1].cpu().numpy()
    return([data.vocab.itos[i] for i in pred_i])

def predict_sentence(text,learn,data,nb_words=10):
    """
    :meth: `predict_word` predicts subsequent sentences based on given string, fastai language model and data bunch
    :param str text: seed text
    :param learn: fastai language model learner
    :param data: fastai data bunch
    :param int nb_words: how many words of sentence to generate
    :return: string of `nb_words` words
    """    
    result = []
    s = tt.tokenizer(text)
    t = torch.LongTensor(data.train_ds.vocab.numericalize(s)).view(-1,1).to(device)
    t.requires_grad = False
    m = learn.model
    m.reset()
    pred,*_ = m(t)
    for i in range(nb_words):
        pred_i = pred[-1].topk(2)[1]
        #get first one if not unknowns, pads, or spaces
        pred_i = pred_i[1] if pred_i.data[0] == 0 else pred_i[0]
        pred_i = pred_i.view(-1,1)
        result.append(data.train_ds.vocab.textify(pred_i))
        t = torch.cat((t,pred_i))
        pred,*_ = m(t)
    return(result)