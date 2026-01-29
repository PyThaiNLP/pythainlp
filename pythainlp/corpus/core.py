# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Corpus related functions."""

from __future__ import annotations

import json
import os
import re
import sys
import tarfile
import zipfile
from http.client import HTTPResponse
from importlib.resources import files
from typing import Optional

from pythainlp import __version__
from pythainlp.corpus import corpus_db_path, corpus_db_url, corpus_path
from pythainlp.tools import get_full_data_path

_CHECK_MODE = os.getenv("PYTHAINLP_READ_MODE")
_USER_AGENT = (
    f"PyThaiNLP/{__version__} "
    f"(Python/{sys.version_info.major}.{sys.version_info.minor}; "
    f"{sys.platform})"
)


class _ResponseWrapper:
    """Wrapper to provide requests.Response-like interface for urllib response."""

    def __init__(self, response: HTTPResponse) -> None:
        self.status_code = response.status
        self.headers = response.headers
        self._content = response.read()

    def json(self) -> dict:
        """Parse JSON content from response."""
        try:
            return json.loads(self._content.decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError) as err:
            raise ValueError(f"Failed to parse JSON response: {err}")


def get_corpus_db(url: str) -> Optional[_ResponseWrapper]:
    """Get corpus catalog from server.

    :param str url: URL corpus catalog

    Security Note: Uses HTTPS with certificate validation enabled by default
    in Python's urllib. Only download corpus from trusted URLs.
    """
    from urllib.error import HTTPError, URLError
    from urllib.request import Request, urlopen

    corpus_db = None
    try:
        req = Request(url, headers={"User-Agent": _USER_AGENT})
        # SSL certificate verification is enabled by default
        with urlopen(req, timeout=10) as response:
            corpus_db = _ResponseWrapper(response)
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except URLError as err:
        print(f"URL error occurred: {err}")
    except Exception as err:
        print(f"Error occurred: {err}")

    return corpus_db


def get_corpus_db_detail(name: str, version: str = "") -> dict[str, str]:
    """Get details about a corpus, using information from local catalog.

    :param str name: name of corpus
    :return: details about corpus
    :rtype: dict
    """
    with open(corpus_db_path(), encoding="utf-8-sig") as f:
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
    """Get path pythainlp.corpus data

    :param str filename: filename of the corpus to be read

    :return: : path of corpus
    :rtype: str
    """
    return os.path.join(corpus_path(), filename)


def get_corpus(filename: str, comments: bool = True) -> frozenset:
    """Read corpus data from file and return a frozenset.

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
    corpus_files = files("pythainlp.corpus")
    corpus_file = corpus_files.joinpath(filename)
    text = corpus_file.read_text(encoding="utf-8-sig")
    lines = text.splitlines()

    if not comments:
        # if the line has a '#' character, take only text before the first '#'
        lines = [line.split("#", 1)[0].strip() for line in lines]

    return frozenset(filter(None, lines))


def get_corpus_as_is(filename: str) -> list[str]:
    """Read corpus data from file, as it is, and return a list.

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
    corpus_files = files("pythainlp.corpus")
    corpus_file = corpus_files.joinpath(filename)
    text = corpus_file.read_text(encoding="utf-8-sig")
    lines = text.splitlines()

    return lines


def get_corpus_default_db(name: str, version: str = "") -> Optional[str]:
    """Get model path from default_db.json

    :param str name: corpus name
    :return: path to the corpus or **None** if the corpus doesn't \
             exist on the device
    :rtype: str

    If you want to edit default_db.json, \
        you can edit pythainlp/corpus/default_db.json
    """
    corpus_files = files("pythainlp.corpus")
    default_db_file = corpus_files.joinpath("default_db.json")
    text = default_db_file.read_text(encoding="utf-8-sig")
    corpus_db = json.loads(text)

    if name in corpus_db:
        if version in corpus_db[name]["versions"]:
            return path_pythainlp_corpus(
                corpus_db[name]["versions"][version]["filename"]
            )
        elif not version:  # load latest version
            version = corpus_db[name]["latest_version"]
            return path_pythainlp_corpus(
                corpus_db[name]["versions"][version]["filename"]
            )

    return None


