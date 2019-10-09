# -*- coding: utf-8 -*-

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
    + "master/db.json"
)

_CORPUS_DB_FILENAME = "db.json"
_CORPUS_DB_PATH = get_full_data_path(_CORPUS_DB_FILENAME)

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
    return db.search(query.name == name)[0]


def read_text_corpus(path: str) -> list:
    lines = []
    with open(path, "r", encoding="utf-8-sig") as fh:
        lines = fh.read().splitlines()
    return lines


def get_corpus(filename: str) -> frozenset:
    """
    Read corpus from file and return a frozenset (Please see the filename from
    `this file
    <https://github.com/PyThaiNLP/pythainlp-corpus/blob/master/db.json>`_

    :param string filename: filename of the corpus to be read

    :return: :mod:`frozenset` consist of lines in the file
    :rtype: :mod:`frozenset`

    :Example:
    ::

        from pythainlp.corpus import get_corpus

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

        get_corpus('negations_th.txt')
        # output:
        # frozenset({'แต่', 'ไม่'})
    """
    lines = read_text_corpus(os.path.join(corpus_path(), filename))

    return frozenset(lines)


def get_corpus_path(name: str) -> Union[str, None]:
    """
    Get corpus path

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
    @param: url to download file
    @param: dst place to put the file
    """
    file_size = int(urlopen(url).info().get("Content-Length", -1))
    r = requests.get(url, stream=True)
    with open(get_full_data_path(dst), "wb") as f:
        pbar = tqdm(total=int(r.headers["Content-Length"]))
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                pbar.update(len(chunk))
        pbar.close()
    return file_size


def _check_hash(dst: str, md5: str) -> NoReturn:
    """
    @param: dst place to put the file
    @param: md5 place to hash the file (MD5)
    """
    if md5 and md5 != "-":
        hashfile = hashlib.md5(
            open(get_full_data_path(dst), "rb").read()
        ).hexdigest()
        if md5 != hashfile:
            raise Exception("Hash does not match expected.")
        else:
            pass
    else:
        pass


def download(name: str, force: bool = False) -> NoReturn:
    """
    Download corpus.
    The available corpus names can be seen in this file:
    https://github.com/PyThaiNLP/pythainlp-corpus/blob/master/db.json

    :param string name: corpus name
    :param bool force: force install

    :Example:
    ::

        from pythainlp.corpus import download

        download('ttc', force=True)
        # output:
        # Download: ttc
        # ttc 0.1
        # ttc_freq.txt:  26%|██▌       | 114k/434k [00:00<00:00, 690kB/s]
        # /root/pythainlp-data/ttc_freq.txt
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
        print("Download:", name)

        # If not found in local, download
        if not local_db.search(query.name == name):
            print(f"Downloading: {name} {corpus['version']}")
            _download(corpus["download"], corpus["file_name"])
            _check_hash(corpus["file_name"], corpus["md5"])
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
                # Already as the same version
                print("Already up to date.")
            else:
                # Has the corpus but different version, update
                current_ver = local_db.search(query.name == name)[0]["version"]
                print(f"Updating: {name} {current_ver} to {corpus['version']}")
                _download(corpus["download"], corpus["file_name"])
                _check_hash(corpus["file_name"], corpus["md5"])
                local_db.update(
                    {"version": corpus["version"]}, query.name == name
                )

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
        return True

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
