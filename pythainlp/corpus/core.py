# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
"""
Corpus related functions.
"""
import os
from typing import Union
import json

from pythainlp.corpus import corpus_db_path, corpus_db_url, corpus_path
from pythainlp.tools import get_full_data_path
from pythainlp import __version__


_CHECK_MODE = os.getenv("PYTHAINLP_READ_MODE")


def get_corpus_db(url: str):
    """
    Get corpus catalog from server.

    :param str url: URL corpus catalog
    """
    import requests

    corpus_db = None
    try:
        corpus_db = requests.get(url)
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Non-HTTP error occurred: {err}")

    return corpus_db


def get_corpus_db_detail(name: str, version: str = '') -> dict:
    """
    Get details about a corpus, using information from local catalog.

    :param str name: name of corpus
    :return: details about corpus
    :rtype: dict
    """
    with open(corpus_db_path(), "r", encoding="utf-8-sig") as f:
        local_db = json.load(f)

    if not version:
        for corpus in local_db["_default"].values():
            if corpus["name"] == name:
                return corpus
    else:
        for corpus in local_db["_default"].values():
            if corpus["name"] == name and corpus["version"] == version:
                return corpus

    return {}


def path_pythainlp_corpus(filename: str) -> str:
    """
    Get path pythainlp.corpus data

    :param str filename: filename of the corpus to be read

    :return: : path of corpus
    :rtype: str
    """
    return os.path.join(corpus_path(), filename)


def get_corpus(filename: str, comments: bool = True) -> frozenset:
    """
    Read corpus data from file and return a frozenset.

    Each line in the file will be a member of the set.

    Whitespace stripped and empty values and duplicates removed.

    If comments is False, any text at any position after the character
    '#' in each line will be discarded.

    :param str filename: filename of the corpus to be read
    :param bool comments: keep comments

    :return: :class:`frozenset` consisting of lines in the file
    :rtype: :class:`frozenset`

    :Example:
    ::

        from pythainlp.corpus import get_corpus

        # input file (negations_th.txt):
        # แต่
        # ไม่

        get_corpus("negations_th.txt")
        # output:
        # frozenset({'แต่', 'ไม่'})

        # input file (ttc_freq.txt):
        # ตัวบท<tab>10
        # โดยนัยนี้<tab>1

        get_corpus("ttc_freq.txt")
        # output:
        # frozenset({'โดยนัยนี้\\t1',
        #    'ตัวบท\\t10',
        #     ...})

        # input file (icubrk_th.txt):
        # # Thai Dictionary for ICU BreakIterator
        # กก
        # กกขนาก

        get_corpus("icubrk_th.txt")
        # output:
        # frozenset({'กกขนาก',
        #     '# Thai Dictionary for ICU BreakIterator',
        #     'กก',
        #     ...})

        get_corpus("icubrk_th.txt", comments=False)
        # output:
        # frozenset({'กกขนาก',
        #     'กก',
        #     ...})

    """
    path = path_pythainlp_corpus(filename)
    lines = []
    with open(path, "r", encoding="utf-8-sig") as fh:
        lines = fh.read().splitlines()

    if not comments:
        # if the line has a '#' character, take only text before the first '#'
        lines = [line.split("#", 1)[0].strip() for line in lines]

    return frozenset(filter(None, lines))


def get_corpus_as_is(filename: str) -> list:
    """
    Read corpus data from file, as it is, and return a list.

    Each line in the file will be a member of the list.

    No modifications in member values and their orders.

    If strip or comment removal is needed, use get_corpus() instead.

    :param str filename: filename of the corpus to be read

    :return: :class:`list` consisting of lines in the file
    :rtype: :class:`list`

    :Example:
    ::

        from pythainlp.corpus import get_corpus

        # input file (negations_th.txt):
        # แต่
        # ไม่

        get_corpus_as_is("negations_th.txt")
        # output:
        # ['แต่', 'ไม่']
    """
    path = path_pythainlp_corpus(filename)
    lines = []
    with open(path, "r", encoding="utf-8-sig") as fh:
        lines = fh.read().splitlines()

    return lines


def get_corpus_default_db(name: str, version: str = '') -> Union[str, None]:
    """
    Get model path from default_db.json

    :param str name: corpus name
    :return: path to the corpus or **None** if the corpus doesn't \
             exist on the device
    :rtype: str

    If you want to edit default_db.json, \
        you can edit pythainlp/corpus/default_db.json
    """
    default_db_path = path_pythainlp_corpus("default_db.json")
    with open(default_db_path, encoding="utf-8-sig") as fh:
        corpus_db = json.load(fh)

    if name in list(corpus_db.keys()):
        if version in list(corpus_db[name]["versions"].keys()):
            return path_pythainlp_corpus(
                corpus_db[name]["versions"][version]["filename"]
            )
        elif not version:  # load latest version
            version = corpus_db[name]["latest_version"]
            return path_pythainlp_corpus(
                corpus_db[name]["versions"][version]["filename"]
            )

    return None


