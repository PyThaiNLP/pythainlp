# -*- coding: utf-8 -*-
from __future__ import absolute_import,division,print_function,unicode_literals
import sys
def pos_tag(list_text,engine='unigram',corpus='orchid'):
    """
    Part of Speech tagging function.

    :param list list_text: takes in a list of tokenized words (put differently, a list of string)
    :param str engine:
        * unigram - unigram tagger
        * perceptron - perceptron tagger
        * artagger - RDR POS tagger
    :param str corpus:
        * orchid - annotated Thai academic articles
        * pud - Parallel Universal Dependencies (PUD) treebanks
    :return: returns a list of labels regarding which part of speech it is
    """
    if engine=='old' or engine=='unigram':
        from .old import tag
    elif engine=='perceptron':
        from .perceptron import tag
    elif engine=='artagger':
        def tag(text1):
            try:
                from artagger import Tagger
            except ImportError:
                from pythainlp.tools import install_package
                install_package('https://github.com/wannaphongcom/artagger/archive/master.zip')
                try:
                    from artagger import Tagger
                except ImportError:
                    print("Error ! using 'pip install https://github.com/wannaphongcom/artagger/archive/master.zip'")
                    sys.exit(0)
            words = Tagger().tag(' '.join(text1))
            totag=[]
            for word in words:
                totag.append((word.word, word.tag))
            return totag
        return tag(list_text)
    return tag(list_text,corpus=corpus)

def pos_tag_sents(sentences,engine='unigram',corpus='orchid'):
    return [pos_tag(i,engine=engine,corpus=corpus) for i in sentences]
