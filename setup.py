# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

readme = """
![PyThaiNLP Logo](https://avatars0.githubusercontent.com/u/32934255?s=200&v=4)

PyThaiNLP is a Python library for Thai natural language processing.
The library provides functions like word tokenization, part-of-speech tagging,
transliteration, soundex generation, and spell checking.

## Install

For stable version:

```sh
pip install pythainlp
```

Some functionalities, like word vector, required extra packages.
See https://github.com/PyThaiNLP/pythainlp for installation options.

**Note for Windows**: `marisa-trie` wheels can be obtained from
https://www.lfd.uci.edu/~gohlke/pythonlibs/#marisa-trie
Install it with pip, for example: `pip install marisa_trie‑xxx.whl`
"""

requirements = [
    "dill>=0.3.0,<1",
    "marisa-trie>=0.7.5,<1",
    "nltk>=3.4.5,<4",
    "requests>=2.22.0,<3",
    "tinydb>=3.13.0,<4",
    "tqdm>=4.35.0,<5",
]

extras = {
    "artagger": ["artagger>=0.1.0.3"],
    "attacut": ["attacut>=1.0.2"],
    "benchmarks": ["numpy>=1.17.2", "pandas>=0.25.1"],
    "deepcut": ["deepcut>=0.6.1.0", "keras>=2.3.0", "tensorflow>=1.14.0"],
    "icu": ["pyicu>=2.3.1"],
    "ipa": ["epitran>=1.1"],
    "ml": ["keras>=2.3.0", "numpy>=1.17.2", "torch>=1.2.0"],
    "ner": ["sklearn-crfsuite>=0.3.6"],
    "ssg": ["ssg>=0.0.4"],
    "thai2fit": ["emoji>0.5.4", "gensim>=3.8.0", "numpy>=1.17.2"],
    "thai2rom": ["torch>=1.2.0", "numpy>=1.17.2"],
    "full": [
        "artagger>=0.1.0.3",
        "attacut>=1.0.2",
        "deepcut>=0.6.1.0",
        "epitran>=1.1",
        "gensim>=3.8.0",
        "keras>=2.3.0",
        "numpy>=1.17.2",
        "pyicu>=2.3.1",
        "sklearn-crfsuite>=0.3.6",
        "tensorflow>=1.14.0",
        "torch>=1.2.0",
        "ssg>=0.0.4",
        "emoji>=0.5.4",
        "pandas>=0.25.1",
    ],
}

setup(
    name="pythainlp",
    version="2.1.dev5",
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
            "negations_th.txt",
            "orchid_pos_th.json",
            "orchid_pt_tagger.dill",
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
       "ThaiNLP",
       "text processing",
       "localization",
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
        'bin/pythainlp',
        'bin/word-tokenization-benchmark',
    ]
)

# TODO: Check extras and decide to download additional data, like model files
