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
transliteration, soundex generation, and spell checking.

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


Made with ❤️

PyThaiNLP Team

"We build Thai NLP"
"""

requirements = [
    "dill>=0.3.0",
    "nltk>=3.3",
    "python-crfsuite>=0.9.6",
    "requests>=2.22.0",
    "tinydb>=3.0",
    "tqdm>=4.1",
]

extras = {
    "attacut": ["attacut>=1.0.6"],
    "benchmarks": ["numpy>=1.16", "pandas>=0.24"],
    "icu": ["pyicu>=2.3"],
    "ipa": ["epitran>=1.1"],
    "ml": ["numpy>=1.16", "torch>=1.0.0"],
    "ner": ["sklearn-crfsuite>=0.3.6"],
    "ssg": ["ssg>=0.0.6"],
    "thai2fit": ["emoji>=0.5.1", "gensim>=3.2.0", "numpy>=1.16"],
    "thai2rom": ["torch>=1.0.0", "numpy>=1.16"],
    "full": [
        "attacut>=1.0.4",
        "emoji>=0.5.1",
        "epitran>=1.1",
        "gensim>=3.2.0",
        "numpy>=1.16",
        "pandas>=0.24",
        "pyicu>=2.3",
        "sklearn-crfsuite>=0.3.6",
        "ssg>=0.0.6",
        "torch>=1.0.0",
    ],
}

setup(
    name="pythainlp",
    version="2.2.0-dev0",
    description="Thai Natural Language Processing library",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="PyThaiNLP",
    author_email="wannaphong@kkumail.com",
    url="https://github.com/PyThaiNLP/pythainlp",
    packages=find_packages(),
    test_suite="tests",
    python_requires=">=3.6",
    package_data={
        "pythainlp.corpus": [
            "corpus_license.md",
            "countries_th.txt",
            "etcc.txt",
            "negations_th.txt",
            "orchid_pos_th.json",
            "orchid_pt_tagger.dill",
            "person_names_female_th.txt",
            "person_names_male_th.txt",
            "sentenceseg-ted.model",
            "stopwords_th.txt",
            "syllables_th.txt",
            "tha-wn.db",
            "thailand_provinces_th.txt",
            "tnc_freq.txt",
            "ttc_freq.txt",
            "ud_thai_pud_pt_tagger.dill",
            "ud_thai_pud_unigram_tagger.dill",
            "words_th_thai2fit_201810.txt",
            "words_th.txt",
        ],
    },
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
    scripts=[
        "bin/word-tokenization-benchmark",
    ],
    entry_points={
        "console_scripts": [
            "thainlp = pythainlp.__main__:main",
        ],
    },
    project_urls={
        "Documentation": "https://www.thainlp.org/pythainlp/docs/dev/",
        "Source": "https://github.com/PyThaiNLP/pythainlp",
        "Bug Reports": "https://github.com/PyThaiNLP/pythainlp/issues",
    },
)

# TODO: Check extras and decide to download additional data, like model files
