# -*- coding: utf-8 -*-

import os
from urllib.request import urlopen

import requests
from pythainlp.tools import get_full_data_path, get_pythainlp_path
from tinydb import Query, TinyDB
from tqdm import tqdm

# Remote and local corpus databases

_CORPUS_DIRNAME = "corpus"
_CORPUS_PATH = os.path.join(get_pythainlp_path(), _CORPUS_DIRNAME)

_CORPUS_DB_URL = (
    "https://raw.githubusercontent.com/PyThaiNLP/pythainlp-corpus/2.0/db.json"
)

_CORPUS_DB_FILENAME = "db.json"
_CORPUS_DB_PATH = get_full_data_path(_CORPUS_DB_FILENAME)

if not os.path.exists(_CORPUS_DB_PATH):
    TinyDB(_CORPUS_DB_PATH)


def corpus_path():
    return _CORPUS_PATH


def corpus_db_url():
    return _CORPUS_DB_URL


def corpus_db_path():
    return _CORPUS_DB_PATH


def get_corpus(filename: str) -> frozenset:
    """
    Read corpus from file and return a frozenset

    :param string filename: file corpus
    """
    lines = []
    with open(os.path.join(corpus_path(), filename), "r", encoding="utf-8-sig") as fh:
        lines = fh.read().splitlines()

    return frozenset(lines)


def get_corpus_path(name: str) -> [str, None]:
    """
    Get corpus path

    :param string name: corpus name
    """
    db = TinyDB(corpus_db_path())
    temp = Query()

    if len(db.search(temp.name == name)) > 0:
        path = get_full_data_path(db.search(temp.name == name)[0]["file"])
        db.close()

        if not os.path.exists(path):
            download(name)

        return path

    return None


def download_(url: str, dst: str):
    """
    @param: url to download file
    @param: dst place to put the file
    """
    file_size = int(urlopen(url).info().get("Content-Length", -1))
    if os.path.exists(dst):
        first_byte = os.path.getsize(dst)
    else:
        first_byte = 0
    if first_byte >= file_size:
        return file_size
    header = {"Range": "bytes=%s-%s" % (first_byte, file_size)}
    pbar = tqdm(
        total=file_size,
        initial=first_byte,
        unit="B",
        unit_scale=True,
        desc=url.split("/")[-1],
    )
    req = requests.get(url, headers=header, stream=True)
    with (open(get_full_data_path(dst), "wb")) as f:
        for chunk in req.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                pbar.update(1024)
    pbar.close()
    # return file_size


def download(name: str, force: bool = False):
    """
    Download corpus

    :param string name: corpus name
    :param bool force: force install
    """
    db = TinyDB(corpus_db_path())
    temp = Query()
    data = requests.get(corpus_db_url())
    data_json = data.json()
    if name in list(data_json.keys()):
        temp_name = data_json[name]
        print("Download: " + name)

        if not db.search(temp.name == name):
            print(name + " " + temp_name["version"])
            download_(temp_name["download"], temp_name["file_name"])
            db.insert(
                {
                    "name": name,
                    "version": temp_name["version"],
                    "file": temp_name["file_name"],
                }
            )
        else:
            if not db.search(
                temp.name == name and temp.version == temp_name["version"]
            ):
                print("Alert: New version is ready to be updated.")
                print(
                    "from "
                    + name
                    + " "
                    + db.search(temp.name == name)[0]["version"]
                    + " update to "
                    + name
                    + " "
                    + temp_name["version"]
                )
                yes_no = "y"
                if not force:
                    yes_no = str(input("yes or no (y / n) : ")).lower()
                if "y" == yes_no:
                    download_(temp_name["download"], temp_name["file_name"])
                    db.update({"version": temp_name["version"]}, temp.name == name)
            else:
                print("Redownload")
                print(
                    "from "
                    + name
                    + " "
                    + db.search(temp.name == name)[0]["version"]
                    + " update to "
                    + name
                    + " "
                    + temp_name["version"]
                )
                yes_no = "y"
                if not force:
                    yes_no = str(input("yes or no (y / n) : ")).lower()
                if "y" == yes_no:
                    download_(temp_name["download"], temp_name["file_name"])
                    db.update({"version": temp_name["version"]}, temp.name == name)
    db.close()


def remove(name: str) -> bool:
    """
    Remove corpus

    :param string name: corpus name
    :return: True or False
    """
    db = TinyDB(corpus_db_path())
    temp = Query()
    data = db.search(temp.name == name)

    if len(data) > 0:
        path = get_corpus_path(name)
        os.remove(path)
        db.remove(temp.name == name)
        return True

    return False


from pythainlp.corpus.common import (
    countries,
    provinces,
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
    "thai_negations",
    "thai_stopwords",
    "thai_syllables",
    "thai_words",
]
