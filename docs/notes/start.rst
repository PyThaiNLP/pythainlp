Getting started
===============

PyThaiNLP is a Python library for Thai natural language processing (NLP). With this package you can perform common NLP tasks such as text classification and tokenization.

**Tokenization example**::

    from pythainlp.tokenize import word_tokenize

    text = "โอเคบ่เรารักภาษาถิ่น"
    word_tokenize(text, engine="newmm")  # ['โอเค', 'บ่', 'เรา', 'รัก', 'ภาษาถิ่น']
    word_tokenize(text, engine="icu")    # ['โอ', 'เค', 'บ่', 'เรา', 'รัก', 'ภาษา', 'ถิ่น']

Thai NLP faces several challenges. A brief list includes:

#. **Sentence boundary detection** — This is one of the biggest challenges in Thai NLP. The lack of explicit end-of-sentence markers makes it difficult to create training sets for many tasks. The issue is twofold: (1) in the writing system, Thai punctuation and spacing do not always indicate sentence endings; (2) in language use, sentences often begin with conjunctions such as 'because' or 'but', which can make sentence boundaries ambiguous even for native speakers.

#. **Word segmentation** — Thai does not use spaces to separate words, so segmentation is challenging. Solving it often requires understanding context to rule out unlikely word breaks. This is similar to issues in other Asian languages such as Japanese and Chinese. Recently, techniques that represent words, subwords, and characters as vectors (embeddings) have improved performance and help address this problem.

Tutorial notebooks
==================
- `PyThaiNLP Get Started <https://pythainlp.org/tutorials/notebooks/pythainlp_get_started.html>`_
- `Other tutorials <https://pythainlp.org/tutorials/>`_
