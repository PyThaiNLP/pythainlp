# -*- coding: utf-8 -*-
from pythainlp.augment.word2vec.core import Word2VecAug
from pythainlp.corpus import get_corpus_path
from pythainlp.tokenize import word_tokenize
from typing import List, Tuple


class LTW2VAug:
    """
    Text Augment using word2vec from LTW2V

    LTW2V:
    `github.com/PyThaiNLP/large-thaiword2vec <https://github.com/PyThaiNLP/large-thaiword2vec>`_
    """
    def __init__(self):
        self.ltw2v_wv = get_corpus_path('ltw2v')
        self.load_w2v()

    def tokenizer(self, text: str) -> List[str]:
        """
        :param str text: thai text
        :rtype: List[str]
        """
        return word_tokenize(text, engine='newmm')

    def load_w2v(self):  # insert substitute
        """
        Load ltw2v word2vec model
        """
        self.aug = Word2VecAug(self.ltw2v_wv, self.tokenizer, type="binary")

    def augment(
        self,
        sentence: str,
        n_sent: int = 1,
        p: float = 0.7
    ) -> List[Tuple[str]]:
        """
        Text Augment using word2vec from Thai2Fit

        :param str sentence: thai sentence
        :param int n_sent: number sentence
        :param float p: Probability of word

        :return: list of text augment
        :rtype: List[Tuple[str]]

        :Example:
        ::

            from pythainlp.augment.word2vec import LTW2VAug

            aug = LTW2VAug()
            aug.augment("ผมเรียน", n_sent=2, p=0.5)
            # output: [('เขา', 'เรียนหนังสือ'), ('เขา', 'สมัครเรียน')]
        """
        return self.aug.augment(sentence, n_sent, p)
