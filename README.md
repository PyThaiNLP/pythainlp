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
[![Facebook](https://img.shields.io/badge/Facebook-0866FF?style=flat&logo=facebook&logoColor=white)](https://www.facebook.com/pythainlp/)
[![Chat on Matrix](https://matrix.to/img/matrix-badge.svg)](https://matrix.to/#/#thainlp:matrix.org)

[pythainlp.org](https://pythainlp.org/) |
[Tutorials](https://pythainlp.org/tutorials) |
[License info](https://pythainlp.org/dev-docs/notes/license.html) |
[Model cards](https://github.com/PyThaiNLP/pythainlp/wiki/Model-Cards) |
[Adopters](https://github.com/PyThaiNLP/pythainlp/blob/dev/INTHEWILD.md) |
*[เอกสารภาษาไทย](https://github.com/PyThaiNLP/pythainlp/blob/dev/README_TH.md)*

Designed to be a Thai-focused counterpart to [NLTK](https://www.nltk.org/),
**PyThaiNLP** provides standard tools for linguistic analysis under
an Apache-2.0 source license, with its data and models covered by CC0-1.0
and CC-BY-4.0.

```sh
pip install pythainlp
```

| Version | Python version | Changes | Documentation |
|:-------:|:--------------:|:-------:|:-------------:|
| [5.2.0](https://github.com/PyThaiNLP/pythainlp/releases) | 3.7+ | [Log](https://github.com/PyThaiNLP/pythainlp/issues/1080) | [pythainlp.org/docs](https://pythainlp.org/docs) |
| [`dev`](https://github.com/PyThaiNLP/pythainlp/tree/dev) | 3.9+ | [Log](https://github.com/PyThaiNLP/pythainlp/issues/1169) | [pythainlp.org/dev-docs](https://pythainlp.org/dev-docs/) |

## Features

- **Linguistic units:** Sentence, word, and subword segmentation
  (`sent_tokenize`, `word_tokenize`, `subword_tokenize`).
- **Tagging:** Part-of-speech tagging (`pos_tag`).
- **Transliteration:** Romanization (`transliterate`) and IPA conversion.
- **Correction:** Spelling suggestion and correction (`spell`, `correct`).
- **Utilities:** Soundex, collation, number-to-text (`bahttext`), datetime
  formatting (`thai_strftime`), and keyboard layout correction.
- **Data:** Built-in Thai character sets, word lists, and stop words.
- **CLI:** Command-line interface via `thainlp`.

  ```sh
  thainlp data catalog  # List datasets
  thainlp help          # Show usage
  ```

## Installation options

To install with specific extras (e.g., `translate`, `wordnet`, `full`):

```sh
pip install "pythainlp[extra1,extra2,...]"
```

Possible `extras` included:

- `compact` — install a stable and small subset of dependencies (recommended)
- `translate` — machine translation support
- `wordnet` — WordNet support
- `full` — install all optional dependencies (may introduce conflicts)

The documentation website maintains
[full list of extras](https://pythainlp.org/dev-docs/notes/installation.html).

For details, see `[project.optional-dependencies]` section in
[`pyproject.toml`](https://github.com/PyThaiNLP/pythainlp/blob/dev/pyproject.toml).

## Data directory

PyThaiNLP downloads data (see the data catalog `db.json` at
[pythainlp-corpus](https://github.com/PyThaiNLP/pythainlp-corpus))
to `~/pythainlp-data` by default.
Set the `PYTHAINLP_DATA_DIR` environment variable to override this location.

When using PyThaiNLP in distributed computing environments
(e.g., Apache Spark), set the `PYTHAINLP_DATA_DIR` environment variable
inside the function that will be distributed to worker nodes.
See details in
[the documentation](https://pythainlp.org/dev-docs/notes/installation.html).

## Testing and test suites

We test core functionalities on all officially supported Python versions.

See [tests/README.md](./tests/README.md) for test matrix and other details.

## Licenses

| | License |
| :-- | :-- |
| PyThaiNLP source codes and notebooks | [Apache Software License 2.0](https://github.com/PyThaiNLP/pythainlp/blob/dev/LICENSE) |
| Corpora, datasets, and documentations created by PyThaiNLP | [Creative Commons Zero 1.0 Universal Public Domain Dedication License (CC0)](https://creativecommons.org/publicdomain/zero/1.0/)|
| Language models created by PyThaiNLP | [Creative Commons Attribution 4.0 International Public License (CC-by)](https://creativecommons.org/licenses/by/4.0/) |
| Other corpora and models that may be included in PyThaiNLP | See [Corpus License](https://github.com/PyThaiNLP/pythainlp/blob/dev/pythainlp/corpus/corpus_license.md) |

## Contribute to PyThaiNLP

Please fork and create a pull request.
See [CONTRIBUTING.md](https://github.com/PyThaiNLP/pythainlp/blob/dev/CONTRIBUTING.md)
for guidelines and algorithm references.

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
| [![VISTEC-depa Thailand Artificial Intelligence Research Institute](https://airesearch.in.th/assets/img/logo/airesearch-logo.svg)](https://airesearch.in.th/) | Since 2019, our contributors Korakot Chaovavanich and Lalita Lowphansirikul have been supported by [VISTEC-depa Thailand Artificial Intelligence Research Institute](https://airesearch.in.th/). |
| [![MacStadium](https://i.imgur.com/rKy1dJX.png)](https://www.macstadium.com) | We get support of free Mac Mini M1 from [MacStadium](https://www.macstadium.com) for running CI builds. |

------

<div align="center">
  Made with ❤️ | PyThaiNLP Team 💻 | "We build Thai NLP" 🇹🇭
</div>

------

<div align="center">
  <strong>We have only one official repository at https://github.com/PyThaiNLP/pythainlp and another mirror at https://gitlab.com/pythainlp/pythainlp</strong>
</div>

<div align="center">
  <strong>Beware of malware if you use code from mirrors other than the official two on GitHub and GitLab.</strong>
</div>
