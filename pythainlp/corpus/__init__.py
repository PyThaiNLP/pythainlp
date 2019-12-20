# -*- coding: utf-8 -*-
"""
Corpus related functions.

Access to dictionaries, word lists, and language models.
Including download manager.
"""
import hashlib
import os
from typing import NoReturn, Union
from urllib.request import urlopen

import requests
from pythainlp.tools import get_full_data_path, get_pythainlp_path
from requests.exceptions import HTTPError
from tinydb import Query, TinyDB
from tqdm import tqdm

# Remote and local corpus databases

_CORPUS_DIRNAME = "corpus"
_CORPUS_PATH = os.path.join(get_pythainlp_path(), _CORPUS_DIRNAME)

_CORPUS_DB_URL = (
    "https://raw.githubusercontent.com/"
    + "PyThaiNLP/pythainlp-corpus/"
    + "2.1/db.json"
)

_CORPUS_DB_FILENAME = "db.json"
_CORPUS_DB_PATH = get_full_data_path(_CORPUS_DB_FILENAME)

# Create a local corpus database if it does not already exist
if not os.path.exists(_CORPUS_DB_PATH):
    TinyDB(_CORPUS_DB_PATH)


def corpus_path() -> str:
    return _CORPUS_PATH


def corpus_db_url() -> str:
    return _CORPUS_DB_URL


def corpus_db_path() -> str:
    return _CORPUS_DB_PATH


def get_corpus_db_detail(name: str) -> dict:
    db = TinyDB(corpus_db_path())
    query = Query()
    res = db.search(query.name == name)
    db.close()

    if res:
        return res[0]
    else:
        return dict()


def get_corpus(filename: str) -> frozenset:
    """
    Read corpus from file and return a frozenset.

    (Please see the filename from
    `this file
    <https://github.com/PyThaiNLP/pythainlp-corpus/blob/master/db.json>`_

    :param string filename: filename of the corpus to be read

    :return: :mod:`frozenset` consist of lines in the file
    :rtype: :mod:`frozenset`

    :Example:
    ::

        from pythainlp.corpus import get_corpus

        get_corpus('negations_th.txt')
        # output:
        # frozenset({'แต่', 'ไม่'})

        get_corpus('ttc_freq.txt')
        # output:
        # frozenset({'โดยนัยนี้\\t1',
        #    'ตัวบท\\t10',
        #    'หยิบยื่น\\t3',
        #    'เอย\\t555',
        #    'ค้าน\\t69',
        #    'เหนี่ยง\\t3',
        #    'ชงฆ์\\t3',
        #     ...})
    """
    path = os.path.join(corpus_path(), filename)
    lines = []
    with open(path, "r", encoding="utf-8-sig") as fh:
        lines = fh.read().splitlines()

    return frozenset(lines)


def get_corpus_path(name: str) -> Union[str, None]:
    """
    Get corpus path.

    :param string name: corpus name
    :return: path to the corpus or **None** of the corpus doesn't
             exist in the device
    :rtype: str

    :Example:

    If the corpus already exists::

        from pythainlp.corpus import get_corpus_path

        print(get_corpus_path('ttc'))
        # output: /root/pythainlp-data/ttc_freq.txt

    If the corpus has not been downloaded yet::

        from pythainlp.corpus import download, get_corpus_path

        print(get_corpus_path('wiki_lm_lstm'))
        # output: None

        download('wiki_lm_lstm')
        # output:
        # Download: wiki_lm_lstm
        # wiki_lm_lstm 0.32
        # thwiki_lm.pth?dl=1: 1.05GB [00:25, 41.5MB/s]
        # /root/pythainlp-data/thwiki_model_lstm.pth

        print(get_corpus_path('wiki_lm_lstm'))
        # output: /root/pythainlp-data/thwiki_model_lstm.pth
    """
    db = TinyDB(corpus_db_path())
    query = Query()
    path = None

    if db.search(query.name == name):
        path = get_full_data_path(db.search(query.name == name)[0]["file"])

        if not os.path.exists(path):
            download(name)

    db.close()
    return path


def _download(url: str, dst: str) -> int:
    """
    Download helper.

    @param: url to download file
    @param: dst place to put the file
    """
    _CHUNK_SIZE = 1024 * 64

    file_size = int(urlopen(url).info().get("Content-Length", -1))
    r = requests.get(url, stream=True)
    with open(get_full_data_path(dst), "wb") as f:
        pbar = tqdm(total=int(r.headers["Content-Length"]))
        for chunk in r.iter_content(chunk_size=_CHUNK_SIZE):
            if chunk:
                f.write(chunk)
                pbar.update(len(chunk))
        pbar.close()
    return file_size


