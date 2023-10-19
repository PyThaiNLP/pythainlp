.. currentmodule:: pythainlp.word_vector

pythainlp.word_vector
=======================
The :class:`word_vector` contains functions that makes use of a pre-trained vector public data.
The `pythainlp.word_vector` module is a valuable resource for working with pre-trained word vectors. These word vectors are trained on large corpora and can be used for various natural language processing tasks, such as word similarity, document similarity, and more.

Dependencies
=======================
Installation of :mod:`numpy` and :mod:`gensim` is required.

Before using this module, you need to ensure that the `numpy` and `gensim` libraries are installed in your environment. These libraries are essential for loading and working with the pre-trained word vectors.

Modules
-------
.. autofunction:: doesnt_match
   :noindex:

   The `doesnt_match` function is designed to identify the word that does not match a set of words in terms of semantic similarity. It is useful for tasks like word sense disambiguation.

.. autofunction:: get_model
   :noindex:

   The `get_model` function allows you to load a pre-trained word vector model, which can then be used for various word vector operations. This function serves as the entry point for accessing pre-trained word vectors.

.. autofunction:: most_similar_cosmul
   :noindex:

   The `most_similar_cosmul` function finds words that are most similar to a given word in terms of cosine similarity. This function is useful for word analogy tasks and word similarity measurement.

.. autofunction:: sentence_vectorizer
   :noindex:

   The `sentence_vectorizer` function takes a sentence as input and returns a vector representation of the entire sentence based on word vectors. This is valuable for document similarity and text classification tasks.

.. autofunction:: similarity
   :noindex:

   The `similarity` function calculates the cosine similarity between two words based on their word vectors. It helps in measuring the semantic similarity between words.

.. autoclass:: WordVector
   :members:

   The `WordVector` class encapsulates word vector operations and functions. It provides a convenient interface for loading models, finding word similarities, and generating sentence vectors.

References
----------

-  [Omer Levy and Yoav Goldberg (2014). Linguistic Regularities in Sparse and Explicit Word Representations](https://www.aclweb.org/anthology/W14-1618/)
   This reference points to the work by Omer Levy and Yoav Goldberg, which discusses linguistic regularities in word representations. It underlines the theoretical foundation of word vectors and their applications in NLP.

This enhanced documentation provides a more detailed and organized overview of the `pythainlp.word_vector` module, making it a valuable resource for NLP practitioners and researchers working with pre-trained word vectors in the Thai language.
