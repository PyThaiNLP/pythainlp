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
from functools import lru_cache
from importlib.resources import files
from typing import TYPE_CHECKING, Any, Optional, cast

from pythainlp import __version__
from pythainlp.corpus import corpus_db_path, corpus_db_url, corpus_path
from pythainlp.tools import get_full_data_path
from pythainlp.tools.path import (
    is_offline_mode,
    is_read_only_mode,
    safe_path_join,
)

if TYPE_CHECKING:
    from http.client import HTTPMessage, HTTPResponse

_USER_AGENT: str = (
    f"PyThaiNLP/{__version__} "
    f"(Python/{sys.version_info.major}.{sys.version_info.minor}; "
    f"{sys.platform})"
)


class _ResponseWrapper:
    """Wrapper to provide requests.Response-like interface for urllib response."""

    status_code: int
    headers: HTTPMessage
    _content: bytes

    def __init__(self, response: HTTPResponse) -> None:
        self.status_code = response.status
        self.headers = response.headers
        self._content = response.read()

    def json(self) -> dict[str, Any]:
        """Parse JSON content from response."""
        try:
            return cast(
                dict[str, Any], json.loads(self._content.decode("utf-8"))
            )
        except (json.JSONDecodeError, UnicodeDecodeError) as err:
            raise ValueError(f"Failed to parse JSON response: {err}") from err


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


def get_corpus_db_detail(name: str, version: str = "") -> dict[str, Any]:
    """Get details about a corpus, using information from local catalog.

    :param str name: name of corpus
    :return: details about corpus
    :rtype: dict
    """
    db_path = corpus_db_path()
    if not os.path.exists(db_path):
        return {}
    with open(db_path, encoding="utf-8-sig") as f:
        local_db = json.load(f)

    if not version:
        for corpus in local_db["_default"].values():
            if corpus["name"] == name:
                return cast(dict[str, Any], corpus)
    else:
        for corpus in local_db["_default"].values():
            if corpus["name"] == name and corpus["version"] == version:
                return cast(dict[str, Any], corpus)

    return {}


