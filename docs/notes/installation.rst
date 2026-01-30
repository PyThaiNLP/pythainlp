Installation
============

Stable release::

    pip install pythainlp

Development (pre-release) version::

    pip install --upgrade --pre pythainlp

Some features (for example, named entity recognition) require additional optional dependencies. Install them using the extras syntax:

    pip install pythainlp[extra1,extra2,...]

The extras can include:
  - ``attacut`` — support for AttaCut (a fast and accurate tokenizer)
  - ``benchmarks`` — support for running benchmarks
  - ``icu`` — support for ICU (International Components for Unicode) used in transliteration and tokenization
  - ``ipa`` — support for IPA (International Phonetic Alphabet) in transliteration
  - ``ml`` — support for ULMFiT models used in classification
  - ``ssg`` — support for SSG (syllable tokenizer)
  - ``thai2fit`` — Thai word vectors (thai2fit)
  - ``thai2rom`` — machine-learned romanization
  - ``translate`` — translation support
  - ``wangchanberta`` — WangchanBERTa models
  - ``mt5`` — mT5 models for Thai text summarization
  - ``wordnet`` — WordNet support
  - ``spell`` — support for spell-checkers (phunspell & symspellpy)
  - ``generate`` — support for text generation (ULMFiT or thai2fit)
  - ``textaugment`` — text augmentation utilities
  - ``oskut`` — OSKUT support
  - ``nlpo3`` — NLPO3 engine support
  - ``spacy_thai`` — spaCy Thai tokenizer integration
  - ``esupar`` — ESuPAR support
  - ``transformers_ud`` — transformers_ud engine support
  - ``dependency_parsing`` — dependency parsing engines
  - ``coreference_resolution`` — coreference resolution engines
  - ``wangchanglm`` — WangchangLM model support
  - ``wsd`` — word-sense disambiguation support (pythainlp.wsd)
  - ``el`` — EL support (pythainlp.el)
  - ``abbreviation`` — abbreviation expansion utilities
  - ``full`` — install all optional dependencies

For dependency details, see the `extras` variable in `setup.py <https://github.com/PyThaiNLP/pythainlp/blob/dev/setup.py>`_.

Notes for Windows installation
-----------------------------

Some features require the `PyICU` libraries on Windows. You have two options to install them.

Option 1 (recommended):

  - Download a pre-built wheel from https://www.lfd.uci.edu/~gohlke/pythonlibs/
  - Choose a wheel that matches your Python version and architecture ("win32" or "amd64").
  - Install it with pip, for example::

      pip install PyICU-xxx-cp36-cp36m-win32.whl

Option 2 (advanced):

  - Attempt to build from source using::

      pip install pyicu

  - Building from source requires development toolchains (for example Microsoft Visual C++ Build Tools) and may require setting environment variables such as ``ICU_VERSION``. For example::

      set ICU_VERSION=62.1

  - Building from source takes longer and requires technical knowledge, but produces a wheel optimized for your system.

Runtime configurations
----------------------

.. envvar:: PYTHAINLP_DATA_DIR

   Specifies the location where downloaded data and the corpus database are stored. If the directory does not exist, PyThaiNLP will create it.

   By default this is a directory named ``pythainlp-data`` in the user's home directory.

   Run ``thainlp data path`` at the command line to display the current `PYTHAINLP_DATA_DIR`.

.. envvar:: PYTHAINLP_READ_MODE

   Configures PyThaiNLP to operate in read-only mode (0 = False, 1 = True).

FAQ
===

Q: How do I set environment variables on each executor node in a distributed environment?

A: See the discussion in `PermissionError: [Errno 13] Permission denied: /home/pythainlp-data <https://github.com/PyThaiNLP/pythainlp/issues/475>`_.

Q: How do I enable read-only mode for PyThaiNLP?

A: Set the environment variable `PYTHAINLP_READ_MODE` to ``1``.
