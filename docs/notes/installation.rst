Installation
============

Stable release::

    pip install pythainlp

Development (pre-release) version::

    pip install --upgrade --pre pythainlp

Some features (for example, named entity recognition) require additional optional dependencies. Install them using the `extras` syntax:

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

3. **Set ``PYTHAINLP_DATA_DIR`` before data access**: Always set the ``PYTHAINLP_DATA_DIR`` environment variable before the first call that reads or writes PyThaiNLP data on each worker.

Example usage with Apache Spark
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Basic example using PySpark RDD::

    from pyspark import SparkContext

    sc = SparkContext("local[*]", "PyThaiNLP Example")
    thai_texts = ["สวัสดีครับ", "ภาษาไทย"]
    rdd = sc.parallelize(thai_texts)

    def tokenize_thai(text):
        import os
        os.environ['PYTHAINLP_DATA_DIR'] = './pythainlp-data'
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
        os.environ['PYTHAINLP_DATA_DIR'] = './pythainlp-data'
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

.. envvar:: PYTHAINLP_DATA_DIR

   Specifies the location where downloaded data and the corpus database are stored. If the directory does not exist, PyThaiNLP will create it.

   By default this is a directory named ``pythainlp-data`` in the user's home directory.

   Run ``thainlp data path`` at the command line to display the current `PYTHAINLP_DATA_DIR`.

.. envvar:: PYTHAINLP_READ_MODE

   Configures PyThaiNLP to operate in read-only mode (0 = False, 1 = True).

Installation FAQ
----------------

Q: How do I set environment variables on each executor node in a distributed environment?

A: When using PyThaiNLP in distributed computing environments like Apache Spark, you need to set the ``PYTHAINLP_DATA_DIR`` environment variable inside the function that will be distributed to executor nodes. For example::

    def tokenize_thai(text):
        import os
        os.environ['PYTHAINLP_DATA_DIR'] = './pythainlp-data'
        from pythainlp.tokenize import word_tokenize
        return word_tokenize(text)

    rdd.map(tokenize_thai)

This ensures that each executor node uses a local data directory instead of the default home directory, which may not be writable on executor nodes.

For detailed examples including PySpark DataFrame API and production best practices, see ``examples/distributed_pyspark.py``.

For more discussion, see `PermissionError: [Errno 13] Permission denied: /home/pythainlp-data <https://github.com/PyThaiNLP/pythainlp/issues/475>`_.

Q: How do I enable read-only mode for PyThaiNLP?

A: Set the environment variable ``PYTHAINLP_READ_MODE`` to ``1``.