@lru_cache(maxsize=None)
def get_corpus(filename: str, comments: bool = True) -> frozenset[str]:
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

        >>> from pythainlp.corpus import get_corpus  # doctest: +SKIP
        >>> get_corpus("negations_th.txt")  # doctest: +SKIP
        frozenset({'แต่', 'ไม่'})
        >>> get_corpus("ttc_freq.txt")  # doctest: +SKIP
        frozenset({'โดยนัยนี้\\t1', 'ตัวบท\\t10', ...})
        >>> get_corpus("icubrk_th.txt")  # doctest: +SKIP
        frozenset({'กกขนาก', '# Thai Dictionary for ICU BreakIterator', 'กก', ...})
        >>> get_corpus("icubrk_th.txt", comments=False)  # doctest: +SKIP
        frozenset({'กกขนาก', 'กก', ...})

    """
    corpus_files = files("pythainlp.corpus")
    corpus_file = corpus_files.joinpath(filename)
    text = corpus_file.read_text(encoding="utf-8-sig")
    lines = text.splitlines()

    if not comments:
        # if the line has a '#' character, take only text before the first '#'
        lines = [line.split("#", 1)[0].strip() for line in lines]

    return frozenset(filter(None, lines))


@lru_cache(maxsize=None)
def get_corpus_as_is(filename: str) -> list[str]:
    """Read corpus data from file, as it is, and return a list.

    Each line in the file will be a member of the list.

    No modifications in member values and their orders.

    If strip or comment removal is needed, use get_corpus() instead.

    :param str filename: filename of the corpus to be read

    :return: :class:`list` consisting of lines in the file
    :rtype: :class:`list`

    :Example:

        >>> from pythainlp.corpus import get_corpus_as_is  # doctest: +SKIP
        >>> get_corpus_as_is("negations_th.txt")  # doctest: +SKIP
        ['แต่', 'ไม่']
    """
    corpus_files = files("pythainlp.corpus")
    corpus_file = corpus_files.joinpath(filename)
    text = corpus_file.read_text(encoding="utf-8-sig")
    lines = text.splitlines()

    return lines


@lru_cache(maxsize=None)
def _load_default_db() -> dict[str, Any]:
    """Load and cache the bundled default_db.json corpus catalog."""
    corpus_files = files("pythainlp.corpus")
    default_db_file = corpus_files.joinpath("default_db.json")
    text = default_db_file.read_text(encoding="utf-8-sig")
    return cast(dict[str, Any], json.loads(text))


def get_corpus_default_db(name: str, version: str = "") -> Optional[str]:
    """Get model path from default_db.json

    :param str name: corpus name
    :return: path to the corpus or **None** if the corpus doesn't \
             exist on the device
    :rtype: str

    If you want to edit default_db.json, \
        you can edit pythainlp/corpus/default_db.json
    """
    corpus_db = _load_default_db()

    if name in corpus_db:
        if version in corpus_db[name]["versions"]:
            return safe_path_join(
                corpus_path(),
                corpus_db[name]["versions"][version]["filename"],
            )
        elif not version:  # load latest version
            version = corpus_db[name]["latest_version"]
            return safe_path_join(
                corpus_path(),
                corpus_db[name]["versions"][version]["filename"],
            )

    return None


def _resolve_corpus_file_path(
    corpus_db_detail: dict[str, Any],
) -> Optional[str]:
    """Resolve the local filesystem path for a corpus catalog entry.

    :param dict corpus_db_detail: a corpus catalog entry from the local DB
    :return: full local path to the corpus file or folder,
             or ``None`` if required path information is missing
    :rtype: Optional[str]
    """
    if corpus_db_detail.get("is_folder"):
        foldername = corpus_db_detail.get("foldername")
        return get_full_data_path(foldername) if foldername else None
    filename = corpus_db_detail.get("filename")
    return get_full_data_path(filename) if filename else None


def get_corpus_path(name: str, version: str = "") -> Optional[str]:
    """Get corpus path.

    The function checks the following locations in order:

    1. A user-defined path override (``CUSTOMIZE`` mapping).
    2. Bundled (default) corpora shipped with PyThaiNLP.
    3. The local download catalog (``~/pythainlp-data/``).

    When the corpus file is not present locally, the behavior depends on the
    ``PYTHAINLP_OFFLINE`` environment variable:

    - If ``PYTHAINLP_OFFLINE`` is set to a truthy value (e.g., ``"1"``),
      a :exc:`FileNotFoundError` is raised immediately.
    - Otherwise, the corpus is downloaded automatically.

    :param str name: corpus name
    :param str version: corpus version (empty string means latest)
    :return: full local path when the corpus exists,
             or ``None`` when the corpus cannot be found or downloaded.
    :rtype: Optional[str]

    :raises FileNotFoundError: when the corpus is missing locally and
        ``PYTHAINLP_OFFLINE`` is set to a truthy value.

    :Example:

    (Please see the filename in
    `this file <https://pythainlp.org/pythainlp-corpus/db.json>`_)

    If the corpus already exists:

        >>> from pythainlp.corpus import get_corpus_path  # doctest: +SKIP
        >>> get_corpus_path("ttc")  # doctest: +SKIP
        '/root/pythainlp-data/ttc_freq.txt'

    If the corpus has not been downloaded yet (online mode):

        >>> get_corpus_path("wiki_lm_lstm")  # doctest: +SKIP
        '/root/pythainlp-data/thwiki_model_lstm.pth'

    To download manually:

        >>> from pythainlp.corpus import download  # doctest: +SKIP
        >>> download("wiki_lm_lstm")  # doctest: +SKIP
        >>> get_corpus_path("wiki_lm_lstm")  # doctest: +SKIP
        '/root/pythainlp-data/thwiki_model_lstm.pth'
    """
    CUSTOMIZE: dict[str, str] = {
        # "the corpus name":"path"
    }
    if name in CUSTOMIZE:
        return CUSTOMIZE[name]

    # Check bundled (default) corpora first
    default_path = get_corpus_default_db(name=name, version=version)
    if default_path is not None:
        return default_path

    # Check the local download catalog
    corpus_db_detail = get_corpus_db_detail(name, version=version)
    if not corpus_db_detail:
        # Corpus not in local catalog; download it unless in offline mode
        if is_offline_mode():
            raise FileNotFoundError(
                f"corpus-not-found name={name!r}\n"
                f"  Corpus '{name}' not found locally.\n"
                f"  PYTHAINLP_OFFLINE is set; automatic downloading is disabled.\n"
                f"  To download, unset PYTHAINLP_OFFLINE, then run:\n"
                f"    Python: pythainlp.corpus.download('{name}')\n"
                f"    CLI:    thainlp data get {name}"
            )
        if not download(name, version=version):
            return None
        corpus_db_detail = get_corpus_db_detail(name, version=version)
        if not corpus_db_detail:
            return None

    path = _resolve_corpus_file_path(corpus_db_detail)
    if path is None:
        return None

    if os.path.exists(path):
        return path

    # File is registered in catalog but missing from disk
    if is_offline_mode():
        raise FileNotFoundError(
            f"corpus-not-found name={name!r} expected-path={path!r}\n"
            f"  Corpus '{name}' expected at '{path}' but file not found.\n"
            f"  PYTHAINLP_OFFLINE is set; automatic re-downloading is disabled.\n"
            f"  To re-download, unset PYTHAINLP_OFFLINE, then run:\n"
            f"    Python: pythainlp.corpus.download('{name}', force=True)\n"
            f"    CLI:    thainlp data get {name}"
        )
    if not download(name, version=version, force=True):
        return None
    return path if os.path.exists(path) else None


def _download(url: str, dst: str) -> int:
    """Download helper.

    :param str url: URL for the file to download.
    :param str dst: local destination path for the downloaded file.

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

    :param str dst: local path of the file to verify.
    :param str md5: expected MD5 checksum of the file.
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

    :param str directory: base directory path.
    :param str target: target file path to check.
    :return: ``True`` if target is within directory, ``False`` otherwise.
    :rtype: bool

    Security Note: This function normalizes paths using os.path.abspath()
    to handle relative paths and .. sequences. It does NOT follow symlinks
    (unlike os.path.realpath()), because:

    - Symlink validation is handled separately in extraction functions.
    - We want to check if the path string itself is safe, not where it points.
    - This prevents false negatives when symlinks don't exist yet.

    For symlink security, use the extraction function's symlink validation.
    """
    # Use abspath to normalize paths but NOT realpath (which follows symlinks)
    abs_directory = os.path.abspath(directory)
    abs_target = os.path.abspath(target)

    # Ensure directory ends with separator for proper prefix check
    # This prevents /foo/bar from matching /foo/barz
    if not abs_directory.endswith(os.sep):
        abs_directory += os.sep

    return abs_target.startswith(
        abs_directory
    ) or abs_target == abs_directory.rstrip(os.sep)


def _safe_extract_tar(tar: tarfile.TarFile, path: str) -> None:
    """Safely extract tar archive, preventing path traversal attacks.

    :param tarfile.TarFile tar: tarfile object to extract.
    :param str path: destination path for extraction.

    Security Note: This function prevents path traversal attacks including:

    - Files with ``..`` in their path.
    - Symlinks pointing outside the extraction directory.
    - Files extracted through malicious symlinks.

    For Python 3.12+, uses ``tarfile.data_filter`` for additional protection.
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
            raise ValueError(str(e)) from e
    else:
        # Manual validation for older Python versions
        for member in tar.getmembers():
            # Check the member's target path
            try:
                safe_path_join(path, member.name)
            except ValueError:
                raise ValueError(
                    f"Attempted path traversal in tar file: {member.name}"
                )

            # For symlinks, also validate the link target
            if member.issym() or member.islnk():
                # Get the link target (can be absolute or relative)
                link_target = member.linkname

                # If it's a relative symlink, resolve it relative to the member's directory.
                # Pass the archive-relative dirname and link target as separate parts to
                # safe_path_join, which canonicalises and validates containment in one step.
                if not os.path.isabs(link_target):
                    try:
                        safe_path_join(
                            path, os.path.dirname(member.name), link_target
                        )
                    except ValueError:
                        raise ValueError(
                            f"Symlink {member.name} points outside extraction directory: {member.linkname}"
                        )
                else:
                    # Absolute symlinks are dangerous - make them relative to extraction path
                    try:
                        safe_path_join(path, link_target.lstrip(os.sep))
                    except ValueError:
                        raise ValueError(
                            f"Symlink {member.name} points outside extraction directory: {member.linkname}"
                        )

        tar.extractall(path=path)


