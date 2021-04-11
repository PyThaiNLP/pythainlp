.. currentmodule:: pythainlp.tokenize
.. _tokenize-doc:

pythainlp.tokenize
=====================================
The :class:`pythainlp.tokenize` contains multiple functions for tokenizing a chunk of Thai text into desirable units.

Modules
-------

.. autofunction:: clause_tokenize
.. autofunction:: sent_tokenize
.. autofunction:: subword_tokenize
.. autofunction:: syllable_tokenize
.. autofunction:: word_tokenize
.. autoclass:: Tokenizer
   :members:

Tokenization Engines
--------------------

Sentence level
--------------

crfcut
------
.. automodule::  pythainlp.tokenize.crfcut

.. autofunction::  pythainlp.tokenize.crfcut.extract_features
.. autofunction::  pythainlp.tokenize.crfcut.segment

Word level
----------

attacut
+++++++
.. automodule::  pythainlp.tokenize.attacut

.. autoclass:: pythainlp.tokenize.attacut.AttacutTokenizer
   :members:

deepcut
+++++++
.. automodule::  pythainlp.tokenize.deepcut

multi_cut
+++++++++
.. automodule::  pythainlp.tokenize.multi_cut

.. autofunction:: pythainlp.tokenize.multi_cut.segment
.. autofunction:: pythainlp.tokenize.multi_cut.find_all_segment

longest
+++++++
.. automodule::  pythainlp.tokenize.longest

.. autofunction:: pythainlp.tokenize.longest.segment

pyicu
+++++
.. automodule::  pythainlp.tokenize.pyicu

nercut
++++++
.. automodule::  pythainlp.tokenize.nercut

.. autofunction:: pythainlp.tokenize.nercut.segment

newmm
+++++

The default word tokenization engine.

.. automodule::  pythainlp.tokenize.newmm

.. autofunction:: pythainlp.tokenize.newmm.segment

Subword level
-------------

tcc
+++
.. automodule:: pythainlp.tokenize.tcc

.. autofunction:: pythainlp.tokenize.tcc.segment
.. autofunction:: pythainlp.tokenize.tcc.tcc
.. autofunction:: pythainlp.tokenize.tcc.tcc_pos

etcc
++++
.. automodule:: pythainlp.tokenize.etcc

.. autofunction:: pythainlp.tokenize.etcc.segment