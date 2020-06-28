# -*- coding: utf-8 -*-
import os
import glob
from collections import Counter

import re

cleanr = re.compile(r'<[^>]+>')


def cleantag(text):
    cleantext = re.sub(cleanr, '', text)
    return cleantext


def get_conll(text):
    list_data = [i.strip() for i in text.split('|')]
    temp = []
    for i in list_data:
        word = cleantag(i)
        tag = "O"
        find_tag = re.findall(cleanr, i)
        if find_tag != []:
            tag = "B-"+find_tag[0].replace('<', '').replace('>', '')
        temp.append((word, tag))
    return temp


class BEST_I:
    def __init__(self, path):
        self.path = path
        self.list_file = list(glob.glob(os.path.join(self.path, "*.txt")))
        self.data = {}
        for i in self.list_file:
            filename = os.path.basename(i)
            self.data[filename] = {}
            self.data[filename]['category'] = filename.split('_')[0]
            with open(i, "r", encoding="utf-8-sig") as f:
                self.data[filename]["raw"] = [j.strip() for j in f.readlines()]
                self.temp = []
                for j in self.data[filename]["raw"]:
                    j = cleantag(j)
                    if j.count('|') > 1:
                        self.temp.append(j.split('|'))
                    else:
                        self.temp.append(j.replace('|', ''))

                self.data[filename]["words"] = self.temp
                self.data[filename]["conll"] = [get_conll(j) for j in self.data[filename]["raw"]]

    def get_words_all(self):
        self.words_all = []
        for i in list(self.data.keys()):
            for j in self.data[i]["words"]:
                self.words_all.append(j)

        return self.words_all

    def count_word_all(self):
        self.words_all = self.get_words_all()
        self.list_word = []
        for i in self.words_all:
            self.list_word.extend(i)
        del self.words_all
        return Counter(self.list_word)
    
    def get_conll_all(self):
        self.list_conll = []
        for i in list(self.data.keys()):
            for j in self.data[i]["conll"]:
                self.list_conll.append(j)
        return self.list_conll