def get_corpus_path(name: str, version: str = "", force: bool = False) -> Optional[str]:
    """Get corpus path.

    :param str name: corpus name
    :param str version: version
    :param bool force: force downloading
    :return: path to the corpus or **None** if the corpus doesn't \
             exist on the device
    :rtype: str

    :Example:

    (Please see the filename in
    `this file
    <https://pythainlp.org/pythainlp-corpus/db.json>`_

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
    CUSTOMIZE: dict[str, str] = {
        # "the corpus name":"path"
    }
    if name in CUSTOMIZE:
        return CUSTOMIZE[name]

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
            foldername = corpus_db_detail.get("foldername")
            if foldername:
                path = get_full_data_path(foldername)
            else:
                return None
        else:
            filename = corpus_db_detail.get("filename")
            if filename:
                path = get_full_data_path(filename)
            else:
                return None
        # check if the corpus file actually exists, download it if not
        if not os.path.exists(path):
            download(name, version=version, force=force)
        if os.path.exists(path):
            return path

    return None


def _download(url: str, dst: str) -> int:
    """Download helper.

    @param: URL for downloading file
    @param: dst place to put the file into

    Security Note: Downloads use HTTPS with SSL certificate validation.
    Files are verified using MD5 checksums after download.
    """
    CHUNK_SIZE = 64 * 1024  # 64 KiB

    from urllib.request import Request, urlopen

    req = Request(url, headers={"User-Agent": _USER_AGENT})
    # SSL certificate verification is enabled by default
    with urlopen(req, timeout=10) as response:
        file_size = int(response.info().get("Content-Length", -1))
        with open(get_full_data_path(dst), "wb") as f:
            pbar = None
            try:
                from tqdm.auto import tqdm

                pbar = tqdm(total=file_size)
            except ImportError:
                pbar = None

            while chunk := response.read(CHUNK_SIZE):
                f.write(chunk)
                if pbar:
                    pbar.update(len(chunk))
            if pbar:
                pbar.close()
            else:
                print("Done.")
    return file_size


def _check_hash(dst: str, md5: str) -> None:
    """Check hash helper.

    @param: dst place to put the file into
    @param: md5 place to file hash (MD5)
    """
    if md5 and md5 != "-":
        import hashlib

        with open(get_full_data_path(dst), "rb") as f:
            content = f.read()
            # MD5 is insecure but sufficient here
            file_md5 = hashlib.md5(content).hexdigest()  # noqa: S324

            if md5 != file_md5:
                raise ValueError("Hash does not match expected.")


def _is_within_directory(directory: str, target: str) -> bool:
    """Check if target path is within directory (prevent path traversal).

    @param: directory base directory path
    @param: target target file path to check
    @return: True if target is within directory, False otherwise

    Security Note: This function normalizes paths using os.path.abspath()
    to handle relative paths and .. sequences. It does NOT follow symlinks
    (unlike os.path.realpath()), because:
    - Symlink validation is handled separately in extraction functions
    - We want to check if the path string itself is safe, not where it points
    - This prevents false negatives when symlinks don't exist yet

    For symlink security, use the extraction function's symlink validation.
    """
    # Use abspath to normalize paths but NOT realpath (which follows symlinks)
    abs_directory = os.path.abspath(directory)
    abs_target = os.path.abspath(target)

    # Ensure directory ends with separator for proper prefix check
    # This prevents /foo/bar from matching /foo/barz
    if not abs_directory.endswith(os.sep):
        abs_directory += os.sep

    return abs_target.startswith(abs_directory) or abs_target == abs_directory.rstrip(
        os.sep
    )


def _safe_extract_tar(tar: tarfile.TarFile, path: str) -> None:
    """Safely extract tar archive, preventing path traversal attacks.

    @param: tar tarfile object
    @param: path destination path for extraction

    Security Note: This function prevents path traversal attacks including:
    - Files with .. in their path
    - Symlinks pointing outside the extraction directory
    - Files extracted through malicious symlinks

    For Python 3.12+, uses tarfile.data_filter for additional protection.
    For Python 3.9-3.11, implements custom validation of all members.
    """
    # Check if data_filter is available (Python 3.12+)
    if hasattr(tarfile, "data_filter"):
        # Use built-in filter which handles symlinks and other security issues
        try:
            tar.extractall(path=path, filter="data")
        except (
            tarfile.OutsideDestinationError,
            tarfile.LinkOutsideDestinationError,
        ) as e:
            # Re-raise as ValueError for consistency with older Python versions
            raise ValueError(str(e))
    else:
        # Manual validation for older Python versions
        for member in tar.getmembers():
            # Check the member's target path
            member_path = os.path.join(path, member.name)
            if not _is_within_directory(path, member_path):
                raise ValueError(f"Attempted path traversal in tar file: {member.name}")

            # For symlinks, also validate the link target
            if member.issym() or member.islnk():
                # Get the link target (can be absolute or relative)
                link_target = member.linkname

                # If it's a relative symlink, resolve it relative to the member's directory
                if not os.path.isabs(link_target):
                    member_dir = os.path.dirname(member_path)
                    link_target = os.path.join(member_dir, link_target)
                else:
                    # Absolute symlinks are dangerous - make them relative to extraction path
                    link_target = os.path.join(path, link_target.lstrip(os.sep))

                # Check if the resolved symlink target is within the directory
                if not _is_within_directory(path, link_target):
                    raise ValueError(
                        f"Symlink {member.name} points outside extraction directory: {member.linkname}"
                    )

        tar.extractall(path=path)


def _safe_extract_zip(zip_file: zipfile.ZipFile, path: str) -> None:
    """Safely extract zip archive, preventing path traversal attacks.

    @param: zip_file zipfile object
    @param: path destination path for extraction

    Security Note: This function prevents path traversal attacks including:
    - Files with .. in their path
    - Symlinks pointing outside the extraction directory (on Unix systems)

    Note: ZIP format has limited symlink support. Symlinks are primarily
    created by Unix-based archiving tools and may not be portable.
    """
    for member in zip_file.namelist():
        member_path = os.path.join(path, member)
        if not _is_within_directory(path, member_path):
            raise ValueError(f"Attempted path traversal in zip file: {member}")

        # Check for potential symlinks in ZIP files
        # ZIP files can contain symlinks on Unix systems (external_attr indicates this)
        info = zip_file.getinfo(member)
        # Check if this is a symlink (Unix: external_attr with S_IFLNK set)
        # The high 16 bits of external_attr contain Unix file mode
        is_symlink = (info.external_attr >> 16) & 0o170000 == 0o120000

        if is_symlink:
            # Read the symlink target from the file content
            link_target = zip_file.read(member).decode("utf-8")

            # Resolve the link target relative to the member's directory
            if not os.path.isabs(link_target):
                member_dir = os.path.dirname(member_path)
                resolved_target = os.path.join(member_dir, link_target)
            else:
                # Absolute symlinks - make them relative to extraction path
                resolved_target = os.path.join(path, link_target.lstrip(os.sep))

            # Check if the symlink target is within the directory
            if not _is_within_directory(path, resolved_target):
                raise ValueError(
                    f"Symlink {member} points outside extraction directory: {link_target}"
                )

    zip_file.extractall(path=path)


def _version2int(v: str) -> int:
    """X.X.X => X0X0X"""
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


def download(name: str, force: bool = False, url: str = "", version: str = "") -> bool:
    """Download corpus.

    The available corpus names can be seen in this file:
    https://pythainlp.org/pythainlp-corpus/db.json

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

        download("wiki_lm_lstm", force=True)
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
        with open(corpus_db_path(), encoding="utf-8-sig") as f:
            local_db = json.load(f)

        corpus = corpus_db[name]
        print("Corpus:", name)
        if not version:
            for v, file in corpus["versions"].items():
                if _check_version(file["pythainlp_version"]):
                    version = v

        # version may still be None here
        if version not in corpus["versions"]:
            print("Corpus not found.")
            return False
        elif _check_version(corpus["versions"][version]["pythainlp_version"]) is False:
            print("Corpus version not supported.")
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
                is_folder = True
                foldername = name + "_" + str(version)
                if not os.path.exists(get_full_data_path(foldername)):
                    os.mkdir(get_full_data_path(foldername))
                with tarfile.open(get_full_data_path(file_name)) as tar:
                    _safe_extract_tar(tar, get_full_data_path(foldername))
            elif corpus_versions["is_zip"] == "True":
                is_folder = True
                foldername = name + "_" + str(version)
                if not os.path.exists(get_full_data_path(foldername)):
                    os.mkdir(get_full_data_path(foldername))
                with zipfile.ZipFile(get_full_data_path(file_name), "r") as zip_file:
                    _safe_extract_zip(zip_file, get_full_data_path(foldername))

            if found:
                local_db["_default"][found]["version"] = version
                local_db["_default"][found]["filename"] = file_name
                local_db["_default"][found]["is_folder"] = is_folder
                local_db["_default"][found]["foldername"] = foldername
            else:
                # This awkward behavior is for backward-compatibility with
                # database files generated previously using TinyDB
                if local_db["_default"]:
                    corpus_no = max(int(no) for no in local_db["_default"]) + 1
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
    """Remove corpus

    :param str name: corpus name
    :return: **True** if the corpus is found and successfully removed.
             Otherwise, it returns **False**.
    :rtype: bool

    :Example:
    ::

        from pythainlp.corpus import remove, get_corpus_path, get_corpus

        print(remove("ttc"))
        # output: True

        print(get_corpus_path("ttc"))
        # output: None

        get_corpus("ttc")
        # output:
        # FileNotFoundError: [Errno 2] No such file or directory:
        # '/usr/local/lib/python3.6/dist-packages/pythainlp/corpus/ttc'
    """
    if _CHECK_MODE == "1":
        print("PyThaiNLP is read-only mode. It can't download.")
        return False
    with open(corpus_db_path(), encoding="utf-8-sig") as f:
        db = json.load(f)
    data = [corpus for corpus in db["_default"].values() if corpus["name"] == name]

    if data:
        path = get_corpus_path(name)
        if data[0].get("is_folder"):
            import shutil

            filename = data[0].get("filename")
            if filename:
                os.remove(get_full_data_path(filename))
            if path:
                shutil.rmtree(path, ignore_errors=True)
        else:
            if path:
                os.remove(path)
        for i, corpus in db["_default"].copy().items():
            if corpus["name"] == name:
                del db["_default"][i]
        with open(corpus_db_path(), "w", encoding="utf-8") as f:
            json.dump(db, f, ensure_ascii=False)
        return True

    return False


