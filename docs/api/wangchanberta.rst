.. currentmodule:: pythainlp.wangchanberta

pythainlp.wangchanberta
=======================
The `pythainlp.wangchanberta` module is built upon the WangchanBERTa base model, specifically the `wangchanberta-base-att-spm-uncased` model, as detailed in the paper by Lowphansirikul et al. [^Lowphansirikul_2021].

This base model is utilized for various natural language processing tasks in the Thai language, including named entity recognition, part-of-speech tagging, and subword tokenization.

If you intend to fine-tune the model or explore its capabilities further, please refer to the [thai2transformers repository](https://github.com/vistec-AI/thai2transformers).

**Speed Benchmark**

============================= ======================== ==============
Function                      Named Entity Recognition Part of Speech
============================= ======================== ==============
PyThaiNLP basic function      89.7 ms                  312 ms
pythainlp.wangchanberta (CPU) 9.64 s                   9.65 s
pythainlp.wangchanberta (GPU) 8.02 s                   8 s
============================= ======================== ==============

For a comprehensive performance benchmark, the following notebooks are available:

-  `PyThaiNLP basic function and pythainlp.wangchanberta CPU at Google
   Colab`_
-  `pythainlp.wangchanberta GPU`_

.. _PyThaiNLP basic function and pythainlp.wangchanberta CPU at Google Colab: https://colab.research.google.com/drive/1ymTVB1UESXAyZlSpjknCb72xpdcZ86Db?usp=sharing
.. _pythainlp.wangchanberta GPU: https://colab.research.google.com/drive/1AtkFT1HMGL2GO7O2tM_hi_7mExKwmhMw?usp=sharing

Modules
-------
.. autoclass:: NamedEntityRecognition
   :members:

   The `NamedEntityRecognition` class is a fundamental component for identifying named entities in Thai text. It allows you to extract entities such as names, locations, and organizations from text data.

.. autoclass:: ThaiNameTagger
   :members:

   The `ThaiNameTagger` class is designed for tagging Thai names within text. This is essential for tasks such as entity recognition, information extraction, and text classification.

.. autofunction:: segment
   :noindex:

   The `segment` function is a subword tokenization tool that breaks down text into subword units, offering a foundation for further text processing and analysis.

References
----------

[^Lowphansirikul_2021] Lowphansirikul L, Polpanumas C, Jantrakulchai N, Nutanong S. WangchanBERTa: Pretraining transformer-based Thai Language Models. [ArXiv:2101.09635](http://arxiv.org/abs/2101.09635) [Internet]. 2021 Jan 23 [cited 2021 Feb 27].
