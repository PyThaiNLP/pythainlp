# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Corpus related functions.

Access to dictionaries, word lists, and language models.
Including download manager.
"""

from __future__ import annotations

__all__: list[str] = [
    "corpus_db_path",
    "corpus_db_url",
    "corpus_path",
    "countries",
    "download",
    "find_synonyms",
    "get_corpus",
    "get_corpus_as_is",
    "get_corpus_db",
    "get_corpus_db_detail",
    "get_corpus_default_db",
    "get_corpus_path",
    "get_hf_hub",
    "provinces",
    "remove",
    "thai_dict",
    "thai_family_names",
    "thai_female_names",
    "thai_icu_words",
    "thai_male_names",
    "thai_negations",
    "thai_orst_words",
    "thai_profanity_words",
    "thai_stopwords",
    "thai_syllables",
    "thai_synonym",
    "thai_synonyms",
    "thai_volubilis_words",
    "thai_wikipedia_titles",
    "thai_words",
    "thai_wsd_dict",
    "make_safe_directory_name",
]

from pythainlp.tools import get_full_data_path, get_pythainlp_path
from pythainlp.tools.path import safe_path_join

# Remote and local corpus databases

_CORPUS_DIRNAME: str = "corpus"
_CORPUS_PATH: str = safe_path_join(get_pythainlp_path(), _CORPUS_DIRNAME)
_CORPUS_DB_URL: str = "https://pythainlp.org/pythainlp-corpus/db.json"

# filename of local corpus catalog
_CORPUS_DB_FILENAME: str = "db.json"

# full path of local corpus catalog
_CORPUS_DB_PATH: str = get_full_data_path(_CORPUS_DB_FILENAME)


def corpus_path() -> str:
    """Get path where corpus files are kept locally."""
    return _CORPUS_PATH


def corpus_db_url() -> str:
    """Get remote URL of corpus catalog."""
    return _CORPUS_DB_URL


def corpus_db_path() -> str:
    """Get local path of corpus catalog."""
    return _CORPUS_DB_PATH


# DO NOT REORDER these pythainlp.corpus.core imports.
# These imports must come before other pythainlp.corpus.* imports
from pythainlp.corpus.core import (  # noqa: I001
    download,
    get_corpus,
    get_corpus_as_is,
    get_corpus_db,
    get_corpus_db_detail,
    get_corpus_default_db,
    get_corpus_path,
    get_hf_hub,
    make_safe_directory_name,
    remove,
)
from pythainlp.corpus.common import (
    countries,
    find_synonyms,
    provinces,
    thai_dict,
    thai_family_names,
    thai_female_names,
    thai_male_names,
    thai_negations,
    thai_orst_words,
    thai_profanity_words,
    thai_stopwords,
    thai_syllables,
    thai_synonym,
    thai_synonyms,
    thai_words,
    thai_wsd_dict,
)
from pythainlp.corpus.icu import thai_icu_words
from pythainlp.corpus.volubilis import thai_volubilis_words
from pythainlp.corpus.wikipedia import thai_wikipedia_titles
