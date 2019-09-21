![PyThaiNLP Logo](https://avatars0.githubusercontent.com/u/32934255?s=200&v=4)

# PyThaiNLP

PyThaiNLP is a Python library for natural language processing (NLP) of Thai language.

PyThaiNLP includes Thai word tokenizers, transliterators, soundex converters, part-of-speech taggers, and spell checkers.

📫 follow us on Facebook [PyThaiNLP](https://www.facebook.com/pythainlp/)

## What's new in 2.1 ?

- Improved `word_tokenize` ("newmm" and "mm" engine), a `custom_dict` dictionary can be provided
- Add AttaCut to be options for `word_tokenize` engine.
- New Thai2rom (PyTorch)
- New Command Line
- Add word tokenization benchmark to PyThaiNLP
- See more examples in [Get Started notebook](https://github.com/PyThaiNLP/pythainlp/blob/dev/notebooks/pythainlp-get-started.ipynb)
- [Full change log](https://github.com/PyThaiNLP/pythainlp/issues/181)

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
- `attacut` - Wrapper for AttaCut (https://github.com/PyThaiNLP/attacut)
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

- User guide: [English](https://github.com/PyThaiNLP/pythainlp/blob/dev/notebooks/pythainlp-get-started.ipynb)
- Docs: https://thainlp.org/pythainlp/docs/2.1/ 
- GitHub: https://github.com/PyThaiNLP/pythainlp
- Issues: https://github.com/PyThaiNLP/pythainlp/issues
- Facebook: [PyThaiNLP](https://www.facebook.com/pythainlp/)


Made with ❤️

We build Thai NLP.

PyThaiNLP Team.