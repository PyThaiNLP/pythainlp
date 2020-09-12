# -*- coding: utf-8 -*-
"""
Corpus related functions.

Access to dictionaries, word lists, and language models.
Including download manager.
"""

__all__ = [
    "corpus_path",
    "corpus_db_path",
    "corpus_db_url",
    "countries",
    "download",
    "get_corpus",
    "get_corpus_db",
    "get_corpus_db_detail",
    "get_corpus_path",
    "provinces",
    "remove",
    "thai_family_names",
    "thai_female_names",
    "thai_male_names",
    "thai_negations",
    "thai_stopwords",
    "thai_syllables",
    "thai_words",
]

import os
from tinydb import TinyDB

from pythainlp.tools import get_full_data_path, get_pythainlp_path

# Remote and local corpus databases

_CORPUS_DIRNAME = "corpus"
_CORPUS_PATH = os.path.join(get_pythainlp_path(), _CORPUS_DIRNAME)

# remote corpus catalog URL
_CORPUS_DB_URL = (
    "https://raw.githubusercontent.com/"
    "PyThaiNLP/pythainlp-corpus/"
    "2.2/db.json"
)

# local corpus catalog filename
_CORPUS_DB_FILENAME = "db.json"

# local corpus catalog full path
_CORPUS_DB_PATH = get_full_data_path(_CORPUS_DB_FILENAME)

# create a local corpus database if it does not already exist
if not os.path.exists(_CORPUS_DB_PATH):
    TinyDB(_CORPUS_DB_PATH)


def corpus_path() -> str:
    """
    Get path where corpus files are kept locally.
    """
    return _CORPUS_PATH


def corpus_db_url() -> str:
    """
    Get remote URL of corpus catalog.
    """
    return _CORPUS_DB_URL


def corpus_db_path() -> str:
    """
    Get local path of corpus catalog.
    """
    return _CORPUS_DB_PATH


from pythainlp.corpus.core import (
    download,
    get_corpus,
    get_corpus_db,
    get_corpus_db_detail,
    get_corpus_path,
    remove,
)  # these imports must come before other pythainlp.corpus.* imports
from pythainlp.corpus.common import (
    countries,
    provinces,
    thai_family_names,
    thai_female_names,
    thai_male_names,
    thai_negations,
    thai_stopwords,
    thai_syllables,
    thai_words,
)
