.. currentmodule:: pythainlp.wangchanberta

pythainlp.wangchanberta
=======================

WangchanBERTa base model: wangchanberta-base-att-spm-uncased [#Lowphansirikul_2021]_

We used WangchanBERTa for Thai name tagger task, part-of-speech and subword tokenizer.

**Speed Benchmark**

+-------------------------+-------------------------+----------------+
| Function                | Named Entity            | Part of Speech |
|                         | Recognition             |                |
+=========================+=========================+================+
| PyThaiNLP basic         | 89.7 ms                 | 312 ms         |
| function (CRF for NER   |                         |                |
| and perceptron model    |                         |                |
| for POS)                |                         |                |
+-------------------------+-------------------------+----------------+
| pythainlp.wangchanberta | 9.64 s                  | 9.65 s         |
| (CPU)                   |                         |                |
+-------------------------+-------------------------+----------------+
| pythainlp.wangchanberta | 8.02 s                  | 8 s            |
| (GPU)                   |                         |                |
+-------------------------+-------------------------+----------------+

Notebook:

-  `PyThaiNLP basic function and pythainlp.wangchanberta CPU at Google
   Colab`_
-  `pythainlp.wangchanberta GPU`_

.. _PyThaiNLP basic function and pythainlp.wangchanberta CPU at Google Colab: https://colab.research.google.com/drive/1ymTVB1UESXAyZlSpjknCb72xpdcZ86Db?usp=sharing
.. _pythainlp.wangchanberta GPU: https://colab.research.google.com/drive/1AtkFT1HMGL2GO7O2tM_hi_7mExKwmhMw?usp=sharing

Modules
-------
.. autoclass:: ThaiNameTagger
.. autofunction:: pos_tag
.. autofunction:: segment

References
----------

.. [#Lowphansirikul_2021] Lowphansirikul L, Polpanumas C, Jantrakulchai N, Nutanong S.
            WangchanBERTa: Pretraining transformer-based Thai Language Models.
            arXiv:210109635 [cs] [Internet]. 2021 Jan 23 [cited 2021 Feb 27];
            Available from: http://arxiv.org/abs/2101.09635
