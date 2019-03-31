![PyThaiNLP Logo](https://avatars0.githubusercontent.com/u/32934255?s=200&v=4)

# PyThaiNLP 2.0

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/cb946260c87a4cc5905ca608704406f7)](https://www.codacy.com/app/pythainlp/pythainlp_2?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=PyThaiNLP/pythainlp&amp;utm_campaign=Badge_Grade)[![pypi](https://img.shields.io/pypi/v/pythainlp.svg)](https://pypi.python.org/pypi/pythainlp)
[![Build Status](https://travis-ci.org/PyThaiNLP/pythainlp.svg?branch=develop)](https://travis-ci.org/PyThaiNLP/pythainlp)
[![Build status](https://ci.appveyor.com/api/projects/status/9g3mfcwchi8em40x?svg=true)](https://ci.appveyor.com/project/wannaphongcom/pythainlp-9y1ch)
[![Coverage Status](https://coveralls.io/repos/github/PyThaiNLP/pythainlp/badge.svg?branch=dev)](https://coveralls.io/github/PyThaiNLP/pythainlp?branch=dev)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

PyThaiNLP is a Python library for natural language processing (NLP) of Thai language.

PyThaiNLP includes Thai word tokenizers, transliterators, soundex converters, part-of-speech taggers, and spell checkers.

📖 For details on upgrading from PyThaiNLP 1.7 to PyThaiNLP 2.0, see [From PyThaiNLP 1.7 to PyThaiNLP 2.0](https://thainlp.org/pythainlp/docs/2.0/notes/pythainlp-1_7-2_0.html)

📖 For ThaiNER user after upgrading from PyThaiNLP 1.7 to PyThaiNLP 2.0, see [Upgrade ThaiNER from PyThaiNLP 1.7 to PyThaiNLP 2.0](https://github.com/PyThaiNLP/pythainlp/wiki/Upgrade-ThaiNER-from-PyThaiNLP-1.7-to-PyThaiNLP-2.0)

📫 follow us on Facebook [Pythainlp](https://www.facebook.com/pythainlp/)

## What's new in version 2.0 ?

- New NorvigSpellChecker spell checker class, which can be initialized with custom dictionary.
- Terminate Python 2 support. Remove all Python 2 compatibility code.
- Remove old, obsolated, deprecated, and experimental code.
- Thai2fit (Upgrade ULMFiT-related codes to fastai 1.0)
- ThaiNER 1.0
- Remove sentiment analysis
- Improved word_tokenize (newmm, mm) and dict_word_tokenize
- Improved POS-tagging
- More and improved examples
- see [PyThaiNLP 2.0 change log](https://github.com/PyThaiNLP/pythainlp/issues/118)

## Install

For stable version:

```sh
pip install pythainlp
```

For some advanced functionalities, like word vector, extra packages  may be needed. Install them with these options during pip install:

```
pip install pythainlp[extra1,extra2,...]
```

where extras can be

- `artagger` (to support artagger part-of-speech tagger)*
- `deepcut` (to support deepcut machine-learnt tokenizer)
- `icu` (for ICU support in transliteration and tokenization)
- `ipa` (for International Phonetic Alphabet support in transliteration)
- `ml` (to support fastai 1.0.22 ULMFiT models)
- `ner` (for named-entity recognizer)
- `thai2fit` (for Thai word vector)
- `thai2rom` (for machine-learnt romanization)
- `full` (install everything)

**Note for Windows**: `marisa-trie` wheels can be obtained from https://www.lfd.uci.edu/~gohlke/pythonlibs/#marisa-trie 
Install it with pip, for example: `pip install marisa_trie‑0.7.5‑cp36‑cp36m‑win32.whl`

## Links

- User guide : [English](https://colab.research.google.com/drive/1MQ10D1mJC5r1vQAHcj4ShoRS14vz8ZF-) , [ภาษาไทย](https://colab.research.google.com/drive/1rEkB2Dcr1UAKPqz4bCghZV7pXx2qxf89)
- Docs: https://thainlp.org/pythainlp/docs/2.0/ 
- GitHub: https://github.com/PyThaiNLP/pythainlp
- Issues: https://github.com/PyThaiNLP/pythainlp/issues
- Facebook : [Pythainlp](https://www.facebook.com/pythainlp/)