def _check_hash(dst: str, md5: str) -> NoReturn:
    """
    Check hash helper.

    @param: dst place to put the file
    @param: md5 place to hash the file (MD5)
    """
    if md5 and md5 != "-":
        with open(get_full_data_path(dst), "rb") as f:
            content = f.read()
            file_md5 = hashlib.md5(content).hexdigest()

            if md5 != file_md5:
                raise Exception("Hash does not match expected.")


def download(name: str, force: bool = False) -> NoReturn:
    """
    Download corpus.

    The available corpus names can be seen in this file:
    https://github.com/PyThaiNLP/pythainlp-corpus/blob/master/db.json

    :param string name: corpus name
    :param bool force: force download

    :Example:
    ::

        from pythainlp.corpus import download

        download('wiki_lm_lstm', force=True)
        # output:
        # Corpus: wiki_lm_lstm
        # - Downloading: wiki_lm_lstm 0.1
        # thwiki_lm.pth:  26%|██▌       | 114k/434k [00:00<00:00, 690kB/s]

    By default, downloaded corpus and model will be saved in ``$HOME/pythainlp-data/``
    (e.g. ``/Users/bact/pythainlp-data/wiki_lm_lstm.pth``).
    """
    local_db = TinyDB(corpus_db_path())
    query = Query()

    try:
        corpus_data = requests.get(corpus_db_url())
    except HTTPError as http_err:
        print(f"Cannot download corpus data from: {corpus_db_url()}")
        print(f"HTTP error occurred: {http_err}")
        return
    except Exception as err:
        print(f"Cannot download corpus data from: {corpus_db_url()}")
        print(f"Non-HTTP error occurred: {err}")
        return

    corpus_data = corpus_data.json()

    if name in list(corpus_data.keys()):
        corpus = corpus_data[name]
        print("Corpus:", name)
        found = local_db.search(query.name == name)

        # If not found in local, download
        if force or not found:
            print(f"- Downloading: {name} {corpus['version']}")
            _download(corpus["download"], corpus["file_name"])
            _check_hash(corpus["file_name"], corpus["md5"])

            if found:
                local_db.update(
                    {"version": corpus["version"]}, query.name == name
                )
            else:
                local_db.insert(
                    {
                        "name": name,
                        "version": corpus["version"],
                        "file": corpus["file_name"],
                    }
                )
        else:
            if local_db.search(
                query.name == name and query.version == corpus["version"]
            ):
                # Already has the same version
                print("- Already up to date.")
            else:
                # Has the corpus but different version
                current_ver = local_db.search(query.name == name)[0]["version"]
                print(f"- Existing version: {current_ver}")
                print(f"- New version available: {corpus['version']}")
                print("- Use download(data_name, force=True) to update")
    else:
        print("Corpus not found:", name)

    local_db.close()


def remove(name: str) -> bool:
    """
    Remove corpus

    :param string name: corpus name
    :return: **True** if the corpus is found and succesfully removed.
             Otherwise, it returns **False**.
    :rtype: bool

    :Example:
    ::

        from pythainlp.corpus import remove, get_corpus_path, get_corpus

        print(remove('ttc'))
        # output: True

        print(get_corpus_path('ttc'))
        # output: None

        get_corpus('ttc')
        # output:
        # FileNotFoundError: [Errno 2] No such file or directory:
        # '/usr/local/lib/python3.6/dist-packages/pythainlp/corpus/ttc'
    """
    db = TinyDB(corpus_db_path())
    query = Query()
    data = db.search(query.name == name)

    if data:
        path = get_corpus_path(name)
        os.remove(path)
        db.remove(query.name == name)
        db.close()
        return True

    db.close()
    return False


from pythainlp.corpus.common import (
    countries,
    provinces,
    thai_female_names,
    thai_male_names,
    thai_negations,
    thai_stopwords,
    thai_syllables,
    thai_words,
)


__all__ = [
    "corpus_path",
    "corpus_db_path",
    "corpus_db_url",
    "countries",
    "download",
    "get_corpus",
    "get_corpus_path",
    "provinces",
    "remove",
    "thai_female_names",
    "thai_male_names",
    "thai_negations",
    "thai_stopwords",
    "thai_syllables",
    "thai_words",
    "get_corpus_db_detail",
]
