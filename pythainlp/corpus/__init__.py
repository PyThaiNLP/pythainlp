# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import os

import requests
from future.moves.urllib.request import urlopen
from pythainlp.tools import get_path_data, get_path_db
from tinydb import Query, TinyDB
from tqdm import tqdm

CORPUS_DB_URL = (
    "https://github.com/PyThaiNLP/pythainlp-corpus/raw/1.7/db.json"
)

# __all__ = ["thaipos", "thaiword","alphabet","tone","country","wordnet"]
path_db_ = get_path_db()


def get_file(name):
    db = TinyDB(path_db_)
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
    db = TinyDB(path_db_)
    temp = Query()
    data = requests.get(CORPUS_DB_URL)
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
    db = TinyDB(path_db_)
    temp = Query()
    data = db.search(temp.name == name)
    if len(data) > 0:
        path = get_file(name)
        os.remove(path)
        db.remove(temp.name == name)
        return True
    return False
