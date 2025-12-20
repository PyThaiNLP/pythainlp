# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2025 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""
Setup script for PyThaiNLP.

https://github.com/PyThaiNLP/pythainlp
"""

from setuptools import find_packages, setup

PYYAML = "PyYAML>=5.4.1"
PANDAS = "pandas>=0.24"
NUMPY = "numpy>=1.22"

LONG_DESC = """
![PyThaiNLP Logo](https://avatars0.githubusercontent.com/u/32934255?s=200&v=4)

PyThaiNLP is a Python library for Thai natural language processing.
The library provides functions like word tokenization, part-of-speech tagging,
transliteration, soundex generation, spell checking, and
date and time parsing/formatting.

Website: [pythainlp.github.io](https://pythainlp.org/)

# Install

For stable version:

```sh
pip install pythainlp
```

For development version:

```sh
pip install --upgrade --pre pythainlp
```

Some functionalities, like named-entity recognition, require extra packages.
See https://github.com/PyThaiNLP/pythainlp for installation options.
"""

requirements = [
    "backports.zoneinfo; python_version<'3.9'",
    "requests>=2.31",
    PYYAML,
    PANDAS,
    NUMPY,
    "tzdata; sys_platform == 'win32'",
]

extras = {
    "abbreviation": ["khamyo>=0.2.0"],
    "attacut": ["attacut>=1.0.6"],
    "benchmarks": [PYYAML, NUMPY, PANDAS],
    "coreference_resolution": [
        "fastcoref>=2.1.5",
        "spacy>=3.0",
    ],
    "dependency_parsing": [
        "spacy_thai>=0.7.1",
        "transformers>=4.22.1",
        "ufal.chu-liu-edmonds>=1.0.2",
    ],
    "el": ["multiel>=0.5"],
    "esupar": [
        "esupar>=1.3.8",
        "numpy",
        "transformers>=4.22.1",
    ],
    "generate": ["fastai<2.0"],
    "icu": ["pyicu>=2.3"],
    "ipa": ["epitran>=1.1"],
    "ml": [NUMPY, "torch>=1.0.0"],
    "mt5": ["sentencepiece>=0.1.91", "transformers>=4.6.0"],
    "nlpo3": ["nlpo3>=1.3.1"],
    "onnx": [NUMPY, "onnxruntime>=1.10.0", "sentencepiece>=0.1.91"],
    "oskut": ["oskut>=1.3"],
    "sefr_cut": ["sefr_cut>=1.1"],
    "spacy_thai": ["spacy_thai>=0.7.1"],
    "spell": ["phunspell>=0.1.6", "symspellpy>=6.7.6"], 
    "ssg": ["ssg>=0.0.8"],
    "textaugment": ["bpemb", "gensim>=4.0.0"],
    "thai_nner": ["thai_nner"],
    "thai2fit": ["emoji>=0.5.1", "gensim>=4.0.0", NUMPY],
    "thai2rom": [NUMPY, "torch>=1.0.0"],
    "budoux": ["budoux>=0.7.0"],
    "translate": [
        'fairseq>=0.10.0,<0.13;python_version<"3.11"',
        'fairseq-fixed==0.12.3.1,<0.13;python_version>="3.11"',
        "sacremoses>=0.0.41",
        "sentencepiece>=0.1.91",
        "torch>=1.0.0",
        "transformers>=4.6.0",
        "word2word>=1.0.0"
    ],
    "transformers_ud": [
        "transformers>=4.22.1",
        "ufal.chu-liu-edmonds>=1.0.2",
    ],
    "wangchanberta": ["sentencepiece>=0.1.91", "transformers>=4.6.0"],
    "wangchanglm": [
        PANDAS,
        "sentencepiece>=0.1.91",
        "transformers>=4.6.0",
    ],
    "word_approximation": ["panphon>=0.20.0"],
    "wordnet": ["nltk>=3.3"],
    "wsd": ["sentence-transformers>=2.2.2"],
    "wtp": ["transformers>=4.6.0", "wtpsplit>=1.0.1"],
    "wunsen": ["wunsen>=0.0.1"],
    # Compact dependencies, this one matches requirements.txt
    "compact": [
        PYYAML,
        "nlpo3>=1.3.1",
        NUMPY,
        "pyicu>=2.3",
        "python-crfsuite>=0.9.7",
    ],
    # Full dependencies
    "full": [
        PYYAML,
        "attacut>=1.0.4",
        "bpemb>=0.3.2",
        "emoji>=0.5.1",
        "epitran>=1.1",
        'fairseq>=0.10.0,<0.13;python_version<"3.11"',
        'fairseq-fixed==0.12.3.1,<0.13;python_version>="3.11"',
        "fastai<2.0",
        "fastcoref>=2.1.5",
        "gensim>=4.0.0",
        "khamyo>=0.2.0",
        "nlpo3>=1.3.1",
        "nltk>=3.3",
        NUMPY,
        "onnxruntime>=1.10.0",
        "oskut>=1.3",
        PANDAS,
        "panphon>=0.20.0",
        "phunspell>=0.1.6",
        "pyicu>=2.3",
        "sacremoses>=0.0.41",
        "sefr_cut>=1.1",
        "sentencepiece>=0.1.91",
        "sentence-transformers>=2.2.2",
        "spacy>=3.0",
        "spacy_thai>=0.7.1",
        "ssg>=0.0.8",
        "symspellpy>=6.7.6",
        "thai_nner",
        "torch>=1.0.0",
        "transformers>=4.22.1",
        "ufal.chu-liu-edmonds>=1.0.2",
        "wtpsplit>=1.0.1",
        "wunsen>=0.0.3",
        "word2word>=1.0.0",
        "budoux>=0.7.0",
    ],
}

setup(
    name="pythainlp",
    version="5.2.0",
    description="Thai Natural Language Processing library",
    long_description=LONG_DESC,
    long_description_content_type="text/markdown",
    author="PyThaiNLP",
    author_email="wannaphong@pythainlp.org",
    url="https://github.com/PyThaiNLP/pythainlp",
    packages=find_packages(exclude=["tests", "tests.*"]),
    test_suite="tests",
    python_requires=">=3.7",
    package_data={
        "pythainlp": [
            "corpus/*",
        ],
    },
    include_package_data=True,
    install_requires=requirements,
    extras_require=extras,
    license="Apache-2.0",
    zip_safe=False,
    keywords=[
        "pythainlp",
        "NLP",
        "natural language processing",
        "text analytics",
        "text processing",
        "localization",
        "computational linguistics",
        "ThaiNLP",
        "Thai NLP",
        "Thai language",
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: Thai",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Text Processing",
        "Topic :: Text Processing :: General",
        "Topic :: Text Processing :: Linguistic",
    ],
    entry_points={
        "console_scripts": [
            "thainlp = pythainlp.__main__:main",
        ],
    },
    project_urls={
        "Documentation": "https://pythainlp.org/docs/5.2/",
        "Tutorials": "https://pythainlp.org/tutorials/",
        "Source Code": "https://github.com/PyThaiNLP/pythainlp",
        "Bug Tracker": "https://github.com/PyThaiNLP/pythainlp/issues",
    },
)

# TODO: Check extras and decide whether or not additional data, like model files, should be downloaded
