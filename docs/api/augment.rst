.. currentmodule:: pythainlp.augment

pythainlp.augment Module
=======================

Introduction
------------

The `pythainlp.augment` module is a powerful toolset for text augmentation in the Thai language. Text augmentation is a process that enriches and diversifies textual data by generating alternative versions of the original text. This module is a valuable resource for improving the quality and variety of Thai language data for NLP tasks.

TextAugment Class
-----------------

The central component of the `pythainlp.augment` module is the `TextAugment` class. This class provides various text augmentation techniques and functions to enhance the diversity of your text data. It offers the following methods:

.. autoclass:: pythainlp.augment.TextAugment
   :members:

WordNetAug Class
----------------

The `WordNetAug` class is designed to perform text augmentation using WordNet, a lexical database for English. This class enables you to augment Thai text using English synonyms, offering a unique approach to text diversification. The following methods are available within this class:

.. autoclass:: pythainlp.augment.WordNetAug
   :members:

Word2VecAug, Thai2fitAug, LTW2VAug Classes
------------------------------------------

The `pythainlp.augment.word2vec` package contains multiple classes for text augmentation using Word2Vec models. These classes include `Word2VecAug`, `Thai2fitAug`, and `LTW2VAug`. Each of these classes allows you to use Word2Vec embeddings to generate text variations. Explore the methods provided by these classes to understand their capabilities.

.. autoclass:: pythainlp.augment.word2vec.Word2VecAug
   :members:

.. autoclass:: pythainlp.augment.word2vec.Thai2fitAug
   :members:

.. autoclass:: pythainlp.augment.word2vec.LTW2VAug
   :members:

FastTextAug and Thai2transformersAug Classes
--------------------------------------------

The `pythainlp.augment.lm` package offers classes for text augmentation using language models. These classes include `FastTextAug` and `Thai2transformersAug`. These classes allow you to use language model-based techniques to diversify text data. Explore their methods to understand their capabilities.

.. autoclass:: pythainlp.augment.lm.FastTextAug
   :members:

.. autoclass:: pythainlp.augment.lm.Thai2transformersAug
   :members:

BPEmbAug Class
--------------

The `pythainlp.augment.word2vec.bpemb_wv` package contains the `BPEmbAug` class, which is designed for text augmentation using subword embeddings. This class is particularly useful when working with subword representations for Thai text augmentation.

.. autoclass:: pythainlp.augment.word2vec.bpemb_wv.BPEmbAug
   :members:

Additional Functions
-------------------

To further enhance your text augmentation tasks, the `pythainlp.augment` module offers the following functions:

- `postype2wordnet`: This function maps part-of-speech tags to WordNet-compatible POS tags, facilitating the integration of WordNet augmentation with Thai text.

These functions and classes provide diverse techniques for text augmentation in the Thai language, making this module a valuable asset for NLP researchers, developers, and practitioners.

For detailed usage examples and guidelines, please refer to the official PyThaiNLP documentation. The `pythainlp.augment` module opens up new possibilities for enriching and diversifying Thai text data, leading to improved NLP models and applications.