def get_corpus_path(
    name: str, version: str = '', force: bool = False
) -> Union[str, None]:
    """
    Get corpus path.

    :param str name: corpus name
    :param str version: version
    :param bool force: force downloading
    :return: path to the corpus or **None** if the corpus doesn't \
             exist on the device
    :rtype: str

    :Example:

    (Please see the filename in
    `this file
    <https://pythainlp.github.io/pythainlp-corpus/db.json>`_

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
    from typing import Dict

    _CUSTOMIZE: Dict[str, str] = {
        # "the corpus name":"path"
    }
    if name in list(_CUSTOMIZE):
        return _CUSTOMIZE[name]

    default_path = get_corpus_default_db(name=name, version=version)
    if default_path is not None:
        return default_path

    # check if the corpus is in local catalog, download it if not
    corpus_db_detail = get_corpus_db_detail(name, version=version)

    if not corpus_db_detail or not corpus_db_detail.get("filename"):
        download(name, version=version, force=force)
        corpus_db_detail = get_corpus_db_detail(name, version=version)

    if corpus_db_detail and corpus_db_detail.get("filename"):
        # corpus is in the local catalog, get full path to the file
        if corpus_db_detail.get("is_folder"):
            path = get_full_data_path(corpus_db_detail.get("foldername"))
        else:
            path = get_full_data_path(corpus_db_detail.get("filename"))
        # check if the corpus file actually exists, download it if not
        if not os.path.exists(path):
            download(name, version=version, force=force)
        if os.path.exists(path):
            return path

    return None


def _download(url: str, dst: str) -> int:
    """
    Download helper.

    @param: URL for downloading file
    @param: dst place to put the file into
    """
    _CHUNK_SIZE = 64 * 1024  # 64 KiB

    import requests
    from urllib.request import urlopen

    file_size = int(urlopen(url).info().get("Content-Length", -1))
    r = requests.get(url, stream=True)
    with open(get_full_data_path(dst), "wb") as f:
        pbar = None
        try:
            from tqdm.auto import tqdm

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

    @param: dst place to put the file into
    @param: md5 place to file hash (MD5)
    """
    if md5 and md5 != "-":
        import hashlib

        with open(get_full_data_path(dst), "rb") as f:
            content = f.read()
            file_md5 = hashlib.md5(content).hexdigest()

            if md5 != file_md5:
                raise Exception("Hash does not match expected.")


def _version2int(v: str) -> int:
    """
    X.X.X => X0X0X
    """
    if "-" in v:
        v = v.split("-")[0]
    if v.endswith(".*"):
        v = v.replace(".*", ".0")  # X.X.* => X.X.0
    v_list = v.split(".")
    if len(v_list) < 3:
        v_list.append("0")
    v_new = ""
    for i, value in enumerate(v_list):
        if i != 0:
            if len(value) < 2:
                v_new += "0" + value
            else:
                v_new += value
        else:
            v_new += value
    return int(v_new)


def _check_version(cause: str) -> bool:
    temp = cause
    check = False
    __version = __version__
    if "dev" in __version:
        __version = __version.split("dev", maxsplit=1)[0]
    elif "beta" in __version:
        __version = __version.split("beta", maxsplit=1)[0]
    v = _version2int(__version)

    if cause == "*":
        check = True
    elif cause.startswith("==") and ">" not in cause and "<" not in cause:
        temp = cause.replace("==", "")
        check = v == _version2int(temp)
    elif cause.startswith(">=") and "<" not in cause:
        temp = cause.replace(">=", "")
        check = v >= _version2int(temp)
    elif cause.startswith(">") and "<" not in cause:
        temp = cause.replace(">", "")
        check = v > _version2int(temp)
    elif cause.startswith(">=") and "<=" not in cause and "<" in cause:
        temp = cause.replace(">=", "").split("<")
        check = _version2int(temp[0]) <= v < _version2int(temp[1])
    elif cause.startswith(">=") and "<=" in cause:
        temp = cause.replace(">=", "").split("<=")
        check = _version2int(temp[0]) <= v <= _version2int(temp[1])
    elif cause.startswith(">") and "<" in cause:
        temp = cause.replace(">", "").split("<")
        check = _version2int(temp[0]) < v < _version2int(temp[1])
    elif cause.startswith("<="):
        temp = cause.replace("<=", "")
        check = v <= _version2int(temp[0])
    elif cause.startswith("<"):
        temp = cause.replace("<", "")
        check = v < _version2int(temp[0])

    return check


