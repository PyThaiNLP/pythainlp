Installation
=====================================

For stable version::

    pip install pythainlp

For development version:

    pip install https://github.com/PyThaiNLP/pythainlp/archive/dev.zip


Note for installation on Windows:

- ``marisa-trie`` and ``PyICU`` libraries may required. You have two options to get them installed on Windows.

- Option 1 (recommended):
    - Find a pre-built package ("wheel") from https://www.lfd.uci.edu/~gohlke/pythonlibs/ 
    - Download a suitable package for your Python version (3.5, 3.6, etc.) and CPU architecture ("win32" for 32-bit Windows and "amd64" for 64-bit Windows)
    - Install them with pip. For example: `pip install marisa_trie‑0.7.5‑cp36‑cp36m‑win32.whl`
    
- Option 2 (advanced):
    - You can also try to install them with a command: `pip install marisa-trie pyicu`
    - With this, pip will try to build the libraries directly from source files.
    - This will take some time and need a set of build tools to be installed in your system, for example Microsoft Visual C++ Compiler. It also requires some technical skills on how things are getting built on Windows system, as you may need to configure some environment variables to accommodate the build process.
    - For PyICU, before the installation, you have to set ``ICU_VERSION`` to ICU version in your environment. For example, ``set ICU_VERSION=62.1``
    - This approach is obviously take more time and effort, but the good side is the library will be optimized for your system. This could mean a better performance.
