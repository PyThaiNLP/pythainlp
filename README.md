<div align="center">
  <img src="https://avatars0.githubusercontent.com/u/32934255?s=200&v=4"/>
  <h1>PyThaiNLP: Thai Natural Language Processing in Python</h1>
  <a href="https://pypi.python.org/pypi/pythainlp"><img alt="pypi" src="https://img.shields.io/pypi/v/pythainlp.svg"/></a>
  <a href="https://www.python.org/downloads/release/python-360/"><img alt="Python 3.6" src="https://img.shields.io/badge/python-3.6-blue.svg"/></a>
  <a href="https://opensource.org/licenses/Apache-2.0"><img alt="License" src="https://img.shields.io/badge/License-Apache%202.0-blue.svg"/></a>
  <a href="https://pepy.tech/project/pythainlp"><img alt="Download" src="https://pepy.tech/badge/pythainlp/month"/></a>
  <a href="https://ci.appveyor.com/project/wannaphongcom/pythainlp-9y1ch"><img alt="Build status" src="https://ci.appveyor.com/api/projects/status/9g3mfcwchi8em40x?svg=true"/></a>
  <a href="https://coveralls.io/github/PyThaiNLP/pythainlp?branch=dev"><img alt="Coverage Status" src="https://coveralls.io/repos/github/PyThaiNLP/pythainlp/badge.svg?branch=dev"/></a>
  <a href="https://www.codacy.com/app/pythainlp/pythainlp_2"><img alt="Codacy Badge" src="https://api.codacy.com/project/badge/Grade/cb946260c87a4cc5905ca608704406f7"/></a>
  <a href="https://app.fossa.io/projects/git%2Bgithub.com%2FPyThaiNLP%2Fpythainlp"><img alt="FOSSA Status" src="https://app.fossa.io/api/projects/git%2Bgithub.com%2FPyThaiNLP%2Fpythainlp.svg?type=shield"/></a>
  <a href="https://colab.research.google.com/github/PyThaiNLP/tutorials/blob/master/source/notebooks/pythainlp_get_started.ipynb"><img alt="Google Colab Badge" src="https://badgen.net/badge/Launch%20Quick%20Start%20Guide/on%20Google%20Colab/blue?icon=terminal"/></a>
  <a href="https://zenodo.org/badge/latestdoi/61813823"><img alt="DOI" src="https://zenodo.org/badge/61813823.svg"/></a>
</div>

