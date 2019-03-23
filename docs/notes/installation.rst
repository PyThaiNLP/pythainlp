Installation
=====================================

For stable version::

    pip install pythainlp

For some advanced functionalities, like word vector, extra packages may be needed. Install them with these options during pip install::

    pip install pythainlp[extra1,extra2,...]

where extras can be

- ``artagger`` (to support artagger part-of-speech tagger)*
- ``deepcut`` (to support deepcut machine-learnt tokenizer)
- ``icu`` (for ICU support in transliteration and tokenization)
- ``ipa`` (for International Phonetic Alphabet support in transliteration)
- ``ml`` (to support fastai 1.0.22 ULMFiT models)
- ``ner`` (for named-entity recognizer)
- ``thai2fit`` (for Thai word vector)
- ``thai2rom`` (for machine-learnt romanization)
- ``full`` (install everything)

Note: standard artagger package from PyPI will not work on Windows, please pip install https://github.com/wannaphongcom/artagger/tarball/master#egg=artagger instead.

For development version::

    pip install https://github.com/PyThaiNLP/pythainlp/archive/dev.zip

** see extras and extras_require in setup.py for package details.

Note for installation on Windows:

- ``marisa-trie`` and ``PyICU`` libraries may required. You have two options to get them installed on Windows.

- Option 1 (recommended):
    - Find a pre-built package ("wheel") from https://www.lfd.uci.edu/~gohlke/pythonlibs/ 
    - Download a suitable wheel for your Python version (3.5, 3.6, etc.) and CPU architecture ("win32" for 32-bit Windows and "amd64" for 64-bit Windows)
    - Install them with pip. For example: `pip install marisa_trie‑0.7.5‑cp36‑cp36m‑win32.whl`
    
- Option 2 (advanced):
    - You can also try to install them with a command: `pip install marisa-trie pyicu`
    - With this, pip will try to build the libraries directly from source files.
    - This will take some time and need a set of build tools to be installed in your system, for example Microsoft Visual C++ Compiler. It also requires some technical skills on how things are getting built on Windows system, as you may need to configure some environment variables to accommodate the build process.
    - For PyICU, before the installation, you have to set ``ICU_VERSION`` environment variable to ICU version in your system. For example, ``set ICU_VERSION=62.1``.
    - This approach is obviously take more time and effort, but the good side is the library will be optimized for your system. This could mean a better performance.