def _safe_extract_zip(zip_file: zipfile.ZipFile, path: str) -> None:
    """Safely extract zip archive, preventing path traversal attacks.

    :param zipfile.ZipFile zip_file: zipfile object to extract.
    :param str path: destination path for extraction.

    Security Note: This function prevents path traversal attacks including:

    - Files with ``..`` in their path.
    - Symlinks pointing outside the extraction directory (on Unix systems).

    Note: ZIP format has limited symlink support. Symlinks are primarily
    created by Unix-based archiving tools and may not be portable.
    """
    for member in zip_file.namelist():
        try:
            safe_path_join(path, member)
        except ValueError:
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

            # Resolve the link target relative to the member's directory.
            # Pass the archive-relative dirname and link target as separate parts to
            # safe_path_join, which canonicalises and validates containment in one step.
            if not os.path.isabs(link_target):
                try:
                    safe_path_join(
                        path, os.path.dirname(member), link_target
                    )
                except ValueError:
                    raise ValueError(
                        f"Symlink {member} points outside extraction directory: {link_target}"
                    )
            else:
                # Absolute symlinks - make them relative to extraction path
                try:
                    safe_path_join(path, link_target.lstrip(os.sep))
                except ValueError:
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
        temp_parts = cause.replace(">=", "").split("<")
        check = _version2int(temp_parts[0]) <= v < _version2int(temp_parts[1])
    elif cause.startswith(">=") and "<=" in cause:
        temp_parts = cause.replace(">=", "").split("<=")
        check = _version2int(temp_parts[0]) <= v <= _version2int(temp_parts[1])
    elif cause.startswith(">") and "<" in cause:
        temp_parts = cause.replace(">", "").split("<")
        check = _version2int(temp_parts[0]) < v < _version2int(temp_parts[1])
    elif cause.startswith("<="):
        temp = cause.replace("<=", "")
        check = v <= _version2int(temp)
    elif cause.startswith("<"):
        temp = cause.replace("<", "")
        check = v < _version2int(temp)

    return check


