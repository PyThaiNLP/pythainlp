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

newmm
+++++
.. automodule::  pythainlp.tokenize.newmm

.. autofunction:: pythainlp.tokenize.newmm.segment


longest
+++++++
.. automodule::  pythainlp.tokenize.longest

.. autofunction:: pythainlp.tokenize.longest.segment

multi_cut
+++++++++
.. automodule::  pythainlp.tokenize.multi_cut

.. autofunction:: pythainlp.tokenize.multi_cut.segment
.. autofunction:: pythainlp.tokenize.multi_cut.find_all_segment

pyicu
+++++
.. automodule::  pythainlp.tokenize.pyicu

deepcut
+++++++
.. automodule::  pythainlp.tokenize.deepcut

attacut
+++++++
.. automodule::  pythainlp.tokenize.attacut

nercut
++++++
.. automodule::  pythainlp.tokenize.nercut

.. autofunction:: pythainlp.tokenize.nercut.segment

tcc
+++
.. automodule:: pythainlp.tokenize.tcc

.. autofunction:: pythainlp.tokenize.tcc.segment
.. autofunction:: pythainlp.tokenize.tcc.tcc
.. autofunction:: pythainlp.tokenize.tcc.tcc_pos

etcc
++++
.. automodule:: pythainlp.tokenize.etcc
