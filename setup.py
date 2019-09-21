# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

readme = """
![PyThaiNLP Logo](https://avatars0.githubusercontent.com/u/32934255?s=200&v=4)

PyThaiNLP is a Python library for Thai natural language processing.
It includes word tokenizers, transliterators, soundex converters, part-of-speech taggers, and spell checkers.

## Install

For stable version:

```sh
pip install pythainlp
```

Some functionalities, like word vector, required extra packages. See https://github.com/PyThaiNLP/pythainlp for installation options.

**Note for Windows**: `marisa-trie` wheels can be obtained from https://www.lfd.uci.edu/~gohlke/pythonlibs/#marisa-trie
Install it with pip, for example: `pip install marisa_trie‑xxx.whl`
"""

requirements = [
    "dill=>0.3.0,<1",
    "marisa-trie=>0.7.5,<1",
    "nltk=>3.4.5,<4",
    "requests=>2.22.0,<3",
    "tinydb=>3.13.0,<4",
    "tqdm=>4.35.0,<5",
]

extras = {
    "artagger": ["artagger"],
    "attacut": ["attacut"],
    "benchmarks": ["numpy", "pandas"],
    "deepcut": ["deepcut", "keras", "tensorflow"],
    "icu": ["pyicu"],
    "ipa": ["epitran"],
    "ml": ["keras", "numpy", "torch"],
    "ner": ["sklearn-crfsuite"],
    "ssg": ["ssg"],
    "thai2fit": ["emoji", "gensim", "numpy"],
    "thai2rom": ["torch", "numpy"],
    "wordnet": ["nltk"],
    "full": [
        "artagger",
        "attacut",
        "deepcut",
        "epitran",
        "gensim",
        "keras",
        "numpy",
        "pyicu",
        "sklearn-crfsuite",
        "tensorflow",
        "torch",
        "ssg",
        "emoji",
        "pandas",
    ],
}

setup(
    name="pythainlp",
    version="2.1.dev4",
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
