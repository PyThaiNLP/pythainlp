Installation
============

For stable version::

    pip install pythainlp

For development version::

    pip install --upgrade --pre pythainlp

For some functionalities, like named entity recognition, extra packages may be needed. Install them with these install options:

    pip install pythainlp[extra1,extra2,...]

where ``extras`` can be
  - ``attacut`` (to support attacut, a fast and accurate tokenizer)
  - ``benchmarks`` (to support benchmarks)
  - ``icu`` (for ICU, International Components for Unicode, support in transliteration and tokenization)
  - ``ipa`` (for IPA, International Phonetic Alphabet, support in transliteration)
  - ``ml`` (to support ULMFiT models for classification)
  - ``ssg`` (to support ssg for syllable tokenizer)
  - ``thai2fit`` (for Thai word vector)
  - ``thai2rom`` (for machine-learnt romanization)
  - ``translate`` (to support translate)
  - ``wangchanberta`` (to support wangchanberta models)
  - ``mt5`` (to mt5 models for Thai text summarizer)
  - ``wordnet`` (to support wordnet)
  - ``spell`` (to support phunspell & symspellpy)
  - ``generate`` (to support text generate with umlfit or thai2fit)
  - ``textaugment`` (to support text augmentation)
  - ``oskut`` (to support OSKUT)
  - ``nlpo3`` (to support nlpo3 engine)
  - ``spacy_thai`` (to support spacy_thai engine)
  - ``esupar`` (to support esupar engine)
  - ``transformers_ud`` (to support transformers_ud engine)
  - ``dependency_parsing`` (to support dependency parsing with all engine)
  - ``coreference_resolution`` (to support coreference esolution with all engine)
  - ``wangchanglm`` (to support wangchanglm model)
  - ``wsd`` (to support pythainlp.wsd)
  - ``el`` (to support pythainlp.el)
  - ``abbreviation`` (to support pythainlp.util.abbreviation_to_full_text)
  - ``full`` (install everything)

For dependency details, look at `extras` variable in `setup.py <https://github.com/PyThaiNLP/pythainlp/blob/dev/setup.py>`_.

Note for installation on Windows:

- ``PyICU`` libraries may required. You have two options to get them installed on Windows.

- Option 1 (recommended):
    - Find a pre-built package ("wheel") from https://www.lfd.uci.edu/~gohlke/pythonlibs/
    - Download a suitable wheel for your Python version (3.5, 3.6, etc.) and CPU architecture ("win32" for 32-bit Windows and "amd64" for 64-bit Windows)
    - Install them with pip. For example: `pip install PyICU-xxx‑cp36‑cp36m‑win32.whl`

- Option 2 (advanced):
    - You can also try to install them with a command: `pip install pyicu`
    - With this, pip will try to build the libraries directly from source files.
    - This will take some time and need a set of build tools to be installed in your system, for example Microsoft Visual C++ Compiler. It also requires some technical skills on how things are getting built on Windows system, as you may need to configure some environment variables to accommodate the build process.
    - For PyICU, before the installation, you have to set ``ICU_VERSION`` environment variable to ICU version in your system. For example, ``set ICU_VERSION=62.1``.
    - This approach is obviously take more time and effort, but the good side is the library will be optimized for your system. This could mean a better performance.


Runtime Configurations
----------------------

.. envvar:: PYTHAINLP_DATA_DIR

   This environment variable specifies the location where the downloaded data
   and the corpus database information are stored. If this directory
   does not exist, PyThaiNLP will automatically create a new one.

   By default, it is specified to the directory called ``pythainlp-data``
   within the home directory.

   Type `thainlp data path` at command line to see current PYTHAINLP_DATA_DIR.

.. envvar:: PYTHAINLP_READ_MODE

   This environment variable specifies config PyThaiNLP to read-only mode. (0 = False, 1 = True)

FAQ
===

Q: How to install pythainlp in Python 3.10+?
A: For Python 3.10+, We have python-crfsuite problem in pythainlp, so you can read about `python-crfsuite dependency fails to build under python 3.10 <https://github.com/PyThaiNLP/pythainlp/issues/626>`_.

Q: How to set the environment variables of each executor node in a distributed environment?
A: You can read `PermissionError: [Errno 13] Permission denied: /home/pythainlp-data <https://github.com/PyThaiNLP/pythainlp/issues/475>`_.

Q: How to fixed PyThaiNLP to read-only mode?
A: You can config PYTHAINLP_READ_MODE.