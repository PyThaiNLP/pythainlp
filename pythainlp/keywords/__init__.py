# -*- coding: utf-8 -*-
from __future__ import absolute_import
from pythainlp.corpus import stopwords
from pythainlp.rank import rank
def find_keyword(word_list,lentext=3):
    '''
    :param list word_list: a list of thai text
    :param int lentext: a number of keyword
    :return: dict
    '''
    filtered_words = [word for word in word_list if word not in set(stopwords.words('thai'))]
    word_list=rank(filtered_words)
    return {k:v for k, v in word_list.items() if v>=lentext}
