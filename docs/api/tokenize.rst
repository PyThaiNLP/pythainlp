.. currentmodule:: pythainlp.tokenize
.. _tokenize-doc:

pythainlp.tokenize
=====================================
The :class:`pythainlp.tokenize` contains multiple functions for tokenizing a chunk of Thai text into desirable units.

Modules
-------

.. autofunction:: clause_tokenize
.. autofunction:: sent_tokenize
.. autofunction:: paragraph_tokenize
.. autofunction:: subword_tokenize
.. autofunction:: syllable_tokenize
.. autofunction:: word_tokenize
.. autofunction:: word_detokenize
.. autoclass:: Tokenizer
   :members:

Tokenization Engines
--------------------

Sentence level
--------------

crfcut
------
.. automodule::  pythainlp.tokenize.crfcut

thaisumcut
----------
.. automodule::  pythainlp.tokenize.thaisumcut

Word level
----------

attacut
+++++++
.. automodule::  pythainlp.tokenize.attacut

deepcut
+++++++
.. automodule::  pythainlp.tokenize.deepcut

multi_cut
+++++++++
.. automodule::  pythainlp.tokenize.multi_cut

nlpo3
+++++
.. automodule::  pythainlp.tokenize.nlpo3

longest
+++++++
.. automodule::  pythainlp.tokenize.longest

pyicu
+++++
.. automodule::  pythainlp.tokenize.pyicu

nercut
++++++
.. automodule::  pythainlp.tokenize.nercut

sefr_cut
++++++++
.. automodule::  pythainlp.tokenize.sefr_cut

oskut
+++++
.. automodule::  pythainlp.tokenize.oskut

newmm
+++++

The default word tokenization engine.

.. automodule::  pythainlp.tokenize.newmm


Subword level
-------------

tcc
+++
.. automodule:: pythainlp.tokenize.tcc

tcc+
++++
.. automodule:: pythainlp.tokenize.tcc_p

etcc
++++
.. automodule:: pythainlp.tokenize.etcc

han_solo
++++++++
.. automodule:: pythainlp.tokenize.han_solo