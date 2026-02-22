.. currentmodule:: pythainlp.benchmarks

pythainlp.benchmarks
====================

Introduction
------------

The `pythainlp.benchmarks` module is a collection of utility functions designed for benchmarking tasks related to Thai Natural Language Processing (NLP). The module includes tools for word tokenization benchmarking and evaluation metrics for text generation tasks (BLEU and ROUGE).

Tokenization
------------

Word tokenization is a fundamental task in NLP, and it plays a crucial role in various applications, such as text analysis and language processing. The `pythainlp.benchmarks` module offers a set of functions to assist in the benchmarking and evaluation of word tokenization methods.

Quality Evaluation
^^^^^^^^^^^^^^^^^^

The quality of word tokenization can significantly impact the accuracy of downstream NLP tasks. To assess the quality of word tokenization, the module provides a qualitative evaluation using various metrics and techniques.

.. figure:: ../images/evaluation.png
   :scale: 50 %

   Qualitative evaluation of word tokenization.

Tokenization Functions
^^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: pythainlp.benchmarks.word_tokenization.compute_stats

    This function is used to compute various statistics and metrics related to word tokenization. It allows you to assess the performance of different tokenization methods.

.. autofunction:: pythainlp.benchmarks.word_tokenization.benchmark

    The `benchmark` function facilitates the benchmarking of word tokenization methods. It provides an organized framework for evaluating and comparing the effectiveness of different tokenization tools.

.. autofunction:: pythainlp.benchmarks.word_tokenization.preprocessing

    Preprocessing is a crucial step in NLP tasks. The `preprocessing` function assists in preparing text data for tokenization, which is essential for accurate and consistent benchmarking.

Evaluation Metrics
------------------

The module provides pure Python implementations of common evaluation metrics (BLEU and ROUGE) that automatically handle Thai text tokenization. These metrics are essential for evaluating machine translation, text summarization, and other text generation tasks.

BLEU Score
^^^^^^^^^^

BLEU (Bilingual Evaluation Understudy) is a metric for evaluating the quality of machine-translated text. It compares the generated text against one or more reference translations by measuring n-gram precision with a brevity penalty.

.. autofunction:: pythainlp.benchmarks.bleu_score

**Example:**

.. code-block:: python

    from pythainlp.benchmarks import bleu_score

    # Single reference
    references = ["สวัสดีครับ วันนี้อากาศดีมาก"]
    hypotheses = ["สวัสดีค่ะ วันนี้อากาศดี"]
    score = bleu_score(references, hypotheses)
    print(f"BLEU: {score['bleu']:.2f}")
    
    # Multiple references per hypothesis
    references = [
        ["สวัสดีครับ", "สวัสดีค่ะ"],
        ["ลาก่อนครับ", "ลาก่อนค่ะ"],
    ]
    hypotheses = ["สวัสดี", "ลาก่อน"]
    score = bleu_score(references, hypotheses)
    print(f"BLEU: {score['bleu']:.2f}")

ROUGE Score
^^^^^^^^^^^

ROUGE (Recall-Oriented Understudy for Gisting Evaluation) is a set of metrics for evaluating automatic summarization and machine translation. It measures the overlap between the generated text and reference text(s).

.. autofunction:: pythainlp.benchmarks.rouge_score

**Example:**

.. code-block:: python

    from pythainlp.benchmarks import rouge_score

    reference = "สวัสดีครับ วันนี้อากาศดีมาก"
    hypothesis = "สวัสดีค่ะ วันนี้อากาศดี"
    scores = rouge_score(reference, hypothesis)
    
    for rouge_type, (precision, recall, fmeasure) in scores.items():
        print(f"{rouge_type}: P={precision:.4f}, R={recall:.4f}, F={fmeasure:.4f}")

Word Error Rate (WER)
^^^^^^^^^^^^^^^^^^^^^

Word Error Rate is a common metric for evaluating speech recognition and machine translation systems. It measures the minimum number of word-level edits (insertions, deletions, substitutions) needed to transform the hypothesis into the reference.

.. autofunction:: pythainlp.benchmarks.word_error_rate

**Example:**

.. code-block:: python

    from pythainlp.benchmarks import word_error_rate

    reference = "สวัสดีครับ วันนี้อากาศดีมาก"
    hypothesis = "สวัสดีค่ะ วันนี้อากาศดี"
    wer = word_error_rate(reference, hypothesis)
    print(f"WER: {wer:.4f}")

Character Error Rate (CER)
^^^^^^^^^^^^^^^^^^^^^^^^^^

Character Error Rate is a metric for evaluating speech recognition and optical character recognition (OCR) systems. It measures the minimum number of character-level edits (insertions, deletions, substitutions) needed to transform the hypothesis into the reference.

.. autofunction:: pythainlp.benchmarks.character_error_rate

**Example:**

.. code-block:: python

    from pythainlp.benchmarks import character_error_rate

    reference = "สวัสดีครับ"
    hypothesis = "สวัสดีค่ะ"
    cer = character_error_rate(reference, hypothesis)
    print(f"CER: {cer:.4f}")

Usage
-----

To make use of these benchmarking functions, you can follow the provided examples and guidelines in the official PyThaiNLP documentation. These tools are invaluable for researchers, developers, and anyone interested in improving and evaluating Thai word tokenization methods and text generation systems.
