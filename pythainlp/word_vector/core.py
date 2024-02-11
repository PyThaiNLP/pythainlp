# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
from typing import List, Tuple

from gensim.models import KeyedVectors
from gensim.models.keyedvectors import Word2VecKeyedVectors
from numpy import ndarray, zeros
from pythainlp.corpus import get_corpus_path
from pythainlp.tokenize import THAI2FIT_TOKENIZER, word_tokenize

WV_DIM = 300  # word vector dimension

_MODEL_NAME = "thai2fit_wv"

_TK_SP = "xxspace"
_TK_EOL = "xxeol"


class WordVector:
    """
    Word Vector class

    :param str model_name: model name

    **Options for model_name**
        * *thai2fit_wv* (default) - word vector from thai2fit
        * *ltw2v* - word vector from LTW2V: The Large Thai Word2Vec v0.1
        * *ltw2v_v1.0_15_window* - word vector from LTW2V v1.0 and 15 window
        * *ltw2v_v1.0_5_window* - word vector from LTW2V v1.0 and 5 window
    """

    def __init__(self, model_name: str = "thai2fit_wv") -> None:
        """
        Word Vector class

        :param str model_name: model name

        **Options for model_name**
            * *thai2fit_wv* (default) - word vector from thai2fit
            * *ltw2v* - word vector from LTW2V: The Large Thai Word2Vec
            * *ltw2v_v1.0_15_window* - word2vec from LTW2V 1.0 and 15 window
            * *ltw2v_v1.0_5_window* - word2vec from LTW2V v1.0 and 5 window
        """
        self.load_wordvector(model_name)

    def load_wordvector(self, model_name: str):
        """
        Load word vector model.

        :param str model_name: model name
        """
        self.model_name = model_name
        self.model = KeyedVectors.load_word2vec_format(
            get_corpus_path(self.model_name),
            binary=True,
            unicode_errors="ignore",
        )
        self.WV_DIM = self.model.vector_size

        if self.model_name == "thai2fit_wv":
            self.tokenize = THAI2FIT_TOKENIZER.word_tokenize
        else:
            self.tokenize = word_tokenize

    def get_model(self) -> Word2VecKeyedVectors:
        """
        Get word vector model.

        :return: `gensim` word2vec model
        :rtype: gensim.models.keyedvectors.Word2VecKeyedVectors
        """
        return self.model

    def doesnt_match(self, words: List[str]) -> str:
        """
        This function returns one word that is mostly unrelated to other words
        in the list. We use the function :func:`doesnt_match`
        from :mod:`gensim`.

        :param list words: a list of words
        :raises KeyError: if there is any word in `positive` or `negative` that is
                          not in the vocabulary of the model.
        :return: the word is that mostly unrelated
        :rtype: str

        :Note:
            * If a word in `words` is not in the vocabulary, :class:`KeyError`
              will be raised.

        :Example:
        Pick the word "พริกไทย" (name of food) out of the list of meals
        ("อาหารเช้า", "อาหารเที่ยง", "อาหารเย็น").
        >>> from pythainlp.word_vector import WordVector
        >>>
        >>> wv = WordVector()
        >>> words = ['อาหารเช้า', 'อาหารเที่ยง', 'อาหารเย็น', 'พริกไทย']
        >>> wv.doesnt_match(words)
        พริกไทย

        Pick the word "เรือ" (name of vehicle) out of the list of words
        related to occupation ("ดีไซน์เนอร์", "พนักงานเงินเดือน", "หมอ").

        >>> from pythainlp.word_vector import WordVector
        >>>
        >>> wv = WordVector()
        >>> words = ['ดีไซน์เนอร์', 'พนักงานเงินเดือน', 'หมอ', 'เรือ']
        >>> wv.doesnt_match(words)
        เรือ
        """
        return self.model.doesnt_match(words)

    def most_similar_cosmul(
        self, positive: List[str], negative: List[str]
    ) -> List[Tuple[str, float]]:
        """
        This function finds the top-10 words that are most similar with respect
        to two lists of words labeled as positive and negative.
        The top-10 most similar words are obtained using multiplication
        combination objective from Omer Levy and Yoav Goldberg
        [OmerLevy_YoavGoldberg_2014]_.

        We use the function :func:`gensim.most_similar_cosmul` directly from
        :mod:`gensim`.

        :param list positive: a list of words to add
        :param list negative: a list of words to subtract

        :raises KeyError: if there is any word in `positive` or `negative` that is
                          not in the vocabulary of the model.
        :return: list of top-10 most similar words and its similarity score
        :rtype:  list[tuple[str, float]]

        :Note:
            *  With a single word in the positive list, it will find the
               most similar words to the word given (similar
               to :func:`gensim.most_similar`)
            *  If a word in `positive` or `negative` is not in the vocabulary,
               :class:`KeyError` will be raised.

        :Example:

        Find the **top-10** most similar words to the word: "แม่น้ำ".

        >>> from pythainlp.word_vector import WordVector
        >>>
        >>> wv = WordVector()
        >>> list_positive = ['แม่น้ำ']
        >>> list_negative = []
        >>> wv.most_similar_cosmul(list_positive, list_negative)
        [('ลำน้ำ', 0.8206598162651062), ('ทะเลสาบ', 0.775945782661438),
        ('ลุ่มน้ำ', 0.7490593194961548), ('คลอง', 0.7471904754638672),
        ('ปากแม่น้ำ', 0.7354257106781006), ('ฝั่งแม่น้ำ', 0.7120099067687988),
        ('ทะเล', 0.7030453681945801), ('ริมแม่น้ำ', 0.7015200257301331),
        ('แหล่งน้ำ', 0.6997432112693787), ('ภูเขา', 0.6960948705673218)]

        Find the **top-10** most similar words to the words: "นายก",
        "รัฐมนตรี", and "ประเทศ".

        >>> from pythainlp.word_vector import WordVector
        >>>
        >>> wv = WordVector()
        >>> list_positive = ['นายก', 'รัฐมนตรี', 'ประเทศ']
        >>> list_negative = []
        >>> wv.most_similar_cosmul(list_positive, list_negative)
        [('รองนายกรัฐมนตรี', 0.2730445861816406),
        ('เอกอัครราชทูต', 0.26500266790390015),
        ('นายกรัฐมนตรี', 0.2649088203907013),
        ('ผู้ว่าราชการจังหวัด', 0.25119125843048096),
        ('ผู้ว่าการ', 0.2510434687137604), ('เลขาธิการ', 0.24824175238609314),
        ('ผู้ว่า', 0.2453523576259613), ('ประธานกรรมการ', 0.24147476255893707),
        ('รองประธาน', 0.24123257398605347), ('สมาชิกวุฒิสภา',
        0.2405330240726471)]

        Find the **top-10** most similar words when having **only** positive
        list and **both** positive and negative lists.

        >>> from pythainlp.word_vector import WordVector
        >>>
        >>> wv = WordVector()
        >>> list_positive = ['ประเทศ', 'ไทย', 'จีน', 'ญี่ปุ่น']
        >>> list_negative = []
        >>> wv.most_similar_cosmul(list_positive, list_negative)
        [('ประเทศจีน', 0.22022421658039093), ('เกาหลี', 0.2196873426437378),
        ('สหรัฐอเมริกา', 0.21660110354423523),
        ('ประเทศญี่ปุ่น', 0.21205860376358032),
        ('ประเทศไทย', 0.21159221231937408), ('เกาหลีใต้',
        0.20321202278137207),
        ('อังกฤษ', 0.19610872864723206), ('ฮ่องกง', 0.1928885132074356),
        ('ฝรั่งเศส', 0.18383873999118805), ('พม่า', 0.18369348347187042)]
        >>>
        >>> list_positive = ['ประเทศ', 'ไทย', 'จีน', 'ญี่ปุ่น']
        >>> list_negative = ['อเมริกา']
        >>> wv.most_similar_cosmul(list_positive, list_negative)
        [('ประเทศไทย', 0.3278159201145172), ('เกาหลี', 0.3201899230480194),
        ('ประเทศจีน', 0.31755179166793823), ('พม่า', 0.30845439434051514),
        ('ประเทศญี่ปุ่น', 0.306713730096817),
        ('เกาหลีใต้', 0.3003999888896942),
        ('ลาว', 0.2995176911354065), ('คนไทย', 0.2885020673274994),
        ('เวียดนาม', 0.2878379821777344), ('ชาวไทย', 0.28480708599090576)]

        The function returns :class:`KeyError` when the term "เมนูอาหารไทย"
        is not in the vocabulary.

        >>> from pythainlp.word_vector import WordVector
        >>>
        >>> wv = WordVector()
        >>> list_positive = ['เมนูอาหารไทย']
        >>> list_negative = []
        >>> wv.most_similar_cosmul(list_positive, list_negative)
        KeyError: "word 'เมนูอาหารไทย' not in vocabulary"
        """
        return self.model.most_similar_cosmul(
            positive=positive, negative=negative
        )

    def similarity(self, word1: str, word2: str) -> float:
        """
        This function computes cosine similarity between two words.

        :param str word1: first word to be compared with
        :param str word2: second word to be compared with

        :raises KeyError: if either `word1` or `word2` is not in the
                          vocabulary of the model.
        :return: the cosine similarity between the two word vectors
        :rtype: float

        :Note:
            *  If a word in `word1` or `word2` is not in the vocabulary,
               :class:`KeyError` will be raised.

        :Example:

        Compute consine similarity between two words: "รถไฟ" and "รถไฟฟ้า"
        (train and electric train).

        >>> from pythainlp.word_vector import WordVector
        >>> wv = WordVector()
        >>> wv.similarity('รถไฟ', 'รถไฟฟ้า')
        0.43387136


        Compute consine similarity between two words: "เสือดาว" and "รถไฟฟ้า"
        (leopard and electric train).

        >>> from pythainlp.word_vector import WordVector
        >>>
        >>> wv = WordVector()
        >>> wv.similarity('เสือดาว', 'รถไฟฟ้า')
        0.04300258

        """
        return self.model.similarity(word1, word2)

    def sentence_vectorizer(self, text: str, use_mean: bool = True) -> ndarray:
        """
        This function converts a Thai sentence into vector.
        Specifically, it first tokenizes that text and map each tokenized word
        with the word vectors from the model.
        Then, word vectors are aggregated into one vector of 300 dimension
        by calculating either mean or summation of all word vectors.

        :param str text: text input
        :param bool use_mean: if `True` aggregate word vectors with mean of all
                                 word vectors. Otherwise, aggregate with
                                 summation of all word vectors

        :return: 300-dimension vector representing the given sentence
                 in form of :mod:`numpy` array
        :rtype: :class:`numpy.ndarray((1,300))`


        :Example:

        Vectorize the sentence, "อ้วนเสี้ยวเข้ายึดแคว้นกิจิ๋ว ในปี พ.ศ. 735",
        into one sentence vector with two aggregation methods: mean
        and summation.

        >>> from pythainlp.word_vector import WordVector
        >>>
        >>> wv = WordVector()
        >>> sentence = 'อ้วนเสี้ยวเข้ายึดแคว้นกิจิ๋ว ในปี พ.ศ. 735'
        >>> wv.sentence_vectorizer(sentence, use_mean=True)
        array([[-0.00421414, -0.08881307,  0.05081136, -0.05632929,
             -0.06607185, 0.03059357, -0.113882  , -0.00074836,  0.05035743,
             0.02914307,
             ...
            0.02893357,  0.11327957,  0.04562086, -0.05015393,  0.11641257,
            0.32304936, -0.05054322,  0.03639471, -0.06531371,  0.05048079]])
        >>>
        >>> wv.sentence_vectorizer(sentence, use_mean=False)
        array([[-0.05899798, -1.24338295,  0.711359  , -0.78861002,
             -0.92500597, 0.42831   , -1.59434797, -0.01047703,  0.705004
            ,  0.40800299,
            ...
            0.40506999,  1.58591403,  0.63869202, -0.702155  ,  1.62977601,
            4.52269109, -0.70760502,  0.50952601, -0.914392  ,  0.70673105]])
        """
        vec = zeros((1, self.WV_DIM))

        words = self.tokenize(text)
        len_words = len(words)

        if not len_words:
            return vec

        for word in words:
            if word == " " and self.model_name == "thai2fit_wv":
                word = _TK_SP
            elif word == "\n" and self.model_name == "thai2fit_wv":
                word = _TK_EOL

            if word in self.model.index_to_key:
                vec += self.model.get_vector(word)

        if use_mean:
            vec /= len_words

        return vec
