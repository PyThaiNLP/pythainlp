.. currentmodule:: pythainlp.wangchanberta

pythainlp.wangchanberta
=======================

WangchanBERTa base model: wangchanberta-base-att-spm-uncased [#Lowphansirikul_2021]_

We used WangchanBERTa for Thai name tagger task, part-of-speech and subword tokenizer.

If you want to finetune model, You can read https://github.com/vistec-AI/thai2transformers

**Speed Benchmark**

============================= ======================== ==============
Function                      Named Entity Recognition Part of Speech
============================= ======================== ==============
PyThaiNLP basic function      89.7 ms                  312 ms
pythainlp.wangchanberta (CPU) 9.64 s                   9.65 s
pythainlp.wangchanberta (GPU) 8.02 s                   8 s
============================= ======================== ==============

Notebook:

-  `PyThaiNLP basic function and pythainlp.wangchanberta CPU at Google
   Colab`_
-  `pythainlp.wangchanberta GPU`_

.. _PyThaiNLP basic function and pythainlp.wangchanberta CPU at Google Colab: https://colab.research.google.com/drive/1ymTVB1UESXAyZlSpjknCb72xpdcZ86Db?usp=sharing
.. _pythainlp.wangchanberta GPU: https://colab.research.google.com/drive/1AtkFT1HMGL2GO7O2tM_hi_7mExKwmhMw?usp=sharing

Modules
-------
.. autofunction:: segment

References
----------

.. [#Lowphansirikul_2021] Lowphansirikul L, Polpanumas C, Jantrakulchai N, Nutanong S.
            WangchanBERTa: Pretraining transformer-based Thai Language Models.
            arXiv:210109635 [cs] [Internet]. 2021 Jan 23 [cited 2021 Feb 27];
            Available from: http://arxiv.org/abs/2101.09635
