# -*- coding: utf-8 -*-
from __future__ import absolute_import,unicode_literals
# NLP
import re
from pythainlp.tokenize import word_tokenize
from pythainlp.tag import pos_tag
from pythainlp.corpus import stopwords
thaicut="newmm" # ตัวตัดคำ
# CRF
try:
    import sklearn_crfsuite
except ImportError:
    from pythainlp.tools import install_package
    install_package('sklearn-crfsuite')
    import sklearn_crfsuite
# FILE
import glob
import codecs
from pythainlp.corpus import get_file,download

stopwords = stopwords.words('thai')


def isThai(chr): # เช็คว่าเป็น char ภาษาไทย
 cVal = ord(chr)
 if(cVal >= 3584 and cVal <= 3711):
  return True
 return False
def isThaiWord(word): # เช็คว่าเป็นคำภาษาไทย
 t=True
 for i in word:
  l=isThai(i)
  if l!=True and i!='.':
   t=False
   break
 return t

def is_stopword(word): # เช็คว่าเป็นคำฟุ่งเฟือง
    return word in stopwords
def doc2features(doc, i):
    word = doc[i][0]
    postag = doc[i][1]
    # Features from current word
    features={
        'word.word': word,
        'word.stopword': is_stopword(word),
        'word.isthai':isThaiWord(word),
        'word.isspace':word.isspace(),
        'postag':postag,
        'word.isdigit()': word.isdigit()
    }
    if word.isdigit() and len(word)==5:
        features['word.islen5']=True
    if i > 0:
        prevword = doc[i-1][0]
        postag1 = doc[i-1][1]
        features['word.prevword'] = prevword
        features['word.previsspace']=prevword.isspace()
        features['word.previsthai']=isThaiWord(prevword)
        features['word.prevstopword']=is_stopword(prevword)
        features['word.prepostag'] = postag1
        features['word.prevwordisdigit'] = prevword.isdigit()
    else:
        features['BOS'] = True # Special "Beginning of Sequence" tag
    # Features from next word
    if i < len(doc)-1:
        nextword = doc[i+1][0]
        postag1 = doc[i+1][1]
        features['word.nextword'] = nextword
        features['word.nextisspace']=nextword.isspace()
        features['word.nextpostag'] = postag1
        features['word.nextisthai']=isThaiWord(nextword)
        features['word.nextstopword']=is_stopword(nextword)
        features['word.nextwordisdigit'] = nextword.isdigit()
    else:
        features['EOS'] = True # Special "End of Sequence" tag
    return features

class thainer:
    def __init__(self):
        self.data_path = get_file('thainer')
        if self.data_path==None:
            download('thainer')
            self.data_path = get_file('thainer')
        self.crf=sklearn_crfsuite.CRF(
            algorithm='lbfgs',
            c1=0.1,
            c2=0.1,
            max_iterations=500,
            all_possible_transitions=True,
            model_filename=self.data_path)
    def get_ner(self,text):
        self.word_cut=word_tokenize(text,engine=thaicut)
        self.list_word=pos_tag(self.word_cut,engine='perceptron')
        self.X_test = self.extract_features([(data,self.list_word[i][1]) for i,data in enumerate(self.word_cut)])
        self.y_=self.crf.predict_single(self.X_test)
        return [(self.word_cut[i],self.list_word[i][1],data) for i,data in enumerate(self.y_)]
    def extract_features(self,doc):
        return [doc2features(doc, i) for i in range(len(doc))]
    def get_labels(self,doc):
        return [tag for (token,postag,tag) in doc]
    def get_model(self):
        return self.crf
