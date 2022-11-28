# -*- coding: utf-8 -*-
from collections import Counter


class WordList(list):
    def __init__(self, collection):
        super(WordList, self).__init__(collection)
    def __str__(self):
        return '|'.join(self)


class nlp(object):
    def __init__(self,text,dictlist=[]):
        from pythainlp.tokenize import word_tokenize
        self.word_tokenize = word_tokenize
        from pythainlp.util import Trie
        self.Trie = Trie
        self.text=text
        self.dictlist=dictlist
        if self.dictlist==[]:
            self.words=WordList(self.word_tokenize(self.text))
        else:
            self.dict=Trie(self.dictlist)
            self.words=WordList(self.word_tokenize(self.text,custom_dict=self.dict))
        self.word_counts=Counter(self.words)
    def change_word_tokenize(self,name):
        if self.dictlist==[]:
            self.words=WordList(self.word_tokenize(self.text,engine=name))
        else:
            self.words=WordList(self.word_tokenize(self.text,custom_dict=self.dict))
    def ngrams(self,n=1):
        return [tuple(self.words[i:i+n]) for i in range(len(self.words)-n+1)]
    def __repr__(self):
        return self.text
    def __str__(self):
        return "|".join(self.words)
