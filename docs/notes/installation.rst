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
   *offline mode*: automatic corpus downloads are disabled, and
   :func:`pythainlp.corpus.get_corpus_path` raises :exc:`FileNotFoundError`
   for any corpus that is not already cached locally.

   Explicit calls to :func:`pythainlp.corpus.download` or ``thainlp data get``
   still work normally, because those are deliberate user actions.

   Use :func:`pythainlp.is_offline_mode` to check the current state programmatically.

   This follows the same convention as ``HF_HUB_OFFLINE`` in `huggingface_hub`.

.. envvar:: PYTHAINLP_READ_ONLY

   When set to a truthy value (``1``, ``true``, ``yes``, ``on``), PyThaiNLP operates in
   *read-only mode*: implicit background writes to PyThaiNLP's internal data directory
   are disabled.

   **What read-only mode blocks** (implicit writes the user may not be aware of):

   - Creating the PyThaiNLP data directory (``~/pythainlp-data`` or
     as configured by :envvar:`PYTHAINLP_DATA`).
   - :func:`pythainlp.corpus.download` — corpus file downloads and catalog
     (``db.json``) updates.
   - :func:`pythainlp.corpus.remove` — corpus file and catalog deletions.

   **What read-only mode does NOT block** (explicit user-initiated writes):

   - Saving trained models or vocabularies to a user-specified path
     (e.g., ``model.save("my_model.json")``, ``tagger.train(..., save_loc="...")``,
     ``tokenizer.save_vocabulary("my_dir/")``) — the user explicitly provided the
     destination path.
   - CLI output files written to a user-specified location
     (e.g., ``thainlp benchmark --save-details``,
     ``thainlp misspell --output myfile.txt``).

   Use :func:`pythainlp.is_read_only_mode` to check the current state programmatically.

   .. note::
      To disable only *automatic* background downloads while keeping explicit
      ``download()`` calls working, use :envvar:`PYTHAINLP_OFFLINE` instead.

   If both :envvar:`PYTHAINLP_READ_ONLY` and :envvar:`PYTHAINLP_READ_MODE` are set at the
   same time, PyThaiNLP raises :exc:`ValueError`.

.. envvar:: PYTHAINLP_READ_MODE

   .. deprecated::
      Use :envvar:`PYTHAINLP_READ_ONLY` instead. Setting ``PYTHAINLP_READ_MODE`` triggers a
      :class:`DeprecationWarning` at runtime. If both ``PYTHAINLP_READ_ONLY`` and
      ``PYTHAINLP_READ_MODE`` are set simultaneously, PyThaiNLP raises :exc:`ValueError`.

      ``PYTHAINLP_READ_MODE=1`` is equivalent to ``PYTHAINLP_READ_ONLY=1``.

Interaction between environment variables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The table below shows how :envvar:`PYTHAINLP_OFFLINE` and :envvar:`PYTHAINLP_READ_ONLY`
affect the two main corpus operations:

.. list-table::
   :header-rows: 1
   :widths: 35 32 33

   * - Operation
     - ``PYTHAINLP_OFFLINE=1``
     - ``PYTHAINLP_READ_ONLY=1``
   * - :func:`pythainlp.corpus.get_corpus_path` — corpus already cached locally
     - Succeeds (returns path)
     - Succeeds (no write needed)
   * - :func:`pythainlp.corpus.get_corpus_path` — corpus **not** cached locally
     - Fails (:exc:`FileNotFoundError`)
     - Fails (:exc:`FileNotFoundError`)
   * - :func:`pythainlp.corpus.download` — corpus already in local catalog
     - Succeeds (download is an explicit user action)
     - Fails (returns ``False``; all writes are blocked)
   * - :func:`pythainlp.corpus.download` — corpus **not** in local catalog
     - Succeeds (downloads the corpus)
     - Fails (returns ``False``; all writes are blocked)

Key differences:

- :envvar:`PYTHAINLP_OFFLINE` blocks only **automatic** downloads.
  Explicit calls to :func:`~pythainlp.corpus.download` (or the
  ``thainlp data get`` CLI command) still work, because those are
  deliberate user actions.

- :envvar:`PYTHAINLP_READ_ONLY` is **more restrictive**: it blocks
  *all* writes to the data directory, including explicit
  :func:`~pythainlp.corpus.download` calls.
  Use this when the data directory is on a read-only file system
  (e.g., a read-only Docker volume or a shared cluster mount).

- :envvar:`PYTHAINLP_DATA` sets the path of the data directory used by
  both modes.  In read-only mode the directory is not created if it
  does not already exist.

Typical use cases:

- **Offline laptop / air-gapped system**: set ``PYTHAINLP_OFFLINE=1``
  after downloading all required corpora.  You can still call
  ``download()`` manually if you have network access.

- **Read-only container image with pre-bundled corpora**:
  set ``PYTHAINLP_READ_ONLY=1`` so that no writes occur at all.
  Any attempt to download a corpus that is missing from the image
  will return ``False`` instead of raising a permission error.

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

A: Set the environment variable ``PYTHAINLP_READ_ONLY`` to ``1``.
The legacy ``PYTHAINLP_READ_MODE=1`` is still accepted but deprecated.
