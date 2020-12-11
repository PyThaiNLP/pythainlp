# -*- coding: utf-8 -*-
"""
Corpus related functions.
"""

import hashlib
import os
from typing import Union
from urllib.request import urlopen

import requests
from pythainlp.corpus import corpus_db_path, corpus_db_url, corpus_path
from pythainlp.tools import get_full_data_path
from requests.exceptions import HTTPError
from tinydb import Query, TinyDB


def get_corpus_db(url: str) -> requests.Response:
    """
    Get corpus catalog from server.

    :param str url: URL corpus catalog
    """
    corpus_db = None
    try:
        corpus_db = requests.get(url)
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Non-HTTP error occurred: {err}")

    return corpus_db


def get_corpus_db_detail(name: str, version: str = None) -> dict:
    """
    Get details about a corpus, using information from local catalog.

    :param str name: name corpus
    :return: details about a corpus
    :rtype: dict
    """
    local_db = TinyDB(corpus_db_path())
    query = Query()
    if version is None:
        res = local_db.search(query.name == name)
    else:
        res = local_db.search((query.name == name) & (query.version == version))
    local_db.close()

    if res:
        return res[0]

    return dict()


def get_corpus(filename: str, as_is: bool = False) -> Union[frozenset, list]:
    """
    Read corpus data from file and return a frozenset or a list.

    Each line in the file will be a member of the set or the list.

    By default, a frozenset will be return, with whitespaces stripped, and
    empty values and duplicates removed.

    If as_is is True, a list will be return, with no modifications
    in member values and their orders.

    (Please see the filename from
    `this file
    <https://github.com/PyThaiNLP/pythainlp-corpus/blob/master/db.json>`_

    :param str filename: filename of the corpus to be read

    :return: :class:`frozenset` or :class:`list` consists of lines in the file
    :rtype: :class:`frozenset` or :class:`list`

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
        #     ...})
    """
    path = os.path.join(corpus_path(), filename)
    lines = []
    with open(path, "r", encoding="utf-8-sig") as fh:
        lines = fh.read().splitlines()

    if as_is:
        return lines

    lines = [line.strip() for line in lines]
    return frozenset(filter(None, lines))


def _update_all():
    print("Update Corpus...")
    with TinyDB(corpus_db_path()) as local_db:
        item_all = local_db.all()
        query = Query()
        for item in item_all:
            name = item["name"]
            if "file_name" in item.keys():
                local_db.update(
                    {"filename": item["file_name"]}, query.name == name
                )
            elif "file" in item.keys():
                local_db.update({"filename": item["file"]}, query.name == name)
    local_db.close()


def get_corpus_path(name: str,  version : str = None) -> Union[str, None]:
    """
    Get corpus path.

    :param str name: corpus name
    :return: path to the corpus or **None** of the corpus doesn't \
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
    # Customize your the corpus path then close the line after lines 164 through 190.
    _CUSTOMIZE = {
        # "the corpus name":"path"
    }
    if name in list(_CUSTOMIZE.keys()):
        return _CUSTOMIZE[name]

    # check if the corpus is in local catalog, download if not
    corpus_db_detail = get_corpus_db_detail(name)
    if (
        corpus_db_detail.get("file_name") is not None
        and corpus_db_detail.get("filename") is None
    ):
        _update_all()
    elif (
        corpus_db_detail.get("file") is not None
        and corpus_db_detail.get("filename") is None
    ):
        _update_all()

    if not corpus_db_detail or not corpus_db_detail.get("filename"):
        download(name,  version =  version)
        corpus_db_detail = get_corpus_db_detail(name)

    if corpus_db_detail and corpus_db_detail.get("filename"):
        # corpus is in the local catalog, get full path to the file
        path = get_full_data_path(corpus_db_detail.get("filename"))
        # check if the corpus file actually exists, download if not
        if not os.path.exists(path):
            download(name)
        if os.path.exists(path):
            return path

    return None


def _download(url: str, dst: str) -> int:
    """
    Download helper.

    @param: url to download file
    @param: dst place to put the file
    """
    _CHUNK_SIZE = 64 * 1024  # 64 KiB

    file_size = int(urlopen(url).info().get("Content-Length", -1))
    r = requests.get(url, stream=True)
    with open(get_full_data_path(dst), "wb") as f:
        pbar = None
        try:
            from tqdm import tqdm

            pbar = tqdm(total=int(r.headers["Content-Length"]))
        except ImportError:
            pbar = None

        for chunk in r.iter_content(chunk_size=_CHUNK_SIZE):
            if chunk:
                f.write(chunk)
                if pbar:
                    pbar.update(len(chunk))
        if pbar:
            pbar.close()
        else:
            print("Done.")
    return file_size


def _check_hash(dst: str, md5: str) -> None:
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


def download(
    name: str, force: bool = False, url: str = None, version: str = None
) -> bool:
    """
    Download corpus.

    The available corpus names can be seen in this file:
    https://github.com/PyThaiNLP/pythainlp-corpus/blob/master/db.json

    :param str name: corpus name
    :param bool force: force download
    :param str url: URL of the corpus catalog
    :param str version: Version of the corpus
    :return: **True** if the corpus is found and succesfully downloaded.
             Otherwise, it returns **False**.
    :rtype: bool

    :Example:
    ::

        from pythainlp.corpus import download

        download('wiki_lm_lstm', force=True)
        # output:
        # Corpus: wiki_lm_lstm
        # - Downloading: wiki_lm_lstm 0.1
        # thwiki_lm.pth:  26%|██▌       | 114k/434k [00:00<00:00, 690kB/s]

    By default, downloaded corpus and model will be saved in
    ``$HOME/pythainlp-data/``
    (e.g. ``/Users/bact/pythainlp-data/wiki_lm_lstm.pth``).
    """
    if not url:
        url = corpus_db_url()

    corpus_db = get_corpus_db(url)
    if not corpus_db:
        print(f"Cannot download corpus catalog from: {url}")
        return False

    corpus_db = corpus_db.json()

    # check if corpus is available
    if name in list(corpus_db.keys()):
        local_db = TinyDB(corpus_db_path())
        query = Query()

        corpus = corpus_db[name.lower()]
        print("Corpus:", name)
        if version is None:
            version = corpus["latest_version"]
        corpus_versions = corpus["versions"][version]
        file_name = corpus_versions["filename"]
        found = local_db.search(
            (query.name == name) & (query.version == version)
        )

        # If not found in local, download
        if force or not found:
            print(f"- Downloading: {name} {version}")
            _download(
                corpus_versions["download_url"], file_name,
            )
            _check_hash(
                file_name, corpus_versions["md5"],
            )

            if found:
                local_db.update({"version": version}, query.name == name)
            else:
                local_db.insert(
                    {"name": name, "version": version, "filename": file_name}
                )
        else:
            if local_db.search(
                query.name == name and query.version == version
            ):
                # Already has the same version
                print("- Already up to date.")
            else:
                # Has the corpus but different version
                current_ver = local_db.search(query.name == name)[0]["version"]
                print(f"- Existing version: {current_ver}")
                print(f"- New version available: {version}")
                print("- Use download(data_name, force=True) to update")

        local_db.close()
        return True

    print("Corpus not found:", name)
    return False


def remove(name: str) -> bool:
    """
    Remove corpus

    :param str name: corpus name
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
