# -*- coding: utf-8 -*-

import os

import requests
import pythainlp
from pythainlp.tools import get_path_data
from tinydb import Query, TinyDB
from tqdm import tqdm
from urllib.request import urlopen

_CORPUS_DIRNAME = "corpus"
CORPUS_PATH = os.path.join(os.path.dirname(pythainlp.__file__), _CORPUS_DIRNAME)

_CORPUS_DB_URL = (
    "https://raw.githubusercontent.com/PyThaiNLP/pythainlp-corpus/master/db.json"
)
_CORPUS_DB_FILENAME = "db.json"
CORPUS_DB_PATH = get_path_data(_CORPUS_DB_FILENAME)
if not os.path.exists(CORPUS_DB_PATH):
    TinyDB(CORPUS_DB_PATH)

_THAI_COUNTRIES_FILENAME = "countries_th.txt"
_THAI_THAILAND_PROVINCES_FILENAME = "thailand_provinces_th.txt"
_THAI_SYLLABLES_FILENAME = "syllables_th.txt"
_THAI_WORDS_FILENAME = "words_th.txt"
_THAI_STOPWORDS_FILENAME = "stopwords_th.txt"

_THAI_NEGATIONS = frozenset(["ไม่", "แต่"])

THAI_NUMBERS = "๐๑๒๓๔๕๖๗๘๙"  # 10
THAI_ALPHABETS = "กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธนบปผฝพฟภมยรลวศษสหฬอฮ"  # 44
THAI_VOWELS = "ฤฦะ\u0e31าำ\u0e34\u0e35\u0e36\u0e37\u0e38\u0e39เแโใไ\u0e45"  # 18
THAI_SYMBOLS = "ฯ\u0e3a฿ๆ\u0e47\u0e4c\u0e4d\u0e4e\u0e4f\u0e5a\u0e5b"  # 11
THAI_TONEMARKS = "\u0e48\u0e49\u0e50\u0e51"  # 4
THAI_LETTERS = "".join(
    [THAI_ALPHABETS, THAI_VOWELS, THAI_TONEMARKS, THAI_SYMBOLS]
)  # 77


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
        path = get_path_data(db.search(temp.name == name)[0]["file"])
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
    with (open(get_path_data(dst), "wb")) as f:
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
