# -*- coding: utf-8 -*-
# Copyright (C) 2016-2023 PyThaiNLP Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
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
    "get_corpus_default_db",
    "get_corpus_path",
    "provinces",
    "remove",
    "thai_dict",
    "thai_family_names",
    "thai_female_names",
    "thai_male_names",
    "thai_negations",
    "thai_synonym",
    "thai_stopwords",
    "thai_syllables",
    "thai_words",
    "thai_wsd_dict",
    "thai_orst_words",
    "path_pythainlp_corpus",
    "get_path_folder_corpus",
]

import os

from pythainlp.tools import get_full_data_path, get_pythainlp_path

# Remote and local corpus databases

_CORPUS_DIRNAME = "corpus"
_CORPUS_PATH = os.path.join(get_pythainlp_path(), _CORPUS_DIRNAME)
_CHECK_MODE = os.getenv("PYTHAINLP_READ_MODE")

# remote corpus catalog URL
_CORPUS_DB_URL = "https://pythainlp.github.io/pythainlp-corpus/db.json"

# local corpus catalog filename
_CORPUS_DB_FILENAME = "db.json"

# local corpus catalog full path
_CORPUS_DB_PATH = get_full_data_path(_CORPUS_DB_FILENAME)

# create a local corpus database if it does not already exist
if not os.path.exists(_CORPUS_DB_PATH) and _CHECK_MODE != "1":
    with open(_CORPUS_DB_PATH, "w", encoding="utf-8") as f:
        f.write(r'{"_default": {}}')


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
    get_corpus_default_db,
    get_corpus_path,
    get_path_folder_corpus,
    remove,
    path_pythainlp_corpus,
)  # these imports must come before other pythainlp.corpus.* imports
from pythainlp.corpus.common import (
    countries,
    provinces,
    thai_family_names,
    thai_female_names,
    thai_male_names,
    thai_negations,
    thai_synonym,
    thai_stopwords,
    thai_syllables,
    thai_words,
    thai_orst_words,
    thai_dict,
    thai_wsd_dict
)
