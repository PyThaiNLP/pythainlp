Installation
============

Stable release::

    pip install pythainlp

Development (pre-release) version::

    pip install --upgrade --pre pythainlp

Some features (for example, named entity recognition) require additional optional dependencies. Install them using the `extras` syntax:

    pip install pythainlp[extra1,extra2,...]

The extras can include:
  - ``compact`` — install a stable and small subset of dependencies (recommended)
  - ``full`` — install all optional dependencies (may introduce large dependencies and conflicts)
  - ``abbreviation`` — abbreviation expansion utilities
  - ``attacut`` — support for AttaCut (a fast and accurate tokenizer)
  - ``budoux`` — support for BudouX text segmentation
  - ``benchmarks`` — support for running benchmarks
  - ``coreference_resolution`` — coreference resolution support
  - ``dependency_parsing`` — dependency parsing support
  - ``el`` — entity linking support
  - ``esupar`` — ESuPAR parser support
  - ``generate`` — support for text generation
  - ``icu`` — support for ICU (International Components for Unicode) used in transliteration and tokenization
  - ``ipa`` — support for IPA (International Phonetic Alphabet) in transliteration
  - ``ml`` — support for ULMFiT models used in classification
  - ``mt5`` — mT5 models for Thai text summarization
  - ``nlpo3`` — nlpo3 Thai word tokenization support
  - ``onnx`` - ONNX model support
  - ``oskut`` — OSKUT support
  - ``sefr_cut`` — SEFR CUT Thai word tokenization support
  - ``spacy_thai`` — spaCy Thai language support
  - ``spell`` — support for more spell-checkers (phunspell & symspellpy)
  - ``ssg`` — support for SSG syllable tokenizer
  - ``textaugment`` — text augmentation utilities
  - ``thai_nner`` — Thai named entity recognition support
  - ``thai2fit`` — Thai word vectors (thai2fit)
  - ``thai2rom`` — machine-learned romanization
  - ``transformers_ud`` — transformers_ud engine support
  - ``translate`` — machine translation support
  - ``wangchanberta`` — WangchanBERTa models
  - ``wangchanglm`` — WangchangLM model support
  - ``word_approximation`` — word approximation support
  - ``wordnet`` — WordNet support
  - ``wsd`` — word-sense disambiguation support (pythainlp.wsd)
  - ``wtp`` — Where's the Point text segmentation support
  - ``wunsen`` — Wunsen spell checker support

For dependency details, see the `project.optional-dependencies` section in `pyproject.toml <https://github.com/PyThaiNLP/pythainlp/blob/dev/pyproject.toml>`_.

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

Using PyThaiNLP in distributed environments
-------------------------------------------

PyThaiNLP can be used in distributed computing environments such as Apache Spark. When using PyThaiNLP in these environments, you need to configure the data directory for each worker node.

Key considerations
~~~~~~~~~~~~~~~~~~

1. **Set environment variables inside distributed functions**: Environment variables must be set inside the function that will be distributed to executor nodes, not in the driver program.

2. **Use a writable local directory**: The default data directory (``~/pythainlp-data``) may not be writable on executor nodes. Use a local directory like ``./pythainlp-data`` instead.

3. **Set ``PYTHAINLP_DATA`` before data access**: Always set the ``PYTHAINLP_DATA`` environment variable before the first call that reads or writes PyThaiNLP data on each worker.
   (``PYTHAINLP_DATA_DIR`` is also accepted for backward compatibility but is deprecated.)

Example usage with Apache Spark
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Basic example using PySpark RDD::

    from pyspark import SparkContext

    sc = SparkContext("local[*]", "PyThaiNLP Example")
    thai_texts = ["สวัสดีครับ", "ภาษาไทย"]
    rdd = sc.parallelize(thai_texts)

    def tokenize_thai(text):
        import os
        os.environ['PYTHAINLP_DATA'] = './pythainlp-data'
        from pythainlp.tokenize import word_tokenize
        return word_tokenize(text)

    tokenized_rdd = rdd.map(tokenize_thai)
    results = tokenized_rdd.collect()

Example using PySpark DataFrame API::

    from pyspark.sql import SparkSession
    from pyspark.sql.functions import udf
    from pyspark.sql.types import ArrayType, StringType

    spark = SparkSession.builder.appName("PyThaiNLP").getOrCreate()
    df = spark.createDataFrame([(1, "สวัสดีครับ")], ["id", "text"])

    @udf(returnType=ArrayType(StringType()))
    def tokenize_udf(text):
        import os
        os.environ['PYTHAINLP_DATA'] = './pythainlp-data'
        from pythainlp.tokenize import word_tokenize
        return word_tokenize(text)

    result_df = df.withColumn("tokens", tokenize_udf(df.text))

For more comprehensive examples including error handling, production best practices, and advanced features, see the file ``examples/distributed_pyspark.py`` in the PyThaiNLP repository.

Thread safety considerations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PyThaiNLP's core tokenization engines are thread-safe, which is important for distributed computing environments where multiple threads may process data concurrently. For detailed information about thread safety guarantees and best practices, see :doc:`threadsafe`.

Note that while the code itself is thread-safe, you still need to configure the data directory appropriately for distributed environments as described above.

Runtime configurations
----------------------

.. envvar:: PYTHAINLP_DATA

   Specifies the location where downloaded data and the corpus database are stored. If the directory does not exist, PyThaiNLP will create it.

   By default this is a directory named ``pythainlp-data`` in the user's home directory.

   Run ``thainlp data path`` at the command line to display the current data directory.

.. envvar:: PYTHAINLP_DATA_DIR

   .. deprecated::
      Use :envvar:`PYTHAINLP_DATA` instead. Setting ``PYTHAINLP_DATA_DIR`` triggers a
      :class:`DeprecationWarning` at runtime. If both ``PYTHAINLP_DATA`` and ``PYTHAINLP_DATA_DIR``
      are set simultaneously, PyThaiNLP raises :exc:`ValueError`.

.. envvar:: PYTHAINLP_OFFLINE

   When set to a truthy value (``1``, ``true``, ``yes``, ``on``), PyThaiNLP operates in
   *offline mode*: corpus downloads are disabled, and :func:`pythainlp.corpus.get_corpus_path`
   raises :exc:`FileNotFoundError` for any corpus that is not already cached locally.

   Use :func:`pythainlp.is_offline_mode` to check the current state programmatically.

   This follows the same convention as ``HF_HUB_OFFLINE`` in `huggingface_hub`.

.. envvar:: PYTHAINLP_READ_MODE

   Configures PyThaiNLP to operate in read-only mode (0 = False, 1 = True).

Installation FAQ
----------------

Q: How do I set environment variables on each executor node in a distributed environment?

A: When using PyThaiNLP in distributed computing environments like Apache Spark, you need to set the ``PYTHAINLP_DATA`` environment variable inside the function that will be distributed to executor nodes. For example::

    def tokenize_thai(text):
        import os
        os.environ['PYTHAINLP_DATA'] = './pythainlp-data'
        from pythainlp.tokenize import word_tokenize
        return word_tokenize(text)

    rdd.map(tokenize_thai)

This ensures that each executor node uses a local data directory instead of the default home directory, which may not be writable on executor nodes.

For detailed examples including PySpark DataFrame API and production best practices, see ``examples/distributed_pyspark.py``.

For more discussion, see `PermissionError: [Errno 13] Permission denied: /home/pythainlp-data <https://github.com/PyThaiNLP/pythainlp/issues/475>`_.

Q: How do I enable read-only mode for PyThaiNLP?

A: Set the environment variable ``PYTHAINLP_READ_MODE`` to ``1``.
