.. currentmodule:: pythainlp.benchmarks

pythainlp.benchmarks
====================================
The :class:`pythainlp.benchmarks` contains utility functions for benchmarking
tasked related to Thai NLP. At the moment, we have only for word tokenization.
Other tasks will be added soon.

Modules
-------

Tokenization
*********

Quality
^^^^
.. figure:: ../images/evaluation.png
   :scale: 50 %

   Qualitative evaluation of word tokenization.

.. autofunction:: pythainlp.benchmarks.word_tokenization.compute_stats
.. autofunction:: pythainlp.benchmarks.word_tokenization.benchmark
.. autofunction:: pythainlp.benchmarks.word_tokenization.preprocessing
