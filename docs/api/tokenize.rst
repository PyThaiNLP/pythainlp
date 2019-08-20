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

Tokenization Engines
--------------------

newmm
+++++
.. automodule::  pythainlp.tokenize.newmm
.. autofunction:: pythainlp.tokenize.newmm.segment


longest
+++++++
.. automodule::  pythainlp.tokenize.longest

multi_cut
+++++++++
.. automodule::  pythainlp.tokenize.multi_cut

pyicu
+++++
.. automodule::  pythainlp.tokenize.pyicu

deepcut
+++++++
.. automodule::  pythainlp.tokenize.deepcut

tcc
+++
.. automodule:: pythainlp.tokenize.tcc

.. autofunction:: pythainlp.tokenize.tcc.segment
.. autofunction:: pythainlp.tokenize.tcc.tcc
.. autofunction:: pythainlp.tokenize.tcc.tcc_pos

etcc
++++
.. automodule:: pythainlp.tokenize.etcc
