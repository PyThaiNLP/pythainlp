![PyThaiNLP Logo](https://avatars0.githubusercontent.com/u/32934255?s=200&v=4)

# PyThaiNLP 2.0.3

PyThaiNLP is a Python library for natural language processing (NLP) of Thai language.

PyThaiNLP includes Thai word tokenizers, transliterators, soundex converters, part-of-speech taggers, and spell checkers.

📫 follow us on Facebook [PyThaiNLP](https://www.facebook.com/pythainlp/)

## What's new in version 2.0 ?

- Terminate Python 2 support. Remove all Python 2 compatibility code.
- Improved `word_tokenize` ("newmm" and "mm" engine) and `dict_word_tokenize`
- Improved Part-Of-Speech tagging
- New `NorvigSpellChecker` spell checker class, which can be initialized with custom dictionary.
- New `thai2fit` (replacing `thai2vec`, upgrade ULMFiT-related code to fastai 1.0)
- Updated ThaiNER to 1.0
  - You may need to [update your existing ThaiNER models from PyThaiNLP 1.7](https://github.com/PyThaiNLP/pythainlp/wiki/Upgrade-ThaiNER-from-PyThaiNLP-1.7-to-PyThaiNLP-2.0)
- Remove old, obsolated, deprecated, duplicated, and experimental code.
  - Sentiment analysis is no longer part of the library, but rather [a text classification example](https://github.com/PyThaiNLP/pythainlp/blob/dev/notebooks/sentiment_analysis.ipynb).
- See more examples in [Get Started notebook](https://github.com/PyThaiNLP/pythainlp/blob/dev/notebooks/pythainlp-get-started.ipynb)
- [Full change log](https://github.com/PyThaiNLP/pythainlp/issues/118)
- [Upgrading from 1.7](https://thainlp.org/pythainlp/docs/2.0/notes/pythainlp-1_7-2_0.html)

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

- User guide: [English](https://github.com/PyThaiNLP/pythainlp/blob/dev/notebooks/pythainlp-get-started.ipynb), [ภาษาไทย](https://colab.research.google.com/drive/1rEkB2Dcr1UAKPqz4bCghZV7pXx2qxf89)
- Docs: https://thainlp.org/pythainlp/docs/2.0/ 
- GitHub: https://github.com/PyThaiNLP/pythainlp
- Issues: https://github.com/PyThaiNLP/pythainlp/issues
- Facebook: [PyThaiNLP](https://www.facebook.com/pythainlp/)
