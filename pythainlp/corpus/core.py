# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Corpus related functions."""

from __future__ import annotations

import copy
import json
import os
import re
import shutil
import stat
import sys
import tarfile
import time
import uuid
import warnings
import zipfile
from contextlib import suppress
from functools import cache
from importlib.resources import files
from typing import TYPE_CHECKING, Any, BinaryIO, Optional

from pythainlp import __version__
from pythainlp.corpus import corpus_db_path, corpus_db_url, corpus_path
from pythainlp.tools import get_full_data_path
from pythainlp.tools.path import (
    get_pythainlp_data_path,
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
    """Wrap a urllib response in a requests.Response-like interface."""

    status_code: int
    headers: HTTPMessage
    _content: bytes

    def __init__(self, response: HTTPResponse) -> None:
        self.status_code = response.status
        self.headers = response.headers
        self._content = response.read()

    def json(self) -> dict[str, Any]:
        """Parse the JSON content of the response."""
        try:
            data: dict[str, Any] = json.loads(self._content.decode("utf-8"))
            return data
        except (json.JSONDecodeError, UnicodeDecodeError) as err:
            raise ValueError(f"Failed to parse JSON response: {err}") from err


def get_corpus_db(url: str) -> Optional[_ResponseWrapper]:
    """
    Get the corpus catalog from a server.

    Uses HTTPS with certificate validation enabled by default in Python's
    urllib. Download a corpus catalog from trusted URLs only.

    :param str url: URL of the corpus catalog
    :return: response wrapper, or None if the request fails
    :rtype: Optional[pythainlp.corpus.core._ResponseWrapper]
    """
    from urllib.error import HTTPError, URLError
    from urllib.request import Request, urlopen

    corpus_db = None
    try:
        req = Request(url, headers={"User-Agent": _USER_AGENT})  # noqa: S310
        # SSL certificate verification is enabled by default
        with urlopen(req, timeout=10) as response:  # noqa: S310  # nosec B310
            corpus_db = _ResponseWrapper(response)
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except URLError as err:
        print(f"URL error occurred: {err}")
    except (OSError, ValueError) as err:
        # Network failure (including timeout) or malformed URL/response
        print(f"Error occurred: {err}")

    return corpus_db


def get_corpus_db_detail(name: str, version: str = "") -> dict[str, Any]:
    """
    Get details about a corpus from the local catalog.

    :param str name: corpus name
    :param str version: corpus version (empty string means any version)
    :return: details about the corpus, or an empty dict if not found
    :rtype: dict[str, Any]
    """
    db_path = corpus_db_path()
    if not os.path.exists(db_path):
        return {}
    with open(db_path, encoding="utf-8-sig") as f:
        local_db: dict[str, Any] = json.load(f)

    for corpus in local_db["_default"].values():
        if corpus["name"] == name and (
            not version or corpus["version"] == version
        ):
            detail: dict[str, Any] = corpus
            return detail

    return {}


@cache
def get_corpus(filename: str, comments: bool = True) -> frozenset[str]:
    r"""
    Read corpus data from a file and return a frozenset.

    Each line in the file becomes a member of the set.
    Whitespace is stripped, and empty values and duplicates are removed.

    If comments is False, any text at any position after the character
    "#" in each line is discarded.

    :param str filename: filename of the corpus to be read
    :param bool comments: keep comments
    :return: frozenset of lines in the file
    :rtype: frozenset[str]

    :Example:

        >>> from pythainlp.corpus import get_corpus  # doctest: +SKIP
        >>> get_corpus("negations_th.txt")  # doctest: +SKIP
        frozenset({'แต่', 'ไม่'})
        >>> get_corpus("ttc_freq.txt")  # doctest: +SKIP
        frozenset({'โดยนัยนี้\t1', 'ตัวบท\t10', ...})
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


@cache
def get_corpus_as_is(filename: str) -> list[str]:
    """
    Read corpus data from a file as it is and return a list.

    Each line in the file becomes a member of the list.
    Member values and their order are not modified.
    To strip whitespace or remove comments, use :func:`get_corpus` instead.

    :param str filename: filename of the corpus to be read
    :return: list of lines in the file
    :rtype: list[str]

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


@cache
def _load_default_db() -> dict[str, Any]:
    """Load and cache the bundled default_db.json corpus catalog."""
    corpus_files = files("pythainlp.corpus")
    default_db_file = corpus_files.joinpath("default_db.json")
    text = default_db_file.read_text(encoding="utf-8-sig")
    db: dict[str, Any] = json.loads(text)
    return db


def get_corpus_default_db(name: str, version: str = "") -> Optional[str]:
    """
    Get the corpus path from default_db.json.

    To edit default_db.json, edit pythainlp/corpus/default_db.json.

    :param str name: corpus name
    :param str version: corpus version (empty string means latest)
    :return: path to the corpus, or None if the corpus does not exist
        on the device
    :rtype: Optional[str]
    """
    corpus_db = _load_default_db()

    if name in corpus_db:
        if version in corpus_db[name]["versions"]:
            return safe_path_join(
                corpus_path(),
                corpus_db[name]["versions"][version]["filename"],
            )
        if not version:  # load latest version
            version = corpus_db[name]["latest_version"]
            return safe_path_join(
                corpus_path(),
                corpus_db[name]["versions"][version]["filename"],
            )

    return None


def _resolve_corpus_file_path(
    corpus_db_detail: dict[str, Any],
) -> Optional[str]:
    """
    Resolve the local file system path of a corpus catalog entry.

    :param dict[str, Any] corpus_db_detail: corpus catalog entry from the
        local catalog
    :return: full local path to the corpus file or folder, or None if
        required path information is missing
    :rtype: Optional[str]
    """
    if corpus_db_detail.get("is_folder"):
        foldername = corpus_db_detail.get("foldername")
        return get_full_data_path(foldername) if foldername else None
    filename = corpus_db_detail.get("filename")
    return get_full_data_path(filename) if filename else None


def _download_corpus_db_detail(name: str, version: str) -> dict[str, Any]:
    """
    Download a corpus that is missing from the local catalog.

    :param str name: corpus name
    :param str version: corpus version (empty string means latest)
    :return: corpus catalog entry, or an empty dict if the download fails
        or the corpus is still not in the catalog
    :rtype: dict[str, Any]
    :raises FileNotFoundError: if ``PYTHAINLP_OFFLINE`` is set
    """
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
        return {}
    return get_corpus_db_detail(name, version=version)


def _redownload_missing_corpus(
    name: str, version: str, path: str
) -> Optional[str]:
    """
    Download again a corpus that is in the catalog but missing on disk.

    :param str name: corpus name
    :param str version: corpus version (empty string means latest)
    :param str path: expected local path of the corpus
    :return: *path* if it exists after the download, otherwise None
    :rtype: Optional[str]
    :raises FileNotFoundError: if ``PYTHAINLP_OFFLINE`` is set
    """
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


def get_corpus_path(name: str, version: str = "") -> Optional[str]:
    """
    Get the local path of a corpus.

    The function checks these locations in order:

    1. Bundled (default) corpora shipped with PyThaiNLP.
    2. The local download catalog (``~/pythainlp-data/``).

    When the corpus file is not present locally, the behavior depends on the
    ``PYTHAINLP_OFFLINE`` environment variable:

    - If ``PYTHAINLP_OFFLINE`` is set to a truthy value (for example,
      ``"1"``), the function raises :exc:`FileNotFoundError` immediately.
    - Otherwise, the function downloads the corpus automatically.

    :param str name: corpus name
    :param str version: corpus version (empty string means latest)
    :return: full local path if the corpus exists, or None if the corpus
        cannot be found or downloaded
    :rtype: Optional[str]
    :raises FileNotFoundError: if the corpus is missing locally and
        ``PYTHAINLP_OFFLINE`` is set to a truthy value

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
    # Check bundled (default) corpora first
    default_path = get_corpus_default_db(name=name, version=version)
    if default_path is not None:
        return default_path

    # Check the local download catalog; download if not there
    corpus_db_detail = get_corpus_db_detail(name, version=version)
    if not corpus_db_detail:
        corpus_db_detail = _download_corpus_db_detail(name, version)
        if not corpus_db_detail:
            return None

    path = _resolve_corpus_file_path(corpus_db_detail)
    if path is None:
        return None

    if os.path.exists(path):
        return path

    # File is registered in catalog but missing from disk
    return _redownload_missing_corpus(name, version, path)


def _download(url: str, dst: str, md5: str = "") -> int:
    """
    Download a file and verify its checksum.

    Download into a new temporary file next to *dst*, verify it, then
    move it into place. If the download or the check fails, or is
    interrupted, remove the temporary file and raise again; a file that
    existed at *dst* stays as it was. A replaced file keeps its
    permission bits, and a symbolic link at *dst* stays a link.

    Downloads use HTTPS with SSL certificate validation.
    Files are verified using MD5 checksums after download.

    :param str url: URL of the file to download
    :param str dst: local destination path of the downloaded file
    :param str md5: expected MD5 checksum of the file
        (an empty string or ``"-"`` skips the check)
    :return: file size from the ``Content-Length`` header,
        or -1 if the header is missing
    :rtype: int
    :raises ValueError: if the checksum does not match
    """
    from urllib.request import Request, urlopen

    req = Request(url, headers={"User-Agent": _USER_AGENT})  # noqa: S310
    # SSL certificate verification is enabled by default
    with urlopen(req, timeout=10) as response:  # noqa: S310  # nosec B310
        file_size = int(response.info().get("Content-Length", -1))
        # Resolve links, so a link at *dst* stays and its target is replaced.
        file_path = os.path.realpath(get_full_data_path(dst))
        mode = _file_mode(file_path)
        tmp_path = _sibling_temp_path(file_path, "part")
        try:
            with open(tmp_path, "xb") as f:
                _copy_response(response, f, file_size)
            _check_hash(tmp_path, md5)
            if mode is not None:
                os.chmod(tmp_path, mode)
            _replace_file(tmp_path, file_path)
        except BaseException:
            with suppress(OSError):
                os.remove(tmp_path)
            raise
    return file_size


def _copy_response(
    response: HTTPResponse, f: BinaryIO, file_size: int
) -> None:
    """Copy a response body to a file; show a progress bar if possible."""
    CHUNK_SIZE = 64 * 1024  # 64 KiB

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


def _check_hash(file_path: str, md5: str) -> None:
    """
    Check the checksum of a file.

    :param str file_path: full path of the file to verify
    :param str md5: expected MD5 checksum of the file
        (an empty string or ``"-"`` skips the check)
    :raises ValueError: if the checksum does not match
    """
    if not md5 or md5 == "-":
        return
    import hashlib

    with open(file_path, "rb") as f:
        # MD5 only detects a damaged download; the catalog supplies it
        file_md5 = hashlib.md5(  # nosec B324  # NOSONAR
            f.read(), usedforsecurity=False
        ).hexdigest()
    if md5 != file_md5:
        raise ValueError("Hash does not match expected.")


def _is_within_directory(directory: str, target: str) -> bool:
    """
    Check if a target path is within a directory.

    This check prevents path traversal. It normalizes paths with
    ``os.path.abspath()`` to handle relative paths and ``..`` sequences.
    It does not follow symbolic links (unlike ``os.path.realpath()``),
    because:

    - The extraction functions validate symbolic links separately.
    - The check is on the path string itself, not on where it points.
    - This avoids false negatives when symbolic links do not exist yet.

    For symbolic link security, use the symbolic link validation of the
    extraction functions.

    :param str directory: base directory path
    :param str target: target file path to check
    :return: True if the target is within the directory, False otherwise
    :rtype: bool
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


def _check_member_path(path: str, member_name: str, archive_type: str) -> None:
    """
    Check that an archive member stays within the extraction directory.

    :param str path: destination path for extraction
    :param str member_name: name of the archive member
    :param str archive_type: archive type for the error message
        (``"tar"`` or ``"zip"``)
    :raises ValueError: if the member path escapes *path*
    """
    try:
        safe_path_join(path, member_name)
    except ValueError:
        raise ValueError(
            f"Attempted path traversal in {archive_type} file: {member_name}"
        ) from None


def _link_error(member_name: str, link_target: str) -> ValueError:
    """Return the error for a link that points outside the destination."""
    return ValueError(
        f"Symlink {member_name} points outside extraction directory: "
        f"{link_target}"
    )


def _check_link_target(
    path: str, member_name: str, link_target: str, base_dir: str
) -> None:
    """
    Check that a link member points within the extraction directory.

    :param str path: destination path for extraction
    :param str member_name: name of the link member
    :param str link_target: target of the link
    :param str base_dir: directory, relative to *path*, from which a
        relative target is resolved
    :raises ValueError: if the link target is absolute or escapes *path*
    """
    if os.path.isabs(link_target) or link_target.startswith(("/", os.sep)):
        raise _link_error(member_name, link_target)
    try:
        safe_path_join(path, base_dir, link_target)
    except ValueError:
        raise _link_error(member_name, link_target) from None


def _check_tar_member(path: str, member: tarfile.TarInfo) -> None:
    """
    Check the name and type of a tar member.

    The check is lexical: it does not look at the file system.
    Only regular files and directories are allowed.

    :param str path: destination path for extraction
    :param tarfile.TarInfo member: tar member to check
    :raises ValueError: if the member name escapes *path*, or if the
        member is a link or a special file (such as a FIFO or a device)
    """
    _check_member_path(path, member.name, "tar")
    if member.issym() or member.islnk():
        raise ValueError(f"Link in tar file: {member.name}")
    if not (member.isreg() or member.isdir()):
        raise ValueError(f"Special file in tar file: {member.name}")


def _data_filter_mode(member: tarfile.TarInfo) -> int:
    """
    Return a safe file mode, similar to ``tarfile.data_filter``.

    Drop the high bits and the group and other write bits. A file gets
    owner read and write; it keeps the executable bits only if the owner
    can execute it. A directory gets owner read, write, and execute.
    Unlike ``tarfile.data_filter``, which does not set the mode of a
    directory, the mode of a directory is limited too.

    :param tarfile.TarInfo member: tar member to get the mode of
    :return: safe file mode
    :rtype: int
    """
    mode = member.mode & 0o755
    if member.isdir():
        return mode | 0o700
    if not mode & 0o100:
        mode &= ~0o111
    return mode | 0o600


def _filter_tar_member(member: tarfile.TarInfo) -> tarfile.TarInfo:
    """
    Return a copy of a tar member with a safe mode and no owner.

    The owner is dropped, so files belong to the extracting user,
    even when it is root. A user or group ID of -1 tells
    :func:`os.chown` to keep the current value.

    :param tarfile.TarInfo member: tar member to filter
    :return: filtered copy of the member
    :rtype: tarfile.TarInfo
    """
    filtered = copy.copy(member)
    filtered.mode = _data_filter_mode(member)
    filtered.uid = filtered.gid = -1
    filtered.uname = filtered.gname = ""
    return filtered


def _safe_extract_tar(tar: tarfile.TarFile, path: str) -> None:
    """
    Extract a tar archive safely, preventing path traversal.

    *path* should be a new, empty directory.

    If ``tarfile.data_filter`` is available (Python 3.9.17+, 3.10.12+,
    3.11.4+, and 3.12+), the function uses it. A ``tarfile.FilterError``
    becomes a :exc:`ValueError`, with the original error as its cause.
    Python releases without the 2025 fixes to the filter (CVE-2025-4517,
    CVE-2025-4330, CVE-2025-4138) can be escaped through symbolic links.
    Use a recent patch release.

    Otherwise, a stricter manual check runs before anything is
    extracted. It rejects:

    - Members whose name is absolute or escapes the destination
      through ``..``.
    - All symbolic and hard links.
    - Special files, such as FIFOs and devices.

    Without links, the checks on names are enough if *path* holds no
    symbolic links. File modes are limited as with ``tarfile.data_filter``,
    and the owner is not restored.

    :param tarfile.TarFile tar: tar file object to extract
    :param str path: destination path for extraction
    :raises ValueError: if a member is unsafe
    """
    if not hasattr(tarfile, "data_filter"):
        members = tar.getmembers()
        for member in members:
            _check_tar_member(path, member)
        tar.extractall(  # noqa: S202  # nosec B202
            path=path, members=[_filter_tar_member(m) for m in members]
        )
        return

    try:
        tar.extractall(path=path, filter="data")
    except tarfile.FilterError as e:
        raise ValueError(str(e)) from e


def _is_zip_symlink(info: zipfile.ZipInfo) -> bool:
    """
    Return whether a zip member is a Unix symbolic link.

    The high 16 bits of ``external_attr`` hold the Unix file mode.

    :param zipfile.ZipInfo info: zip member to check
    :return: True if the member is a symbolic link, False otherwise
    :rtype: bool
    """
    return (info.external_attr >> 16) & 0o170000 == 0o120000


def _safe_extract_zip(zip_file: zipfile.ZipFile, path: str) -> None:
    """
    Extract a zip archive safely, preventing path traversal.

    The function prevents path traversal attacks, including:

    - Files with ``..`` in their path.
    - Symbolic links with an absolute target, or with a target outside
      the extraction directory (on Unix systems).

    Each entry is checked, including entries with a duplicate name.

    The zip format has limited symbolic link support. Unix-based
    archiving tools mainly create symbolic links, and they may not be
    portable. :meth:`zipfile.ZipFile.extractall` writes them as regular
    files.

    :param zipfile.ZipFile zip_file: zip file object to extract
    :param str path: destination path for extraction
    :raises ValueError: if a member is unsafe (nothing is extracted then)
    """
    for info in zip_file.infolist():
        _check_member_path(path, info.filename, "zip")
        if _is_zip_symlink(info):
            # The symlink target is stored as the member content
            link_target = zip_file.read(info).decode("utf-8")
            _check_link_target(
                path,
                info.filename,
                link_target,
                os.path.dirname(info.filename),
            )

    zip_file.extractall(path=path)  # noqa: S202  # nosec B202


def _version2int(v: str) -> int:
    """
    Convert a version string X.Y.Z to an integer that sorts like the version.

    A missing minor or patch number counts as 0, so ``"9"``, ``"9.0"``, and
    ``"9.0.0"`` give the same integer. The minor and patch numbers each have
    4 digits (up to 9999). A part after a "-" and components after the third
    are ignored.

    :param str v: version string, such as ``"5.3"`` or ``"5.3.*"``
    :return: version as an integer
    :rtype: int
    :raises ValueError: if a component is not a number
    """
    v = v.split("-")[0].removesuffix(".*")  # X.X.* => X.X
    major, minor, patch = ([int(x) for x in v.split(".")] + [0, 0])[:3]
    return major * 10**8 + minor * 10**4 + patch


def _installed_version_int() -> int:
    """
    Return the installed PyThaiNLP version as an integer.

    A "dev" or "beta" suffix is dropped.

    :return: installed version as an integer
    :rtype: int
    """
    version = __version__
    if "dev" in version:
        version = version.split("dev", maxsplit=1)[0]
    elif "beta" in version:
        version = version.split("beta", maxsplit=1)[0]
    return _version2int(version)


def _check_lower_bound(cause: str, v: int) -> bool:
    """
    Check *v* against a cause that starts with ``">"``.

    The cause can also have an upper bound, like ``">=5.0<6.0"``.

    :param str cause: version constraint
    :param int v: installed version as an integer
    :return: True if *v* satisfies the lower bound of *cause*
    :rtype: bool
    """
    if "<" not in cause:
        if cause.startswith(">="):
            return v >= _version2int(cause.replace(">=", ""))
        return v > _version2int(cause.replace(">", ""))
    if not cause.startswith(">="):
        parts = cause.replace(">", "").split("<")
        return _version2int(parts[0]) < v < _version2int(parts[1])
    if "<=" in cause:
        parts = cause.replace(">=", "").split("<=")
        return _version2int(parts[0]) <= v <= _version2int(parts[1])
    parts = cause.replace(">=", "").split("<")
    return _version2int(parts[0]) <= v < _version2int(parts[1])


def _check_version(cause: str) -> bool:
    """
    Check if the installed PyThaiNLP version satisfies a constraint.

    :param str cause: version constraint, such as ``"*"``, ``"==5.0"``,
        ``">=5.0"``, ``"<6.0"``, or ``">=5.0<6.0"``
    :return: True if the installed version satisfies *cause*
    :rtype: bool
    """
    v = _installed_version_int()
    if cause == "*":
        return True
    if cause.startswith("=="):
        if ">" in cause or "<" in cause:
            return False
        return v == _version2int(cause.replace("==", ""))
    if cause.startswith(">"):
        return _check_lower_bound(cause, v)
    if cause.startswith("<="):
        return v <= _version2int(cause.replace("<=", ""))
    if cause.startswith("<"):
        return v < _version2int(cause.replace("<", ""))
    return False


def _load_local_db() -> dict[str, Any]:
    """Load the local corpus catalog, or return an empty one."""
    db_path = corpus_db_path()
    if not os.path.exists(db_path):
        return {"_default": {}}
    with open(db_path, encoding="utf-8-sig") as f:
        local_db: dict[str, Any] = json.load(f)
    return local_db


def _highest_compatible_version(versions: dict[str, Any]) -> str:
    """
    Return the highest corpus version that works with this PyThaiNLP.

    :param dict[str, Any] versions: ``versions`` of a catalog entry
    :return: the version, or an empty string if none is compatible
    :rtype: str
    """
    best = ""
    best_key = -1
    for v, file in versions.items():
        if not _check_version(file["pythainlp_version"]):
            continue
        try:
            key = _version2int(v)
        except ValueError:
            key = -1  # not a number: lowest, but still usable
        if key >= best_key:
            best, best_key = v, key
    return best


def _select_version(corpus: dict[str, Any], version: str) -> Optional[str]:
    """
    Select the corpus version to download and check that it is supported.

    Without *version*, the highest compatible version wins. If two versions
    are equal, the later one in catalog order wins.

    :param dict[str, Any] corpus: corpus entry from the remote catalog
    :param str version: requested version (empty string means any)
    :return: selected version, or None (with a printed message) if it is
        missing or not supported
    :rtype: Optional[str]
    """
    versions = corpus["versions"]
    if not version:
        version = _highest_compatible_version(versions)

    if version not in versions:
        print("Corpus not found.")
        return None
    if _check_version(versions[version]["pythainlp_version"]) is False:
        print("Corpus version not supported.")
        return None
    return version


def _find_local_corpus_no(
    local_db: dict[str, Any], name: str
) -> Optional[str]:
    """
    Return the local catalog key of the first entry named *name*.

    The version is not checked. Return None if not found.
    Any key counts, even an empty string.
    """
    entries: dict[str, Any] = local_db["_default"]
    for i, item in entries.items():
        if item["name"] == name:
            return i
    return None


def _next_local_corpus_no(entries: dict[str, Any]) -> int:
    """
    Return the number for a new local catalog entry.

    It is one more than the largest numeric key. Keys that are not
    decimal numbers, such as an empty string, are ignored.
    """
    numbers = [int(no) for no in entries if no.isdecimal()]
    return max(numbers, default=0) + 1


def _extract_corpus_archive(
    corpus_versions: dict[str, Any], name: str, version: str, file_name: str
) -> Optional[str]:
    """
    Extract a downloaded tar or zip corpus into its own folder.

    Extract into a new temporary folder next to the corpus folder, then
    swap it into place. An existing corpus folder is replaced as a whole.
    If the extraction fails, remove the temporary folder, then raise
    again; an existing corpus folder stays as it was.

    :return: folder name, or None if the corpus is not an archive
    :rtype: Optional[str]
    """
    if corpus_versions["is_tar_gz"] == "True":
        is_tar = True
    elif corpus_versions["is_zip"] == "True":
        is_tar = False
    else:
        return None

    foldername = name + "_" + str(version)
    folder_path = get_full_data_path(foldername)
    tmp_path = _sibling_temp_path(folder_path, "tmp")
    os.mkdir(tmp_path)
    try:
        _extract_archive(get_full_data_path(file_name), tmp_path, is_tar)
        _swap_in_folder(tmp_path, folder_path)
    except BaseException:
        shutil.rmtree(tmp_path, ignore_errors=True)
        raise
    return foldername


def _extract_archive(
    archive_path: str, folder_path: str, is_tar: bool
) -> None:
    """Extract a tar or zip archive safely into *folder_path*."""
    if is_tar:
        with tarfile.open(archive_path) as tar:
            _safe_extract_tar(tar, folder_path)
    else:
        with zipfile.ZipFile(archive_path, "r") as zip_file:
            _safe_extract_zip(zip_file, folder_path)


def _sibling_temp_path(path: str, suffix: str) -> str:
    """
    Return a unique hidden path in the directory of *path*.

    The name is ``.<name>.<random hex>.<suffix>``.
    """
    return safe_path_join(
        os.path.dirname(os.path.abspath(path)),
        f".{os.path.basename(path)}.{uuid.uuid4().hex}.{suffix}",
    )


def _remove_path(path: str) -> None:
    """
    Remove a file, a link, or a directory tree; ignore errors.

    A symbolic link is removed, not followed.
    """
    if os.path.isdir(path) and not os.path.islink(path):
        shutil.rmtree(path, ignore_errors=True)
        return
    with suppress(OSError):
        os.remove(path)


def _swap_in_folder(new_path: str, folder_path: str) -> None:
    """
    Move *new_path* to *folder_path*, replacing what is there.

    The old entry is moved aside first, and is moved back if the move
    of *new_path* fails. It is removed only after the swap succeeds.
    If the move back fails too, the old entry stays at its hidden
    temporary path and the error of the first move is raised.
    """
    if not os.path.lexists(folder_path):
        os.rename(new_path, folder_path)
        return
    old_path = _sibling_temp_path(folder_path, "old")
    os.rename(folder_path, old_path)
    try:
        os.rename(new_path, folder_path)
    except BaseException as e:
        try:
            os.rename(old_path, folder_path)
        except OSError:
            _add_note(e, f"The old folder is kept at: {old_path}")
        raise
    _remove_path(old_path)


# A hidden temporary entry: ``.<name>.<32 hex digits>.<suffix>``.
_TEMP_ENTRY = re.compile(
    r"^\.(?P<name>.+)\.[0-9a-f]{32}\.(?P<suffix>part|tmp|old)$"
)

# Age after which a hidden temporary entry counts as abandoned.
_STALE_TEMP_SECONDS: int = 24 * 60 * 60


def _sweep_stale_temp_paths(
    max_age: float = _STALE_TEMP_SECONDS, now: Optional[float] = None
) -> None:
    """
    Remove abandoned hidden temporary entries from the data directory.

    A crash or a failed cleanup can leave ``.<name>.<hex>.part``, ``.tmp``,
    or ``.old`` entries (see :func:`_sibling_temp_path`). An entry is
    removed only if it has not changed for *max_age* seconds, so a
    download in another process is not disturbed. An ``.old`` entry is also
    kept if there is no ``<name>`` next to it: it is then the only copy of
    a corpus that failed to swap in. Errors are ignored.

    :param float max_age: age in seconds after which an entry is stale
    :param Optional[float] now: current time in seconds
        (default: ``time.time()``)
    """
    now = time.time() if now is None else now
    try:
        data_dir = get_pythainlp_data_path()
        names = os.listdir(data_dir)
    except OSError:
        return
    for entry in names:
        match = _TEMP_ENTRY.match(entry)
        if match is None:
            continue
        try:
            path = safe_path_join(data_dir, entry)
            if now - os.lstat(path).st_mtime < max_age:
                continue
            if match["suffix"] == "old" and not os.path.lexists(
                safe_path_join(data_dir, match["name"])
            ):
                continue
        except (OSError, ValueError):
            continue
        _remove_path(path)


def _add_note(error: BaseException, note: str) -> None:
    """Add *note* to *error*; warn instead before Python 3.11."""
    add_note = getattr(error, "add_note", None)
    if add_note is not None:
        add_note(note)
    else:
        warnings.warn(note, RuntimeWarning, stacklevel=2)


# Times to retry os.replace() after a PermissionError. On Windows, the
# error is often temporary: another process has the file open.
_REPLACE_RETRIES: int = 5 if os.name == "nt" else 0


def _replace_file(src: str, dst: str) -> None:
    """Replace *dst* with *src*, retrying on a temporary PermissionError."""
    for _ in range(_REPLACE_RETRIES):
        try:
            os.replace(src, dst)
            return
        except PermissionError:
            time.sleep(0.05)
    os.replace(src, dst)


def _file_mode(path: str) -> Optional[int]:
    """Return the permission bits of *path*, or None if missing."""
    try:
        return stat.S_IMODE(os.stat(path).st_mode)
    except FileNotFoundError:
        return None


def _write_local_db(local_db: dict[str, Any]) -> None:
    """
    Write the local corpus catalog atomically.

    Write to a temporary file in the same directory, then replace the
    catalog with it, so a crash cannot leave a partly written catalog.
    The permission bits of the old catalog are kept. If the catalog is
    a symbolic link, its target is replaced and the link stays.
    """
    db_path = os.path.realpath(corpus_db_path())
    mode = _file_mode(db_path)
    tmp_path = _sibling_temp_path(db_path, "tmp")
    try:
        with open(tmp_path, "x", encoding="utf-8") as f:
            json.dump(local_db, f, ensure_ascii=False)
            f.flush()
            os.fsync(f.fileno())
        if mode is not None:
            os.chmod(tmp_path, mode)
        _replace_file(tmp_path, db_path)
    except BaseException:
        with suppress(OSError):
            os.remove(tmp_path)
        raise


def _save_local_db_entry(
    local_db: dict[str, Any],
    found: Optional[str],
    name: str,
    version: str,
    file_name: str,
    foldername: Optional[str],
) -> None:
    """Add or update a corpus entry and write the local catalog."""
    is_folder = foldername is not None
    entries = local_db["_default"]
    if found is not None:
        entries[found]["version"] = version
        entries[found]["filename"] = file_name
        entries[found]["is_folder"] = is_folder
        entries[found]["foldername"] = foldername
    else:
        # This awkward behavior is for backward-compatibility with
        # database files generated previously using TinyDB
        entries[str(_next_local_corpus_no(entries))] = {
            "name": name,
            "version": version,
            "filename": file_name,
            "is_folder": is_folder,
            "foldername": foldername,
        }

    _write_local_db(local_db)


def _install_corpus(
    name: str,
    version: str,
    corpus_versions: dict[str, Any],
    file_name: str,
    local_db: dict[str, Any],
    found: Optional[str],
) -> None:
    """Download, verify, and extract a corpus, then record it locally."""
    print(f"- Downloading: {name} {version}")
    # A file that already exists is replaced only by a verified download
    _download(
        corpus_versions["download_url"], file_name, corpus_versions["md5"]
    )
    foldername = _extract_corpus_archive(
        corpus_versions, name, version, file_name
    )
    _save_local_db_entry(local_db, found, name, version, file_name, foldername)


def _print_installed_status(current_ver: str, version: str) -> None:
    """Report an installed corpus that is not downloaded again."""
    if current_ver == version:
        print("- Already up to date.")
        return
    print(f"- Existing version: {current_ver}")
    print(f"- New version available: {version}")
    print("- Use download(data_name, force=True) to update")


def download(
    name: str, force: bool = False, url: str = "", version: str = ""
) -> bool:
    """
    Download a corpus.

    The available corpus names are listed in this file:
    https://pythainlp.org/pythainlp-corpus/db.json

    This function always performs the download regardless of the
    ``PYTHAINLP_OFFLINE`` environment variable, because an explicit call
    to ``download()`` is a deliberate user action.
    ``PYTHAINLP_OFFLINE`` only blocks the *automatic* download triggered
    by :func:`pythainlp.corpus.get_corpus_path`.

    By default, downloaded corpora and models are saved in
    ``$HOME/pythainlp-data/``
    (for example, ``/Users/bact/pythainlp-data/wiki_lm_lstm.pth``).

    :param str name: corpus name
    :param bool force: force the download
    :param str url: URL of the corpus catalog
    :param str version: corpus version (empty string means latest)
    :return: True if the corpus is found and downloaded successfully,
        False otherwise
    :rtype: bool

    :Example:

        >>> from pythainlp.corpus import download  # doctest: +SKIP
        >>> download("wiki_lm_lstm", force=True)  # doctest: +SKIP
        Corpus: wiki_lm_lstm
        - Downloading: wiki_lm_lstm 0.1
        ...
    """
    if is_read_only_mode():
        print("PyThaiNLP is in read-only mode. It cannot download.")
        return False

    _sweep_stale_temp_paths()

    if not url:
        url = corpus_db_url()

    corpus_db = get_corpus_db(url)
    if not corpus_db:
        print(f"Cannot download corpus catalog from: {url}")
        return False

    corpus_db_dict = corpus_db.json()

    # check if corpus is available
    if name not in corpus_db_dict:
        print("Corpus not found:", name)
        return False

    local_db = _load_local_db()
    corpus = corpus_db_dict[name]
    print("Corpus:", name)
    selected_version = _select_version(corpus, version)
    if selected_version is None:
        return False

    corpus_versions = corpus["versions"][selected_version]
    file_name = corpus_versions["filename"]
    found = _find_local_corpus_no(local_db, name)

    if force or found is None:
        _install_corpus(
            name, selected_version, corpus_versions, file_name, local_db, found
        )
    else:
        # Found in the local catalog and a re-download is not forced
        _print_installed_status(
            local_db["_default"][found]["version"], selected_version
        )
    return True


def remove(name: str) -> bool:
    """
    Remove a corpus.

    :param str name: corpus name
    :return: True if the corpus is found and removed successfully,
        False otherwise
    :rtype: bool

    :Example:

        >>> from pythainlp.corpus import (
        ...     remove,
        ...     get_corpus_path,
        ... )  # doctest: +SKIP
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
        # Use the catalog entry: never download a missing corpus to remove it.
        path = _resolve_corpus_file_path(data[0])
        if data[0].get("is_folder"):
            filename = data[0].get("filename")
            if filename:
                with suppress(FileNotFoundError):
                    os.remove(get_full_data_path(filename))
            if path:
                shutil.rmtree(path, ignore_errors=True)
        elif path:
            with suppress(FileNotFoundError):
                os.remove(path)
        for i, corpus in db["_default"].copy().items():
            if corpus["name"] == name:
                del db["_default"][i]
        _write_local_db(db)
        return True

    return False


def make_safe_directory_name(name: str) -> str:
    """
    Make a safe directory name.

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


def get_hf_hub(
    repo_id: str, filename: str = "", revision: Optional[str] = None
) -> str:
    """
    Download a Hugging Face Hub repository into the PyThaiNLP data directory.

    :param str repo_id: repository ID
    :param str filename: name of the file to download
        (if empty, download the entire snapshot)
    :param Optional[str] revision: git revision ID, which can be a branch
        name, a tag, or a commit hash (default is None).
        Pin to a full commit hash for reproducible and secure downloads.
    :return: path to the downloaded file or snapshot
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
            repo_id=repo_id,
            filename=filename,
            local_dir=root_project,
            revision=revision,
        )
    else:
        output_path = snapshot_download(
            repo_id=repo_id,
            local_dir=root_project,
            revision=revision,
        )
    return str(output_path)
