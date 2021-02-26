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
    "python-crfsuite>=0.9.6",
    "requests>=2.22.0",
    "tinydb>=3.0",
]

extras = {
    "attacut": ["attacut>=1.0.6"],
    "benchmarks": ["PyYAML>=5.3.1", "numpy>=1.16.1", "pandas>=0.24"],
    "icu": ["pyicu>=2.3"],
    "ipa": ["epitran>=1.1"],
    "ml": ["numpy>=1.16", "torch>=1.0.0"],
    "ssg": ["ssg>=0.0.6"],
    "thai2fit": ["emoji>=0.5.1", "gensim>=3.2.0", "numpy>=1.16.1"],
    "thai2rom": ["numpy>=1.16.1", "torch>=1.0.0"],
    "translate": [
        "fairseq>=0.10.0",
        "sacremoses>=0.0.41",
        "sentencepiece>=0.1.91",
        "torch>=1.0.0",
    ],
    "wangchanberta": ["transformers", "sentencepiece"],
    "mt5": ["transformers>=4.1.1", "sentencepiece>=0.1.91"],
    "wordnet": ["nltk>=3.3.*"],
    "full": [
        "PyYAML>=5.3.1",
        "attacut>=1.0.4",
        "emoji>=0.5.1",
        "epitran>=1.1",
        "fairseq>=0.10.0",
        "gensim>=3.2.0",
        "nltk>=3.3.*",
        "numpy>=1.16.1",
        "pandas>=0.24",
        "pyicu>=2.3",
        "sacremoses>=0.0.41",
        "sentencepiece>=0.1.91",
        "ssg>=0.0.6",
        "torch>=1.0.0",
        "transformers>=4.1.1",
    ],
}

setup(
    name="pythainlp",
    version="2.3.0dev0",
    description="Thai Natural Language Processing library",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="PyThaiNLP",
    author_email="wannaphong@kkumail.com",
    url="https://github.com/PyThaiNLP/pythainlp",
    packages=find_packages(exclude=["tests", "tests.*"]),
    test_suite="tests",
    python_requires=">=3.6",
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
        "Documentation": "https://www.thainlp.org/pythainlp/docs/2.2/",
        "Tutorials": "https://www.thainlp.org/pythainlp/tutorials/",
        "Source Code": "https://github.com/PyThaiNLP/pythainlp",
        "Bug Tracker": "https://github.com/PyThaiNLP/pythainlp/issues",
    },
)

# TODO: Check extras and decide to download additional data, like model files