def download(
    name: str, force: bool = False, url: str = '', version: str = ''
) -> bool:
    """
    Download corpus.

    The available corpus names can be seen in this file:
    https://pythainlp.github.io/pythainlp-corpus/db.json

    :param str name: corpus name
    :param bool force: force downloading
    :param str url: URL of the corpus catalog
    :param str version: version of the corpus
    :return: **True** if the corpus is found and successfully downloaded.
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

    By default, downloaded corpora and models will be saved in
    ``$HOME/pythainlp-data/``
    (e.g. ``/Users/bact/pythainlp-data/wiki_lm_lstm.pth``).
    """
    if _CHECK_MODE == "1":
        print("PyThaiNLP is read-only mode. It can't download.")
        return False
    if not url:
        url = corpus_db_url()

    corpus_db = get_corpus_db(url)
    if not corpus_db:
        print(f"Cannot download corpus catalog from: {url}")
        return False

    corpus_db = corpus_db.json()

    # check if corpus is available
    if name in corpus_db:
        with open(corpus_db_path(), "r", encoding="utf-8-sig") as f:
            local_db = json.load(f)

        corpus = corpus_db[name]
        print("Corpus:", name)
        if not version:
            for v, file in corpus["versions"].items():
                if _check_version(file["pythainlp_version"]):
                    version = v

        # version may still be None here
        if version not in corpus["versions"]:
            print("Not found corpus")
            return False
        elif _check_version(corpus["versions"][version]["pythainlp_version"]) is False:
            print("Versions Corpus not support")
            return False
        corpus_versions = corpus["versions"][version]
        file_name = corpus_versions["filename"]
        found = ""
        for i, item in local_db["_default"].items():
            # Do not check version here
            if item["name"] == name:
                # Record corpus no. if found in local database
                found = i
                break

        # If not found in local, download it
        if force or not found:
            print(f"- Downloading: {name} {version}")
            _download(
                corpus_versions["download_url"],
                file_name,
            )
            _check_hash(
                file_name,
                corpus_versions["md5"],
            )

            is_folder = False
            foldername = None

            if corpus_versions["is_tar_gz"] == "True":
                import tarfile

                is_folder = True
                foldername = name + "_" + str(version)
                if not os.path.exists(get_full_data_path(foldername)):
                    os.mkdir(get_full_data_path(foldername))
                with tarfile.open(get_full_data_path(file_name)) as tar:
                    tar.extractall(path=get_full_data_path(foldername))
            elif corpus_versions["is_zip"] == "True":
                import zipfile

                is_folder = True
                foldername = name + "_" + str(version)
                if not os.path.exists(get_full_data_path(foldername)):
                    os.mkdir(get_full_data_path(foldername))
                with zipfile.ZipFile(get_full_data_path(file_name), "r") as zip:
                    zip.extractall(path=get_full_data_path(foldername))

            if found:
                local_db["_default"][found]["version"] = version
                local_db["_default"][found]["filename"] = file_name
                local_db["_default"][found]["is_folder"] = is_folder
                local_db["_default"][found]["foldername"] = foldername
            else:
                # This awkward behavior is for backward-compatibility with
                # database files generated previously using TinyDB
                if local_db["_default"]:
                    corpus_no = max((int(no) for no in local_db["_default"])) + 1
                else:
                    corpus_no = 1
                local_db["_default"][str(corpus_no)] = {
                    "name": name,
                    "version": version,
                    "filename": file_name,
                    "is_folder": is_folder,
                    "foldername": foldername,
                }

            with open(corpus_db_path(), "w", encoding="utf-8") as f:
                json.dump(local_db, f, ensure_ascii=False)
        # Check if versions match or if the corpus is found in local database
        # but a re-download is not forced
        else:
            current_ver = local_db["_default"][found]["version"]

            if current_ver == version:
                # Corpus of the same version already exists
                print("- Already up to date.")
            else:
                # Corpus exists but is of different version
                print(f"- Existing version: {current_ver}")
                print(f"- New version available: {version}")
                print("- Use download(data_name, force=True) to update")

        return True

    print("Corpus not found:", name)
    return False


def remove(name: str) -> bool:
    """
    Remove corpus

    :param str name: corpus name
    :return: **True** if the corpus is found and successfully removed.
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
    if _CHECK_MODE == "1":
        print("PyThaiNLP is read-only mode. It can't remove corpus.")
        return False
    with open(corpus_db_path(), "r", encoding="utf-8-sig") as f:
        db = json.load(f)
    data = [corpus for corpus in db["_default"].values() if corpus["name"] == name]

    if data:
        path = get_corpus_path(name)
        if data[0].get("is_folder"):
            import shutil

            os.remove(get_full_data_path(data[0].get("filename")))
            shutil.rmtree(path, ignore_errors=True)
        else:
            os.remove(path)
        for i, corpus in db["_default"].copy().items():
            if corpus["name"] == name:
                del db["_default"][i]
        with open(corpus_db_path(), "w", encoding="utf-8") as f:
            json.dump(db, f, ensure_ascii=False)
        return True

    return False


def get_path_folder_corpus(name, version, *path):
    return os.path.join(get_corpus_path(name, version), *path)
