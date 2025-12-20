# PyThaiNLP: Thai Natural Language Processing in Python

![Project Logo](https://avatars0.githubusercontent.com/u/32934255?s=200&v=4)

[![pypi](https://img.shields.io/pypi/v/pythainlp.svg)](https://pypi.python.org/pypi/pythainlp)
[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3519354.svg)](https://doi.org/10.5281/zenodo.3519354)

[![Project Status: Active](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)
[![Codacy Grade](https://app.codacy.com/project/badge/Grade/5821a0de122041c79999bbb280230ffb)](https://www.codacy.com/gh/PyThaiNLP/pythainlp/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=PyThaiNLP/pythainlp&amp;utm_campaign=Badge_Grade)
[![Coverage Status](https://coveralls.io/repos/github/PyThaiNLP/pythainlp/badge.svg?branch=dev)](https://coveralls.io/github/PyThaiNLP/pythainlp?branch=dev)

[![Google Colab Badge](https://badgen.net/badge/Launch%20Quick%20Start%20Guide/on%20Google%20Colab/blue?icon=terminal)](https://colab.research.google.com/github/PyThaiNLP/tutorials/blob/master/source/notebooks/pythainlp_get_started.ipynb)
[![Chat on Matrix](https://matrix.to/img/matrix-badge.svg)](https://matrix.to/#/#thainlp:matrix.org)

PyThaiNLP is a Python package for text processing and linguistic analysis, similar to [NLTK](https://www.nltk.org/) with a focus on Thai language.

PyThaiNLP เป็นไลบารีภาษาไพทอนสำหรับประมวลผลภาษาธรรมชาติ คล้ายกับ NLTK โดยเน้นภาษาไทย [ดูรายละเอียดภาษาไทยได้ที่ README_TH.MD](https://github.com/PyThaiNLP/pythainlp/blob/dev/README_TH.md)

## Quick install

```sh
pip install pythainlp
```

| Version | Description | Status |
|:------:|:--:|:------:|
| [5.2.0](https://github.com/PyThaiNLP/pythainlp/releases) | Stable | [Change Log](https://github.com/PyThaiNLP/pythainlp/issues/1080) |
| [`dev`](https://github.com/PyThaiNLP/pythainlp/tree/dev) | Release Candidate for 5.3 | [Change Log](https://github.com/PyThaiNLP/pythainlp/issues/1169) |

## Getting Started

- PyThaiNLP requires Python 3.7+.
  - Python 2.7 users can use PyThaiNLP 1.6. See [2.0 change log](https://github.com/PyThaiNLP/pythainlp/issues/118) | [Upgrading from 1.7](https://pythainlp.org/docs/2.0/notes/pythainlp-1_7-2_0.html) | [Upgrading ThaiNER from 1.7](https://github.com/PyThaiNLP/pythainlp/wiki/Upgrade-ThaiNER-from-PyThaiNLP-1.7-to-PyThaiNLP-2.0)
- [PyThaiNLP Get Started notebook](https://pythainlp.org/tutorials/notebooks/pythainlp_get_started.html) | [API document](https://pythainlp.org/docs) | [Tutorials](https://pythainlp.org/tutorials)
- [Official website](https://pythainlp.org/) | [PyPI](https://pypi.org/project/pythainlp/) | [Facebook page](https://www.facebook.com/pythainlp/)
- [Who uses PyThaiNLP?](https://github.com/PyThaiNLP/pythainlp/blob/dev/INTHEWILD.md)
- [Model cards](https://github.com/PyThaiNLP/pythainlp/wiki/Model-Cards) - for technical details, caveats, and ethical considerations of the models developed and used in PyThaiNLP

## Capabilities

PyThaiNLP provides standard linguistic analysis for Thai language and standard Thai locale utility functions.
Some of these functions are also available via the command-line interface (run `thainlp` in your shell).

Partial list of features:

- Convenient character and word classes, like Thai consonants (`pythainlp.thai_consonants`), vowels (`pythainlp.thai_vowels`), digits (`pythainlp.thai_digits`), and stop words (`pythainlp.corpus.thai_stopwords`) -- comparable to constants like `string.letters`, `string.digits`, and `string.punctuation`
- Linguistic unit segmentation at different levels: sentence (`sent_tokenize`), word (`word_tokenize`), and subword (`subword_tokenize`)
- Part-of-speech tagging (`pos_tag`)
- Spelling suggestion and correction (`spell` and `correct`)
- Phonetic algorithm and transliteration (`soundex`  and `transliterate`)
- Collation (sorted by dictionary order) (`collate`)
- Number read out (`num_to_thaiword` and `bahttext`)
- Datetime formatting (`thai_strftime`)
- Thai-English keyboard misswitched fix (`eng_to_thai`, `thai_to_eng`)

## Installation

```sh
pip install --upgrade pythainlp
```

This will install the latest stable release of PyThaiNLP.

Install different releases:

- Stable release: `pip install --upgrade pythainlp`
- Pre-release (nearly ready): `pip install --upgrade --pre pythainlp`
- Development (likely to break things): `pip install https://github.com/PyThaiNLP/pythainlp/archive/dev.zip`

### Installation Options

Some functionalities, like Thai WordNet, may require extra packages. To install those requirements, specify a set of `[name]` immediately after `pythainlp`:

```sh
pip install "pythainlp[extra1,extra2,...]"
```

Possible `extras`:

- `full` (install everything)
- `compact` (install a stable and small subset of dependencies)
- `attacut` (to support attacut, a fast and accurate tokenizer)
- `benchmarks` (for [word tokenization benchmarking](tokenization-benchmark.md))
- `icu` (for ICU, International Components for Unicode, support in transliteration and tokenization)
- `ipa` (for IPA, International Phonetic Alphabet, support in transliteration)
- `ml` (to support ULMFiT models for classification)
- `thai2fit` (for Thai word vector)
- `thai2rom` (for machine-learnt romanization)
- `wordnet` (for Thai WordNet API)

For dependency details, look at the `extras` variable in
[`setup.py`](https://github.com/PyThaiNLP/pythainlp/blob/dev/setup.py).

## Data Directory

- Some additional data, like word lists and language models, may be automatically downloaded during runtime.
- PyThaiNLP caches these data under the directory `~/pythainlp-data` by default.
- The data directory can be changed by specifying the environment variable `PYTHAINLP_DATA_DIR`.
- See the data catalog (`db.json`) at <https://github.com/PyThaiNLP/pythainlp-corpus>

## Command-Line Interface

Some of PyThaiNLP functionalities can be used via command line with the `thainlp` command.

For example, to display a catalog of datasets:

```sh
thainlp data catalog
```

To show how to use:

```sh
thainlp help
```

## Testing and test suites

We test core functionalities on all officially supported Python versions.

Some functionality requiring extra dependencies may be tested less frequently
due to potential version conflicts or incompatibilities between packages.

Test cases are categorized into three groups: core, compact, and extra.
You can find these tests in the [tests/](/tests/) directory.

For more detailed information on testing, please refer to the tests README:
[tests/README.md](./tests/README.md)

## Licenses

| | License |
|:---|:----|
| PyThaiNLP source codes and notebooks | [Apache Software License 2.0](https://github.com/PyThaiNLP/pythainlp/blob/dev/LICENSE) |
| Corpora, datasets, and documentations created by PyThaiNLP | [Creative Commons Zero 1.0 Universal Public Domain Dedication License (CC0)](https://creativecommons.org/publicdomain/zero/1.0/)|
| Language models created by PyThaiNLP | [Creative Commons Attribution 4.0 International Public License (CC-by)](https://creativecommons.org/licenses/by/4.0/)  |
| Other corpora and models that may be included in PyThaiNLP | See [Corpus License](https://github.com/PyThaiNLP/pythainlp/blob/dev/pythainlp/corpus/corpus_license.md) |

## Contribute to PyThaiNLP

- Please fork and create a pull request :)
- For style guides and other information, including references to algorithms we use,
  please refer to our [contributing](https://github.com/PyThaiNLP/pythainlp/blob/dev/CONTRIBUTING.md) page.

## Who uses PyThaiNLP?

You can read [INTHEWILD.md](https://github.com/PyThaiNLP/pythainlp/blob/dev/INTHEWILD.md).

## Citations

If you use `PyThaiNLP` in your project or publication,
please cite the library as follows:

> Phatthiyaphaibun, Wannaphong, Korakot Chaovavanich, Charin Polpanumas, Arthit Suriyawongkul, Lalita Lowphansirikul, and Pattarawat Chormai. “Pythainlp: Thai Natural Language Processing in Python”. Zenodo, 2 June 2024. <http://doi.org/10.5281/zenodo.3519354>.

or by BibTeX entry:

```bibtex
@software{pythainlp,
    title = "{P}y{T}hai{NLP}: {T}hai Natural Language Processing in {P}ython",
    author = "Phatthiyaphaibun, Wannaphong  and
      Chaovavanich, Korakot  and
      Polpanumas, Charin  and
      Suriyawongkul, Arthit  and
      Lowphansirikul, Lalita  and
      Chormai, Pattarawat",
    doi = {10.5281/zenodo.3519354},
    license = {Apache-2.0},
    month = jun,
    url = {https://github.com/PyThaiNLP/pythainlp/},
    version = {v5.0.4},
    year = {2024},
}
```

Our [NLP-OSS 2023](https://nlposs.github.io/2023/) paper:

> Wannaphong Phatthiyaphaibun, Korakot Chaovavanich, Charin Polpanumas, Arthit Suriyawongkul, Lalita Lowphansirikul, Pattarawat Chormai, Peerat Limkonchotiwat, Thanathip Suntorntip, and Can Udomcharoenchaikit. 2023. [PyThaiNLP: Thai Natural Language Processing in Python.](https://aclanthology.org/2023.nlposs-1.4) In Proceedings of the 3rd Workshop for Natural Language Processing Open Source Software (NLP-OSS 2023), pages 25–36, Singapore, Singapore. Empirical Methods in Natural Language Processing.

and its BibTeX entry:

```bibtex
@inproceedings{phatthiyaphaibun-etal-2023-pythainlp,
    title = "{P}y{T}hai{NLP}: {T}hai Natural Language Processing in {P}ython",
    author = "Phatthiyaphaibun, Wannaphong  and
      Chaovavanich, Korakot  and
      Polpanumas, Charin  and
      Suriyawongkul, Arthit  and
      Lowphansirikul, Lalita  and
      Chormai, Pattarawat  and
      Limkonchotiwat, Peerat  and
      Suntorntip, Thanathip  and
      Udomcharoenchaikit, Can",
    editor = "Tan, Liling  and
      Milajevs, Dmitrijs  and
      Chauhan, Geeticka  and
      Gwinnup, Jeremy  and
      Rippeth, Elijah",
    booktitle = "Proceedings of the 3rd Workshop for Natural Language Processing Open Source Software (NLP-OSS 2023)",
    month = dec,
    year = "2023",
    address = "Singapore, Singapore",
    publisher = "Empirical Methods in Natural Language Processing",
    url = "https://aclanthology.org/2023.nlposs-1.4",
    pages = "25--36",
    abstract = "We present PyThaiNLP, a free and open-source natural language processing (NLP) library for Thai language implemented in Python. It provides a wide range of software, models, and datasets for Thai language. We first provide a brief historical context of tools for Thai language prior to the development of PyThaiNLP. We then outline the functionalities it provided as well as datasets and pre-trained language models. We later summarize its development milestones and discuss our experience during its development. We conclude by demonstrating how industrial and research communities utilize PyThaiNLP in their work. The library is freely available at https://github.com/pythainlp/pythainlp.",
}
```

## Sponsors

| Logo | Description |
| --- | ----------- |
| [![VISTEC-depa Thailand Artificial Intelligence Research Institute](https://airesearch.in.th/assets/img/logo/airesearch-logo.svg)](https://airesearch.in.th/)   | Since 2019, our contributors Korakot Chaovavanich and Lalita Lowphansirikul have been supported by [VISTEC-depa Thailand Artificial Intelligence Research Institute](https://airesearch.in.th/).                 |
| [![MacStadium](https://i.imgur.com/rKy1dJX.png)](https://www.macstadium.com)   | We get support of free Mac Mini M1 from [MacStadium](https://www.macstadium.com) for running CI builds.                  |

------

<div align="center">
  Made with ❤️ | PyThaiNLP Team 💻 |  "We build Thai NLP" 🇹🇭
</div>

------

<div align="center">
  <strong>We have only one official repository at https://github.com/PyThaiNLP/pythainlp and another mirror at https://gitlab.com/pythainlp/pythainlp</strong>
</div>

<div align="center">
  <strong>Beware of malware if you use codes from mirrors other than the official two on GitHub and GitLab.</strong>
</div>
