.. currentmodule:: pythainlp.tokenize
.. _tokenize-doc:

pythainlp.tokenize
=====================================
The :class:`pythainlp.tokenize` contains multiple functions for tokenizing a chunk of Thai text into desirable units.

Modules
-------

.. autofunction:: sent_tokenize
.. autofunction:: word_tokenize
.. autofunction:: syllable_tokenize
.. autofunction:: subword_tokenize
.. autofunction:: dict_trie
.. autoclass:: Tokenizer
   :members:

NEWMM
-----
.. autofunction:: pythainlp.tokenize.newmm.segment

TCC
---
Thai Character Cluster

.. autofunction:: pythainlp.tokenize.tcc.segment
.. autofunction:: pythainlp.tokenize.tcc.tcc
.. autofunction:: pythainlp.tokenize.tcc.tcc_pos
