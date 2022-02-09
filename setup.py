# -*- coding: utf-8 -*-
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

Some functionalities, like named-entity recognition, required extra packages.
See https://github.com/PyThaiNLP/pythainlp for installation options.
"""

requirements = [
    "requests>=2.22.0",
    "tinydb>=3.0",
]

extras = {
    "attacut": ["attacut>=1.0.6"],
    "benchmarks": ["PyYAML>=5.3.1", "numpy>=1.16.1", "pandas>=0.24"],
    "icu": ["pyicu>=2.3"],
    "ipa": ["epitran>=1.1"],
    "ml": ["numpy>=1.16", "torch>=1.0.0"],
    "ssg": ["ssg>=0.0.8"],
    "thai2fit": ["emoji>=0.5.1", "gensim>=4.0.0", "numpy>=1.16.1"],
    "thai2rom": ["numpy>=1.16.1", "torch>=1.0.0"],
    "translate": [
        "fairseq>=0.10.0",
        "sacremoses>=0.0.41",
        "sentencepiece>=0.1.91",
        "torch>=1.0.0",
        "transformers>=4.6.0",
    ],
    "textaugment": [
        "bpemb",
        "gensim>=4.0.0"
    ],
    "wangchanberta": [
        "transformers>=4.6.0",
        "sentencepiece>=0.1.91"
    ],
    "mt5": ["transformers>=4.6.0", "sentencepiece>=0.1.91"],
    "wordnet": ["nltk>=3.3.*"],
    "generate": ["fastai<2.0"],
    "sefr_cut": ["sefr_cut>=1.1"],
    "spell": [
        "phunspell>=0.1.6",
        "spylls>=0.1.5",
        "symspellpy>=6.7.0"
    ],
    "tltk": ["tltk>=1.3.8"],
    "oskut": ["oskut>=1.3"],
    "nlpo3": ["nlpo3>=1.2.2"],
    "full": [
        "PyYAML>=5.3.1",
        "attacut>=1.0.4",
        "emoji>=0.5.1",
        "epitran>=1.1",
        "fairseq>=0.10.0",
        "gensim>=4.0.0",
        "nltk>=3.3.*",
        "numpy>=1.16.1",
        "pandas>=0.24",
        "pyicu>=2.3",
        "sacremoses>=0.0.41",
        "sentencepiece>=0.1.91",
        "ssg>=0.0.8",
        "torch>=1.0.0",
        "fastai<2.0",
        "bpemb>=0.3.2",
        "transformers>=4.6.0",
        "sefr_cut>=1.1",
        "phunspell>=0.1.6",
        "spylls>=0.1.5",
        "symspellpy>=6.7.0",
        "tltk>=1.3.8",
        "oskut>=1.3",
        "nlpo3>=1.2.2",
    ],
}

setup(
    name="pythainlp",
    version="3.0.1",
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
        "Documentation": "https://pythainlp.github.io/docs/3.0/",
        "Tutorials": "https://pythainlp.github.io/tutorials/",
        "Source Code": "https://github.com/PyThaiNLP/pythainlp",
        "Bug Tracker": "https://github.com/PyThaiNLP/pythainlp/issues",
    },
)

# TODO: Check extras and decide to download additional data, like model files