def get_path_folder_corpus(name: str, version: str, *path: str) -> str:
    corpus_path = get_corpus_path(name, version)
    if corpus_path is None:
        raise ValueError(f"Corpus path not found for {name} version {version}")
    return os.path.join(corpus_path, *path)


def make_safe_directory_name(name: str) -> str:
    """Make safe directory name

    :param str name: directory name
    :return: safe directory name
    :rtype: str
    """
    # Replace invalid characters with an underscore
    safe_name = re.sub(r'[<>:"/\\|?*]', "_", name)
    # Remove leading/trailing spaces or periods (especially important for Windows)
    safe_name = safe_name.strip(" .")
    # Prevent names that are reserved on Windows
    reserved_names = [
        "CON",
        "PRN",
        "AUX",
        "NUL",
        "COM1",
        "COM2",
        "COM3",
        "COM4",
        "COM5",
        "COM6",
        "COM7",
        "COM8",
        "COM9",
        "LPT1",
        "LPT2",
        "LPT3",
        "LPT4",
        "LPT5",
        "LPT6",
        "LPT7",
        "LPT8",
        "LPT9",
    ]
    if safe_name.upper() in reserved_names:
        safe_name = f"_{safe_name}"  # Prepend underscore to avoid conflict
    return safe_name


def get_hf_hub(repo_id: str, filename: str = "") -> str:
    """HuggingFace Hub in :mod:`pythainlp` data directory.

    :param str repo_id: repo_id
    :param str filename: filename (optional, default is empty string).
        If empty, downloads entire snapshot.
    :return: path
    :rtype: str
    """
    try:
        from huggingface_hub import hf_hub_download, snapshot_download
    except ModuleNotFoundError:
        raise ModuleNotFoundError(
            """
        huggingface-hub isn't found!
        Please installing the package via 'pip install huggingface-hub'.
        """
        )
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred: {e}") from e
    hf_root = get_full_data_path("hf_models")
    name_dir = make_safe_directory_name(repo_id)
    root_project = os.path.join(hf_root, name_dir)
    if filename:
        output_path = hf_hub_download(
            repo_id=repo_id, filename=filename, local_dir=root_project
        )
    else:
        output_path = snapshot_download(repo_id=repo_id, local_dir=root_project)
    return output_path
