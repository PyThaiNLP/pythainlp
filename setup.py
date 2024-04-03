# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
"""
Setup script for PyThaiNLP.

https://github.com/PyThaiNLP/pythainlp
"""
from setuptools import find_packages, setup

readme = """
![PyThaiNLP Logo](https://avatars0.githubusercontent.com/u/32934255?s=200&v=4)

PyThaiNLP is a Python library for Thai natural language processing.
The library provides functions like word tokenization, part-of-speech tagging,
transliteration, soundex generation, spell checking, and
date and time parsing/formatting.

Website: [pythainlp.github.io](https://pythainlp.github.io/)

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
    "requests>=2.22.0",
    "backports.zoneinfo; python_version<'3.9'",
    "tzdata; sys_platform == 'win32'"
]

extras = {
    "attacut": ["attacut>=1.0.6"],
    "benchmarks": ["PyYAML>=5.3.1", "numpy>=1.22", "pandas>=0.24"],
    "icu": ["pyicu>=2.3"],
    "ipa": ["epitran>=1.1"],
    "ml": ["numpy>=1.22", "torch>=1.0.0"],
    "ssg": ["ssg>=0.0.8"],
    "thai2fit": ["emoji>=0.5.1", "gensim>=4.0.0", "numpy>=1.22"],
    "thai2rom": ["numpy>=1.22", "torch>=1.0.0"],
    "translate": [
        "fairseq>=0.10.0",
        "sacremoses>=0.0.41",
        "sentencepiece>=0.1.91",
        "torch>=1.0.0",
        "transformers>=4.6.0",
    ],
    "wunsen": ["wunsen>=0.0.1"],
    "textaugment": [
        "bpemb",
        "gensim>=4.0.0"
    ],
    "wangchanberta": [
        "transformers>=4.6.0",
        "sentencepiece>=0.1.91"
    ],
    "mt5": ["transformers>=4.6.0", "sentencepiece>=0.1.91"],
    "wtp": ["transformers>=4.6.0", "wtpsplit>=1.0.1"],
    "wordnet": ["nltk>=3.3"],
    "generate": ["fastai<2.0"],
    "sefr_cut": ["sefr_cut>=1.1"],
    "spell": [
        "phunspell>=0.1.6",
        "spylls>=0.1.5",
        "symspellpy>=6.7.6"
    ],
    "oskut": ["oskut>=1.3"],
    "nlpo3": ["nlpo3>=1.2.2"],
    "onnx": [
        "sentencepiece>=0.1.91",
        "numpy>=1.22",
        "onnxruntime>=1.10.0"
    ],
    "thai_nner": ["thai_nner"],
    "esupar": [
        "esupar>=1.3.8",
        "numpy",
        "transformers>=4.22.1",
    ],
    "spacy_thai": ["spacy_thai>=0.7.1"],
    "transformers_ud": [
        "ufal.chu-liu-edmonds>=1.0.2",
        "transformers>=4.22.1",
    ],
    "dependency_parsing": [
        "spacy_thai>=0.7.1",
        "ufal.chu-liu-edmonds>=1.0.2",
        "transformers>=4.22.1",
    ],
    "coreference_resolution":{
        "spacy>=3.0",
        "fastcoref>=2.1.5",
    },
    "word_approximation":{
        "panphon>=0.20.0"
    },
    "wangchanglm": [
        "transformers>=4.6.0",
        "sentencepiece>=0.1.91",
        "pandas>=0.24"
    ],
    "wsd":{
        "sentence-transformers>=2.2.2"
    },
    "el":{
        "multiel>=0.5"
    },
    "abbreviation":{
        "khamyo>=0.2.0"
    },
    "full": [
        "PyYAML>=5.3.1",
        "attacut>=1.0.4",
        "emoji>=0.5.1",
        "epitran>=1.1",
        "fairseq>=0.10.0",
        "gensim>=4.0.0",
        "nltk>=3.3",
        "numpy>=1.22",
        "pandas>=0.24",
        "pyicu>=2.3",
        "sacremoses>=0.0.41",
        "sentencepiece>=0.1.91",
        "ssg>=0.0.8",
        "torch>=1.0.0",
        "fastai<2.0",
        "bpemb>=0.3.2",
        "transformers>=4.22.1",
        "sefr_cut>=1.1",
        "phunspell>=0.1.6",
        "spylls>=0.1.5",
        "symspellpy>=6.7.6",
        "oskut>=1.3",
        "nlpo3>=1.2.2",
        "onnxruntime>=1.10.0",
        "thai_nner",
        "wunsen>=0.0.3",
        "wtpsplit>=1.0.1",
        "spacy_thai>=0.7.1",
        "spacy>=3.0",
        "fastcoref>=2.1.5",
        "ufal.chu-liu-edmonds>=1.0.2",
        "panphon>=0.20.0",
        "sentence-transformers>=2.2.2",
        "khamyo>=0.2.0",
    ],
}

setup(
    name="pythainlp",
    version="5.0.2",
    description="Thai Natural Language Processing library",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="PyThaiNLP",
    author_email="email@wannaphong.com",
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
    license="Apache Software License 2.0",
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
        "Documentation": "https://pythainlp.github.io/docs/5.0/",
        "Tutorials": "https://pythainlp.github.io/tutorials/",
        "Source Code": "https://github.com/PyThaiNLP/pythainlp",
        "Bug Tracker": "https://github.com/PyThaiNLP/pythainlp/issues",
    },
)

# TODO: Check extras and decide whether or not additional data, like model files, should be downloaded