PyThaiNLP is a Python package for text processing and linguistic analysis, similar to [NLTK](https://www.nltk.org/) with focus on Thai language.

PyThaiNLP เป็นไลบารีภาษาไพทอนสำหรับประมวลผลภาษาธรรมชาติ คล้ายกับ NLTK โดยเน้นภาษาไทย [ดูรายละเอียดภาษาไทยได้ที่ README_TH.MD](https://github.com/PyThaiNLP/pythainlp/blob/dev/README_TH.md)

**News**

>We are conducting a 2-minute survey to know more about your experience using the library and your expectations regarding what the library should be able to do. Take part in [this survey](https://forms.gle/aLdSHnvkNuK5CFyt9).

| Version | Description | Status |
|:------:|:--:|:------:|
| [2.2.6](https://github.com/PyThaiNLP/pythainlp/releases) | Stable | [Change Log](https://github.com/PyThaiNLP/pythainlp/issues/330) |
| [`dev`](https://github.com/PyThaiNLP/pythainlp/tree/dev) | Release Candidate for 2.3  | [Change Log](https://github.com/PyThaiNLP/pythainlp/issues/445) |

Please follow our [PyThaiNLP Facebook page](https://www.facebook.com/pythainlp/) for more updates.


## Getting Started with PyThaiNLP

We provide [PyThaiNLP Get Started Tutorial](https://www.thainlp.org/pythainlp/tutorials/notebooks/pythainlp_get_started.html) for exploring features in PyThaiNLP; We also have tutorials for specific tasks. Please visit [our tutorial page](https://www.thainlp.org/pythainlp/tutorials).

Latest document is available at [https://thainlp.org/pythainlp/docs/2.2/](https://thainlp.org/pythainlp/docs/2.2/).

We try to make the package easy to use as much as possible; therefore, some additional data (like word lists and language models) may get automatically download during runtime. PyThaiNLP caches additional data under the directory `~/pythainlp-data` by default, but the user can change the value by specifying the environment variable `PYTHAINLP_DATA_DIR`. See corpus catalog at [PyThaiNLP/pythainlp-corpus](https://github.com/PyThaiNLP/pythainlp-corpus).


## Capabilities

PyThaiNLP provides standard NLP functions for Thai, for example part-of-speech tagging, linguistic unit segmentation (syllable, word, or sentence). Some of these functions are also available via command-line interface.

<details>
  <summary>List of Features</summary>

- Convenient character and word classes, like Thai consonants (`pythainlp.thai_consonants`), vowels (`pythainlp.thai_vowels`), digits (`pythainlp.thai_digits`), and stop words (`pythainlp.corpus.thai_stopwords`) -- comparable to constants like `string.letters`, `string.digits`, and `string.punctuation`
- Thai linguistic unit segmentation/tokenization, including sentence (`sent_tokenize`), word (`word_tokenize`), and subword segmentations based on Thai Character Cluster (`subword_tokenize`)
- Thai part-of-speech tagging (`pos_tag`)
- Thai spelling suggestion and correction (`spell` and `correct`)
- Thai transliteration (`transliterate`)
- Thai soundex (`soundex`) with three engines (`lk82`, `udom83`, `metasound`)
- Thai collation (sort by dictionary order) (`collate`)
- Read out number to Thai words (`bahttext`, `num_to_thaiword`)
- Thai datetime formatting (`thai_strftime`)
- Thai-English keyboard misswitched fix (`eng_to_thai`, `thai_to_eng`)
- Command-line interface for basic functions, like tokenization and pos tagging (run `thainlp` in your shell)
</details>

Please see [our tutorials](https://www.thainlp.org/pythainlp/tutorials) on how to apply these functions to machine-learning problems.


## Installation

```sh
pip install --upgrade pythainlp
```

This will install the latest stable release of PyThaiNLP.
PyThaiNLP uses pip as its package manager and PyPI as its main distribution channel, see [https://pypi.org/project/pythainlp/](https://pypi.org/project/pythainlp/)

Install different releases:

- Stable release: `pip install --upgrade pythainlp`
- Pre-release (near ready): `pip install --upgrade --pre pythainlp`
- Development (likely to break things): `pip install https://github.com/PyThaiNLP/pythainlp/archive/dev.zip`

### Installation Options

Some functionalities, like Thai WordNet, may require extra packages. To install those requirements, specify a set of                                                                                                                                                                                         `[name]` immediately after `pythainlp`:

```sh
pip install pythainlp[extra1,extra2,...]
```

<details>
  <summary>List of possible `extras`</summary>

-  `full` (install everything)
-  `attacut` (to support attacut, a fast and accurate tokenizer)
-  `benchmarks` (for [word tokenization benchmarking](tokenization-benchmark.md))
-  `icu` (for ICU, International Components for Unicode, support in transliteration and tokenization)
-  `ipa` (for IPA, International Phonetic Alphabet, support in transliteration)
-  `ml` (to support ULMFiT models for classification)
-  `thai2fit` (for Thai word vector)
-  `thai2rom` (for machine-learnt romanization)
-  `wordnet` (for Thai WordNet API)
</details>

For dependency details, look at `extras` variable in [`setup.py`](https://github.com/PyThaiNLP/pythainlp/blob/dev/setup.py).


## Command-Line Interface

Some of PyThaiNLP functionalities can be used at command line, using `thainlp` command.

For example, displaying a catalog of datasets:
```sh
thainlp data catalog
```

Showing how to use:
```sh
thainlp help
```


## Python 2 Users

- PyThaiNLP 2 supports Python 3.6+. Some functions may work with older version of Python 3, but it is not well-tested and will not be supported. See [1.7 -> 2.0 change log](https://github.com/PyThaiNLP/pythainlp/issues/118).
  - [Upgrading from 1.7](https://thainlp.org/pythainlp/docs/2.0/notes/pythainlp-1_7-2_0.html)
  - [Upgrade ThaiNER from 1.7](https://github.com/PyThaiNLP/pythainlp/wiki/Upgrade-ThaiNER-from-PyThaiNLP-1.7-to-PyThaiNLP-2.0)
- Python 2.7 users can use PyThaiNLP 1.6


## Citations

If you use `PyThaiNLP` in your project or publication, please cite the library as follows

```
Wannaphong Phatthiyaphaibun, Korakot Chaovavanich, Charin Polpanumas, Arthit Suriyawongkul, Lalita Lowphansirikul, & Pattarawat Chormai. (2016, Jun 27). PyThaiNLP: Thai Natural Language Processing in Python. Zenodo. http://doi.org/10.5281/zenodo.3519354
```

or BibTeX entry:

``` bib
@misc{pythainlp,
    author       = {Wannaphong Phatthiyaphaibun, Korakot Chaovavanich, Charin Polpanumas, Arthit Suriyawongkul, Lalita Lowphansirikul, Pattarawat Chormai},
    title        = {{PyThaiNLP: Thai Natural Language Processing in Python}},
    month        = Jun,
    year         = 2016,
    doi          = {10.5281/zenodo.3519354},
    publisher    = {Zenodo},
    url          = {http://doi.org/10.5281/zenodo.3519354}
}
```

## Contribute to PyThaiNLP

- Please do fork and create a pull request :)
- For style guide and other information, including references to algorithms we use, please refer to our [contributing](https://github.com/PyThaiNLP/pythainlp/blob/dev/CONTRIBUTING.md) page.

## Who uses PyThaiNLP?

You can read [INTHEWILD.md](https://github.com/PyThaiNLP/pythainlp/blob/dev/INTHEWILD.md).


## Licenses

| | License |
|:---|:----|
| PyThaiNLP Source Code and Notebooks | [Apache Software License 2.0](https://github.com/PyThaiNLP/pythainlp/blob/dev/LICENSE) |
| Corpora, datasets, and documentations created by PyThaiNLP | [Creative Commons Zero 1.0 Universal Public Domain Dedication License (CC0)](https://creativecommons.org/publicdomain/zero/1.0/)|
| Language models created by PyThaiNLP | [Creative Commons Attribution 4.0 International Public License (CC-by)](https://creativecommons.org/licenses/by/4.0/)  |
| Other corpora and models that may included with PyThaiNLP | See [Corpus License](https://github.com/PyThaiNLP/pythainlp/blob/dev/pythainlp/corpus/corpus_license.md) |


## Model Cards

For technical details, caveats, and ethical considerations of the models developed and used in PyThaiNLP, see [Model cards](https://github.com/PyThaiNLP/pythainlp/wiki/Model-Cards).


## Sponsors

[![VISTEC-depa Thailand Artificial Intelligence Research Institute](https://airesearch.in.th/assets/img/logo/airesearch-logo.svg)](https://airesearch.in.th/)

Since 2019, our contributors Korakot Chaovavanich and Lalita Lowphansirikul have been supported by [VISTEC-depa Thailand Artificial Intelligence Research Institute](https://airesearch.in.th/).

------

<div align="center">
  Made with ❤️ | PyThaiNLP Team 💻 |  "We build Thai NLP" 🇹🇭
</div>

------

<div align="center">
  <strong>We have only one official repository at https://github.com/PyThaiNLP/pythainlp and another mirror at https://gitlab.com/pythainlp/pythainlp</strong>
</div>

<div align="center">
  <strong>Beware of malware if you use code from mirrors other than the official two at GitHub and GitLab.</strong>
</div>
