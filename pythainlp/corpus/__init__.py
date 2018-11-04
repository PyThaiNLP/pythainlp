# -*- coding: utf-8 -*-

import os

from pythainlp.tools import get_full_data_path, get_pythainlp_path
import requests
from tinydb import Query, TinyDB
from tqdm import tqdm
from urllib.request import urlopen

_CORPUS_DIRNAME = "corpus"
CORPUS_PATH = os.path.join(get_pythainlp_path(), _CORPUS_DIRNAME)

_CORPUS_DB_URL = (
    "https://raw.githubusercontent.com/PyThaiNLP/pythainlp-corpus/master/db.json"
)
_CORPUS_DB_FILENAME = "db.json"
CORPUS_DB_PATH = get_full_data_path(_CORPUS_DB_FILENAME)
if not os.path.exists(CORPUS_DB_PATH):
    TinyDB(CORPUS_DB_PATH)

_THAI_COUNTRIES_FILENAME = "countries_th.txt"
_THAI_THAILAND_PROVINCES_FILENAME = "thailand_provinces_th.txt"
_THAI_SYLLABLES_FILENAME = "syllables_th.txt"
_THAI_WORDS_FILENAME = "words_th.txt"
_THAI_STOPWORDS_FILENAME = "stopwords_th.txt"

_THAI_NEGATIONS = frozenset(["ไม่", "แต่"])


def get_corpus(filename):
    """
    Read corpus from file and return a frozenset
    """
    lines = []
    with open(os.path.join(CORPUS_PATH, filename), "r", encoding="utf8") as fh:
        lines = fh.read().splitlines()
    return frozenset(lines)


def countries():
    """
    Return a frozenset of country names in Thai
    """
    return get_corpus(_THAI_COUNTRIES_FILENAME)


def provinces():
    """
    Return a frozenset of Thailand province names in Thai
    """
    return get_corpus(_THAI_THAILAND_PROVINCES_FILENAME)


def thai_syllables():
    """
    Return a frozenset of Thai syllables
    """
    return get_corpus(_THAI_SYLLABLES_FILENAME)


def thai_words():
    """
    Return a frozenset of Thai words
    """
    return get_corpus(_THAI_WORDS_FILENAME)


def thai_stopwords():
    """
    Return a frozenset of Thai stopwords
    """
    # TODO: Cache? Not reading the disk everytime
    return get_corpus(_THAI_STOPWORDS_FILENAME)


def thai_negations():
    return _THAI_NEGATIONS


def get_file(name):
    db = TinyDB(CORPUS_DB_PATH)
    temp = Query()
    if len(db.search(temp.name == name)) > 0:
        path = get_full_data_path(db.search(temp.name == name)[0]["file"])
        db.close()
        if not os.path.exists(path):
            download(name)
        return path


def download_(url, dst):
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


def download(name, force=False):
    db = TinyDB(CORPUS_DB_PATH)
    temp = Query()
    data = requests.get(_CORPUS_DB_URL)
    data_json = data.json()
    if name in list(data_json.keys()):
        temp_name = data_json[name]
        print("Download : " + name)

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
                print("have update")
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
                    yes_no = str(input("y or n : ")).lower()
                if "y" == yes_no:
                    download_(temp_name["download"], temp_name["file_name"])
                    db.update({"version": temp_name["version"]}, temp.name == name)
            else:
                print("re-download")
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
                    yes_no = str(input("y or n : ")).lower()
                if "y" == yes_no:
                    download_(temp_name["download"], temp_name["file_name"])
                    db.update({"version": temp_name["version"]}, temp.name == name)
    db.close()


def remove(name):
    db = TinyDB(CORPUS_DB_PATH)
    temp = Query()
    data = db.search(temp.name == name)
    if len(data) > 0:
        path = get_file(name)
        os.remove(path)
        db.remove(temp.name == name)
        return True
    return False
