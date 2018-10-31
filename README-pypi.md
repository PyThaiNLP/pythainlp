![PyThaiNLP Logo](https://avatars0.githubusercontent.com/u/32934255?s=200&v=4)

# PyThaiNLP 1.7

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/cb946260c87a4cc5905ca608704406f7)](https://www.codacy.com/app/pythainlp/pythainlp_2?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=PyThaiNLP/pythainlp&amp;utm_campaign=Badge_Grade)[![pypi](https://img.shields.io/pypi/v/pythainlp.svg)](https://pypi.python.org/pypi/pythainlp)
[![Build Status](https://travis-ci.org/PyThaiNLP/pythainlp.svg?branch=develop)](https://travis-ci.org/PyThaiNLP/pythainlp)
[![Build status](https://ci.appveyor.com/api/projects/status/9g3mfcwchi8em40x?svg=true)](https://ci.appveyor.com/project/wannaphongcom/pythainlp-9y1ch)
[![Coverage Status](https://coveralls.io/repos/github/PyThaiNLP/pythainlp/badge.svg?branch=dev)](https://coveralls.io/github/PyThaiNLP/pythainlp?branch=dev)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

PyThaiNLP is a Python library for natural language processing (NLP) of Thai language.

PyThaiNLP features include Thai word and subword segmentations, soundex, romanization, part-of-speech taggers, and spelling corrections.

## What's new in version 1.7 ?

- Deprecate Python 2 support
- Refactor pythainlp.tokenize.pyicu for readability
- Add Thai NER model to pythainlp.ner
- thai2vec v0.2 - larger vocab, benchmarking results on Wongnai dataset
- Sentiment classifier based on ULMFit and various product review datasets
- Add ULMFit utility to PyThaiNLP
- Add Thai romanization model thai2rom
- Retrain POS-tagging model
- Improved word_tokenize (newmm, mm) and dict_word_tokenize
- Documentation added

## Install

```sh
pip install pythainlp
```

**Note for Windows**: `marisa-trie` wheels can be obtained from https://www.lfd.uci.edu/~gohlke/pythonlibs/#marisa-trie 
Install it with pip, for example: `pip install marisa_trie‑0.7.5‑cp36‑cp36m‑win32.whl`

## Links

- Docs: https://thainlp.org/pythainlp/docs/1.7/ 
- GitHub: https://github.com/PyThaiNLP/pythainlp
- Issues: https://github.com/PyThaiNLP/pythainlp/issues