def download(
    name: str, force: bool = False, url: str = "", version: str = ""
) -> bool:
    """Download corpus.

    The available corpus names can be seen in this file:
    https://pythainlp.org/pythainlp-corpus/db.json

    This function always performs the download regardless of the
    ``PYTHAINLP_OFFLINE`` environment variable, because an explicit call
    to ``download()`` is a deliberate user action.
    ``PYTHAINLP_OFFLINE`` only blocks the *automatic* download triggered
    by :func:`pythainlp.corpus.get_corpus_path`.

    :param str name: corpus name
    :param bool force: force downloading
    :param str url: URL of the corpus catalog
    :param str version: version of the corpus
    :return: **True** if the corpus is found and successfully downloaded.
             Otherwise, it returns **False**.
    :rtype: bool

    :Example:

        >>> from pythainlp.corpus import download  # doctest: +SKIP
        >>> download("wiki_lm_lstm", force=True)  # doctest: +SKIP
        Corpus: wiki_lm_lstm
        - Downloading: wiki_lm_lstm 0.1
        ...

    By default, downloaded corpora and models will be saved in
    ``$HOME/pythainlp-data/``
    (e.g. ``/Users/bact/pythainlp-data/wiki_lm_lstm.pth``).
    """
    if is_read_only_mode():
        print("PyThaiNLP is in read-only mode. It cannot download.")
        return False

    if not url:
        url = corpus_db_url()

    corpus_db = get_corpus_db(url)
    if not corpus_db:
        print(f"Cannot download corpus catalog from: {url}")
        return False

    corpus_db_dict = corpus_db.json()

    # check if corpus is available
    if name in corpus_db_dict:
        db_path = corpus_db_path()
        if os.path.exists(db_path):
            with open(db_path, encoding="utf-8-sig") as f:
                local_db = json.load(f)
        else:
            local_db = {"_default": {}}

        corpus = corpus_db_dict[name]
        print("Corpus:", name)
        if not version:
            for v, file in corpus["versions"].items():
                if _check_version(file["pythainlp_version"]):
                    version = v

        # version may still be None here
        if version not in corpus["versions"]:
            print("Corpus not found.")
            return False
        elif (
            _check_version(corpus["versions"][version]["pythainlp_version"])
            is False
        ):
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
                with zipfile.ZipFile(
                    get_full_data_path(file_name), "r"
                ) as zip_file:
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

        >>> from pythainlp.corpus import remove, get_corpus_path  # doctest: +SKIP
        >>> remove("ttc")  # doctest: +SKIP
        True
        >>> get_corpus_path("ttc")  # doctest: +SKIP
        None
    """
    if is_read_only_mode():
        print("PyThaiNLP is in read-only mode. It cannot remove corpus.")
        return False
    db_path = corpus_db_path()
    if not os.path.exists(db_path):
        return False
    with open(db_path, encoding="utf-8-sig") as f:
        db = json.load(f)
    data = [
        corpus for corpus in db["_default"].values() if corpus["name"] == name
    ]

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
    except ModuleNotFoundError as e:
        raise ModuleNotFoundError(
            "huggingface-hub is not installed."
            " Install it with: pip install huggingface-hub"
        ) from e
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred: {e}") from e
    hf_root = get_full_data_path("hf_models")
    name_dir = make_safe_directory_name(repo_id)
    root_project = safe_path_join(hf_root, name_dir)
    if filename:
        output_path = hf_hub_download(
            repo_id=repo_id, filename=filename, local_dir=root_project
        )
    else:
        output_path = snapshot_download(
            repo_id=repo_id, local_dir=root_project
        )
    return str(output_path)
