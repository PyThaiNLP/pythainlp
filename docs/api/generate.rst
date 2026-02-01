.. currentmodule:: pythainlp.generate

pythainlp.generate
==================

The :mod:`pythainlp.generate` module provides classes and functions for generating Thai text using n-gram and neural language models.

N-gram generators
-----------------

.. autoclass:: pythainlp.generate.Unigram
   :members:

.. autoclass:: pythainlp.generate.Bigram
   :members:

.. autoclass:: pythainlp.generate.Trigram
   :members:

Thai2fit helper
---------------

.. autofunction:: pythainlp.generate.thai2fit.gen_sentence
   :noindex:

WangChanLM
----------

.. autoclass:: pythainlp.generate.wangchanglm.WangChanGLM
   :members:

Usage
-----

Choose the generator class or function for the model you want, initialize it with appropriate parameters, and call its generation methods. Generated text can be used for chatbots, content generation, or data augmentation.

Example
-------

::
   from pythainlp.generate import Unigram

   unigram = Unigram()
   sentence = unigram.gen_sentence("สวัสดีครับ")
   print(sentence)
