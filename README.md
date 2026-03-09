# PyThaiNLP: Thai Natural Language Processing in Python

![Project Logo](./docs/images/logo.png)

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

[pythainlp.org](https://pythainlp.org/)
| [Tutorials](https://pythainlp.org/tutorials)
| [License info](https://pythainlp.org/dev-docs/notes/license.html)
| [Model cards](https://github.com/PyThaiNLP/pythainlp/wiki/Model-Cards)
| [Adopters](https://github.com/PyThaiNLP/pythainlp/blob/dev/INTHEWILD.md)
| *[เอกสารภาษาไทย](https://github.com/PyThaiNLP/pythainlp/blob/dev/README_TH.md)*

Designed to be a Thai-focused counterpart to [NLTK](https://www.nltk.org/),
**PyThaiNLP** provides standard tools for linguistic analysis under
an Apache-2.0 license, with its data and models covered by CC0-1.0
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

The documentation website maintains the
[full list of extras](https://pythainlp.org/dev-docs/notes/installation.html).
To see the specific libraries included in each extra,
please inspect the `[project.optional-dependencies]` section of
[`pyproject.toml`](https://github.com/PyThaiNLP/pythainlp/blob/dev/pyproject.toml).

## Environment variables

| Variable | Description | Status |
|---|---|---|
| `PYTHAINLP_DATA` | Path to the data directory (default: `~/pythainlp-data`). | Current |
| `PYTHAINLP_DATA_DIR` | Legacy alias for `PYTHAINLP_DATA`. Emits a `DeprecationWarning`. Setting both raises `ValueError`. | Deprecated; use `PYTHAINLP_DATA` |
| `PYTHAINLP_OFFLINE` | Set to `1` to disable automatic corpus downloads. Explicit `download()` calls still work. | Current |
| `PYTHAINLP_READ_ONLY` | Set to `1` to enable read-only mode, which prevents implicit background writes to PyThaiNLP's internal data directory (corpus downloads, catalog updates, directory creation). Explicit user-initiated saves to user-specified paths are unaffected. | Current |
| `PYTHAINLP_READ_MODE` | Legacy alias for `PYTHAINLP_READ_ONLY`. Emits a `DeprecationWarning`. Setting both raises `ValueError`. | Deprecated; use `PYTHAINLP_READ_ONLY` |

### Data directory

PyThaiNLP downloads data (see the data catalog `db.json` at
[pythainlp-corpus](https://github.com/PyThaiNLP/pythainlp-corpus))
to `~/pythainlp-data` by default.
Set the `PYTHAINLP_DATA` environment variable to override this location.
(`PYTHAINLP_DATA_DIR` is still accepted but deprecated.)

When using PyThaiNLP in distributed computing environments
(e.g., Apache Spark), set the `PYTHAINLP_DATA` environment variable
inside the function that will be distributed to worker nodes.
See details in
[the documentation](https://pythainlp.org/dev-docs/notes/installation.html).

### Offline mode

Set `PYTHAINLP_OFFLINE=1` to disable **automatic** corpus downloads.
When this variable is set and a corpus is not already cached locally,
a `FileNotFoundError` is raised instead of attempting a network download.
Explicit calls to `pythainlp.corpus.download()` are unaffected.
Use `pythainlp.is_offline_mode()` to check the current state programmatically.

```python
import pythainlp
print(pythainlp.is_offline_mode())  # True if PYTHAINLP_OFFLINE=1
```

### Read-only mode

Set `PYTHAINLP_READ_ONLY=1` to prevent implicit background writes to PyThaiNLP's
internal data directory. This blocks corpus downloads, catalog updates, and
automatic data directory creation — writes that happen as side effects the user
may not be aware of.

Operations where the user explicitly specifies an output path are unaffected
(e.g., `model.save("path")`, `tagger.train(..., save_loc="path")`,
`thainlp misspell --output myfile.txt`).

Use `pythainlp.is_read_only_mode()` to check the current state programmatically.

```python
import pythainlp
print(pythainlp.is_read_only_mode())  # True if PYTHAINLP_READ_ONLY=1
```

## Testing

We test core functionalities on all officially supported Python versions.

See [tests/README.md](./tests/README.md) for test matrix and other details.

## Contribute to PyThaiNLP

Please fork and create a pull request.
See [CONTRIBUTING.md](https://github.com/PyThaiNLP/pythainlp/blob/dev/CONTRIBUTING.md)
for guidelines and algorithm references.

## Citations

If you use `PyThaiNLP` library in your project,
please cite the software as follows:

> Phatthiyaphaibun, Wannaphong, Korakot Chaovavanich, Charin Polpanumas,
> Arthit Suriyawongkul, Lalita Lowphansirikul, and Pattarawat Chormai.
> “PyThaiNLP: Thai Natural Language Processing in Python”.
> Zenodo, 2 June 2024. <https://doi.org/10.5281/zenodo.3519354>.

with this BibTeX entry:

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

To cite our [NLP-OSS 2023](https://nlposs.github.io/2023/) academic paper,
please cite the paper as follows:

> Wannaphong Phatthiyaphaibun, Korakot Chaovavanich, Charin Polpanumas,
> Arthit Suriyawongkul, Lalita Lowphansirikul, Pattarawat Chormai,
> Peerat Limkonchotiwat, Thanathip Suntorntip, and Can Udomcharoenchaikit.
> 2023.
> [PyThaiNLP: Thai Natural Language Processing in Python.](https://aclanthology.org/2023.nlposs-1.4)
> In Proceedings of the 3rd Workshop for Natural Language Processing
> Open Source Software (NLP-OSS 2023),
> pages 25–36, Singapore, Singapore.
> Empirical Methods in Natural Language Processing.

with this BibTeX entry:

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

## Acknowledgements

PyThaiNLP was founded by Wannaphong Phatthiyaphaibun in 2016.
His contributions from 2021 were made during a PhD studentship supported by
[Vidyasirimedhi Institute of Science and Technology (VISTEC)][vistec].

The contributions of Arthit Suriyawongkul to PyThaiNLP
from November 2017 until August 2019 were funded by [Wisesight][].
His contributions from November 2019 until October 2024 were made during
a PhD studentship supported by
[Taighde Éireann – Research Ireland][researchireland]
under Grant Number 18/CRT/6224
([Research Ireland Centre for Research Training in Digitally-Enhanced Reality
(d-real)][dreal]).

The contributions of Pattarawat Chormai to PyThaiNLP from 2018 until 2019
were made during a research internship at the
[Natural Language Processing Lab,
Department of Linguistics, Faculty of Arts,
Chulalongkorn University][nlp-chula].

The contributions of Korakot Chaovavanich and Lalita Lowphansirikul
to PyThaiNLP from 2019 until 2022 were funded by the
[VISTEC-depa Thailand AI Research Institute][airesearch].

The Mac Mini M1 used for macOS testing was donated by [MacStadium][].
This hardware was essential for the project's testing suite from October 2022
to October 2023, filling a critical gap before GitHub Actions introduced
native support for Apple Silicon runners.

[vistec]: https://www.vistec.ac.th/
[airesearch]: https://airesearch.in.th/
[wisesight]: https://wisesight.com/
[researchireland]: https://www.researchireland.ie/
[dreal]: https://d-real.ie/
[nlp-chula]: https://attapol.github.io/lab.html
[macstadium]: https://www.macstadium.com/

![VISTEC-depa Thailand AI Research Institute](./docs/images/airesearch-logo.png)
![MacStadium](./docs/images/macstadium-logo.png)

We have only one official repository at
<https://github.com/PyThaiNLP/pythainlp>
and another mirror at
<https://gitlab.com/pythainlp/pythainlp>.

Beware of malware if you use code from places other than these two.

Made with ❤️ | PyThaiNLP Team 💻 | "We build Thai NLP" 🇹🇭
